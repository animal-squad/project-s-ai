import json
import logging
import os

import requests

from service.content_extractor import ContentExtractor
from service.crawlability_checker import CrawlabilityChecker


class ContentReader:
    def __init__(self, crawlability_checker: CrawlabilityChecker, content_extractor: ContentExtractor, logger: logging.Logger):
        self.GOOGLE_SEARCH_API_KEY = os.getenv("GOOGLE_SEARCH_API_KEY")
        self.GOOGLE_SEARCH_CX = os.getenv("GOOGLE_SEARCH_CX")
        self.crawlability_checker = crawlability_checker
        self.content_extractor = content_extractor
        self.logger = logger

    def fetch_html_content(self, url: str) -> str:
        """
        주어진 URL의 HTML 정보를 반환. 주어진 URL은 크롤링이 가능하여야 합니다.
        :param url: 정보를 얻어오려는 URL
        :return: 읽은 HTML
        """
        response = requests.get(url)

        return response.text

    def perform_google_search(self, query: str) -> dict[str, str] | None:
        """
        주어진 쿼리를 Google에 검색한 결과를 반환.
        :param query: Google에 검색하려는 쿼리
        :return:
            검색한 결과 { "title": string, "content": string }
            결과가 없다면 None을 반환합니다.
        """
        request = f"https://www.googleapis.com/customsearch/v1?key={self.GOOGLE_SEARCH_API_KEY}&cx={self.GOOGLE_SEARCH_CX}&q={query}"
        response = requests.get(request)

        results = json.loads(response.text)
        content = ""
        try:
            for result in results["items"]:
                content += result["snippet"]
            return { "title": results["items"][0]["title"], "content": content }
        except KeyError:
            return None

    def extract(self, url: str, content: str) -> dict[str, str] | None:
        """
        주어진 URL에 따라 HTML 내용에서 주요 정보를 추출합니다.
        :param url: HTML의 정보를 추출한 URL
        :param content: HTML 정보
        :return: 추출한 주요 정보
        """
        if url.find("youtube.com/watch") != -1:
            return self.content_extractor.process_content(content, self.content_extractor.extract_youtube)
        elif url.find("velog.io/@") != -1:
            return self.content_extractor.process_content(content, self.content_extractor.extract_velog)
        elif url.find("okky.kr/questions") != -1 or url.find("okky.kr/articles") != -1:
            return self.content_extractor.process_content(content, self.content_extractor.extract_okky)
        elif url.find("tistory.com") != -1:
            return self.content_extractor.process_content(content, self.content_extractor.extract_tistory)
        else:
            return self.content_extractor.process_content(content, self.content_extractor.extract_generic)

    def read_content(self, url: str, content: str | None) -> dict[str, str] | None:
        """
        URL의 컨텐츠 정보를 반환. 만약 정보를 읽을 수 없다면 None 반환
        :param url: 내용을 알고 싶은 URL
        :param content: URL의 정보
        :return:
            읽을 수 있는 정보 반환
            읽을 수 없는 정보라면 None 반환
        """
        if not content:
            if self.crawlability_checker.can_crawl(url):
                self.logger.info(f" OK  {url}")
                content = self.fetch_html_content(url)
            else:
                self.logger.info(f"[NO] {url}")

        if content:
            return self.extract(url, content)
        else:
            return self.perform_google_search(url)
