import os
import requests
import random
from datetime import datetime
from openai import OpenAI

# 1. 初始化 OpenAI Client
# 請確保環境變數中已設定 OPENAI_API_KEY
client = OpenAI()

# 2. 設定與計畫參數
keywords = ["低調", "尊重", "同理心", "純真希望"]
style_prompt = "A hyper-realistic close-up shot, capturing intricate skin texture and pores, Shot on Phase One XF, 100mm macro lens, f/2.8, Ray Tracing, cinematic bokeh, 8k resolution, photorealistic"

IMAGE_DIR = "images"
if not os.path.exists(IMAGE_DIR):
    os.makedirs(IMAGE_DIR)

# --- 步驟 1: 生成提示詞 ---
def generate_prompts():
    print("正在生成創意提示詞...")
    prompts = []
    for i in range(5):
        today_seed = datetime.now().strftime("%Y-%m-%d")
        random.seed(today_seed + str(i))
        theme = random.choice(keywords)
        
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": "You are a creative prompt generator for soul-stirring images inspired by the '微光 100' plan..."},
                {"role": "user", "content": f"Generate a short, poetic subject description incorporating the theme '{theme}'..."}
            ]
        )
        subject = response.choices[0].message.content.strip()
        prompts.append(f"{subject}, {style_prompt}")
    return prompts

# --- 步驟 2: 生成並下載圖片 ---
def generate_images(prompts):
    print("正在透過 DALL-E 3 生成圖片 (這需要一點時間)...")
    image_paths = []
    today = datetime.now().strftime("%Y-%m-%d")
    for idx, prompt in enumerate(prompts, start=1):
        try:
            response = client.images.generate(
                model="dall-e-3",
                prompt=prompt,
                size="1024x1792",
                quality="hd",
                n=1
            )
            image_url = response.data[0].url
            img_data = requests.get(image_url).content
            
            img_filename = f"{today}_{idx}.jpg"
            full_path = os.path.join(IMAGE_DIR, img_filename)
            
            with open(full_path, 'wb') as handler:
                handler.write(img_data)
            
            image_paths.append(full_path)
            print(f"成功下載: {full_path}")
        except Exception as e:
            print(f"圖片 {idx} 生成失敗: {e}")
            
    return image_paths

# --- 步驟 3: 生成配文 ---
def generate_phrases(num=5):
    print("正在生成感性配文...")
    phrases = []
    for _ in range(num):
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": "Generate warm, sentimental short phrases inspired by subtlety, respect, empathy, and pure hope."},
                {"role": "user", "content": "Create one short, touching phrase."}
            ]
        )
        phrases.append(response.choices[0].message.content.strip())
    return phrases

# --- 步驟 4: 產生 index.html 檔案 ---
def generate_webpage(image_files, phrases):
    print("正在建構 index.html 網頁...")
    html_content = f"""
<!DOCTYPE html>
<html lang="zh-TW">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>微光 100 - Daily Glimmers</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <style>
        .fade-in {{ animation: fadeIn 3s ease-in; }}
        @keyframes fadeIn {{ from {{ opacity: 0; }} to {{ opacity: 1; }} }}
    </style>
</head>
<body class="bg-gray-900 text-white flex flex-col items-center min-h-screen p-8">
    <h1 class="text-4xl font-serif mb-2 text-center text-amber-50">微光 100</h1>
    <p class="mb-12 text-gray-500 font-light italic">Daily Glimmers • {datetime.now().strftime("%Y-%m-%d")}</p>
    
    <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-12 w-full max-w-6xl">
"""

    for img, phrase in zip(image_files, phrases):
        # 修正：在網頁中，路徑分隔符號應統一使用 /
        web_img_path = img.replace('\\', '/')
        html_content += f"""
        <div class="flex flex-col items-center space-y-4">
            <div class="overflow-hidden rounded-lg shadow-2xl border border-gray-800">
                <img src="{web_img_path}" alt="Glimmer Image" class="w-full h-auto fade-in transition-transform duration-700 hover:scale-105">
            </div>
            <p class="text-lg font-light text-center text-gray-300 leading-relaxed px-4">"{phrase}"</p>
        </div>
"""

    html_content += """
    </div>
    <footer class="mt-24 mb-12 text-gray-600 text-xs tracking-widest uppercase">
        Beyond AI Lab © 2026
    </footer>
</body>
</html>
"""

    with open('index.html', 'w', encoding='utf-8') as f:
        f.write(html_content)
    print("✅ index.html 已成功產生！")

# --- 主程式執行區 ---
def main():
    try:
        prompts = generate_prompts()
        image_files = generate_images(prompts)
        
        if not image_files:
            print("❌ 沒有圖片被生成，停止網頁製作。")
            return
            
        phrases = generate_phrases(len(image_files))
        generate_webpage(image_files, phrases)
        print("\n[微光 100] 計畫：今日流程全部自動化完成。")
        
    except Exception as e:
        print(f"程序執行中發生嚴重錯誤: {e}")

if __name__ == "__main__":
    main()
