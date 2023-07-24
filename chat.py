import streamlit as st
import os
from dotenv import load_dotenv
from PyPDF2 import PdfReader
from langchain.text_splitter import CharacterTextSplitter
from langchain.embeddings import OpenAIEmbeddings, HuggingFaceInstructEmbeddings
from langchain.vectorstores import FAISS
from langchain.chat_models import ChatOpenAI
from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationalRetrievalChain
# from htmlTemplates import css, bot_template, user_template
from langchain.llms import HuggingFaceHub
import openai
from dotenv import load_dotenv
from llama_index import GPTVectorStoreIndex, SimpleDirectoryReader,download_loader

# from gpt_index import GPTFaissIndex, SimpleDirectoryReader

# openai.api_key = "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"

# def getpdf_text(files):
#     text = ""
#     for pdf in files:
#         pdf_reader = PdfReader(pdf)
#         for page in pdf_reader.pages:
#             text += page.extract_text()
#     return text
def getpdf_text(path):
    text = ""
    pdf_reader = PdfReader(path)
    for page in pdf_reader.pages:
        text += page.extract_text()
    return text

def getTxt(file):
    text= ""
    for i in file:
        txtfile = open(file)
    return text

def splitText(text):
    splitter = CharacterTextSplitter(
        separator="\n",  chunk_size=1000,
        chunk_overlap=200, length_function=len
    )
    chunks = splitter.split_text(text)
    return chunks

def embeddingAndVector(textChunk):
    embedBro = HuggingFaceInstructEmbeddings(model_name="hkunlp/instructor-large")
    embedBro.embed_documents(textChunk)
    vector = FAISS.from_texts(textChunk,embedBro)
    return vector


def gptVector(vector):
    indexGpt = GPTVectorStoreIndex.from_documents(vector)
    return indexGpt


def get_conversation_chain(vectorstore):
    llm = ChatOpenAI()
    # llm = HuggingFaceHub(repo_id="google/flan-t5-xxl", model_kwargs={"temperature":0.5, "max_length":512})

    memory = ConversationBufferMemory(
        memory_key='chat_history', return_messages=True)
    conversation_chain = ConversationalRetrievalChain.from_llm(
        llm=llm,
        retriever=vectorstore.as_retriever(),
        memory=memory
    )
    return conversation_chain


def handleUser(userinput):
    print()

def generateAnswerGPT(query,index):
    query_engine = index.as_query_engine()
    response = query_engine.query(query)
    return response.response

def generateAnswerFaiss(query,index):
    ans = index.similarity_search(query)
    return ans[0].page_content


def pdfIndex(paths_list):

    # PDFReader = download_loader("PDFReader")

    # loader = PDFReader()
    # file_path = os.path.join("uploads", filename)
    # print(file_path)
    # documents = loader.load_data(file=file_path)

    # return documents

    reader = SimpleDirectoryReader(input_files=paths_list)
    docs = reader.load_data()
    index = GPTVectorStoreIndex.from_documents(docs)
    return index



# if __name__=='__main__':
#     main()

    #get text from pdf -> split -> embed -> store in vector database
load_dotenv()
# documents = SimpleDirectoryReader('uploads').load_data()
# print(documents)
# file_path = os.path.join("uploads", "Austin - Resume.pdf")

# texts = getpdf_text(file_path)  
# index = GPTVectorStoreIndex.from_documents(texts)


# file_path = os.path.join("uploads", "Austin - Resume.pdf")
# texts = getpdf_text(file_path)  
# chunks = splitText(texts)
# #     # print(chunks)
# # vectors = embeddingAndVector(chunks)
# gptvec = gptVector(chunks)
# # convo  = get_conversation_chain(vectors)
# x = generateAnswerGPT("What is the name of the person who's resume I'm reading?", vectors)
# print(x)