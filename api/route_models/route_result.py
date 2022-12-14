from fastapi import APIRouter, HTTPException
import json

import loader.result as result

router = APIRouter()

@router.get("/")
async def get_results(message: str):
    return result.get_result(message)