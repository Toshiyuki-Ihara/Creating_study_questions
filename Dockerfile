# Python 3.12 ベース
FROM python:3.12-slim

# 必要な OS パッケージのインストール
RUN apt-get update && apt-get install -y \
    poppler-utils \
    tesseract-ocr \
    tesseract-ocr-jpn \
    libgl1 \
    libglib2.0-0 \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# 作業ディレクトリ
WORKDIR /app

# Python依存パッケージをインストール
COPY requirements.txt .
RUN pip install --no-cache-dir --break-system-packages -r requirements.txt

# NLTK データを事前にダウンロードして指定パスに保存
RUN python -m nltk.downloader wordnet omw-1.4 -d /usr/local/nltk_data
ENV NLTK_DATA=/usr/local/nltk_data

# アプリケーションのコードをコピー
COPY . .

# ポート公開
EXPOSE 8000

# サーバー起動
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
