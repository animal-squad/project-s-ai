from fastapi import FastAPI

from entity.reqeust_dto import ClassifyRequest
from entity.response_dto import ClassifyResultResponse
from model.gpt_model import GPTModel
from service.categorize_service import CategorizeService

app = FastAPI()

gpt_model = GPTModel()
categorize_service = CategorizeService(gpt_model)

@app.post("/ai/classify")
async def classify(req: ClassifyRequest):
    """
    메인 카테고리 분류 엔드포인트
    """
    category = categorize_service.categorize(req.content)
    return ClassifyResultResponse(category=category)