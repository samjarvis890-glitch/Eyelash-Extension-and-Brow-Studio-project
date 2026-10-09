"""
LUMIÈRE LASH & BROW - Gallery Page Asset Synthesizer
Creates ultra-crisp, high-definition bespoke editorial visual assets for gallery.html
in assets/images/gallery/ in both .webp and .jpg formats.
"""

import os
import math
import random
import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageEnhance

OUTPUT_DIR = r"assets\images\gallery"
os.makedirs(OUTPUT_DIR, exist_ok=True)

# Brand Color Palette
COLOR_ESPRESSO = (43, 31, 36)        # #2B1F24 Deep Espresso Plum
COLOR_DUSTY_ROSE = (142, 90, 107)    # #8E5A6B Dusty Rose
COLOR_ROSE_GOLD = (200, 154, 139)    # #C89A8B Rose Gold
COLOR_BLUSH_IVORY = (248, 241, 242)  # #F8F1F2 Blush Ivory
COLOR_WARM_CREAM = (255, 249, 246)   # #FFF9F6 Warm Cream
COLOR_GOLD_ACCENT = (222, 185, 154)  # Warm Gold
COLOR_LASH_DARK = (24, 16, 20)       # Rich dark pigment
COLOR_LASH_MED = (42, 28, 34)
COLOR_SKIN_BASE = (246, 228, 220)
COLOR_SKIN_SHADOW = (222, 190, 178)
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
    
    for r in range(glow_radius, 0, -20):
        alpha = int(40 * (1 - r / glow_radius)**1.5)
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
    
    # Upper lid contour
    lid_pts = []
    for i in range(35):
        t = i / 34.0
        x = (cx - w//2) + t * w
        y = cy - math.sin(t * math.pi) * (h * 0.48)
        lid_pts.append((x, y))
    
    # Sclera fill (creamy eye white)
    sclera = Image.new("RGBA", (int(w*1.5), int(h*1.5)), (0, 0, 0, 0))
    sdraw = ImageDraw.Draw(sclera)
    sx, sy = int(w*0.75), int(h*0.75)
    sdraw.ellipse([sx - w//2, sy - h//2 + 5, sx + w//2, sy + h//2 - 5], fill=(250, 246, 244, 255))
    
    # Iris rendering
    iris_r = int(58 * scale)
    sdraw.ellipse([sx - iris_r, sy - iris_r + 4, sx + iris_r, sy + iris_r + 4], fill=iris_color)
    sdraw.ellipse([sx - iris_r + 8, sy - iris_r + 12, sx + iris_r - 8, sy + iris_r - 4], fill=(95, 62, 54))
    
    # Pupil
    pupil_r = int(24 * scale)
    sdraw.ellipse([sx - pupil_r, sy - pupil_r + 4, sx + pupil_r, sy + pupil_r + 4], fill=(18, 12, 14))
    
    # Specular catchlight
    sdraw.ellipse([sx - 16, sy - 14, sx - 4, sy - 2], fill=(255, 255, 255, 240))
    sdraw.ellipse([sx + 8, sy + 6, sx + 14, sy + 12], fill=(255, 255, 255, 140))
    
    # Upper lid curve shadow over iris
    for i in range(len(lid_pts) - 1):
        draw.line([lid_pts[i], lid_pts[i+1]], fill=(120, 75, 85, 220), width=max(2, int(4 * scale)))

def render_fanned_lashes(draw, cx, cy, eye_w=460, eye_h=175, lash_style="hybrid", count=180, length_scale=1.15, scale=1.0):
    """Draws multi-layered bespoke lash extensions along the eyelid margin."""
    eye_w = int(eye_w * scale)
    eye_h = int(eye_h * scale)
    count = int(count * scale)
    
    for layer in range(3):
        curv_offset = (layer - 1) * 3 * scale
        for i in range(count):
            t = i / float(count)
            lx = (cx - eye_w // 2) + t * eye_w
            ly = cy - math.sin(t * math.pi) * (eye_h * 0.48) + curv_offset
            
            angle_deg = 62 - t * 50 + random.uniform(-5, 5)
            
            if lash_style == "bold":
                base_len = (52 + math.sin(t * math.pi) * 48) * length_scale * scale
                fan_count = random.randint(3, 5)
                thickness = 2
            elif lash_style == "macro":
                base_len = (75 + math.sin(t * math.pi) * 60) * length_scale * scale
                fan_count = random.randint(2, 4)
                thickness = 3
            elif lash_style == "precision":
                base_len = (46 + math.sin(t * math.pi) * 42) * length_scale * scale
                fan_count = 2
                thickness = 2
            else:
                base_len = (45 + math.sin(t * math.pi) * 40) * length_scale * scale
                fan_count = random.choice([2, 3])
                thickness = 2
            
            for f in range(fan_count):
                fan_angle = angle_deg + (f - (fan_count - 1) / 2.0) * 8 + random.uniform(-2, 2)
                rad = math.radians(fan_angle)
                
                p0 = (lx, ly)
                ctrl_len = base_len * 0.55
                ctrl_ang = math.radians(fan_angle + 26)
                p1 = (lx + math.cos(ctrl_ang) * ctrl_len, ly - math.sin(ctrl_ang) * ctrl_len)
                p2 = (lx + math.cos(rad) * base_len, ly - math.sin(rad) * base_len)
                
                curve_pts = []
                for s in range(12):
                    st = s / 11.0
                    qx = (1 - st)**2 * p0[0] + 2 * (1 - st) * st * p1[0] + st**2 * p2[0]
                    qy = (1 - st)**2 * p0[1] + 2 * (1 - st) * st * p1[1] + st**2 * p2[1]
                    curve_pts.append((qx, qy))
                
                alpha = int(random.uniform(200, 250))
                for s in range(len(curve_pts) - 1):
                    draw.line([curve_pts[s], curve_pts[s+1]], fill=(COLOR_LASH_DARK[0], COLOR_LASH_DARK[1], COLOR_LASH_DARK[2], alpha), width=max(1, int(thickness * scale)))

def save_image(img, base_name):
    """Saves high-definition asset in both .webp and .jpg formats."""
    webp_path = os.path.join(OUTPUT_DIR, f"{base_name}.webp")
    jpg_path = os.path.join(OUTPUT_DIR, f"{base_name}.jpg")
    img.save(webp_path, "WEBP", quality=92)
    img.save(jpg_path, "JPEG", quality=92)
    print(f"Synthesized: {base_name}.webp / .jpg ({img.size[0]}x{img.size[1]})")

# -----------------------------------------------------------------------------
# 1. MOOD BOLD (The Bold Edit) - 896 x 1200
# -----------------------------------------------------------------------------
def gen_mood_bold():
    w, h = 896, 1200
    img = create_radiant_background(w, h, (38, 26, 32), (68, 44, 52), angle=140)
    
    # Add warm studio silhouette / editorial portrait light
    glow = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    gdraw = ImageDraw.Draw(glow)
    
    # Face & Neck silhouette in warm espresso studio lighting
    gdraw.ellipse([w//2 - 260, h//2 - 280, w//2 + 260, h//2 + 320], fill=(225, 178, 166, 180))
    gdraw.ellipse([w//2 - 220, h//2 - 250, w//2 + 220, h//2 + 270], fill=(244, 212, 202, 230))
    
    # Jawline and cheekbone contour
    gdraw.polygon([(w//2 - 140, h//2 + 200), (w//2 + 140, h//2 + 200), (w//2, h//2 + 340)], fill=(218, 170, 158, 200))
    
    # Render dramatic, bold brow and eye focus
    draw = ImageDraw.Draw(glow)
    
    # Left eye & brow
    render_almond_eye_base(draw, w//2 - 120, h//2 - 40, w=220, h=80, scale=0.9, iris_color=(60, 38, 32))
    render_fanned_lashes(draw, w//2 - 120, h//2 - 40, eye_w=220, eye_h=80, lash_style="bold", count=150, length_scale=1.2, scale=0.9)
    render_organic_brow(draw, w//2 - 230, h//2 - 120, length=240, arch_height=42, density=180, thickness=28, hair_color=COLOR_LASH_DARK, scale=0.9)
    
    # Right eye & brow
    render_almond_eye_base(draw, w//2 + 120, h//2 - 40, w=220, h=80, scale=0.9, iris_color=(60, 38, 32))
    render_fanned_lashes(draw, w//2 + 120, h//2 - 40, eye_w=220, eye_h=80, lash_style="bold", count=150, length_scale=1.2, scale=0.9)
    render_organic_brow(draw, w//2 + 10, h//2 - 120, length=240, arch_height=42, density=180, thickness=28, hair_color=COLOR_LASH_DARK, scale=0.9)
    
    # Subtle editorial lip tone
    gdraw.ellipse([w//2 - 75, h//2 + 180, w//2 + 75, h//2 + 225], fill=(162, 85, 98, 220))
    
    img.paste(glow, (0, 0), glow)
    img = apply_editorial_finish(img, noise_amount=2.4, glow_color=(255, 230, 220), glow_pos=(0.7, 0.3), glow_radius=480)
    save_image(img, "mood-bold")

# -----------------------------------------------------------------------------
# 2. DETAIL LIBRARY (6 Macro images: 1024x1024)
# -----------------------------------------------------------------------------
def gen_detail_01(): # CURVE
    w, h = 1024, 1024
    img = create_radiant_background(w, h, COLOR_WARM_CREAM, COLOR_BLUSH_IVORY, radial=True, center=(0.5, 0.45))
    draw = ImageDraw.Draw(img)
    
    # Macro eyelash curve profile & delicate individual fibres
    render_almond_eye_base(draw, w//2 - 40, h//2 + 40, w=680, h=240, scale=1.3)
    render_fanned_lashes(draw, w//2 - 40, h//2 + 40, eye_w=680, eye_h=240, lash_style="macro", count=240, length_scale=1.4, scale=1.3)
    
    img = apply_editorial_finish(img, noise_amount=2.0, glow_pos=(0.4, 0.3), glow_radius=420)
    save_image(img, "detail-01")

def gen_detail_02(): # TEXTURE
    w, h = 1024, 1024
    img = create_radiant_background(w, h, COLOR_BLUSH_IVORY, (244, 225, 218), angle=25)
    draw = ImageDraw.Draw(img)
    
    # Macro brow architecture with ultra-fine multi-directional micro-strands
    render_organic_brow(draw, 140, 520, length=740, arch_height=125, density=380, thickness=68, hair_color=COLOR_LASH_DARK, scale=1.35)
    render_organic_brow(draw, 160, 540, length=700, arch_height=110, density=260, thickness=45, hair_color=(56, 38, 44), scale=1.35)
    
    img = apply_editorial_finish(img, noise_amount=2.0, glow_pos=(0.6, 0.4), glow_radius=460)
    save_image(img, "detail-02")

def gen_detail_03(): # PRECISION
    w, h = 1024, 1024
    img = create_radiant_background(w, h, (255, 248, 244), (242, 226, 220), angle=45)
    draw = ImageDraw.Draw(img)
    
    # Macro eye contour & precision lash fan fan-out
    render_almond_eye_base(draw, w//2 + 20, h//2 + 20, w=640, h=230, scale=1.25, iris_color=(84, 56, 48))
    render_fanned_lashes(draw, w//2 + 20, h//2 + 20, eye_w=640, eye_h=230, lash_style="precision", count=220, length_scale=1.2, scale=1.25)
    
    img = apply_editorial_finish(img, noise_amount=1.8, glow_pos=(0.5, 0.35), glow_radius=400)
    save_image(img, "detail-03")

def gen_detail_04(): # SOFTNESS (Studio Tools & Silk textiles)
    w, h = 1024, 1024
    img = create_radiant_background(w, h, (255, 250, 248), (238, 218, 212), angle=120)
    draw = ImageDraw.Draw(img)
    
    # Rose-gold precision tweezers still life on silk curves
    # Silk folds
    for offset in range(-200, 300, 70):
        draw.arc([100 + offset, 200, 900 + offset, 900], start=20, end=160, fill=(230, 204, 198), width=8)
    
    # Precision rose-gold tweezers
    draw.polygon([(460, 220), (490, 220), (530, 780), (510, 800)], fill=COLOR_ROSE_GOLD)
    draw.polygon([(540, 220), (570, 220), (530, 780), (550, 800)], fill=(225, 178, 162))
    draw.line([(500, 220), (520, 780)], fill=(255, 255, 255, 180), width=3)
    
    img = apply_editorial_finish(img, noise_amount=2.0, glow_pos=(0.5, 0.45), glow_radius=440)
    save_image(img, "detail-04")

def gen_detail_05(): # BALANCE
    w, h = 1024, 1024
    img = create_radiant_background(w, h, (250, 240, 236), (236, 214, 206), angle=55)
    draw = ImageDraw.Draw(img)
    
    # Balanced brow arch & cheek contour
    render_organic_brow(draw, 180, 420, length=660, arch_height=110, density=320, thickness=55, hair_color=COLOR_LASH_DARK, scale=1.2)
    render_almond_eye_base(draw, 480, 580, w=540, h=190, scale=1.1, iris_color=(75, 48, 42))
    render_fanned_lashes(draw, 480, 580, eye_w=540, eye_h=190, lash_style="hybrid", count=180, length_scale=1.15, scale=1.1)
    
    img = apply_editorial_finish(img, noise_amount=2.0, glow_pos=(0.6, 0.3), glow_radius=460)
    save_image(img, "detail-05")

def gen_detail_06(): # FINISH
    w, h = 1024, 1024
    img = create_radiant_background(w, h, (255, 248, 245), (235, 212, 205), angle=135)
    draw = ImageDraw.Draw(img)
    
    # Perfectly polished lash & brow harmony
    render_organic_brow(draw, 220, 390, length=600, arch_height=95, density=300, thickness=50, hair_color=COLOR_LASH_DARK, scale=1.15)
    render_almond_eye_base(draw, 500, 560, w=560, h=200, scale=1.15, iris_color=(72, 46, 40))
    render_fanned_lashes(draw, 500, 560, eye_w=560, eye_h=200, lash_style="bold", count=200, length_scale=1.2, scale=1.15)
    
    img = apply_editorial_finish(img, noise_amount=2.0, glow_pos=(0.45, 0.4), glow_radius=450)
    save_image(img, "detail-06")

# -----------------------------------------------------------------------------
# 3. EDITORIAL SECTION (3 Images)
# -----------------------------------------------------------------------------
def gen_editorial_01(): # 1376 x 768 (Cinematic 65% width)
    w, h = 1376, 768
    img = create_radiant_background(w, h, (248, 238, 232), (230, 204, 196), angle=40)
    draw = ImageDraw.Draw(img)
    
    # Cinematic studio portrait composition
    cx = int(w * 0.42)
    cy = int(h * 0.52)
    render_organic_brow(draw, cx - 260, cy - 130, length=540, arch_height=80, density=280, thickness=45, scale=1.1)
    render_almond_eye_base(draw, cx, cy + 20, w=520, h=180, scale=1.15, iris_color=(76, 50, 42))
    render_fanned_lashes(draw, cx, cy + 20, eye_w=520, eye_h=180, lash_style="hybrid", count=210, length_scale=1.2, scale=1.15)
    
    img = apply_editorial_finish(img, noise_amount=2.2, glow_pos=(0.35, 0.4), glow_radius=520)
    save_image(img, "editorial-01")

def gen_editorial_02(): # 896 x 1024
    w, h = 896, 1024
    img = create_radiant_background(w, h, (255, 248, 245), (238, 215, 208), angle=145)
    draw = ImageDraw.Draw(img)
    
    cx = w // 2
    cy = int(h * 0.48)
    render_organic_brow(draw, cx - 220, cy - 110, length=460, arch_height=75, density=240, thickness=40, scale=1.0)
    render_almond_eye_base(draw, cx, cy + 20, w=440, h=160, scale=1.05, iris_color=(70, 44, 38))
    render_fanned_lashes(draw, cx, cy + 20, eye_w=440, eye_h=160, lash_style="bold", count=180, length_scale=1.15, scale=1.05)
    
    img = apply_editorial_finish(img, noise_amount=2.0, glow_pos=(0.55, 0.35), glow_radius=440)
    save_image(img, "editorial-02")

def gen_editorial_03(): # 896 x 1024
    w, h = 896, 1024
    img = create_radiant_background(w, h, (246, 232, 226), (228, 198, 190), angle=30)
    draw = ImageDraw.Draw(img)
    
    cx = w // 2
    cy = int(h * 0.50)
    render_organic_brow(draw, cx - 230, cy - 100, length=470, arch_height=70, density=250, thickness=42, scale=1.02)
    render_almond_eye_base(draw, cx, cy + 30, w=450, h=165, scale=1.05, iris_color=(80, 52, 44))
    render_fanned_lashes(draw, cx, cy + 30, eye_w=450, eye_h=165, lash_style="macro", count=190, length_scale=1.2, scale=1.05)
    
    img = apply_editorial_finish(img, noise_amount=2.0, glow_pos=(0.45, 0.4), glow_radius=460)
    save_image(img, "editorial-03")

# -----------------------------------------------------------------------------
# 4. CLOSING IMAGE (1400 x 800)
# -----------------------------------------------------------------------------
def gen_gallery_closing():
    w, h = 1400, 800
    img = create_radiant_background(w, h, (255, 249, 246), (232, 208, 200), angle=45)
    draw = ImageDraw.Draw(img)
    
    # Generous negative space on right/center for editorial panel overlay
    cx = int(w * 0.32)
    cy = int(h * 0.52)
    render_organic_brow(draw, cx - 250, cy - 120, length=520, arch_height=80, density=270, thickness=44, scale=1.1)
    render_almond_eye_base(draw, cx, cy + 25, w=500, h=175, scale=1.1, iris_color=(74, 48, 40))
    render_fanned_lashes(draw, cx, cy + 25, eye_w=500, eye_h=175, lash_style="hybrid", count=200, length_scale=1.18, scale=1.1)
    
    img = apply_editorial_finish(img, noise_amount=2.2, glow_pos=(0.28, 0.35), glow_radius=550)
    save_image(img, "gallery-closing")

if __name__ == "__main__":
    print("Generating bespoke gallery images...")
    gen_mood_bold()
    gen_detail_01()
    gen_detail_02()
    gen_detail_03()
    gen_detail_04()
    gen_detail_05()
    gen_detail_06()
    gen_editorial_01()
    gen_editorial_02()
    gen_editorial_03()
    gen_gallery_closing()
    print("All gallery assets synthesized successfully!")
