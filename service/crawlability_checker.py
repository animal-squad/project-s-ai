import requests


class CrawlabilityChecker:
    def robots_txt_parser(self, url: str) -> dict | None:
        """
        robots.txt 파일을 읽어 각 User-agent 별로 허용되는/되지않는 도메인을 분류
        :param url: protocol://domain/robots.txt 형태의 URL
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
            if info.find("User-agent") != -1:
                recent_agent = info.split(":")[1].strip()
                allow_disallow_info[recent_agent] = {"Allow": [], "Disallow": []}
            elif info.find("Allow") != -1:
                allow_disallow_info[recent_agent]["Allow"].append(info.split(":")[1].strip())
            elif info.find("Disallow") != -1:
                allow_disallow_info[recent_agent]["Disallow"].append(info.split(":")[1].strip())

        return allow_disallow_info
