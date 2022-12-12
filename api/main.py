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

@app.post("/pdf/")
async def create_upload_file(document: UploadFile = File(...)):
    pdf_file = BytesIO(await document.read())
    parser = PDFParser.PDFParser(pdf_file)
    data = parser.parsePDF()
    return {"data": data}