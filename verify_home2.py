"""
LUMIÈRE LASH & BROW - Home 2 Page Quality & Asset Audit
"""

import os
from html.parser import HTMLParser

class Home2Auditor(HTMLParser):
    def __init__(self):
        super().__init__()
        self.images = []
        self.sources = []
        self.links = []
        
    def handle_starttag(self, tag, attrs):
        attr_dict = dict(attrs)
        if tag == "img":
            self.images.append(attr_dict)
        elif tag == "source":
            self.sources.append(attr_dict)
        elif tag == "a":
            href = attr_dict.get("href")
            if href:
                self.links.append(href)

def run_audit():
    print("=" * 60)
    print("AUDITING LUMIÈRE HOME 2 (home2.html)")
    print("=" * 60)
    
    html_file = "home2.html"
    assert os.path.exists(html_file), "home2.html does not exist!"
    
    with open(html_file, "r", encoding="utf-8") as f:
        content = f.read()
        
    parser = Home2Auditor()
    parser.feed(content)
    
    print(f"[+] Found {len(parser.images)} <img> tags in home2.html:")
    for img in parser.images:
        src = img.get("src")
        alt = img.get("alt")
        assert src, "Image tag missing src!"
        assert os.path.exists(src), f"Image file missing on disk: {src}"
        assert alt, f"Image missing alt attribute: {src}"
        print(f"    - Image OK: {src} (alt='{alt[:35]}...')")
        
    print(f"[+] Found {len(parser.sources)} <source> tags:")
    for src in parser.sources:
        srcset = src.get("srcset")
        assert srcset, "Source tag missing srcset!"
        assert os.path.exists(srcset), f"WebP source missing on disk: {srcset}"
        print(f"    - WebP Source OK: {srcset}")
        
    print(f"[+] Found {len(parser.links)} links in home2.html.")
    print("=" * 60)
    print("[SUCCESS] ALL HOME 2 ASSETS & IMAGES AUDITED AND VERIFIED PERFECTLY!")
    print("=" * 60)

if __name__ == "__main__":
    run_audit()
