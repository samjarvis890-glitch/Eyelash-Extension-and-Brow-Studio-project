"""
LUMIÈRE LASH & BROW - Dedicated Pricing Page Asset Synthesizer
Generates all 7 bespoke luxury editorial images for pricing.html in assets/images/pricing/
Outputs both .webp and .jpg formats in high definition.
"""

import os
import math
import random
import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageEnhance

OUTPUT_DIR = r"assets\images\pricing"
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
        # Position along the upper lid
        lx = start_x + t * span_w + random.uniform(-2, 2) * scale
        ly = cy - int(38 * scale) + math.sin(t * math.pi) * int(18 * scale)
        
        # Lash length profile (natural wing/doll curve)
        bell = math.sin(t * math.pi * 0.92)
        l_len = (base_len * (0.45 + bell * 0.75)) * scale * random.uniform(0.9, 1.1)
        if is_wispy and random.random() < 0.18:
            l_len *= 1.42  # Spikes for wispy look
            
        # Angle based on eye zone (inner corner to outer wing)
        base_angle = 125 - t * 75 + random.uniform(-5, 5)
        
        # Curve segments
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
            
        # Draw tapered stroke
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
# 1. PRICING INTRO (3:4 Editorial Cover Composition)
# ==============================================================================
def generate_pricing_intro():
    print("Generating Image 1: pricing-intro...")
    W, H = 1200, 1600
    base = create_radiant_background(W, H, COLOR_WARM_CREAM, (244, 226, 220), angle=45)
    draw_layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    draw = ImageDraw.Draw(draw_layer)
    
    # Soft background organic studio forms
    for i in range(12):
        r = 500 - i * 35
        alpha = int(22 * (1 - i / 12.0))
        draw.ellipse([650 - r, 750 - r, 650 + r, 750 + r], fill=(200, 154, 139, alpha))
        
    # Luxury metallic geometry lines & editorial framing
    draw.rectangle([60, 60, W - 60, H - 60], outline=(200, 154, 139, 90), width=2)
    draw.rectangle([76, 76, W - 76, H - 76], outline=(142, 90, 107, 45), width=1)
    
    # Central refined portrait study
    cx, cy = 600, 780
    scale = 1.35
    
    # Skin & Face contour shadow
    draw.ellipse([cx - int(340*scale), cy - int(420*scale), cx + int(340*scale), cy + int(480*scale)], fill=(248, 230, 224, 210))
    draw.ellipse([cx - int(300*scale), cy - int(380*scale), cx + int(300*scale), cy + int(420*scale)], fill=(255, 244, 239, 250))
    
    # Render delicate brow
    render_organic_brow(draw, cx - int(240*scale), cy - int(160*scale), length=460, arch_height=75, density=240, thickness=38, scale=scale)
    
    # Render eye and luxury bespoke lashes
    render_almond_eye_base(draw, cx, cy, w=440, h=165, scale=scale, iris_color=(62, 40, 36))
    render_feathered_lash_set(draw, cx, cy, count=160, base_len=92, curl_factor=1.4, scale=scale, is_wispy=True)
    
    # Lower lash line detail
    for j in range(45):
        t = j / 45.0
        lx = cx - int(170*scale) + t * int(340*scale)
        ly = cy + int(45*scale) + math.sin(t * math.pi) * int(12*scale)
        ang = 250 + t * 40 + random.uniform(-5, 5)
        rad = math.radians(ang)
        l_len = random.uniform(14, 28) * scale
        draw.line([(lx, ly), (lx + math.cos(rad)*l_len, ly - math.sin(rad)*l_len)], fill=(34, 22, 26, 160), width=1)
        
    base.paste(draw_layer, (0, 0), draw_layer)
    final_img = apply_editorial_finish(base, noise_amount=2.0, glow_pos=(0.6, 0.4), glow_radius=600)
    save_image_pair(final_img, "pricing-intro")

