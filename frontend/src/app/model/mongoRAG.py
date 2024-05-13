#%pip install --upgrade --quiet  langchain langchain-community langchainhub langchain-openai langchain-chroma bs4

import os

from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from langchain_openai import ChatOpenAI
from langchain_openai.embeddings import OpenAIEmbeddings
from langchain.prompts import ChatPromptTemplate
from langchain_mongodb import MongoDBAtlasVectorSearch
from langchain_core.messages import HumanMessage
from langchain.chains import create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain.chains import create_history_aware_retriever
from langchain_core.prompts import MessagesPlaceholder
from openai import OpenAI
import certifi

#load conn to mongodb atlas search & initialize vector search?

def conn_to_cluster(MONGO_URI):
    cluster = MongoClient(MONGO_URI, server_api=ServerApi('1'), tlsCAFile=certifi.where())
# Connect to MongoDB Atlas cluster using the connection string.
    #cluster = MongoClient(MONGO_URI)

# Define the MongoDB database and collection name.
    DB_NAME = "test"
    COLLECTION_NAME = "Cluster0"

# Connect to the specific collection in the database.
    MONGODB_COLLECTION = cluster[DB_NAME][COLLECTION_NAME]

    vector_search_index = "vector_index"
    
    return MONGODB_COLLECTION

def OpenAI_init_LLM():
    #llm = ChatOpenAI(model_name="gpt-3.5-turbo", temperature=0.4) # Increasing the temperature, the model becomes more creative and takes longer for inference.
    llm = OpenAI()
    return llm

def generate_full_prompt(sourced_info, prompt):
    combined_information = f""" 
    Original Input: {prompt}\n\n 
    Answer Query With Search Results From Here: {sourced_info} . \n
    """
    return combined_information

def rag_template():
    template = """
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

    Context: {context}

    Question: {question}

    """
    return template

def get_vectorstore(MONGODB_COLLECTION):
    vectorstore = MongoDBAtlasVectorSearch(
        MONGODB_COLLECTION,
        OpenAIEmbeddings(),
        index_name = "vector_index"
    )
    return vectorstore
#set retriever for chain template
def set_retriever(MONGODB_COLLECTION):
    vector_store = get_vectorstore(MONGODB_COLLECTION)
    retriever = vector_store.as_retriever()
    return retriever

def set_history_aware_retriever(MONGODB_COLLECTION):
    llm = ChatOpenAI(model_name="gpt-3.5-turbo", temperature=0.3)
    rag_template = rag_template()
    retriever = set_retriever(MONGODB_COLLECTION)
    history_aware_retriever = create_history_aware_retriever(
        llm, retriever, rag_template
    )
    return history_aware_retriever

def source_info(vectorstore, prompt):
    sourced_info = vectorstore.similarity_search(prompt, k=5)
    return sourced_info
#Fetch chat history to update prompt with a list of chat history. Question = curr user query , Response = chatbot response. 
#Both stored in chat_history[] and returned
def fetch_chat_history(MONGODB_COLLECTION,question):
    chat_history = []
    response = get_response(MONGODB_COLLECTION,question)
    chat_history.extend([HumanMessage(content=question), response["answer"]])
    return chat_history

def get_response(MONGODB_COLLECTION,u_input):
    history_retriever = set_history_aware_retriever(MONGODB_COLLECTION)
    chat_history = fetch_chat_history(u_input)
    template = rag_template()
    prompt = ChatPromptTemplate.from_messages(
        [
            ("system",template),
            MessagesPlaceholder("chat_history"),
            ("human", "{input}")
        ]
    )
    return prompt.invoke({"input": u_input, "chat_history": chat_history})

def process(MONGODB_COLLECTION,vectorstore, text):
    print("processing")
    sourced_info = source_info(vectorstore, text)
    print("info from vectorstore obtained")
    full_prompt = generate_full_prompt(sourced_info, text)
    print("prompt generated")
    response = get_response(MONGODB_COLLECTION,text)
    print("response obtained")
    return response