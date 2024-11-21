import logging

from entity.link_info import LinkWithTags, LinkInfo
from model.gpt_model import GPTModel
from service.content_reader import ContentReader


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
    def __init__(self, gpt_model: GPTModel, content_reader: ContentReader, logger: logging.Logger):
        self.content_reader = content_reader
        self.gpt_model = gpt_model
        self.logger = logger
        with open("prompt/main_category", "r") as f:
            self.main_category_prompt = f.read()

    def categorize_contents(self, contents: list[LinkInfo]) -> list[LinkWithTags]:
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
                data["tags"] = self.categorize_main(content_info["title"], content_info["content"])
            else:
                data["title"] = None
                data["tags"] = []

            if not data["tags"]:
                data["tags"].append("기타")

            results.append(LinkWithTags(**data))

        return results

    def categorize_main(self, title: str, content: str) -> list[str]:
        """
        내용의 태그를 부여
        :param title: 분류하려는 텍스트의 제목
        :param content: 분류하려는 텍스트
        :return: 분류된 여러개의 태그
        """
        query = f"{title if title else ''}\n\n{content if content else ''}"
        category = self.gpt_model.generate_response(self.main_category_prompt, query)

        return get_tags(category)
