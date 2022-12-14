# FastAPI boilerplate with a single endpoint
# See https://fastapi.tiangolo.com/tutorial/first-steps/

from fastapi import FastAPI, File, UploadFile
import api.lib.PDFParser as PDFParser
from io import BytesIO



# app = FastAPI()

# # @app.post("/files/")
# # async def create_file(file: bytes = File()):
# #     file.save(f"./pdfs/{file.filename}")
# #     return {"data": "sheesh"}

# @app.post("/pdf/")
# async def create_upload_file(document: UploadFile = File(...)):
#     pdf_file = BytesIO(await document.read())
#     parser = PDFParser.PDFParser(pdf_file)
#     data = parser.parsePDF()
#     return {"data": data}



from fastapi.middleware.cors import CORSMiddleware
from fastapi import APIRouter, FastAPI

from api.base import app_router

def include_router(app):
    app.include_router(app_router)

def add_cors(app):
    origins = ["*"]
    
    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

def start_application():
    app = FastAPI(title="ABCD-EDU API", description="ABCD-EDU", version=1.0)
    include_router(app)
    add_cors(app)
    
    return app

app = start_application()