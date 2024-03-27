from langchain_community.document_loaders.generic import GenericLoader
from langchain_community.document_loaders.parsers import LanguageParser
from langchain_text_splitters import Language
from langchain_community.vectorstores import Chroma
from langchain_openai import OpenAIEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain.chains import ConversationalRetrievalChain
from langchain.memory import ConversationSummaryMemory
from langchain_openai import ChatOpenAI
import dotenv
import os
dotenv.load_dotenv()

class LangchainLoader:
    __repo_path = "/Users/ujjwalanand/Desktop/ulaws/langchain"
    __documents = None
    __texts = None
    __retriever= None
    __qa_bot = None
    
    def __init__(self):
        self.__load_documents()
        self.__split_documents()
        self.__initialize_retriever()
        self.__setup_chatbot()


    def __load_documents(self):
        loader = GenericLoader.from_filesystem(
            self.__repo_path + "/libs/langchain/langchain",
            glob="**/*",
            suffixes=[".py"],
            exclude=["**/non-utf8-encoding.py"],
            parser=LanguageParser(language=Language.PYTHON, parser_threshold=500),
        )
        self.__documents = loader.load()

    def __split_documents(self):
        python_splitter = RecursiveCharacterTextSplitter.from_language(
            language=Language.PYTHON, chunk_size=2000, chunk_overlap=200
        )
        self.__texts = python_splitter.split_documents(self.__documents)

    def __initialize_retriever(self):
        db = Chroma.from_documents(self.__texts, OpenAIEmbeddings(disallowed_special=()))
        self.__retriever = db.as_retriever(
            search_type="mmr",  # Also test "similarity"
            search_kwargs={"k": 8},
        )

    def __setup_chatbot(self):
        llm = ChatOpenAI(model_name="gpt-3.5-turbo")
        memory = ConversationSummaryMemory(
            llm=llm, memory_key="chat_history", return_messages=True
        )
        self.__qa_bot = ConversationalRetrievalChain.from_llm(llm, retriever=self.__retriever, memory=memory)

    def ask_questions(self,question):
        return self.__qa_bot(question)