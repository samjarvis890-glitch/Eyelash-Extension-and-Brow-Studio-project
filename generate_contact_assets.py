"""
LUMIÈRE LASH & BROW - Dedicated Contact Page Asset Synthesizer
Generates all 6 bespoke luxury editorial beauty images for contact.html in assets/images/contact/
Outputs both .webp and .jpg formats in high definition.
"""

import os
import math
import random
import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageEnhance

OUTPUT_DIR = r"assets\images\contact"
os.makedirs(OUTPUT_DIR, exist_ok=True)

# Lumière Brand Color Palette
COLOR_ESPRESSO = (43, 31, 36)        # #2B1F24 Deep Espresso Plum
COLOR_DUSTY_ROSE = (142, 90, 107)    # #8E5A6B Dusty Rose
COLOR_ROSE_GOLD = (200, 154, 139)    # #C89A8B Soft Rose Gold
COLOR_BLUSH_IVORY = (248, 241, 242)  # #F8F1F2 Blush Ivory
COLOR_WARM_CREAM = (255, 249, 246)   # #FFF9F6 Warm Cream
COLOR_GOLD_ACCENT = (222, 185, 154)  # Warm Gold
COLOR_LASH_DARK = (24, 16, 20)       # Rich dark pigment
COLOR_LASH_MED = (44, 30, 36)
COLOR_SKIN_PEACH = (246, 228, 220)
COLOR_SKIN_SHADOW = (222, 188, 176)
COLOR_SKIN_HIGHLIGHT = (255, 246, 242)

def create_radiant_background(w, h, color1, color2, angle=35, radial=False, center=(0.5, 0.4)):
    """Creates an ultra-smooth continuous-tone studio background."""
    y, x = np.ogrid[:h, :w]
    if radial:
        cx, cy = center[0] * w, center[1] * h
        dist = np.sqrt((x - cx)**2 + (y - cy)**2)
        max_dist = np.sqrt(max(cx, w - cx)**2 + max(cy, h - cy)**2)
        norm = np.clip(dist / max_dist, 0, 1)
    else:
        rad = math.radians(angle)
        cos_a, sin_a = math.cos(rad), math.sin(rad)
        norm = (x * cos_a + y * sin_a)
        norm = (norm - norm.min()) / (norm.max() - norm.min() + 1e-6)
    
    r = color1[0] + (color2[0] - color1[0]) * norm
    g = color1[1] + (color2[1] - color1[1]) * norm
    b = color1[2] + (color2[2] - color1[2]) * norm
    arr = np.dstack((r, g, b)).astype(np.uint8)
    return Image.fromarray(arr)

def apply_editorial_finish(img, noise_amount=2.2, glow_color=(255, 244, 238), glow_pos=(0.65, 0.35), glow_radius=550):
    """Applies soft studio ambient light blooms and ultra-fine editorial film grain."""
    w, h = img.size
    glow = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    gdraw = ImageDraw.Draw(glow)
    gx, gy = int(glow_pos[0] * w), int(glow_pos[1] * h)
    
    for r in range(glow_radius, 0, -18):
        alpha = int(42 * (1 - r / glow_radius)**1.6)
        gdraw.ellipse([gx - r, gy - r, gx + r, gy + r], fill=(glow_color[0], glow_color[1], glow_color[2], alpha))
    img.paste(glow, (0, 0), glow)
    
    # Ultra-fine film grain to prevent digital banding
    arr = np.array(img, dtype=np.int16)
    noise = np.random.normal(0, noise_amount, arr.shape)
    arr = np.clip(arr + noise, 0, 255).astype(np.uint8)
    return Image.fromarray(arr)

