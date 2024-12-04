from fastapi import FastAPI

from config.log import get_logger
from entity.request_dto import ExtractRequest
from entity.response_dto import ExtractResponse
from model.gpt_model import GPTModel
from service.metadata_extractor import MetadataExtractor
from service.content_extractor import ContentExtractor
from service.content_reader import ContentReader
from service.crawlability_checker import CrawlabilityChecker

app = FastAPI()

gpt_model = GPTModel()

crawlability_checker = CrawlabilityChecker()
content_extractor = ContentExtractor()
content_reader = ContentReader(crawlability_checker, content_extractor)

extractor_logger = get_logger("ExtractorLogger")
metadata_extractor = MetadataExtractor(gpt_model, content_reader, extractor_logger)

@app.post("/ai/extract")
async def classify_main(req: ExtractRequest):
    """
    메타 데이터 추출 엔드포인트
    """
    data = {
        "links": metadata_extractor.extract_metadata_batch(req.links),
    }

    return ExtractResponse(**data)
