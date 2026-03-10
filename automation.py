import os
import openai
import requests
from datetime import datetime
import random

# Set your OpenAI API key
openai.api_key = os.getenv('OPENAI_API_KEY')  # Make sure to set this environment variable

# Keywords from '微光 100' plan
keywords = ["低調", "尊重", "同理心", "純真希望"]

# Fixed style prompt
style_prompt = "A hyper-realistic close-up shot, capturing intricate skin texture and pores, Phase One XF, 100mm macro, cinematic bokeh, 8k resolution, photorealistic"

# Step 1: Generate 5 image prompts daily
def generate_prompts():
    prompts = []
    for i in range(5):
        # Use OpenAI to generate a unique subject based on keywords, varying daily
        today_seed = datetime.now().strftime("%Y-%m-%d")
        random.seed(today_seed + str(i))  # Seed for daily variation
        theme = random.choice(keywords)
        
        # Generate a creative subject using ChatGPT
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are a creative prompt generator for soul-stirring images inspired by the '微光 100' plan, emphasizing subtlety, respect, empathy, and pure hope."},
                {"role": "user", "content": f"Generate a short, poetic subject description incorporating the theme '{theme}'. Keep it concise, e.g., 'a gentle hand reaching out in quiet support'."}
            ]
        )
        subject = response.choices[0].message.content.strip()
        
        full_prompt = f"{subject}, {style_prompt}"
        prompts.append(full_prompt)
    return prompts

# Step 2: Generate 5 images (9:16 aspect ratio) using DALL-E 3
def generate_images(prompts):
    image_urls = []
    for prompt in prompts:
        response = openai.Image.create(
            model="dall-e-3",
            prompt=prompt,
            size="1024x1792",  # Closest to 9:16 (9/16 ≈ 0.5625, 1024x1792 = 0.5714)
            quality="hd",
            n=1
        )
        image_url = response.data[0].url
        # Download the image
        img_data = requests.get(image_url).content
        img_filename = f"image_{len(image_urls) + 1}.png"
        with open(img_filename, 'wb') as handler:
            handler.write(img_data)
        image_urls.append(img_filename)
    return image_urls

# Generate warm, sentimental phrases for each image
def generate_phrases(num=5):
    phrases = []
    for i in range(num):
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "Generate warm, sentimental short phrases inspired by subtlety, respect, empathy, and pure hope."},
                {"role": "user", "content": "Create one short, touching phrase, e.g., 'In quiet moments, hope whispers.'"}
            ]
        )
        phrase = response.choices[0].message.content.strip()
        phrases.append(phrase)
    return phrases

# Step 3: Generate minimal index.html with Tailwind CSS, dark background, slow fade-in for images
def generate_webpage(image_files, phrases):
    html_content = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>微光 100</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <style>
        .fade-in {
            animation: fadeIn 3s ease-in;
        }
        @keyframes fadeIn {
            from { opacity: 0; }
            to { opacity: 1; }
        }
    </style>
</head>
<body class="bg-gray-900 text-white flex flex-col items-center justify-center min-h-screen p-4">
    <h1 class="text-4xl font-serif mb-8">微光 100 - Daily Glimmers</h1>
    <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
"""

    for img, phrase in zip(image_files, phrases):
        html_content += f"""
        <div class="flex flex-col items-center">
            <img src="{img}" alt="Glimmer Image" class="w-full max-w-md rounded-lg shadow-lg fade-in">
            <p class="mt-4 text-lg italic text-center">"{phrase}"</p>
        </div>
"""

    html_content += """
    </div>
</body>
</html>
"""

    with open('index.html', 'w') as f:
        f.write(html_content)

# Main function to run the entire process
def main():
    prompts = generate_prompts()
    image_files = generate_images(prompts)
    phrases = generate_phrases(len(image_files))
    generate_webpage(image_files, phrases)
    print("Process completed: Prompts generated, images created, webpage updated.")

if __name__ == "__main__":
    main()
