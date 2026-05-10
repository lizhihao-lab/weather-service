from flask import Flask, request, render_template_string
import os
import requests
import random
import json

app = Flask(__name__)

# --- 設定 (Configuration) ---
SECRET_PASSWORD = os.environ.get("MY_SITE_PASSWORD", "fukuoka2026")

@app.route("/")
def get_weather_web():
    # --- 認証チェック (Authentication) ---
    user_token = request.cookies.get('auth_token')

    if user_token != SECRET_PASSWORD:
        # 注意：这里的 CSS/JS 大括号都改成了双大括号 {{ }}
        return f"""
        <body style="text-align:center;padding-top:100px;font-family:sans-serif;background:#f0f2f5;">
            <div style="display:inline-block;padding:40px;background:white;border-radius:15px;box-shadow:0 4px 15px rgba(0,0,0,0.1);">
                <h2 style="color:#333;">🔒 認証が必要です</h2>
                <p style="color:#666;font-size:14px;">合言葉を入力してください</p>
                <input type="password" id="pw" placeholder="暗号を入力" style="padding:10px;border:1px solid #ddd;border-radius:5px;width:200px;margin-bottom:10px;"><br>
                <button onclick="login()" style="padding:10px 20px;background:#007bff;color:white;border:none;border-radius:5px;cursor:pointer;font-weight:bold;">送信</button>
            </div>
            <script>
                function login() {{
                    document.cookie = "auth_token=" + document.getElementById('pw').value + ";path=/";
                    location.reload();
                }}
            </script>
        </body>
        """, 403

    # --- データの準備 (Data Preparation) ---
    api_key = os.environ.get("WEATHER_API_KEY")
    city = "Fukuoka"
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric&lang=ja"

    fortunes = ["大吉 🌟", "中吉 ✨", "小吉 🌱", "吉 ☘️", "末吉 🍂"]
    lucky_items = ["ラーメン", "お守り", "青いペン", "スニーカー", "抹茶ラテ"]

    try:
        res = requests.get(url, timeout=10).json()

        # 万が一APIがエラーを返した場合のハンドリング
        if res.get("cod") != 200:
            return f"APIエラー: {res.get('message')}. WEATHER_API_KEYを確認してください。", 500

        temp = res['main']['temp']
        feels_like = res['main']['feels_like']
        humidity = res['main']['humidity']
        wind = res['wind']['speed']
        desc = res['weather'][0]['description']
        icon = res['weather'][0]['icon']

        # --- HTMLテンプレート (Frontend) ---
        # 重要：HTML/CSS/JS内の { } はすべて {{ }} に置換しています
        return f"""
        <!DOCTYPE html>
        <html lang="ja">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Fukuoka Weather & Fortune</title>
            <style>
                body {{ font-family: 'Helvetica Neue', Arial, sans-serif; background: linear-gradient(135deg, #74ebd5 0%, #ACB6E5 100%); min-height: 100vh; margin: 0; display: flex; justify-content: center; align-items: center; }}
                .container {{ background: rgba(255, 255, 255, 0.9); padding: 30px; border-radius: 20px; box-shadow: 0 10px 30px rgba(0,0,0,0.2); width: 90%; max-width: 400px; text-align: center; }}
                .temp {{ font-size: 52px; font-weight: bold; color: #ff4757; margin: 5px 0; }}
                .details {{ display: grid; grid-template-columns: 1fr 1fr; gap: 10px; font-size: 14px; color: #666; background: #f8f9fa; padding: 15px; border-radius: 10px; margin-top: 15px; }}
                .fortune-box {{ margin-top: 30px; padding: 20px; border: 2px dashed #007bff; border-radius: 15px; background: #eef2f7; }}
                .wheel {{ width: 80px; height: 80px; border-radius: 50%; border: 4px solid #fff; box-shadow: 0 4px 10px rgba(0,0,0,0.1); margin: 15px auto; display: flex; align-items: center; justify-content: center; font-size: 40px; background: white; transition: transform 2s cubic-bezier(0.1, 0.7, 0.1, 1); }}
                .btn-spin {{ background: #007bff; color: white; border: none; padding: 12px 25px; border-radius: 25px; cursor: pointer; font-weight: bold; font-size: 16px; }}
            </style>
        </head>
        <body>
            <div class="container">
                <div class="weather-card">
                    <h2 style="margin:0;color:#2f3542;">{city} の天気</h2>
                    <img src="http://openweathermap.org/img/wn/{icon}@2x.png" alt="icon">
                    <div class="temp">{temp}℃</div>
                    <p style="font-size:18px; color:#57606f; margin: 0;">{desc}</p>
                    <div class="details">
                        <div>体感: {feels_like}℃</div>
                        <div>湿度: {humidity}%</div>
                        <div>风速: {wind}m/s</div>
                        <div>エリア: 九州</div>
                    </div>
                </div>

                <div class="fortune-box">
                    <h3 style="margin:0; color:#007bff;">🔮 今日の運勢</h3>
                    <div id="wheel" class="wheel">?</div>
                    <div id="result" style="margin:10px 0; font-weight:bold; height:24px; color:#333;">ボタンを押して占う</div>
                    <button class="btn-spin" onclick="spinWheel()">運勢を占う</button>
                    <p id="item" style="font-size:13px; color:#777; margin-top:10px; min-height:15px;"></p>
                </div>
            </div>

            <script>
                function spinWheel() {{
                    const wheel = document.getElementById('wheel');
                    const result = document.getElementById('result');
                    const item = document.getElementById('item');
                    
                    const fortunes = {json.dumps(fortunes)};
                    const items = {json.dumps(lucky_items)};
                    
                    wheel.style.transform = 'rotate(' + (1800 + Math.random() * 360) + 'deg)';
                    result.innerText = "鑑定中...";
                    item.innerText = "";
                    
                    setTimeout(() => {{
                        const f = fortunes[Math.floor(Math.random() * fortunes.length)];
                        const i = items[Math.floor(Math.random() * items.length)];
                        
                        // 絵文字の抽出ロジック（修正：バックスラッシュのエスケープ）
                        const emoji = f.match(/[\\uD800-\\uDBFF][\\uDC00-\\uDFFF]|\\S/g).pop();
                        wheel.innerText = emoji;
                        result.innerText = f;
                        item.innerText = "ラッキーアイテム: " + i;
                    }}, 2000);
                }}
            </script>
        </body>
        </html>
        """
    except Exception as e:
        # 直接把报错信息显示在网页上，这样就不需要找 textPayload 了
        return f"""
        <div style="color:red; padding:20px; border:2px solid red;">
            <h1>代码运行报错了！</h1>
            <p>具体原因: {e}</p>
            <p>当前的 Commit SHA: 10260aa (确认版本用)</p>
        </div>
        """, 200 # 返回 200 以确保网页能显示出来

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port)