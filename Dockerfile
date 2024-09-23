FROM python:3.11-slim

# 작업 디렉토리 설정
WORKDIR /usr/src/app

# requirements.txt 파일을 컨테이너로 복사
COPY requirements.txt ./

# 종속성 설치
RUN pip install --no-cache-dir -r requirements.txt

# Django 프로젝트 파일을 컨테이너로 복사
COPY . .

# 포트 8000을 오픈
EXPOSE 8000

# Django 서버 실행 (자동 재시작 비활성화)
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
