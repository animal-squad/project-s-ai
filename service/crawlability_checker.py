from urllib.parse import urlparse, parse_qs

import requests
from requests.packages import target


class CrawlabilityChecker:
    def robots_txt_parser(self, url: str) -> dict[str, dict[str, list[str]]] | None:
        """
        robots.txt 파일을 읽어 각 User-agent 별로 허용되는/되지않는 도메인을 분류
        :param url: {protocol}://{domain}/robots.txt 형태의 URL
        :return:
            robots.txt가 없으면 None 반환
            User-agent 별로 허용되는/되지않는 도메인을 분류하여 전달
        :raise ValueError: robots.txt에 접근이 불가능할 때 오류 반환
        """
        robots_txt = requests.get(url)
        if robots_txt.status_code == 404:
            return None
        elif robots_txt.status_code == 403:
            raise ValueError("robots.txt 파일에 접근할 수 없습니다.")

        texts = robots_txt.text.split('\n')

        allow_disallow_info = {}

        recent_agent = ""
        for info in texts:
            if len(info) and info[0] == '#':
                continue

            if info.find(":") != -1:
                key, value = info.split(":")[:2]
                key = key.lower()

                if key.find("user-agent") != -1:
                    recent_agent = value.strip()
                    allow_disallow_info[recent_agent] = {"Allow": [], "Disallow": []}
                elif key.find("disallow") != -1:
                    allow_disallow_info[recent_agent]["Disallow"].append(value.strip())
                elif key.find("allow") != -1:
                    allow_disallow_info[recent_agent]["Allow"].append(value.strip())

        return allow_disallow_info

    def parse_url(self, url: str) -> dict[str, str]:
        """
        주어진 URL을 protocol, domain, path, query로 분류
        :param url: 분류하려는 URL
        :return: 분류된 결과 dictionary
        """
        parsed_url = urlparse(url)

        protocol = parsed_url.scheme
        domain = parsed_url.netloc
        path = parsed_url.path
        query = parse_qs(parsed_url.query)

        return {
            "protocol": protocol,
            "domain": domain,
            "path": path,
            "query": query
        }

    def can_crawl(self, url: str) -> bool:
        """
        URL의 robots.txt를 읽어 크롤링이 가능한지 판단
        :param url: 크롤링할 URL
        :return: 크롤링 가능 여부
        """
        parsed_url = self.parse_url(url)

        robots_txt_url = f'{parsed_url["protocol"]}://{parsed_url["domain"]}/robots.txt'
        try:
            robots_txt = self.robots_txt_parser(robots_txt_url)
        except ValueError:  # robots.txt 파일에 접근하지 못하는 경우
            return False

        if (
                (robots_txt is None) or  # robots.txt 파일이 아예 없는 경우
                ("*" not in robots_txt) or  # User-agent에 *이 없거나
                (not robots_txt["*"]["Allow"] and not robots_txt["*"]["Disallow"]) or  # User-agent: "*"이 비어있거나
                ("/" in robots_txt["*"]["Allow"])  # User-agent: "*"의 "/"가 allow라면
        ):  # 크롤링 가능
            return True

        # Disallow가 있는 경우
        all_agent = robots_txt["*"]
        if "/" in all_agent["Disallow"]:  # Disallow: "/"라면 크롤링 불가능
            return False

        # 모든 Disallow의 path를 확인하며 현재 URL의 path와 비교
        can_crawl_flag = True
        target_path_list = parsed_url["path"].split("/")
        for disallow in all_agent["Disallow"]:
            disallow_path_list = disallow.split("/")
            is_disallow = True  # 주어진 URL이 현재 검사하려는 Disallow path와 같은지

            # 만약 disallow_path의 길이가 더 긴 상황에서 IndexError가 발생하는 상황은 아래와 같은 2가지 경우
            # target_path = /a/b/c
            # disallow_path = /*/*/*/d
            # disallow_path = /a/b/c/d
            # 위의 두가지 경우 모두 disallow에 해당되지 않기 때문에 크롤링이 가능한 페이지이다.
            if len(target_path_list) < len(disallow_path_list):
                break

            for idx, path in enumerate(disallow_path_list):
                # disallow path와 URL의 path가 다른 경우
                if path != "*" and target_path_list[idx] != path:
                    is_disallow = False
                    break

            # disallow path와 URL의 path가 같은 경우
            if is_disallow:
                can_crawl_flag = False
                break

        return can_crawl_flag
