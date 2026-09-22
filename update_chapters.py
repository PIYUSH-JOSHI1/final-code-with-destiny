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

    # 1. Remove all Copy page buttons
    content = re.sub(r'<button class="btn btn-paper page-copy">Copy page</button>', '', content)
    
    # 2. Remove all Copy chapter buttons
    content = re.sub(r'<button class="btn btn-dark btn-copy-ch">Copy chapter.*?<\/button>', '', content)

    # 3. Add Mobile responsive CSS for tabs
    # We find `@media (max-width:560px) {` and prepend our new 768px media query
    css_insert = """
    .mobile-next-btn {
      display: none;
      width: 100%;
      margin-top: 24px;
      padding: 16px;
      text-align: center;
      background: var(--paper-2);
      color: var(--ink);
      font-family: var(--mono, monospace);
      font-weight: 600;
      text-transform: uppercase;
      letter-spacing: .1em;
      border: 1px solid var(--paper-edge);
      border-radius: 6px;
      cursor: pointer;
    }
    @media (max-width:768px) {
      .tabs {
        top: auto;
        bottom: 0;
        border-bottom: none;
        border-top: 1px solid var(--line);
        padding-bottom: env(safe-area-inset-bottom);
      }
      .mobile-next-btn {
        display: block;
      }
    }
    @media (max-width:560px) {"""
    
    if ".mobile-next-btn" not in content:
        content = content.replace("@media (max-width:560px) {", css_insert, 1)

    # 4. Replace JS copy block with Next Page block
    # The block starts at `function copyText(text, cb) {` and ends before `// tabs scrollspy`
    # We will use regex to find and replace this segment.
    
    js_replace = """
        // Add "Next page" buttons for mobile reading
        document.querySelectorAll(".page").forEach(function(page) {
            var next = page.nextElementSibling;
            if(next && next.classList.contains("page")) {
                var btn = document.createElement("button");
                btn.className = "mobile-next-btn";
                btn.innerHTML = "Next Page &darr;";
                btn.addEventListener("click", function() {
                    var smooth = !window.matchMedia("(prefers-reduced-motion: reduce)").matches;
                    // Account for bottom navigation height
                    var y = next.getBoundingClientRect().top + window.pageYOffset - 20;
                    window.scrollTo({top: y, behavior: smooth ? "smooth" : "auto"});
                });
                page.appendChild(btn);
            }
        });

        // tabs scrollspy"""
        
    content = re.sub(r'function copyText\(text, cb\) \{.*?// tabs scrollspy', js_replace, content, flags=re.DOTALL)

    # 5. Remove the `<style>` block that hides the copy buttons at the very bottom
    content = re.sub(r'<style>\s*\.btn-paper\.page-copy,\s*\.btn-dark\.btn-copy-ch,\s*#copyAll\s*\{\s*display:\s*none\s*!important;\s*\}\s*</style>', '', content)

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
        
print("Chapters updated successfully.")
