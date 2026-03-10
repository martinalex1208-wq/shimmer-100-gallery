def generate_webpage(image_files, phrases):
    html_content = f"""
<!DOCTYPE html>
<html lang="zh-TW">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>微光 100 - Daily Glimmers</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <style>
        .fade-in {{
            animation: fadeIn 3s ease-in;
        }}
        @keyframes fadeIn {{
            from {{ opacity: 0; }}
            to {{ opacity: 1; }}
        }}
    </style>
</head>
<body class="bg-gray-900 text-white flex flex-col items-center justify-center min-h-screen p-4">
    <h1 class="text-4xl font-serif mb-8 text-center">微光 100 - Daily Glimmers</h1>
    <p class="mb-12 text-gray-400 font-light">{datetime.now().strftime("%Y-%m-%d")}</p>
    <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
"""

    for img, phrase in zip(image_files, phrases):
        # 這裡的 img 路徑會是 "images/xxxx.jpg"
        html_content += f"""
        <div class="flex flex-col items-center">
            <img src="{img}" alt="Glimmer Image" class="w-full max-w-md rounded-lg shadow-2xl fade-in border border-gray-800">
            <p class="mt-4 text-lg italic text-center text-gray-300">"{phrase}"</p>
        </div>
"""

    html_content += """
    </div>
    <footer class="mt-20 mb-10 text-gray-600 text-sm">
        Beyond AI Lab © 2026
    </footer>
</body>
</html>
"""

    with open('index.html', 'w', encoding='utf-8') as f:
        f.write(html_content)
