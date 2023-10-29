from fastapi import APIRouter, Depends, Request
from fastapi.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession
from sdek.sdek import SdekService

router = APIRouter()

@router.get("/callback")
async def callback(sdek_id: int):
    sdek_service = SdekService()
    result = await sdek_service.get_status_about_order(sdek_id)
    if result is not None:
        return JSONResponse({"message": "order info received successfully", "data": result})
    return JSONResponse({"message": "order info receiving failed"})