from fastapi import FastAPI

from config.log import get_logger
from entity.request_dto import CategorizeRequest
from entity.response_dto import CategorizeResponse
from model.gpt_model import GPTModel
from service.categorize_service import CategorizeService
from service.content_extractor import ContentExtractor
from service.content_reader import ContentReader
from service.crawlability_checker import CrawlabilityChecker

app = FastAPI()

gpt_model = GPTModel()

crawlability_checker = CrawlabilityChecker()
content_extractor = ContentExtractor()
content_reader = ContentReader(crawlability_checker, content_extractor)

categorize_logger = get_logger("CategorizeServiceLogger")
categorize_service = CategorizeService(gpt_model, content_reader, categorize_logger)

@app.post("/ai/categorize")
async def classify_main(req: CategorizeRequest):
    """
    메인 카테고리 분류 엔드포인트
    """
    data = {
        "links": categorize_service.categorize_contents(req.links),
    }

    return CategorizeResponse(**data)
