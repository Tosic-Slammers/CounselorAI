import os

from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from langchain.callbacks.tracers import ConsoleCallbackHandler
from langchain.chat_models import ChatOpenAI
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.llms import HuggingFacePipeline
from langchain_core.messages import HumanMessage, SystemMessage
from langchain.document_loaders import TextLoader
from langchain.embeddings import OpenAIEmbeddings
#from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from langchain.schema.runnable import RunnablePassthrough
from langchain.schema.output_parser import StrOutputParser
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.vectorstores import MongoDBAtlasVectorSearch

#load conn to mongodb atlas search & initialize vector search?

def conn_to_cluster(MONGO_URI):
    mclient = MongoClient(MONGO_URI, server_api=ServerApi('1'))
# Connect to MongoDB Atlas cluster using the connection string.
    cluster = MongoClient(MONGO_URI)

# Define the MongoDB database and collection name.
    DB_NAME = "test"
    COLLECTION_NAME = "Cluster0"

# Connect to the specific collection in the database.
    MONGODB_COLLECTION = cluster[DB_NAME][COLLECTION_NAME]

    vector_search_index = "vector_index"
    
    return MONGODB_COLLECTION

def OpenAI_init_LLM():
    llm = ChatOpenAI(model_name="gpt-3.5-turbo", temperature=0.4) # Increasing the temperature, the model becomes more creative and takes longer for inference.
    return llm
    
def rag_template():
    template = """
You are a mental health professional, counseling the user prompting you. By all means you cannot diagnose the user.
Use the following pieces of retrieved context to answer the question at the end.
If you don't know the answer, just say that you don't know.

Context: {context}

Question: {question}

"""
#History: {history} - possible template addition to get historical context of conversation. Maybe summarizer model?
    custom_rag_prompt = ChatPromptTemplate.from_template(template)
    return custom_rag_prompt
    
#initialize the retriever with a vector_search as retriever by similarity, getting the k'th highest scores after .89
'''
def retriever_init():
    retriever = vector_search.as_retriever(
        search_type = "similarity", # similarity, mmr, similarity_score_threshold. https://api.python.langchain.com/en/latest/vectorstores/langchain_core.vectorstores.VectorStore.html#langchain_core.vectorstores.VectorStore.as_retriever
        search_kwargs = {"k": 10, "score_threshold": 0.89}
    )
    return retriever

#format documents for rag_chain initializer
def format_docs(docs):
    return "\n\n".join(doc.page_content for doc in docs)

def rag_chain_init():
    rag_chain = (
    { "context": retriever | format_docs, "question": RunnablePassthrough()}
    | custom_rag_prompt
    | llm
    | StrOutputParser() 
)
    
    return rag_chain

#user querying and answering for rag model , outputs answer / takes in u-input
def query_answer(in_text , rag_chain):
    answer = rag_chain.invoke(query)
    #if needed this will show source documents that lead to output
    source_docs = retriever.get_relevant_documents(query)
    
    return answer
'''
def get_vectorstore(MONGODB_COLLECTION):
    vectorstore = MongoDBAtlasVectorSearch(
        MONGODB_COLLECTION,
        OpenAIEmbeddings(),
        index_name = "vector_index"
    )
    return vectorstore

def source_info(vectorstore, prompt):
    sourced_info = vectorstore.similarity_search(prompt, k=1)
    return sourced_info

def generate_full_prompt(sourced_info, prompt):
    combined_information = f""" 
    Original Input: {prompt}\n\n Answer Query With Search Results From Here: {sourced_info} . \n
    """
    return combined_information

def get_response(client, full_prompt):
    response = client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=[
    {"role": "system", "content": "You are a professional Blackjack player, named Big Dog, coaching someone who doesn't know what to do with their hand."},
    {"role": "user", "content": full_prompt}
    ],
    temperature = 0.3
    )
    return response.choices[0].message.content

def process(client, vectorstore, text):
    sourced_info = source_info(vectorstore, text)
    full_prompt = generate_full_prompt(sourced_info, text)
    response = get_response(client, full_prompt)
    return response