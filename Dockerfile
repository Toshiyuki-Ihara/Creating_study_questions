# Python 3.12 をベースに使用
FROM python:3.12-slim

# 必要なシステムパッケージをインストール
RUN apt-get update && apt-get install -y \
    poppler-utils \
    tesseract-ocr \
    tesseract-ocr-jpn \
    libgl1 \
    libglib2.0-0 \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# 作業ディレクトリを作成・移動
WORKDIR /app

# Python依存パッケージのインストール
COPY . .
RUN pip install --no-cache-dir --break-system-packages -r requirements.txt

# アプリケーションコードのコピー
COPY . .

# FastAPI用のポートを公開
EXPOSE 8000

# アプリケーションの起動コマンド
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
