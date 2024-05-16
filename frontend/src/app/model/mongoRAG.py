import os
import certifi
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from langchain_openai import ChatOpenAI
from langchain_openai.embeddings import OpenAIEmbeddings
from langchain.prompts import ChatPromptTemplate
from langchain_mongodb import MongoDBAtlasVectorSearch
from langchain_core.messages import HumanMessage
from langchain.chains import create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_community.chat_message_histories import ChatMessageHistory
from langchain_core.chat_history import BaseChatMessageHistory
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain.chains import create_history_aware_retriever
from langchain_core.prompts import MessagesPlaceholder
from openai import OpenAI
#global chat history storage var
store = {}

# Connect to MongoDB Atlas cluster using the connection string.
def conn_to_cluster(MONGO_URI):
    cluster = MongoClient(MONGO_URI, server_api=ServerApi('1'), tlsCAFile=certifi.where())
    DB_NAME = "test"
    COLLECTION_NAME = "Cluster0"
    MONGODB_COLLECTION = cluster[DB_NAME][COLLECTION_NAME]
    return MONGODB_COLLECTION

def OpenAI_init_LLM():
    return ChatOpenAI(model_name="gpt-3.5-turbo", temperature=0.4)

def generate_full_prompt(sourced_info, prompt):
    return f"Original Input: {prompt}\n\n Answer Query With Search Results From Here: {sourced_info} .\n"

def rag_template():
    return """
    Given a chat history and the latest user question, which might reference context in the chat history,
    formulate a response based on the context, the history of the chat and the user's query.
    Role: You are a mental health professional, counseling the user prompting you. By all means you cannot diagnose the user, but you 
    can suggest diagnosis.
    Use the following pieces of retrieved context to answer the question at the end.
    If you don't know the answer, just say that you don't know.
    You are a mental health professional, counseling the user prompting you. By all means you cannot diagnose the user.
    If the user ever mentions self harm OR suicide:
    refer them to the Suicide Hotline phone and text service - '988' - note this is only for USA users.
    Use the following pieces of retrieved context to answer the question at the end.
    If you don't know the answer, just say that you don't know.
    {context}
    """

def get_vectorstore(MONGODB_COLLECTION):
    return MongoDBAtlasVectorSearch(
        MONGODB_COLLECTION,
        OpenAIEmbeddings(),
        index_name="vector_index"
    )

def set_retriever(MONGODB_COLLECTION):
    vector_store = get_vectorstore(MONGODB_COLLECTION)
    return vector_store.as_retriever()

def source_info(vectorstore, prompt):
    return vectorstore.similarity_search(prompt, k=5)



def context_q_init(MONGODB_COLLECTION, u_input):
    vector_store = get_vectorstore(MONGODB_COLLECTION)
    sourced_info = source_info(vector_store, u_input)
    template = """
    Given a chat history and the latest user question which might reference context in the chat history, 
    formulate a standalone question which can be understood without the chat history. Do NOT answer the question, 
    just reformulate it if needed and otherwise return it as is. 
    """
    context_q = ChatPromptTemplate.from_messages(
        [
            ("system", template),
            MessagesPlaceholder("chat_history"),
            ("human", "{input}"),
        ]
        
    )
    return context_q

def history_aware_retriever(MONGODB_COLLECTION, u_input, llm):
    retriever = set_retriever(MONGODB_COLLECTION)
    context_q_prompt = context_q_init(MONGODB_COLLECTION, u_input)
    full_prompt = rag_template()
    context_q_prompt_str = context_q_prompt + "\n" + full_prompt + u_input
    history_aware_retriever = create_history_aware_retriever(
        llm, retriever, context_q_prompt
    )
    return history_aware_retriever

def qa_sys_prompt():
    sys_prompt = """
    You are a mental health professional, counseling the user prompting you. By all means you cannot diagnose the user, but you 
    can suggest diagnosis.
    Use the following pieces of retrieved context to answer the question at the end.
    If you don't know the answer, just say that you don't know.
    You are a mental health professional, counseling the user prompting you. By all means you cannot diagnose the user.
    If the user ever mentions self harm OR suicide:
    refer them to the Suicide Hotline phone and text service - '988' - note this is only for USA users.
    Use the following pieces of retrieved context to answer the question at the end.
    If you don't know the answer, just say that you don't know.
    Do not by any means mention the phrase or a similar phrase to: In the context of the book.
    {context}"""
    
    qa_prompt = ChatPromptTemplate.from_messages(
        [
            ("system", sys_prompt),
            MessagesPlaceholder("chat_history"),
            ("human", "{input}"),
        ]
    )
    return qa_prompt
    
#Create a chain for passing a list of Documents to a model.
def q_a_chain(llm):
    qa_prompt = qa_sys_prompt()
    question_answer_chain = create_stuff_documents_chain(llm, qa_prompt)
    return question_answer_chain

def rag_chain_retrieval(MONGODB_COLLECTION, u_input, llm):
    question_answer_chain = q_a_chain(llm)
    hist_retriever = history_aware_retriever(MONGODB_COLLECTION, u_input, llm)
    rag_chain = create_retrieval_chain(hist_retriever, question_answer_chain)
    return rag_chain

def get_session_history(session_id: str) -> BaseChatMessageHistory:
    if session_id not in store:
        store[session_id] = ChatMessageHistory()
    return store[session_id]

def get_response(MONGODB_COLLECTION, u_input, llm):
    history_aware_ret = history_aware_retriever(MONGODB_COLLECTION, u_input, llm)
    qa_chain = q_a_chain(llm)
    rag_chain = create_retrieval_chain(history_aware_ret, qa_chain)
#rag chgain now with conversation!
    conversational_rag_chain = RunnableWithMessageHistory(
    rag_chain,
    get_session_history,
    input_messages_key="input",
    history_messages_key="chat_history",
    output_messages_key="answer",
)
    return conversational_rag_chain.invoke(
        {"input": u_input},
        config={
        "configurable": {"session_id": "abc123"}
    },
    )["answer"]
#clear messsages storage on exit
def clear_store():
    return store.clear()

def process(MONGODB_COLLECTION, vectorstore, text, llm):
    print("processing")
    sourced_info = source_info(vectorstore, text)
    print("info from vectorstore obtained")
    full_prompt = generate_full_prompt(sourced_info, text)
    print("prompt generated")
    response = get_response(MONGODB_COLLECTION, text, llm)
    print("response obtained")
    return response
