# 공식 Python 이미지를 베이스로 사용
FROM python:3.11-slim

# 컨테이너 내 작업 디렉토리 설정
WORKDIR /app

# 요구사항 파일을 컨테이너에 복사
COPY requirement.txt .

# 의존성 설치
RUN pip install --no-cache-dir -r requirement.txt

# 현재 디렉토리의 내용을 컨테이너의 /app 디렉토리에 복사
COPY . .

# PYTHONPATH를 현재 디렉토리를 포함하도록 수정
ENV PYTHONPATH="./"

# 애플리케이션이 사용하는 포트 노출
EXPOSE 80

# API 키를 위한 환경 변수 정의 (값은 Kubernetes에서 주입됨)
ENV OPENAI_API_KEY=""
ENV GOOGLE_SEARCH_API_KEY=""
ENV GOOGLE_SEARCH_CX=""

# Uvicorn을 사용하여 FastAPI 애플리케이션 실행
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "80"]
