from dotenv import load_dotenv
from dotenv import load_dotenv
from PyPDF2 import PdfReader
from langchain.text_splitter import CharacterTextSplitter
from langchain.embeddings import OpenAIEmbeddings, HuggingFaceInstructEmbeddings
#from langchain.embeddings import OllamaEmbeddings
from langchain.vectorstores import FAISS
from langchain.callbacks.manager import CallbackManager
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler
from langchain.chat_models import ChatOllama
from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationalRetrievalChain
from langchain.chat_models import ChatOpenAI
from functools import wraps
import time
import sys
import os
from transformers import pipeline


# Decorator for measuring execution time
def timeit(func):
    @wraps(func)
    def timeit_wrapper(*args, **kwargs):
        start_time = time.perf_counter()
        result = func(*args, **kwargs)
        end_time = time.perf_counter()
        total_time = end_time - start_time
        print(f"\nFunction {func.__name__} Took {total_time:.4f} seconds")
        return result

    return timeit_wrapper


def list_files_with_full_path(directory):
    files_with_paths = [
        os.path.join(directory, filename)
        for filename in os.listdir(directory)
        if os.path.isfile(os.path.join(directory, filename))
    ]
    return files_with_paths



# Function to get text from PDF documents
@timeit
def get_pdf_text():
    directory = "./pdfs"
    pdf_docs = list_files_with_full_path(directory)
    text = ""
    for pdf in pdf_docs:
        pdf_reader = PdfReader(pdf)
        for page in pdf_reader.pages:
            text += page.extract_text()
    return text


# Function to split text into chunks
@timeit
def get_text_chunks(text):
    text_splitter = CharacterTextSplitter(
        separator="\n", chunk_size=1000, chunk_overlap=200, length_function=len
    )
    chunks = text_splitter.split_text(text)
    return chunks


# Function to create a vector store
@timeit
def get_vectorstore(text_chunks):
    #embeddings = OllamaEmbeddings(model="llama2:70b-chat")
    embeddings = OpenAIEmbeddings()
    # embeddings = HuggingFaceInstructEmbeddings(model_name="hkunlp/instructor-xl")
    vectorstore = FAISS.from_texts(texts=text_chunks, embedding=embeddings)
    return vectorstore


# Function to create a conversation chain
@timeit
def get_conversation_chain(vectorstore):
    llm = ChatOpenAI()
    # llm = ChatOllama(
    #         model="llama2:70b-chat",
    #     callback_manager=CallbackManager([StreamingStdOutCallbackHandler()]),
    #     # num_gpu=2
    # )
    # llm = HuggingFaceHub(repo_id="google/flan-t5-xxl", model_kwargs={"temperature":0.5, "max_length":512})

    memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)
    conversation_chain = ConversationalRetrievalChain.from_llm(
        llm=llm, retriever=vectorstore.as_retriever(), memory=memory
    )
    return conversation_chain


# Function to handle user input and generate responses
@timeit
def handle_userinput(conversation, user_question):
    response = conversation({"question": user_question})


# Main function
def main(chain, user_question):
    load_dotenv()
    conversation = None
    chat_history = None

    ## Get text from PDFs
    #raw_text = get_pdf_text()

    ## Split text into chunks
    #text_chunks = get_text_chunks(raw_text)

    ## Create vector store
    #vectorstore = get_vectorstore(text_chunks)

    ## create conversation chain
    #chain = get_conversation_chain(vectorstore) 

    if user_question:
        prompt = f"""
        ### System:
        You are an respectful and honest assistant. You have to answer the user's \
        questions using only the context provided to you in not more than 100 Words. If you don't know the answer, \
        just say you don't know. Don't try to make up an answer.
        
        ### User:
        {user_question}
        
        ### Response:
        """
        response = chain({"question": prompt})
        print("------------------------------------")
        print(response['answer'])
        print("------------------------------------")
        return response['answer']


if __name__ == "__main__":
    main("What is Bitaxe?")
