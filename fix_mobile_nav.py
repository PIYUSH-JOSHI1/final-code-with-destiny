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

    js_pattern = r'// Mobile reading bottom nav.*?// tabs scrollspy'
    
    new_js = """// Mobile reading bottom nav
        var pages = Array.prototype.slice.call(document.querySelectorAll(".page"));
        var currentPageIndex = 0;
        var isFullScreen = false;
        var isScrolling = false;
        var scrollTimeout = null;

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
            if (isFullScreen || isScrolling || pages.length === 0) return;
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
            syncCurrentPage();
        });

        btnPrev.addEventListener("click", function() {
            if (currentPageIndex > 0) {
                if (isFullScreen) {
                    pages[currentPageIndex].style.display = 'none';
                    pages[currentPageIndex].classList.remove('mobile-fullscreen-page');
                }
                currentPageIndex--;
                if (isFullScreen) {
                    pages[currentPageIndex].style.display = '';
                    pages[currentPageIndex].classList.add('mobile-fullscreen-page');
                    pages[currentPageIndex].scrollTop = 0;
                } else {
                    isScrolling = true;
                    pages[currentPageIndex].scrollIntoView({behavior: "smooth", block: "start"});
                    clearTimeout(scrollTimeout);
                    scrollTimeout = setTimeout(function(){ isScrolling = false; syncCurrentPage(); }, 800);
                }
                updateNav();
            }
        });

        btnNext.addEventListener("click", function() {
            if (currentPageIndex < pages.length - 1) {
                if (isFullScreen) {
                    pages[currentPageIndex].style.display = 'none';
                    pages[currentPageIndex].classList.remove('mobile-fullscreen-page');
                }
                currentPageIndex++;
                if (isFullScreen) {
                    pages[currentPageIndex].style.display = '';
                    pages[currentPageIndex].classList.add('mobile-fullscreen-page');
                    pages[currentPageIndex].scrollTop = 0;
                } else {
                    isScrolling = true;
                    pages[currentPageIndex].scrollIntoView({behavior: "smooth", block: "start"});
                    clearTimeout(scrollTimeout);
                    scrollTimeout = setTimeout(function(){ isScrolling = false; syncCurrentPage(); }, 800);
                }
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
                        p.style.display = '';
                        p.classList.add('mobile-fullscreen-page');
                        p.scrollTop = 0;
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
        
print("Mobile navigation logic fixed.")