# ==============================================================================
# 2. PRICING LASHES (4:3 Refined Macro Lash Set Detail)
# ==============================================================================
def generate_pricing_lashes():
    print("Generating Image 2: pricing-lashes...")
    W, H = 1400, 1050
    base = create_radiant_background(W, H, COLOR_BLUSH_IVORY, (240, 218, 212), angle=25)
    draw_layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    draw = ImageDraw.Draw(draw_layer)
    
    # Studio soft spotlight
    for i in range(15):
        r = 600 - i * 35
        alpha = int(30 * (1 - i / 15.0))
        draw.ellipse([700 - r, 525 - r, 700 + r, 525 + r], fill=(255, 248, 245, alpha))
        
    # Dramatic Close-up Macro Eye with Multi-Dimensional Silk Fans
    cx, cy = 680, 560
    scale = 1.6
    
    render_almond_eye_base(draw, cx, cy, w=480, h=180, scale=scale, iris_color=(54, 36, 32))
    render_feathered_lash_set(draw, cx, cy, count=220, base_len=98, curl_factor=1.45, scale=scale, is_wispy=True)
    
    # Lash Mapping Guide Lines in soft gold tone (Art of isolation & mapping)
    for k in range(5):
        rad = math.radians(130 - k * 20)
        sx = cx - int(180*scale) + k * int(90*scale)
        sy = cy - int(38*scale)
        ex = sx + math.cos(rad) * int(140*scale)
        ey = sy - math.sin(rad) * int(140*scale)
        draw.line([(sx, sy), (ex, ey)], fill=(200, 154, 139, 45), width=1)
        
    base.paste(draw_layer, (0, 0), draw_layer)
    final_img = apply_editorial_finish(base, noise_amount=2.3, glow_pos=(0.55, 0.45), glow_radius=580)
    save_image_pair(final_img, "pricing-lashes")

# ==============================================================================
# 3. PRICING LIFT (16:9 Natural Curvature & Clean Elevation)
# ==============================================================================
def generate_pricing_lift():
    print("Generating Image 3: pricing-lift...")
    W, H = 1600, 900
    base = create_radiant_background(W, H, COLOR_WARM_CREAM, (246, 230, 226), angle=15)
    draw_layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    draw = ImageDraw.Draw(draw_layer)
    
    # Soft glowing studio atmosphere
    for i in range(16):
        r = 650 - i * 38
        alpha = int(25 * (1 - i / 16.0))
        draw.ellipse([800 - r, 450 - r, 800 + r, 450 + r], fill=(255, 245, 240, alpha))
        
    # Lift Geometry Diagram overlay (subtle aesthetic curves)
    for c in range(4):
        curve_y = 480 - c * 25
        pts = []
        for x in range(200, 1400, 20):
            t = (x - 200) / 1200.0
            y = curve_y - math.sin(t * math.pi) * (180 + c * 25)
            pts.append((x, y))
        for p in range(len(pts) - 1):
            draw.line([pts[p], pts[p+1]], fill=(200, 154, 139, 40 - c*8), width=1)
            
    # Beautiful Natural Lifted Eye Study
    cx, cy = 800, 490
    scale = 1.45
    
    render_almond_eye_base(draw, cx, cy, w=440, h=165, scale=scale, iris_color=(68, 48, 42))
    # Natural lift features crisp, perfectly upward-curved natural lashes
    render_feathered_lash_set(draw, cx, cy, count=130, base_len=82, curl_factor=1.7, scale=scale, is_wispy=False)
    
    base.paste(draw_layer, (0, 0), draw_layer)
    final_img = apply_editorial_finish(base, noise_amount=2.0, glow_pos=(0.6, 0.4), glow_radius=600)
    save_image_pair(final_img, "pricing-lift")

