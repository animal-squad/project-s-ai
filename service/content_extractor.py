import re
from bs4 import BeautifulSoup
import html2text

class ContentExtractor:
    """
    url과 html을 모두 전달받은 경우 html에서 중요한 내용만 추출  
    - 특정 사이트: html 요소를 지정해서 추출 및 텍스트 변환
    - 나머지 사이트: 바로 텍스트로 변환
    """
    def __preprocess(self, html_content):   
        soup = BeautifulSoup(html_content, 'html.parser')
        text_maker = html2text.HTML2Text()
        text_maker.ignore_links = True # 링크는 무시
        return soup, text_maker
    
    
    def extract_youtube(self, html_content):
        soup, _ = self.__preprocess(html_content)
        
        title = soup.find('title')
        content = soup.find('meta', attrs={'name': 'description'})["content"]
        
        return title if title else None, content if content else None
    

    def extract_velog(self, html_content):
        soup, _ = self.__preprocess(html_content)
        
        title = soup.find('meta', property='og:title')["content"]
        content = soup.find('div', class_='sc-eGRUor gdnhbG atom-one')
        
        return title if title else None, content if content else None
    

    def extract_okky(self, html_content):
        soup, _ = self.__preprocess(html_content)
        
        title = soup.find('title')
        content = soup.find('div', {
            'contenteditable': 'false', 
            'class': 'ProseMirror remirror-editor remirror-a11y-dark'
        }).text
        
        return title if title else None, content if content else None

   
    
    def extract_tistory(self, html_content):
        soup, _ = self.__preprocess(html_content)
        
        title = (
            soup.find('meta', property='og:title')["content"] or
            soup.find('title') or
            soup.find('h2') or
            soup.find('h1') or
            soup.find('p', class_='txt_sub_tit') 
        )
        content = (
            soup.find('div', id='article-view') or
            soup.find('div', class_='area_view') or
            soup.find('div', class_='contents_style') or
            soup.find('article', id='article')
        )
        
        return title if title else None, content if content else None
    
    
    def extract_generic(self, html_content):
        # 특정되지 않은 일반 사이트의 특정 콘텐츠 추출 (title, content)
        soup, _ = self.__preprocess(html_content)
        
        title = (
            soup.find('title') or 
            soup.find('meta', attrs={'name': 'description'}) or 
            soup.find('meta', property='og:title') or
            soup.find('h1')
        )
        content = (
            soup.find('article') or 
            soup.find('div', id='content') or 
            soup.find('div', class_='post') or 
            soup.find('main') or
            soup.find('body')
        )
        
        return title if title else None, content if content else None


    def html_to_text(self, title, content):
        # 특정 사이트 + 일반 사이트 전체 HTML을 텍스트로 변환
        text_maker = html2text.HTML2Text()
        text_maker.ignore_links = True
        
        title_text = text_maker.handle(str(title)) if title else None
        content_text = text_maker.handle(str(content)) if content else None
        
        return title_text, content_text 
    
    
    def _post_process(self, title_text, content_text):
        # 변환한 텍스트를 정규표현식으로 후처리
        def clean_text(text):
            if text is None:
                return None
            combined_pattern = r"[^\w\s.,!?()]+|!\([^)]*\)|http\S+"
            cleaned_text = re.sub(combined_pattern, "", text)
            return re.sub(r"\s+", " ", cleaned_text).strip()
        
        return clean_text(title_text), clean_text(content_text)


    def _format_result(self, title, content):
        # 딕셔너리 형식으로 최종 반환
        if title is None and content is None:
            return None
        return {
            "title": title,
            "content": content
        }

    def process_content(self, html_content, extract_method):
        # 추출-처리 파이프라인 실행
        title, content = extract_method(html_content)
        title_text, content_text = self.html_to_text(title, content)
        clean_title, clean_content = self._post_process(title_text, content_text)
        return self._format_result(clean_title, clean_content)