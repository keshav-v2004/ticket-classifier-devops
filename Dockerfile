FROM python:3.10-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .
# Expose ports for both FastAPI and Streamlit
EXPOSE 8000 8501