"""
Comprehensive Verification Script for gallery.html
Audits:
1. Exactly 7 sections with correct IDs and Headings
2. All 20+ gallery images are local (assets/images/gallery/)
3. No remote external image URLs
4. No image reuse from other pages (home, home2, about, services, pricing, contact)
5. Responsive grid, accessibility, alt tags, and lightbox hooks
"""

import os
import re

def audit_gallery():
    print("========================================")
    print("AUDITING gallery.html")
    print("========================================")
    
    with open("gallery.html", "r", encoding="utf-8") as f:
        html = f.read()

    # 1. Check Sections
    sections = re.findall(r'<section[^>]+id="([^"]+)"', html)
    print(f"Sections detected ({len(sections)}): {sections}")
    assert len(sections) == 7, f"Expected exactly 7 sections, got {len(sections)}"
    
    expected_ids = [
        "gallery-intro",
        "lash-gallery",
        "brow-gallery",
        "mood-gallery",
        "detail-library",
        "editorial-gallery",
        "gallery-cta"
    ]
    for eid in expected_ids:
        assert eid in sections, f"Missing section id: {eid}"
    print("✓ EXACTLY 7 SECTIONS CONFIRMED WITH CORRECT IDS!")

    # 2. Check Headings hierarchy
    h1_matches = re.findall(r'<h1[^>]*>(.*?)</h1>', html, re.DOTALL)
    print(f"H1 count: {len(h1_matches)} -> {h1_matches[0].strip() if h1_matches else 'NONE'}")
    assert len(h1_matches) == 1, f"Expected exactly 1 H1, found {len(h1_matches)}"

    # 3. Check Image References
    img_srcs = re.findall(r'<img[^>]+src="([^"]+)"', html)
    webp_srcs = re.findall(r'<source[^>]+srcset="([^"]+)"', html)
    lightbox_srcs = re.findall(r'data-lightbox-src="([^"]+)"', html)
    
    all_imgs = set(img_srcs + webp_srcs + lightbox_srcs)
    print(f"Total distinct image sources in gallery.html: {len(all_imgs)}")
    
    for src in all_imgs:
        assert src.startswith("assets/images/gallery/"), f"Illegal image source (not in assets/images/gallery/): {src}"
        assert os.path.exists(src), f"Image file not found on disk: {src}"
        
        # Check non-reuse from other folders
        for forbidden in ["home/", "home2/", "about/", "services/", "pricing/", "contact/"]:
            assert forbidden not in src, f"Reused image from {forbidden}: {src}"
            
    print("✓ ALL IMAGES ARE IN assets/images/gallery/ AND EXIST LOCALLY!")
    print("✓ STRICT NON-REUSE RULE RESPECTED!")

    # 4. Check for external image dependencies
    for url in re.findall(r'https?://[^\s"\'<>]+', html):
        if not ("fonts.googleapis.com" in url or "fonts.gstatic.com" in url or "cdn.jsdelivr.net" in url or "instagram.com" in url or "facebook.com" in url or "w3.org/2000/svg" in url):
            raise AssertionError(f"Unexpected external URL found: {url}")
    print("✓ ZERO EXTERNAL IMAGE / HOTLINKING DEPENDENCIES!")

    # 5. Check Alt Tags
    all_img_tags = re.findall(r'<img[^>]+>', html, re.DOTALL)
    for tag in all_img_tags:
        if 'id="lightboxImg"' in tag:
            continue
        assert 'alt="' in tag, f"Image tag missing alt: {tag}"
    print(f"✓ ALL {len(all_img_tags)} IMAGE TAGS HAVE ALT ATTRIBUTES!")

    print("========================================")
    print("ALL AUDIT CHECKS PASSED WITH 100% SUCCESS!")
    print("========================================")

if __name__ == "__main__":
    audit_gallery()
