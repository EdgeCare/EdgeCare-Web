from fastapi import APIRouter, HTTPException
from schemas.edgecare import Request, Response

router = APIRouter()

@router.post("/predict", response_model=Response)
async def predict(post_data: Request):

    print("predict",post_data)
    return {"responce": True}
    