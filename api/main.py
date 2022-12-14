# FastAPI boilerplate with a single endpoint
# See https://fastapi.tiangolo.com/tutorial/first-steps/

from fastapi import FastAPI, File, UploadFile
import lib.PDFParser as PDFParser
from io import BytesIO

app = FastAPI()

# @app.post("/files/")
# async def create_file(file: bytes = File()):
#     file.save(f"./pdfs/{file.filename}")
#     return {"data": "sheesh"}

@app.post("/upload/")
async def create_upload_file(document: UploadFile = File(...)):
    # get filename of uploaded file
    period = document.filename.rfind(".")
    file = BytesIO(await document.read())
    data = None
    print(file)
    if document.filename[period:] == ".pdf":
        parser = PDFParser.PDFParser(file)
        data = parser.parsePDF()
    else:
        parser = PDFParser.PDFParser(file.read().decode("utf-8"))
        # print(type(file.read()))
        print(parser.src)
        data = parser.parseText()
    return {"data": data}