# ==============================================================================
# 4. PRICING BROW (4:3 Pure Feathered Brow Architecture)
# ==============================================================================
def generate_pricing_brow():
    print("Generating Image 4: pricing-brow...")
    W, H = 1400, 1050
    base = create_radiant_background(W, H, (252, 244, 240), (238, 214, 208), angle=35)
    draw_layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    draw = ImageDraw.Draw(draw_layer)
    
    # Soft background framing
    for i in range(14):
        r = 550 - i * 35
        alpha = int(28 * (1 - i / 14.0))
        draw.ellipse([700 - r, 525 - r, 700 + r, 525 + r], fill=(200, 154, 139, alpha))
        
    # High-Definition Feathered Brow Macro
    bx, by = 350, 460
    scale = 1.65
    render_organic_brow(draw, bx, by, length=440, arch_height=80, density=260, thickness=45, scale=scale)
    
    # Below: subtle eye contour to establish proportion
    cx, cy = 700, 680
    render_almond_eye_base(draw, cx, cy, w=460, h=160, scale=1.3, iris_color=(56, 38, 34))
    render_feathered_lash_set(draw, cx, cy, count=110, base_len=75, curl_factor=1.3, scale=1.3)
    
    base.paste(draw_layer, (0, 0), draw_layer)
    final_img = apply_editorial_finish(base, noise_amount=2.2, glow_pos=(0.5, 0.4), glow_radius=580)
    save_image_pair(final_img, "pricing-brow")

# ==============================================================================
# 5. PRICING MAINTENANCE (1:1 Routine & Cycle Editorial Composition)
# ==============================================================================
def generate_pricing_maintenance():
    print("Generating Image 5: pricing-maintenance...")
    W, H = 1200, 1200
    base = create_radiant_background(W, H, COLOR_WARM_CREAM, (242, 222, 216), radial=True, center=(0.5, 0.5))
    draw_layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    draw = ImageDraw.Draw(draw_layer)
    
    # Concentric beauty cycle rings (Editorial graphic art)
    cx, cy = 600, 600
    for r in [480, 400, 320, 240, 160]:
        draw.ellipse([cx - r, cy - r, cx + r, cy + r], outline=(200, 154, 139, 65), width=1)
        
    # Cardinal cycle nodes in soft rose gold
    for deg in [0, 90, 180, 270]:
        rad = math.radians(deg)
        nx = cx + math.cos(rad) * 320
        ny = cy + math.sin(rad) * 320
        draw.ellipse([nx - 18, ny - 18, nx + 18, ny + 18], fill=(142, 90, 107, 180))
        draw.ellipse([nx - 8, ny - 8, nx + 8, ny + 8], fill=(255, 249, 246, 240))
        
    # Luxury Studio Still Life Objects (Care Spoolie, Dropper bottle, Silk swatch)
    # 1. Silk cushion swatch
    draw.ellipse([cx - 180, cy - 120, cx + 180, cy + 120], fill=(250, 238, 234, 220))
    
    # 2. Precision Rose-Gold Care Wand / Spoolie
    wand_pts = [(420, 780), (780, 420)]
    draw.line(wand_pts, fill=(200, 154, 139, 230), width=6)
    # Brush head micro-bristles
    for b in range(40):
        t = b / 40.0
        wx = 720 + t * 60
        wy = 480 - t * 60
        ang = 45 + 90
        rad = math.radians(ang)
        draw.line([(wx, wy), (wx + math.cos(rad)*14, wy - math.sin(rad)*14)], fill=(43, 31, 36, 210), width=2)
        draw.line([(wx, wy), (wx - math.cos(rad)*14, wy + math.sin(rad)*14)], fill=(43, 31, 36, 210), width=2)
        
    base.paste(draw_layer, (0, 0), draw_layer)
    final_img = apply_editorial_finish(base, noise_amount=2.0, glow_pos=(0.5, 0.5), glow_radius=600)
    save_image_pair(final_img, "pricing-maintenance")

