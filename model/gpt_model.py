import logging
import time

from openai import OpenAI


class GPTModel:
    def __init__(self, logger: logging.Logger):
        self.client = OpenAI()
        self.logger = logger

    def generate_response(self, prompt: str, user_message: str) -> str:
        """
        프롬프트와 사용자 메시지가 주어지면 GPT의 결과를 반환
        :param prompt: 프롬프트
        :param user_message: 사용자 메시지
        :return: 결과 텍스트
        """
        messages = [
            {"role": "system", "content": prompt},
            {"role": "user", "content": user_message}
        ]

        before = time.time()
        response = self.client.chat.completions.create(
            model="gpt-4o-mini",
            messages=messages,
        )
        self.logger.info(f"[TOKEN] {response.usage.total_tokens}")
        self.logger.info(f"[TIME] {time.time() - before: .2f}s")

        return response.choices[0].message.content
