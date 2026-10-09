"""
LUMIÈRE LASH & BROW - Contact Page Complete Quality & Completeness Audit
Validates contact.html structure, section IDs, booking form, real map, FAQ, images, and links.
"""

import os
import re
from html.parser import HTMLParser

class SimpleContactAuditor(HTMLParser):
    def __init__(self):
        super().__init__()
        self.sections = []
        self.in_main = False
        self.images = []
        self.sources = []
        self.links = []
        self.iframes = []
        self.inputs = []
        self.selects = []
        self.labels = []
        self.titles = []
        self.in_title = False
        
    def handle_starttag(self, tag, attrs):
        attr_dict = dict(attrs)
        if tag == "title":
            self.in_title = True
        elif tag == "main":
            self.in_main = True
        elif tag == "section" and self.in_main:
            s_id = attr_dict.get("id")
            if s_id:
                self.sections.append(s_id)
        elif tag == "img":
            self.images.append(attr_dict)
        elif tag == "source":
            self.sources.append(attr_dict)
        elif tag == "iframe":
            self.iframes.append(attr_dict)
        elif tag == "a":
            href = attr_dict.get("href")
            if href:
                self.links.append(href)
        elif tag in ["input", "textarea"]:
            self.inputs.append(attr_dict)
        elif tag == "select":
            self.selects.append(attr_dict)
        elif tag == "label":
            self.labels.append(attr_dict)
                
    def handle_endtag(self, tag):
        if tag == "title":
            self.in_title = False
        elif tag == "main":
            self.in_main = False
            
    def handle_data(self, data):
        if self.in_title:
            self.titles.append(data.strip())

def run_audit():
    print("=" * 60)
    print("AUDITING LUMIÈRE CONTACT PAGE (contact.html)")
    print("=" * 60)
    
    html_file = "contact.html"
    if not os.path.exists(html_file):
        print("[-] FAILED: contact.html does not exist!")
        return
        
    with open(html_file, "r", encoding="utf-8") as f:
        content = f.read()
        
    parser = SimpleContactAuditor()
    parser.feed(content)
    
    print(f"[+] Page Title: {' '.join(parser.titles)}")
    print(f"[+] Found {len(parser.sections)} Main Sections: {parser.sections}")
    
    expected_ids = [
        "contact-intro",
        "booking",
        "beauty-direction",
        "before-you-visit",
        "studio-location",
        "contact-faq",
        "contact-closing"
    ]
    
    assert parser.sections == expected_ids, f"Section IDs mismatch! Got {parser.sections} vs {expected_ids}"
    print("[+] Section IDs match exactly 7 required sections.")
    
    # Check images
    print(f"[+] Checking {len(parser.images)} <img> tags...")
    for img in parser.images:
        src = img.get("src")
        alt = img.get("alt")
        assert src, "Image tag missing src!"
        assert os.path.exists(src), f"Image missing on disk: {src}"
        assert alt is not None, f"Image missing alt attribute: {src}"
        print(f"    - Image OK: {src} (alt='{alt[:35]}...')")
        
    for src in parser.sources:
        srcset = src.get("srcset")
        assert srcset, "Source tag missing srcset!"
        assert os.path.exists(srcset), f"WebP source missing on disk: {srcset}"
        print(f"    - WebP Source OK: {srcset}")
        
    # Check Map
    print(f"[+] Checking Map iFrames: {len(parser.iframes)} found...")
    assert len(parser.iframes) >= 1, "Visible Map iframe missing!"
    for iframe in parser.iframes:
        src = iframe.get("src")
        title = iframe.get("title")
        assert src, "iFrame missing src!"
        assert title, "iFrame missing accessible title attribute!"
        print(f"    - Visible Map OK: {title} (src='{src[:40]}...')")
        
    # Check Form Controls & Labels
    print(f"[+] Checking Form: {len(parser.inputs)} inputs/textareas, {len(parser.selects)} selects, {len(parser.labels)} labels.")
    assert len(parser.labels) >= 6, "Form missing accessible labels!"
    assert "bookingStatusMessage" in content, "Booking status feedback message container missing!"
    
    # Check Links
    print(f"[+] Checking {len(parser.links)} links...")
    for link in set(parser.links):
        if link.startswith("#") or link.startswith("http") or link.startswith("mailto:"):
            continue
        base_link = link.split("#")[0]
        if base_link and not os.path.exists(base_link):
            print(f"    [!] Warning: internal link target not found: {link}")
        else:
            print(f"    - Internal link verified: {link}")
            
    print("=" * 60)
    print("[SUCCESS] ALL CONTACT PAGE AUDITS PASSED PERFECTLY!")
    print("=" * 60)

if __name__ == "__main__":
    run_audit()
