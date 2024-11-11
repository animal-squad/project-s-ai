# project-s-ai
Project S AI 파트 repository입니다.

## API
`/docs` 참조

## 실행
1. 필요 모듈 설치
    ```shell
    pip install -r requirment.txt
    ```
2. 환경 변수 설정
    ```shell
    export PYTHONPATH="${PYTHONPATH}:<현재 디렉토리>"
    export OPENAI_API_KEY="<api_key>"
    export GOOGLE_SEARCH_API_KEY="<google_search_api_key>"
    export GOOGLE_SEARCH_CX="<google_search_cx>" 
    ```
3. 서버 실행
    ```shell
    fastapi run
    ```