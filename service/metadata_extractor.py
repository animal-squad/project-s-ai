import logging

from entity.link_info import LinkWithTags, LinkInfo
from model.gpt_model import GPTModel
from prompt.extract_keyword_prompt import EXTRACT_KEYWORD_PROMPT
from prompt.extract_tag_prompt import EXTRACT_TAG_PROMPT
from service.content_reader import ContentReader


class MetadataExtractor:
    """
    주어진 텍스트의 카테고리를 분류하는 서비스
    :param gpt_model: 사용하려는 GPT 모델을 주입
    """
    def __init__(self, gpt_model: GPTModel, content_reader: ContentReader, logger: logging.Logger):
        self.content_reader = content_reader
        self.gpt_model = gpt_model
        self.logger = logger

    @staticmethod
    def _parse_response(response: str) -> list[str]:
        parse_single_quotes = response.split("'")[1:-1]

        result = []
        for tag in parse_single_quotes:
            if tag.find(",") == -1:
                result.append(tag)

        return result

    def extract_metadata_batch(self, contents: list[LinkInfo]) -> list[LinkWithTags]:
        """
        링크들의 태그를 부여
        :param contents: 분류하려는 링크들의 정보
        :return: 각 링크들의 분류된 태그들, linkId, title
        """
        results = []
        for link_info in contents:
            data = {
                "linkId": link_info.linkId,
            }

            try:
                content_info = self.content_reader.read_content(link_info.URL, link_info.content)
            except Exception as e:
                content_info = None
                error_type = type(e).__name__
                self.logger.error(
                    f"Failed to read content for URL: {link_info.URL}.\n"
                    f"Error Type: {error_type}, Message: {e}"
                )

            if content_info:
                data["title"] = content_info["title"]
                data["tags"] = self.extract_metadata(content_info["title"], content_info["content"], EXTRACT_TAG_PROMPT)
            else:
                data["title"] = None
                data["tags"] = []
                data["keywords"] = []

            if not data["tags"]:
                data["tags"].append("기타")

            results.append(LinkWithTags(**data))

        return results

    def extract_metadata(self, title: str, content: str, prompt: str) -> list[str]:
        """
        내용의 태그를 부여
        :param title: 분류하려는 텍스트의 제목
        :param content: 분류하려는 텍스트
        :return: 분류된 여러개의 태그
        """
        query = f"{title if title else ''}\n\n{content if content else ''}"
        category = self.gpt_model.generate_response(prompt, query)

        return self._parse_response(category)
