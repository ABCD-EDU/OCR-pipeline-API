from fastapi import APIRouter

import loader.result as result
app_router = APIRouter()

@app_router.post('/')
async def get_results(texts:list):
   return result.get_result(texts)



# app_router.include_router(route_models.router, prefix="/models", tags=["models"])