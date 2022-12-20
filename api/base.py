import loader.result as result
from fastapi import FastAPI, File, UploadFile, APIRouter
from fastapi.middleware.cors import CORSMiddleware
import api.lib.PDFParser as PDFParser
from io import BytesIO

app_router = APIRouter()

# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["*"],
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )

@app_router.post('/')
async def get_results(texts:list):
    return result.get_result(texts)

@app_router.post("/upload/")
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

    print("---- inputted ----")
    print(data)
    data = result.get_result(data)
    print("---- returned ----")
    print(data)
    return {"data": data}


# app_router.include_router(route_models.router, prefix="/models", tags=["models"])