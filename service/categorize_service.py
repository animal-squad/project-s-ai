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

        with open("prompt/sub_category", "r") as f:
            self.sub_category_prompt = f.read()

    def categorize_main(self, content: str) -> str:
        """
        메인 카테고리를 분류
        :param content: 분류하려는 텍스트
        :return: 분류된 1개의 카테고리
        """
        category = json.loads(self.gpt_model.generate_response(self.main_category_prompt, content))

        return category["main_categories"][0]

    def categorize_sub(self, content: str, main_category: str, all_sub_categories: set[str]) -> list[str]:
        """
        하위 카테고리를 분류
        :param content: 분류하려는 텍스트
        :param main_category: 텍스트의 주요 카테고리
        :param all_sub_categories: 주요 카테고리의 하위 카테고리 목록
        :return:
        """

        user_message = f"주요 카테고리: {main_category}, 텍스트: {content}"
        system_message = f"{self.sub_category_prompt}[{', '.join(all_sub_categories)}]"

        sub_categories = json.loads(self.gpt_model.generate_response(system_message, user_message))

        return sub_categories["sub_categories"]
