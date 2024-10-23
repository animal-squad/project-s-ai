import json

from model.gpt_model import GPTModel


class CategorizeService:
    """
    주어진 텍스트의 카테고리를 분류하는 서비스
    :param gpt_model: 사용하려는 GPT 모델을 주입
    """
    def __init__(self, gpt_model: GPTModel):
        self.gpt_model = gpt_model
        with open("prompt/main_category", "r") as f:
            self.main_category_prompt = f.read()

    def categorize_main(self, content: str) -> str:
        """
        메인 카테고리를 분류
        :param content: 분류하려는 텍스트
        :return: 분류된 1개의 카테고리
        """
        category = json.loads(self.gpt_model.generate_response(self.main_category_prompt, content))

        return category["main_categories"][0]