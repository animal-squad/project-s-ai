from model.gpt_model import GPTModel


def get_tags(result: str) -> list[str]:
    result = result.split("'")[1:-1]
    tags = []
    for tag in result:
        if tag.find(",") == -1:
            tags.append(tag)

    return tags


class CategorizeService:
    """
    주어진 텍스트의 카테고리를 분류하는 서비스
    :param gpt_model: 사용하려는 GPT 모델을 주입
    """
    def __init__(self, gpt_model: GPTModel):
        self.gpt_model = gpt_model
        with open("prompt/main_category", "r") as f:
            self.main_category_prompt = f.read()

    def categorize_main(self, content: str) -> list[str]:
        """
        메인 카테고리를 분류
        :param content: 분류하려는 텍스트
        :return: 분류된 여러개의 태그
        """
        category = self.gpt_model.generate_response(self.main_category_prompt, content)

        return get_tags(category)
