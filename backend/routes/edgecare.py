from model.run_model import predict_entities
from fastapi import APIRouter
from schemas.edgecare import Request, Response

router = APIRouter()

@router.post("/predict", response_model=Response)
async def predict(post_data: Request):

    results = await predict_entities(post_data.text)
    return {"response": "Success", "results": results}
