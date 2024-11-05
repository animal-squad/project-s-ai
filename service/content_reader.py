class ContentReader:
    def can_crawl(self, url: str) -> bool:
        """
        주어진 URL의 robots.txt를 읽어 크롤링 할 수 있는지 없는지 판단
        :param url: 판단하려는 URL
        :return: 크롤링 할 수 있는지 여부
        """
        pass

    def fetch_html_content(self, url: str) -> str:
        """
        주어진 URL의 HTML 정보를 반환
        :param url: 정보를 얻어오려는 URL
        :return: 읽은 HTML
        """
        pass

    def perform_google_search(self, query: str) -> str | None:
        """
        주어진 쿼리를 Google에 검색한 결과를 반환. 결과가 없다면 None 반환
        :param query: Google에 검색하려는 쿼리
        :return: 검색한 결과
        """
        pass

    def read_content(self, url: str) -> str | None:
        """
        URL의 컨텐츠 정보를 반환. 만약 정보를 읽을 수 없다면 None 반환
        :param url:
        :return:
        """
        if self.can_crawl(url):
            return self.fetch_html_content(url)
        else:
            return self.perform_google_search(url)