# ==============================================================================
# 6. PRICING GOOD TO KNOW (3:4 Considered Preparation & Care)
# ==============================================================================
def generate_pricing_good_to_know():
    print("Generating Image 6: pricing-good-to-know...")
    W, H = 1200, 1600
    base = create_radiant_background(W, H, (254, 248, 244), (240, 218, 212), angle=55)
    draw_layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    draw = ImageDraw.Draw(draw_layer)
    
    # Editorial magazine margins and fine hairline borders
    draw.rectangle([70, 70, W - 70, H - 70], outline=(200, 154, 139, 80), width=1)
    
    # Still life arrangement: Luxury Ceramic Tray, Glass Dropper, Organic Fibers
    cx, cy = 600, 850
    # Elegant oval ceramic tray
    draw.ellipse([cx - 420, cy - 260, cx + 420, cy + 260], fill=(248, 240, 236, 230), outline=(200, 154, 139, 90), width=2)
    draw.ellipse([cx - 390, cy - 230, cx + 390, cy + 230], fill=(255, 250, 248, 240))
    
    # Precision isolation tweezers in rose gold
    tw_p1 = (cx - 180, cy + 80)
    tw_tip = (cx + 120, cy - 140)
    draw.line([tw_p1, tw_tip], fill=(200, 154, 139, 240), width=7)
    draw.line([(cx - 165, cy + 95), (cx + 120, cy - 140)], fill=(142, 90, 107, 200), width=4)
    
    # Fine lash cluster tray
    for row in range(4):
        ry = cy - 80 + row * 45
        for col in range(8):
            rx = cx - 120 + col * 35
            draw.line([(rx, ry), (rx - 8, ry - 24)], fill=(28, 18, 22, 200), width=2)
            draw.line([(rx, ry), (rx, ry - 26)], fill=(28, 18, 22, 220), width=2)
            draw.line([(rx, ry), (rx + 8, ry - 24)], fill=(28, 18, 22, 200), width=2)
            
    base.paste(draw_layer, (0, 0), draw_layer)
    final_img = apply_editorial_finish(base, noise_amount=2.1, glow_pos=(0.55, 0.45), glow_radius=580)
    save_image_pair(final_img, "pricing-good-to-know")

# ==============================================================================
# 7. PRICING CLOSING (16:9 Confident, Serene Final Editorial Campaign)
# ==============================================================================
def generate_pricing_closing():
    print("Generating Image 7: pricing-closing...")
    W, H = 1600, 900
    base = create_radiant_background(W, H, COLOR_WARM_CREAM, (242, 220, 214), angle=30)
    draw_layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    draw = ImageDraw.Draw(draw_layer)
    
    # Warm cinematic glow bloom
    for i in range(18):
        r = 700 - i * 36
        alpha = int(24 * (1 - i / 18.0))
        draw.ellipse([1100 - r, 450 - r, 1100 + r, 450 + r], fill=(255, 246, 242, alpha))
        
    # Serene side-profile / gaze portrait composition
    cx, cy = 1080, 480
    scale = 1.4
    
    # Soft facial contours & highlight
    draw.ellipse([cx - int(280*scale), cy - int(320*scale), cx + int(280*scale), cy + int(360*scale)], fill=(248, 230, 224, 210))
    draw.ellipse([cx - int(240*scale), cy - int(280*scale), cx + int(240*scale), cy + int(300*scale)], fill=(255, 245, 240, 245))
    
    # Refined Brow
    render_organic_brow(draw, cx - int(210*scale), cy - int(140*scale), length=420, arch_height=70, density=220, thickness=38, scale=scale)
    
    # Luxury Lash Extension Set
    render_almond_eye_base(draw, cx, cy, w=440, h=165, scale=scale, iris_color=(60, 42, 38))
    render_feathered_lash_set(draw, cx, cy, count=180, base_len=90, curl_factor=1.45, scale=scale, is_wispy=True)
    
    # Editorial aesthetic framing lines on the left side
    draw.line([(100, 150), (100, 750)], fill=(200, 154, 139, 70), width=1)
    draw.line([(140, 150), (140, 750)], fill=(142, 90, 107, 40), width=1)
    
    base.paste(draw_layer, (0, 0), draw_layer)
    final_img = apply_editorial_finish(base, noise_amount=2.0, glow_pos=(0.7, 0.4), glow_radius=650)
    save_image_pair(final_img, "pricing-closing")

if __name__ == "__main__":
    print("=" * 60)
    print("LUMIÈRE LASH & BROW - Synthesizing All 7 Pricing Assets...")
    print("=" * 60)
    generate_pricing_intro()
    generate_pricing_lashes()
    generate_pricing_lift()
    generate_pricing_brow()
    generate_pricing_maintenance()
    generate_pricing_good_to_know()
    generate_pricing_closing()
    print("=" * 60)
    print("All 7 Pricing page images generated successfully!")
    print("=" * 60)
