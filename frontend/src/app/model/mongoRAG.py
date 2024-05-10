import os

from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
#from langchain.chat_models import ChatOpenAI
from langchain_openai.embeddings import OpenAIEmbeddings
#from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from langchain_mongodb import MongoDBAtlasVectorSearch
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
    
def rag_template():
    template = """
    You are a mental health professional, counseling the user prompting you. By all means you cannot diagnose the user.
    If the user ever mentions self harm OR suicide:
    refer them to the Suicide Hotline phone and text service - '988' - note this is only for USA users.
    Use the following pieces of retrieved context to answer the question at the end.
    If you don't know the answer, just say that you don't know.

    Context: {context}

    Question: {question}

    """
    #History: {history} - possible template addition to get historical context of conversation. Maybe summarizer model?
    custom_rag_prompt = ChatPromptTemplate.from_template(template)
    return custom_rag_prompt

def get_vectorstore(MONGODB_COLLECTION):
    vectorstore = MongoDBAtlasVectorSearch(
        MONGODB_COLLECTION,
        OpenAIEmbeddings(),
        index_name = "vector_index"
    )
    return vectorstore

def source_info(vectorstore, prompt):
    sourced_info = vectorstore.similarity_search(prompt, k=5)
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
    {"role": "system", 
             "content":  '''You are a mental health professional, counseling the user prompting you. By all means you cannot diagnose the user.
                            Use the following pieces of retrieved context to answer the question at the end.
                            If you don't know the answer, just say that you don't know.'''},
    {"role": "user", "content": full_prompt}
    ],
    temperature = 0.3
    )
    return response.choices[0].message.content

def process(client, vectorstore, text):
    print("processing")
    sourced_info = source_info(vectorstore, text)
    print("info from vectorstore obtained")
    full_prompt = generate_full_prompt(sourced_info, text)
    print("prompt generated")
    response = get_response(client, full_prompt)
    print("response obtained")
    return response