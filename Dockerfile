# 1. ベースイメージの指定
# 軽量なPython 3.9イメージを使用（OSの余計なファイルを削ったバージョン）
FROM python:3.9-slim

# 2. コンテナ内の作業ディレクトリを設定
# これ以降のコマンド（COPYやRUN）はこのフォルダ内で行われます
WORKDIR /app

# 3. ローカルファイルをコンテナにコピー
# 自分のパソコンにあるファイルをすべてコンテナの /app フォルダにコピーします
COPY . .

# 4. 依存ライブラリのインストール
# requirements.txtに書かれたFlaskやrequestsなどのライブラリをインストールします
# --no-cache-dir を付けるとイメージサイズを小さく保てます
RUN pip install --no-cache-dir -r requirements.txt

# 5. アプリケーションの実行（Cloud Run 向け最適化）
# Cloud Runは環境変数 $PORT を使用するため、main.py側でそのポートを聴くようにします。
# CMD ["python", "main.py"] でも動きますが、本番環境では Gunicorn などの
# Webサーバーを使用するのが一般的です（ITパスポート：可用性と性能の向上）。
CMD ["python", "main.py"]