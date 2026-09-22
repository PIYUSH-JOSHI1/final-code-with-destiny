import os
import re

chapters = [
    "chapter1_extension.html",
    "chapter2_extension.html",
    "chapter3_extension.html",
    "chapter4_extension.html",
    "chapter5_extension.html"
]

for chapter in chapters:
    filepath = os.path.join(r"c:\Users\Piyush\Downloads\Code with destiny", chapter)
    if not os.path.exists(filepath):
        continue
        
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # 1. Remove ALL `.page-copy` buttons properly (accounting for newlines and spaces)
    content = re.sub(r'<button[^>]*class="[^"]*page-copy[^"]*"[^>]*>.*?<\/button>', '', content, flags=re.DOTALL)
    
    # 2. Remove ALL `.btn-copy-ch` buttons
    content = re.sub(r'<button[^>]*class="[^"]*btn-copy-ch[^"]*"[^>]*>.*?<\/button>', '', content, flags=re.DOTALL)

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
        
print("Successfully removed remaining copy buttons.")