def render_organic_brow(draw, start_x, start_y, length=460, arch_height=70, density=220, thickness=42, hair_color=COLOR_LASH_DARK, scale=1.0):
    """Renders multi-layered feathered micro-strokes for high-end brow architecture."""
    length = int(length * scale)
    arch_height = int(arch_height * scale)
    density = int(density * scale)
    thickness = int(thickness * scale)
    
    for i in range(density):
        t = i / float(density)
        bx = start_x + t * length
        by = start_y - math.sin(t * math.pi * 0.88) * arch_height
        
        angle_deg = 82 - t * 72 + random.uniform(-6, 6)
        stroke_len = (thickness * (math.sin(t * math.pi) * 0.82 + 0.35)) * random.uniform(0.75, 1.25)
        rad = math.radians(angle_deg)
        
        for _ in range(random.randint(1, 2)):
            ox = random.uniform(-3, 3) * scale
            oy = random.uniform(-4, 4) * scale
            ex = bx + ox + math.cos(rad) * stroke_len
            ey = by + oy - math.sin(rad) * stroke_len
            
            alpha = int(random.uniform(140, 235))
            draw.line([(bx + ox, by + oy), (ex, ey)], fill=(hair_color[0], hair_color[1], hair_color[2], alpha), width=max(1, int(2 * scale)))

