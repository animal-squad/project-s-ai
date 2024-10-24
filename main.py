from fastapi import FastAPI

from entity.content import ContentSubCategory
from entity.request_dto import CategorizeMainRequest, CategorizeSubRequest
from entity.response_dto import CategorizeMainResponse, CategorizeSubResponse
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


@app.post("/ai/categorize/sub")
async def classify_sub(req: CategorizeSubRequest):
    """
    하위 카테고리 분류 엔드포인트
    """
    # 주요 카테고리가 가지고 있는 모든 하위 카테고리 리스트
    sub_categories_of_main = { key: val for sub in req.sub_categories for key, val in sub.items() }

    results = []
    for content_info in req.data:
        content_id, content_type, main_category, content = content_info.dict().values()
        sub_categories = categorize_service.categorize_sub(
            content,
            main_category,
            all_sub_categories=sub_categories_of_main[main_category]
        )

        results.append(ContentSubCategory(
            content_id=content_id,
            type=content_type,
            sub_categories=sub_categories
        ))

    return CategorizeSubResponse(data=results)
