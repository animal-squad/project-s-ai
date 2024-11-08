import re
from bs4 import BeautifulSoup
import html2text

class ContentExtractor:
    """
    url과 html을 모두 전달받은 경우 html에서 중요한 내용만 추출  
    - 특정 사이트: html 요소를 지정해서 추출 및 텍스트 변환
    - 나머지 사이트: 바로 텍스트로 변환
    """
    def __init__(self, html_content):   # extract한 html을 텍스트로 변환 준비
        self.html_content = html_content
        self.soup = BeautifulSoup(html_content, 'html.parser')
        self.text_maker = html2text.HTML2Text()
        self.text_maker.ignore_links = True # 링크는 무시
    
    
    def extract_youtube(self):
        elements = []
        title = self.soup.find('yt-formatted-string', class_='style-scope ytd-watch-metadata')
        content = self.soup.find('span', class_='yt-core-attributed-string--link-inherit-color')
        
        if title:
            elements.append(str(title))
        if content:
            elements.append(str(content))
        
        return self._post_process(elements) if elements else "No content found in YouTube"


    def extract_velog(self):
        elements = []
        title = self.soup.find('div', class_='head_wrapper')
        content = self.soup.find('div', class_='sc-eGRUor gdnhbG atom-one')
        
        if title:
            elements.append(str(title))
        if content:
            elements.append(str(content))
        
        return self._post_process(elements) if elements else "No content found in Velog"


    def extract_okky(self):
        elements = []
        title = self.soup.find('title')
        content = self.soup.find('div', {'contenteditable': 'false', 'class': 'ProseMirror remirror-editor remirror-a11y-dark'})
        
        if title:
            elements.append(str(title))
        if content:
            elements.append(str(content))
        
        return self._post_process(elements) if elements else "No content found in Okky"
    
    
    def extract_tistory(self):
        elements = []
        title = (
            self.soup.find('title') or
            self.soup.find('h2') or
            self.soup.find('h1') or
            self.soup.find('p', class_='txt_sub_tit')
        )
        content = (
            self.soup.find('div', id='article-view') or
            self.soup.find('div', class_='area_view') or
            self.soup.find('div', class_='contents_style') or
            self.soup.find('article', id='article')
        )
        
        if title:
            elements.append(str(title))
        if content:
            elements.append(str(content))
        
        return self._post_process(elements) if elements else "No content found in Tistory"
    
    
    def extract_generic(self):
        # 일반 사이트의 특정 콘텐츠 추출 (title, content)
        title = self.soup.find('title')
        if not title:
            title = self.soup.find('meta', attrs={'name': 'description'}) or self.soup.find('meta', property='og:title')
        title_text = title.get_text() if title else "Title not found"

        content = self.soup.find('article') or self.soup.find('div', id='content') or \
                self.soup.find('div', class_='post') or self.soup.find('body')
        content_text = self.text_maker.handle(str(content)) if content else "Content not found"
        
        # 리스트 형태로 _post_process로 전달
        return self._post_process([title_text, content_text])


    def html_to_text(self):
        # 특정 사이트 + 일반 사이트 전체 HTML을 텍스트로 변환
        plain_text = self.text_maker.handle(self.html_content)
        return self._post_process(plain_text)   
    
    
    def _post_process(self, elements):
        # 변환한 텍스트를 정규표현식으로 후처리
        combined_text = ' '.join(elements)
        combined_pattern = r"[^\w\s.,!?()]+|!\([^)]*\)|http\S+"
        cleaned_text = re.sub(combined_pattern, "", combined_text)
        return re.sub(r"\s+", " ", cleaned_text).strip()