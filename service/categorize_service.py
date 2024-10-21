import json

from model.gpt_model import GPTModel

class CategorizeService:
    def __init__(self, gpt_model: GPTModel):
        self.gpt_model = gpt_model
        with open("prompt/main_category", "r") as f:
            self.prompt = f.read()

    def categorize(self, content: str) -> str:
        category = json.loads(self.gpt_model.generate_response(self.prompt, content))

        return category["main_categories"][0]