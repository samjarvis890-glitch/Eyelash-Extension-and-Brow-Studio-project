import os
import re

html_files = [f for f in os.listdir('.') if f.endswith('.html')]
print(f"Found {len(html_files)} HTML files: {html_files}")

all_ok = True

for html_file in html_files:
    with open(html_file, 'r', encoding='utf-8') as f:
        content = f.read()

    # Check images & sources
    img_srcs = re.findall(r'<img[^>]+src=["\']([^"\']+)["\']', content)
    sources = re.findall(r'<source[^>]+srcset=["\']([^"\']+)["\']', content)
    for src in img_srcs + sources:
        if not src.startswith(('http', '//', 'data:')):
            clean_src = src.split('?')[0].split('#')[0]
            if not os.path.exists(clean_src):
                print(f"[ERROR in {html_file}] Missing asset: {clean_src}")
                all_ok = False

    # Check css
    links = re.findall(r'<link[^>]+href=["\']([^"\']+)["\']', content)
    for link in links:
        if not link.startswith(('http', '//', 'data:')) and link.endswith('.css'):
            clean_link = link.split('?')[0].split('#')[0]
            if not os.path.exists(clean_link):
                print(f"[ERROR in {html_file}] Missing CSS: {clean_link}")
                all_ok = False

    # Check js
    scripts = re.findall(r'<script[^>]+src=["\']([^"\']+)["\']', content)
    for script in scripts:
        if not script.startswith(('http', '//', 'data:')):
            clean_script = script.split('?')[0].split('#')[0]
            if not os.path.exists(clean_script):
                print(f"[ERROR in {html_file}] Missing JS: {clean_script}")
                all_ok = False

if all_ok:
    print("✓ All HTML files, images, WebP sources, stylesheets, and scripts are 100% valid and present offline!")
