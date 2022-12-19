# FastAPI boilerplate with a single endpoint
# See https://fastapi.tiangolo.com/tutorial/first-steps/

from fastapi import FastAPI, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
import lib.PDFParser as PDFParser
from io import BytesIO

app = FastAPI()

# set CORS policy to any origin
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# @app.post("/files/")
# async def create_file(file: bytes = File()):
#     file.save(f"./pdfs/{file.filename}")
#     return {"data": "sheesh"}

# accept pdf files and return parsed data

@app.post("/upload/")
async def create_upload_file(document: UploadFile = File(...)):
    # get filename of uploaded file
    period = document.filename.rfind(".")
    file = BytesIO(await document.read())
    data = None

    if document.filename[period:] == ".pdf":
        parser = PDFParser.PDFParser(file)
        data = parser.parsePDF()
    else:
        parser = PDFParser.PDFParser(file.read().decode("utf-8"))
        print(parser.src)
        data = parser.parseText()

    return {"data": data}

@app.get("/")
async def root():
    return {"message": "Hello World"}