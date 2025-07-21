# 使用官方 Python 映像
FROM python:3.12-slim

WORKDIR /app

# 複製需求檔並安裝依賴
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 複製程式碼
COPY . .

# 設定環境變數避免 Python buffer
ENV PYTHONUNBUFFERED=1

# 容器啟動時執行 Flask
CMD ["python", "app.py"]
