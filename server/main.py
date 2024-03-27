from typing import Union
from fastapi import FastAPI
from qnaService import QnALoader
from fastapi import File, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI()
qnaLoader = QnALoader()
origins = ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def questions():
    return "Let the QnA begin!"


@app.post("/doc/")
async def get_doc(doc:UploadFile=File(...)):
    # try:
    #     qnaLoader.load_doc_by_type(doc)
    #     return "OK"
    # except:
    #     raise HTTPException(status_code=502, detail="Couldn't add document!")
    qnaLoader.load_doc_by_type(doc)
    return "OK"

@app.post("/questions/")
async def get_doc(questions:UploadFile=File(...)):
    # try:
    #     return qnaLoader.get_answers_for_questions(questions)
    # except:
    #     raise HTTPException(status_code=502, detail="Couldn't fetch answers!")
    return qnaLoader.get_answers_for_questions(questions)