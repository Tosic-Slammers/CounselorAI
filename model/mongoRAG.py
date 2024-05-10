# !pip install gradio icecream langchain openai sentence-transformers tiktoken langchain-mongodb langchain-openai
# !python -m pip install "pymongo[srv]"

# Import libraries.
import getpass
import gradio as gr
import os
import pprint
import requests
import sys

from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from gradio.themes.base import Base
from google.colab import drive
from icecream import ic
from langchain.callbacks.tracers import ConsoleCallbackHandler
from langchain.chat_models import ChatOpenAI
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.llms import HuggingFacePipeline
from langchain_core.messages import HumanMessage, SystemMessage
from langchain.document_loaders import TextLoader
from langchain.embeddings import OpenAIEmbeddings
from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from langchain.schema.runnable import RunnablePassthrough
from langchain.schema.output_parser import StrOutputParser
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.vectorstores import MongoDBAtlasVectorSearch
from transformers import AutoModelForCausalLM, AutoTokenizer, pipeline

#load conn to mongodb atlas search & initialize vector search?

def load_env_vars():
#Secret Key Loading , Please readdress to load as env var
    os.environ["OPENAI_API_KEY"] = getpass.getpass()
    os.environ["MONGO_URI"] = getpass.getpass()
# Retrieve environment variable.
    OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
    MONGO_URI = os.getenv('MONGO_URI')
    

def conn_to_cluster():
    mclient = MongoClient(MONGO_URI, server_api=ServerApi('1'))
# Connect to MongoDB Atlas cluster using the connection string.
    cluster = MongoClient(MONGO_URI)

# Define the MongoDB database and collection name.
    DB_NAME = "test"
    COLLECTION_NAME = "Cluster0"

# Connect to the specific collection in the database.
    MONGODB_COLLECTION = cluster[DB_NAME][COLLECTION_NAME]

    vector_search_index = "vector_index"
    
#this can be used to debug connection issues, doesnt need to be used but can be
def ping_mdb_client():
    try:
# The ismaster command is cheap and does not require auth.
        mclient.admin.command('ismaster')
        print("MongoDB is connected")
    except Exception as e:
        print("Failed to connect to MongoDB", e)
        
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
    
#initialize the retriever with a vector_search as retriever by similarity, getting the k'th highest scores after .89
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