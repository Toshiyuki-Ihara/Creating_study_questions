# Creating_study_questions

このプロジェクトは、画像またはPDFファイルから日本語・英語のテキストを抽出し、選択式または記述式のクイズを自動生成するWebアプリケーションです。FastAPIを利用しており、ブラウザから簡単にアップロードして学習用問題を作成できます。

## 主な機能

- 画像やPDFのアップロードによるテキスト抽出
- 抽出した文章をもとに日本語・英語のクイズを生成
  - 選択式（4択）の単語穴埋め問題
  - 記述式の単語穴埋め問題
- Webブラウザから直感的に利用可能

## 事前準備

1. Python 3.12 以上をインストールしてください。
2. `requirements.txt` に記載されているライブラリをインストールします。

```bash
pip install -r requirements.txt
```

また、OCR を行うために Tesseract と日本語辞書が必要です。Docker 環境を利用する場合は `Dockerfile` を参考にしてください。

## 使い方

1. サーバーを起動します。

```bash
uvicorn main:app --reload
```

2. ブラウザで `http://localhost:8000` にアクセスし、画像または PDF をアップロードしてクイズタイプ（選択式 / 記述式）を選びます。
3. 生成された問題を解いて学習に活用してください。

## フォルダ構成

- `main.py` - FastAPI のエンドポイント定義
- `text_extraction.py` - 画像前処理とテキスト抽出・整形
- `generate_jp_quiz.py` - 日本語のクイズ生成ロジック
- `generate_eng_quiz.py` - 英語のクイズ生成ロジック
- `static/` - ブラウザ向け HTML / JavaScript

## ライセンス

MIT License
