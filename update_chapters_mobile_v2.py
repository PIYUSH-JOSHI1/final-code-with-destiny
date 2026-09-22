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

    # 1. Revert CSS from previous injection
    # We find .mobile-next-btn { ... } @media (max-width:768px) { ... }
    # and replace it with just the new CSS
    
    css_pattern = r'\.mobile-next-btn\s*\{.*?\@media\s*\(max-width:768px\)\s*\{.*?\}\s*\n\s*\@media\s*\(max-width:560px\)\s*\{'
    
    new_css = """/* mobile bottom nav and no-copy */
    body {
      -webkit-user-select: none;
      -moz-user-select: none;
      -ms-user-select: none;
      user-select: none;
    }
    .mobile-bottom-nav {
      display: none;
      position: fixed;
      bottom: 0; left: 0; right: 0;
      background: var(--desk);
      border-top: 1px solid var(--line);
      z-index: 100;
      padding: 10px 16px;
      padding-bottom: calc(10px + env(safe-area-inset-bottom));
      justify-content: space-between;
      gap: 8px;
    }
    .mobile-bottom-nav button {
      background: var(--paper-2);
      color: var(--ink);
      border: none;
      border-radius: 4px;
      padding: 12px 10px;
      font-family: var(--mono, monospace);
      font-size: 11.5px;
      font-weight: 700;
      flex: 1;
      text-transform: uppercase;
      letter-spacing: .05em;
      cursor: pointer;
    }
    .mobile-bottom-nav button:disabled {
      opacity: 0.5;
    }
    .mobile-fullscreen-page {
      position: fixed !important;
      top: 0 !important;
      left: 0 !important;
      right: 0 !important;
      bottom: 60px !important;
      z-index: 99 !important;
      margin: 0 !important;
      border-radius: 0 !important;
      overflow-y: auto !important;
      padding-bottom: 40px !important;
    }
    @media (max-width: 768px) {
      .mobile-bottom-nav {
        display: flex;
      }
      body {
        padding-bottom: 70px;
      }
    }
    @media (max-width:560px) {"""
    
    content = re.sub(css_pattern, new_css, content, flags=re.DOTALL)

    # 2. Revert the previous JS injection and inject the new bottom nav JS + no-copy JS
    js_pattern = r'// Add "Next page" buttons for mobile reading.*?// tabs scrollspy'
    
    new_js = """// Prevent right click / copy
        document.addEventListener('contextmenu', function(e) { e.preventDefault(); });
        document.addEventListener('copy', function(e) { e.preventDefault(); });

        // Mobile reading bottom nav
        var pages = Array.prototype.slice.call(document.querySelectorAll(".page"));
        var currentPageIndex = 0;
        var isFullScreen = false;

        var navHtml = '<div class="mobile-bottom-nav">' +
          '<button id="btnPrevPage">Back Page</button>' +
          '<button id="btnFullScreen">Full Screen</button>' +
          '<button id="btnNextPage">Next Page</button>' +
        '</div>';
        document.body.insertAdjacentHTML('beforeend', navHtml);

        var btnPrev = document.getElementById("btnPrevPage");
        var btnNext = document.getElementById("btnNextPage");
        var btnFull = document.getElementById("btnFullScreen");

        function updateNav() {
            btnPrev.disabled = currentPageIndex <= 0;
            btnNext.disabled = currentPageIndex >= pages.length - 1;
        }

        function syncCurrentPage() {
            if (isFullScreen || pages.length === 0) return;
            var minDiff = Infinity;
            var bestIdx = 0;
            pages.forEach(function(p, i) {
                var rect = p.getBoundingClientRect();
                var diff = Math.abs(rect.top);
                if (diff < minDiff) {
                    minDiff = diff;
                    bestIdx = i;
                }
            });
            currentPageIndex = bestIdx;
            updateNav();
        }

        window.addEventListener('scroll', function() {
            if(!isFullScreen) syncCurrentPage();
        });

        btnPrev.addEventListener("click", function() {
            if (currentPageIndex > 0) {
                currentPageIndex--;
                pages[currentPageIndex].scrollIntoView({behavior: "smooth", block: "start"});
                updateNav();
            }
        });

        btnNext.addEventListener("click", function() {
            if (currentPageIndex < pages.length - 1) {
                currentPageIndex++;
                pages[currentPageIndex].scrollIntoView({behavior: "smooth", block: "start"});
                updateNav();
            }
        });

        btnFull.addEventListener("click", function() {
            isFullScreen = !isFullScreen;
            if (isFullScreen) {
                btnFull.textContent = "Exit Full";
                pages.forEach(function(p, i) {
                    if (i !== currentPageIndex) p.style.display = 'none';
                    else {
                        p.classList.add('mobile-fullscreen-page');
                        p.scrollIntoView();
                    }
                });
                document.body.style.overflow = 'hidden';
            } else {
                btnFull.textContent = "Full Screen";
                pages.forEach(function(p) {
                    p.style.display = '';
                    p.classList.remove('mobile-fullscreen-page');
                });
                document.body.style.overflow = '';
                pages[currentPageIndex].scrollIntoView({block: "start"});
            }
        });
        syncCurrentPage();

        // tabs scrollspy"""
        
    content = re.sub(js_pattern, new_js, content, flags=re.DOTALL)

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
        
print("Chapters updated with mobile bottom nav and copy prevention.")
