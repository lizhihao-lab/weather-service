# 🌦️ Fukuoka Weather & Fortune Web App

福岡市のリアルタイムな天気情報と、楽しい「運勢占い」ができるWebアプリケーションです。

## 🌟 主な機能 (Main Features)
- **リアルタイム天気**: OpenWeather APIを使用して、現在の気温、湿度、体感温度などを表示します。
- **運勢占いホイール**: JavaScriptによるアニメーションで、今日の運勢とラッキーアイテムを占います。
- **セキュリティ**: シンプルな「合言葉」によるアクセス制限機能を搭載しています。

## 🛠️ 技術スタック (Tech Stack)
- **Backend**: Python (Flask)
- **Frontend**: HTML5, CSS3, JavaScript
- **Infrastructure**: Docker, Google Cloud Run
- **API**: OpenWeatherMap API

## 🚀 セットアップ方法 (How to Setup)

### 1. 環境変数の設定
クラウド（GCP）にデプロイする際、以下の環境変数を設定してください。
- `WEATHER_API_KEY`: OpenWeatherMapのAPIキー
- `MY_SITE_PASSWORD`: サイトにアクセスするための合言葉（デフォルト: fukuoka2026）

### 2. 開発用コマンド
ローカル環境でテストする場合：
```bash
export WEATHER_API_KEY="あなたのAPIキー"
python main.py
