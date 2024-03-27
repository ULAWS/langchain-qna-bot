from langchain import hub
from langchain_community.document_loaders import WebBaseLoader
from langchain_community.vectorstores import Chroma
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import PyPDFLoader
from langchain_community.document_loaders import JSONLoader
import json
import dotenv
import os 
import shutil

dotenv.load_dotenv()

class QnALoader:
    __rag_chain = None

    def __init__(self):
       print("Let's QnA!!")
       
    def load_doc_by_type(self,doc:object):
        try:
            os.mkdir("temp")
        except Exception as e:
            print("Couldn't make directory!")
        file_name = os.getcwd()+"/temp/"+doc.filename.replace(" ", "-")
        with open(file_name,'wb+') as f:
            f.write(doc.file.read())
            f.close()
        if doc.filename.endswith("pdf"):
            loader = PyPDFLoader(file_name)
            docs = loader.load_and_split()    
        elif doc.filename.endswith("json"):
            loader = JSONLoader(
            file_path=file_name,
            jq_schema='.content[]',
            text_content=False,)
            docs = loader.load()

        text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
        splits = text_splitter.split_documents(docs)
        vectorstore = Chroma.from_documents(documents=splits, embedding=OpenAIEmbeddings())

        # Retrieve and generate using the relevant snippets of the blog.
        retriever = vectorstore.as_retriever()
        prompt = hub.pull("rlm/rag-prompt")
        llm = ChatOpenAI(model_name="gpt-3.5-turbo", temperature=0)


        self.__rag_chain = (
            {"context": retriever | self.__format_docs, "question": RunnablePassthrough()}
            | prompt
            | llm
            | StrOutputParser()
        )
        shutil.rmtree("temp")

    def __format_docs(self,docs):
        return "\n\n".join(doc.page_content for doc in docs)

    def get_answers_for_questions(self,questionsJson):
        try:
            data = json.load(questionsJson.file)
            questions = data['questions']
            answers = self.fetch_answers(questions)
            result ={}
            for i in range(len(questions)):
                result[questions[i]]=answers[i]
            return result
        except :
            raise TypeError("Only json files allowed!")

    def fetch_answers(self,questions):
        answers=[]
        if not self.__rag_chain:
            raise ValueError("Rag chain not defined!")
        for i in questions:
            ans = self.__rag_chain.invoke(i)
            answers.append(ans)
        return answers
        


    