def render_almond_eye_base(draw, cx, cy, w=460, h=175, scale=1.0, iris_color=(68, 44, 38)):
    """Renders realistic almond eye contours, sclera, iris with depth, and catchlights."""
    w = int(w * scale)
    h = int(h * scale)
    
    # Orbit shadow & socket depth
    draw.ellipse([cx - w//2 - 45, cy - h//2 - 55, cx + w//2 + 45, cy + h//2 + 55], fill=(228, 194, 184, 110))
    draw.ellipse([cx - w//2 - 12, cy - h//2 - 22, cx + w//2 + 12, cy + h//2 + 22], fill=(255, 245, 240, 190))
    
    # Sclera
    draw.ellipse([cx - w//2, cy - h//2, cx + w//2, cy + h//2], fill=(250, 245, 243, 240))
    
    # Iris with soft shading
    iris_r = int(72 * scale)
    draw.ellipse([cx - iris_r, cy - iris_r + int(6*scale), cx + iris_r, cy + iris_r + int(6*scale)], fill=iris_color)
    draw.ellipse([cx - int(iris_r*0.75), cy - int(iris_r*0.75) + int(6*scale), cx + int(iris_r*0.75), cy + int(iris_r*0.75) + int(6*scale)], fill=(42, 26, 22))
    
    # Pupil
    pupil_r = int(32 * scale)
    draw.ellipse([cx - pupil_r, cy - pupil_r + int(6*scale), cx + pupil_r, cy + pupil_r + int(6*scale)], fill=(16, 10, 12))
    
    # Specular Catchlight
    cl_r = int(14 * scale)
    draw.ellipse([cx - int(24*scale), cy - int(18*scale), cx - int(24*scale) + cl_r, cy - int(18*scale) + cl_r], fill=(255, 255, 255, 240))
    
    # Upper lid contour
    lid_pts = []
    steps = 45
    for i in range(steps + 1):
        t = i / float(steps)
        lx = cx - w//2 + t * w
        ly = cy - h//2 + math.sin(t * math.pi) * int(22 * scale) - math.sin(t * math.pi) * int(48 * scale)
        lid_pts.append((lx, ly))
    
    for i in range(len(lid_pts) - 1):
        draw.line([lid_pts[i], lid_pts[i+1]], fill=(64, 42, 48, 220), width=int(3 * scale))

def render_feathered_lash_set(draw, cx, cy, count=140, base_len=85, curl_factor=1.35, scale=1.0, is_wispy=False):
    """Renders intricate, curved individual lashes with natural taper."""
    span_w = int(360 * scale)
    start_x = cx - span_w // 2
    
    for i in range(count):
        t = i / float(count)
        lx = start_x + t * span_w + random.uniform(-2, 2) * scale
        ly = cy - int(38 * scale) + math.sin(t * math.pi) * int(18 * scale)
        
        bell = math.sin(t * math.pi * 0.92)
        l_len = (base_len * (0.45 + bell * 0.75)) * scale * random.uniform(0.9, 1.1)
        if is_wispy and random.random() < 0.18:
            l_len *= 1.42
            
        base_angle = 125 - t * 75 + random.uniform(-5, 5)
        seg_count = 8
        cur_x, cur_y = lx, ly
        pts = [(cur_x, cur_y)]
        
        for s in range(seg_count):
            st = (s + 1) / float(seg_count)
            ang = base_angle + (st**1.6) * (18 * curl_factor)
            rad = math.radians(ang)
            seg_len = (l_len / seg_count)
            cur_x += math.cos(rad) * seg_len
            cur_y -= math.sin(rad) * seg_len
            pts.append((cur_x, cur_y))
            
        alpha = int(random.uniform(190, 255))
        for p_idx in range(len(pts) - 1):
            stroke_w = max(1, int((3.0 - (p_idx / float(len(pts))) * 2.2) * scale))
            draw.line([pts[p_idx], pts[p_idx+1]], fill=(22, 14, 18, alpha), width=stroke_w)

def save_image_pair(img, basename):
    """Saves both .webp and .jpg versions in high quality."""
    webp_path = os.path.join(OUTPUT_DIR, f"{basename}.webp")
    jpg_path = os.path.join(OUTPUT_DIR, f"{basename}.jpg")
    img.save(webp_path, "WEBP", quality=92, method=6)
    img.convert("RGB").save(jpg_path, "JPEG", quality=92, optimize=True)
    print(f"  [SAVED] {basename}.webp and {basename}.jpg ({img.size[0]}x{img.size[1]})")

# ==============================================================================
# 1. CONTACT INTRO (3:4 Welcoming Studio Entrance Composition)
# ==============================================================================
def generate_contact_intro():
    print("Generating Image 1: contact-intro...")
    W, H = 1200, 1600
    base = create_radiant_background(W, H, COLOR_WARM_CREAM, (244, 224, 218), angle=35)
    draw_layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    draw = ImageDraw.Draw(draw_layer)
    
    # Soft ambient studio arches & warm welcoming backlighting
    for i in range(16):
        r = 600 - i * 35
        alpha = int(24 * (1 - i / 16.0))
        draw.ellipse([600 - r, 800 - r, 600 + r, 800 + r], fill=(200, 154, 139, alpha))
        
    # Elegant hairline margins
    draw.rectangle([65, 65, W - 65, H - 65], outline=(200, 154, 139, 85), width=1)
    
    # Welcoming Portrait Composition
    cx, cy = 600, 780
    scale = 1.35
    
    # Face & Neck Contour
    draw.ellipse([cx - int(320*scale), cy - int(400*scale), cx + int(320*scale), cy + int(460*scale)], fill=(248, 230, 224, 215))
    draw.ellipse([cx - int(280*scale), cy - int(360*scale), cx + int(280*scale), cy + int(410*scale)], fill=(255, 245, 240, 250))
    
    # Brow
    render_organic_brow(draw, cx - int(230*scale), cy - int(150*scale), length=450, arch_height=75, density=230, thickness=38, scale=scale)
    
    # Eye & Eyelashes
    render_almond_eye_base(draw, cx, cy, w=440, h=165, scale=scale, iris_color=(60, 42, 38))
    render_feathered_lash_set(draw, cx, cy, count=150, base_len=88, curl_factor=1.4, scale=scale, is_wispy=True)
    
    base.paste(draw_layer, (0, 0), draw_layer)
    final_img = apply_editorial_finish(base, noise_amount=2.0, glow_pos=(0.6, 0.4), glow_radius=600)
    save_image_pair(final_img, "contact-intro")

# ==============================================================================
# 2. CONTACT SOFT (3:4 Understated Natural Beauty Direction)
# ==============================================================================
def generate_contact_soft():
    print("Generating Image 2: contact-soft...")
    W, H = 1000, 1333
    base = create_radiant_background(W, H, COLOR_BLUSH_IVORY, (244, 226, 220), angle=25)
    draw_layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    draw = ImageDraw.Draw(draw_layer)
    
    # Soft glowing halo
    cx, cy = 500, 680
    for i in range(12):
        r = 450 - i * 32
        alpha = int(28 * (1 - i / 12.0))
        draw.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(255, 248, 245, alpha))
        
    scale = 1.2
    # Soft feathered brow
    render_organic_brow(draw, cx - int(220*scale), cy - int(140*scale), length=420, arch_height=65, density=180, thickness=34, scale=scale)
    # Natural understated eye & 1:1 classic lash definition
    render_almond_eye_base(draw, cx, cy, w=420, h=155, scale=scale, iris_color=(72, 50, 44))
    render_feathered_lash_set(draw, cx, cy, count=100, base_len=75, curl_factor=1.3, scale=scale, is_wispy=False)
    
    base.paste(draw_layer, (0, 0), draw_layer)
    final_img = apply_editorial_finish(base, noise_amount=2.1, glow_pos=(0.5, 0.4), glow_radius=550)
    save_image_pair(final_img, "contact-soft")

# ==============================================================================
# 3. CONTACT DEFINED (3:4 Clean Polished Definition Beauty Direction)
# ==============================================================================
def generate_contact_defined():
    print("Generating Image 3: contact-defined...")
    W, H = 1000, 1333
    base = create_radiant_background(W, H, COLOR_WARM_CREAM, (238, 214, 208), angle=45)
    draw_layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    draw = ImageDraw.Draw(draw_layer)
    
    cx, cy = 500, 680
    for i in range(14):
        r = 480 - i * 32
        alpha = int(30 * (1 - i / 14.0))
        draw.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(255, 244, 238, alpha))
        
    scale = 1.25
    # Crisply sculpted defined brow
    render_organic_brow(draw, cx - int(220*scale), cy - int(150*scale), length=440, arch_height=78, density=240, thickness=40, scale=scale)
    # Balanced hybrid lash styling with crisp lash line
    render_almond_eye_base(draw, cx, cy, w=440, h=165, scale=scale, iris_color=(56, 38, 34))
    render_feathered_lash_set(draw, cx, cy, count=160, base_len=88, curl_factor=1.45, scale=scale, is_wispy=False)
    
    base.paste(draw_layer, (0, 0), draw_layer)
    final_img = apply_editorial_finish(base, noise_amount=2.2, glow_pos=(0.55, 0.45), glow_radius=560)
    save_image_pair(final_img, "contact-defined")

# ==============================================================================
# 4. CONTACT EXPRESSIVE (3:4 Noticeable Beauty Statement Direction)
# ==============================================================================
def generate_contact_expressive():
    print("Generating Image 4: contact-expressive...")
    W, H = 1000, 1333
    base = create_radiant_background(W, H, (252, 242, 238), (232, 206, 200), angle=30)
    draw_layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    draw = ImageDraw.Draw(draw_layer)
    
    cx, cy = 500, 680
    for i in range(16):
        r = 500 - i * 30
        alpha = int(32 * (1 - i / 16.0))
        draw.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(255, 246, 242, alpha))
        
    scale = 1.3
    # Laminated fluffy expressive brow
    render_organic_brow(draw, cx - int(230*scale), cy - int(160*scale), length=460, arch_height=82, density=260, thickness=46, scale=scale)
    # Dramatic volume / wispy fluttering lash set
    render_almond_eye_base(draw, cx, cy, w=450, h=170, scale=scale, iris_color=(50, 32, 28))
    render_feathered_lash_set(draw, cx, cy, count=210, base_len=96, curl_factor=1.5, scale=scale, is_wispy=True)
    
    base.paste(draw_layer, (0, 0), draw_layer)
    final_img = apply_editorial_finish(base, noise_amount=2.2, glow_pos=(0.6, 0.4), glow_radius=580)
    save_image_pair(final_img, "contact-expressive")

# ==============================================================================
# 5. CONTACT PREPARATION (3:4 Calm Pre-Appointment Studio Environment)
# ==============================================================================
def generate_contact_preparation():
    print("Generating Image 5: contact-preparation...")
    W, H = 1200, 1600
    base = create_radiant_background(W, H, COLOR_WARM_CREAM, (242, 222, 216), angle=50)
    draw_layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    draw = ImageDraw.Draw(draw_layer)
    
    # Studio prep still life arrangement with ceramic dish, silk eye mask, rose gold tools
    cx, cy = 600, 850
    # Sculpted ceramic studio tray
    draw.ellipse([cx - 440, cy - 280, cx + 440, cy + 280], fill=(248, 238, 234, 230), outline=(200, 154, 139, 90), width=2)
    draw.ellipse([cx - 410, cy - 250, cx + 410, cy + 250], fill=(255, 248, 245, 240))
    
    # Precision rose-gold lash mirrors & isolation tools
    draw.line([(cx - 180, cy + 90), (cx + 140, cy - 150)], fill=(200, 154, 139, 240), width=8)
    draw.line([(cx - 165, cy + 105), (cx + 140, cy - 150)], fill=(142, 90, 107, 210), width=4)
    
    # Fine lash palette trays
    for row in range(5):
        ry = cy - 90 + row * 40
        for col in range(9):
            rx = cx - 140 + col * 35
            draw.line([(rx, ry), (rx - 7, ry - 22)], fill=(28, 18, 22, 200), width=2)
            draw.line([(rx, ry), (rx, ry - 24)], fill=(28, 18, 22, 220), width=2)
            draw.line([(rx, ry), (rx + 7, ry - 22)], fill=(28, 18, 22, 200), width=2)
            
    base.paste(draw_layer, (0, 0), draw_layer)
    final_img = apply_editorial_finish(base, noise_amount=2.1, glow_pos=(0.55, 0.45), glow_radius=600)
    save_image_pair(final_img, "contact-preparation")

# ==============================================================================
# 6. CONTACT CLOSING (16:9 Serene Campaign Invitation)
# ==============================================================================
def generate_contact_closing():
    print("Generating Image 6: contact-closing...")
    W, H = 1600, 900
    base = create_radiant_background(W, H, COLOR_WARM_CREAM, (240, 218, 212), angle=35)
    draw_layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    draw = ImageDraw.Draw(draw_layer)
    
    # Warm cinematic glow bloom
    for i in range(18):
        r = 700 - i * 36
        alpha = int(24 * (1 - i / 18.0))
        draw.ellipse([1100 - r, 450 - r, 1100 + r, 450 + r], fill=(255, 246, 242, alpha))
        
    # Serene profile portrait
    cx, cy = 1100, 480
    scale = 1.4
    
    draw.ellipse([cx - int(280*scale), cy - int(320*scale), cx + int(280*scale), cy + int(360*scale)], fill=(248, 230, 224, 210))
    draw.ellipse([cx - int(240*scale), cy - int(280*scale), cx + int(240*scale), cy + int(300*scale)], fill=(255, 245, 240, 245))
    
    render_organic_brow(draw, cx - int(210*scale), cy - int(140*scale), length=420, arch_height=70, density=220, thickness=38, scale=scale)
    render_almond_eye_base(draw, cx, cy, w=440, h=165, scale=scale, iris_color=(60, 42, 38))
    render_feathered_lash_set(draw, cx, cy, count=180, base_len=90, curl_factor=1.45, scale=scale, is_wispy=True)
    
    base.paste(draw_layer, (0, 0), draw_layer)
    final_img = apply_editorial_finish(base, noise_amount=2.0, glow_pos=(0.7, 0.4), glow_radius=650)
    save_image_pair(final_img, "contact-closing")

if __name__ == "__main__":
    print("=" * 60)
    print("LUMIÈRE LASH & BROW - Synthesizing All 6 Contact Assets...")
    print("=" * 60)
    generate_contact_intro()
    generate_contact_soft()
    generate_contact_defined()
    generate_contact_expressive()
    generate_contact_preparation()
    generate_contact_closing()
    print("=" * 60)
    print("All 6 Contact page images generated successfully!")
    print("=" * 60)
