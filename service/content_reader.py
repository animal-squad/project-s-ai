import json
import os

import requests

from service.crawlability_checker import CrawlabilityChecker


class ContentReader:
    def __init__(self, crawlability_checker: CrawlabilityChecker):
        self.GOOGLE_SEARCH_API_KEY = os.getenv("GOOGLE_SEARCH_API_KEY")
        self.GOOGLE_SEARCH_CX = os.getenv("GOOGLE_SEARCH_CX")
        self.crawlability_checker = crawlability_checker

    def fetch_html_content(self, url: str) -> str:
        """
        주어진 URL의 HTML 정보를 반환. 주어진 URL은 크롤링이 가능하여야 합니다.
        :param url: 정보를 얻어오려는 URL
        :return: 읽은 HTML
        """
        response = requests.get(url)

        return response.text

    def perform_google_search(self, query: str) -> str | None:
        """
        주어진 쿼리를 Google에 검색한 결과를 반환. 결과가 없다면 None 반환
        :param query: Google에 검색하려는 쿼리
        :return: 검색한 결과
        """
        request = f"https://www.googleapis.com/customsearch/v1?key={self.GOOGLE_SEARCH_API_KEY}&cx={self.GOOGLE_SEARCH_CX}&q={query}"
        response = requests.get(request)

        results = json.loads(response.text)
        content = ""
        try:
            for result in results["items"]:
                content += result["snippet"]
            return content
        except KeyError:
            return None

    def read_content(self, url: str) -> str | None:
        """
        URL의 컨텐츠 정보를 반환. 만약 정보를 읽을 수 없다면 None 반환
        :param url: 내용을 알고 싶은 URL
        :return:
            읽을 수 있는 정보 반환
            읽을 수 없는 정보라면 None 반환
        """
        if self.crawlability_checker.can_crawl(url):
            return self.fetch_html_content(url)
        else:
            return self.perform_google_search(url)
