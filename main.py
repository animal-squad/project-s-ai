from fastapi import FastAPI

from entity.reqeust_dto import CategorizeMainRequest
from entity.response_dto import CategorizeMainResponse
from model.gpt_model import GPTModel
from service.categorize_service import CategorizeService

app = FastAPI()

gpt_model = GPTModel()
categorize_service = CategorizeService(gpt_model)

@app.post("/ai/categorize/main")
async def classify_main(req: CategorizeMainRequest):
    """
    메인 카테고리 분류 엔드포인트
    """
    category = categorize_service.categorize_main(req.content)
    return CategorizeMainResponse(category=category)