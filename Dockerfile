FROM python:3.10.8-slim

WORKDIR /app

COPY . /app

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 8000 8501

CMD ["sh", "-c", "streamlit run app/frontend/app.py --server.port 8501 & uvicorn app.backend.main:app --host 0.0.0.0 --port 8000"]

