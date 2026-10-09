"""
LUMIÈRE LASH & BROW - Bespoke Creative Asset Synthesizer
Generates all 12 High-Definition (1920px+ landscape, 1600px+ portrait, 1200px+ cards)
custom luxury editorial visuals for the LUMIÈRE Lash & Brow Studio homepage.
"""

import os
import math
import random
import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageEnhance

OUTPUT_DIR = r"assets\images\home"
os.makedirs(OUTPUT_DIR, exist_ok=True)

# Brand Color Palette
COLOR_ESPRESSO = (43, 31, 36)        # #2B1F24 Deep Espresso Plum
COLOR_DUSTY_ROSE = (142, 90, 107)    # #8E5A6B
COLOR_ROSE_GOLD = (200, 154, 139)    # #C89A8B
COLOR_BLUSH_IVORY = (248, 241, 242)  # #F8F1F2
COLOR_WARM_CREAM = (255, 249, 246)   # #FFF9F6
COLOR_SKIN_BASE = (247, 230, 222)
COLOR_SKIN_SHADOW = (226, 196, 186)
COLOR_SKIN_HIGHLIGHT = (255, 248, 244)
COLOR_LASH_DARK = (24, 16, 20)
COLOR_LASH_MED = (38, 26, 32)

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

def apply_editorial_finish(img, noise_amount=2.5, glow_color=(255, 242, 236), glow_pos=(0.65, 0.35), glow_radius=550):
    """Applies soft studio ambient light blooms and ultra-fine editorial film grain."""
    w, h = img.size
    glow = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    gdraw = ImageDraw.Draw(glow)
    gx, gy = int(glow_pos[0] * w), int(glow_pos[1] * h)
    
    for r in range(glow_radius, 0, -18):
        alpha = int(45 * (1 - r / glow_radius)**1.6)
        gdraw.ellipse([gx - r, gy - r, gx + r, gy + r], fill=(glow_color[0], glow_color[1], glow_color[2], alpha))
    img.paste(glow, (0, 0), glow)
    
    # Ultra-fine film grain to prevent digital banding
    arr = np.array(img, dtype=np.int16)
    noise = np.random.normal(0, noise_amount, arr.shape)
    arr = np.clip(arr + noise, 0, 255).astype(np.uint8)
    return Image.fromarray(arr)

def render_organic_brow(draw, start_x, start_y, length=440, arch_height=65, density=180, thickness=38, hair_color=COLOR_LASH_DARK, scale=1.0):
    """Renders multi-layered feathered micro-strokes for high-end brow architecture."""
    length = int(length * scale)
    arch_height = int(arch_height * scale)
    density = int(density * scale)
    thickness = int(thickness * scale)
    
    for i in range(density):
        t = i / float(density)
        bx = start_x + t * length
        by = start_y - math.sin(t * math.pi * 0.88) * arch_height
        
        # Angle flows naturally: vertical at head (80 deg) -> sweeping at arch (45 deg) -> horizontal at tail (10 deg)
        angle_deg = 80 - t * 70 + random.uniform(-8, 8)
        stroke_len = (thickness * (math.sin(t * math.pi) * 0.82 + 0.32)) * random.uniform(0.75, 1.25)
        rad = math.radians(angle_deg)
        
        for _ in range(random.randint(1, 2)):
            ox = random.uniform(-3, 3) * scale
            oy = random.uniform(-4, 4) * scale
            ex = bx + ox + math.cos(rad) * stroke_len
            ey = by + oy - math.sin(rad) * stroke_len
            
            alpha = int(random.uniform(140, 235))
            draw.line([(bx + ox, by + oy), (ex, ey)], fill=(hair_color[0], hair_color[1], hair_color[2], alpha), width=max(1, int(2 * scale)))

def render_almond_eye_base(draw, cx, cy, w=420, h=160, scale=1.0, iris_color=(72, 48, 40)):
    """Renders realistic almond eye contours, sclera, iris with depth, and catchlights."""
    w = int(w * scale)
    h = int(h * scale)
    
    # Outer eye orbit shadow & socket depth
    draw.ellipse([cx - w//2 - 40, cy - h//2 - 50, cx + w//2 + 40, cy + h//2 + 50], fill=(225, 192, 182, 110))
    draw.ellipse([cx - w//2 - 10, cy - h//2 - 20, cx + w//2 + 10, cy + h//2 + 20], fill=(255, 244, 240, 180))
    
    # Sclera (eyeball) with warm gradient
    draw.ellipse([cx - w//2, cy - h//2, cx + w//2, cy + h//2], fill=(250, 246, 245, 255))
    
    # Iris with depth & striations
    iris_r = int(h * 0.48)
    draw.ellipse([cx - iris_r, cy - iris_r, cx + iris_r, cy + iris_r], fill=iris_color)
    draw.ellipse([cx - int(iris_r*0.75), cy - int(iris_r*0.75), cx + int(iris_r*0.75), cy + int(iris_r*0.75)], fill=(110, 75, 58))
    
    # Pupil
    pupil_r = int(iris_r * 0.42)
    draw.ellipse([cx - pupil_r, cy - pupil_r, cx + pupil_r, cy + pupil_r], fill=(18, 12, 15))
    
    # Studio Softbox / Ring-light Catchlights
    draw.ellipse([cx - int(iris_r*0.45), cy - int(iris_r*0.45), cx - int(iris_r*0.15), cy - int(iris_r*0.15)], fill=(255, 255, 255, 230))
    draw.ellipse([cx + int(iris_r*0.2), cy + int(iris_r*0.2), cx + int(iris_r*0.35), cy + int(iris_r*0.35)], fill=(255, 255, 255, 160))
    
    # Upper lid crease line
    crease_pts = []
    for i in range(40):
        t = i / 39.0
        lx = cx - w//2 + t * w
        ly = cy - h//2 - math.sin(t * math.pi) * (32 * scale)
        crease_pts.append((lx, ly))
    draw.line(crease_pts, fill=(195, 155, 145, 180), width=max(1, int(3 * scale)))

def render_bespoke_eyelashes(draw, cx, cy, eye_w=400, eye_h=110, lash_type="hybrid", count=160, length_scale=1.0, scale=1.0):
    """Renders hyper-realistic individual and fanned eyelash extensions with dynamic curl physics."""
    eye_w = int(eye_w * scale)
    eye_h = int(eye_h * scale)
    count = int(count * scale)
    
    # Tightline along upper lid
    lid_pts = []
    for i in range(60):
        t = i / 59.0
        lx = cx - eye_w/2 + t * eye_w
        ly = cy - math.sin(t * math.pi) * (eye_h / 2)
        lid_pts.append((lx, ly))
    draw.line(lid_pts, fill=(28, 18, 22, 240), width=max(2, int(4.5 * scale)))
    
    tones = [
        (22, 14, 18, 240),
        (34, 22, 28, 220),
        (44, 30, 36, 200)
    ]
    
    for i in range(count):
        t = i / float(count)
        lx = cx - eye_w/2 + t * eye_w + random.uniform(-2.5, 2.5) * scale
        ly = cy - math.sin(t * math.pi) * (eye_h / 2)
        
        # Lash length distribution: elegant cat-eye sweep
        if t < 0.2:
            base_len = (38 + t * 180) * scale
        elif t < 0.75:
            base_len = (75 + math.sin((t - 0.2)/0.55 * math.pi) * 48) * scale
        else:
            base_len = (85 - (t - 0.75) * 95) * scale
            
        base_len *= length_scale
        
        if lash_type == "classic":
            fan_count = 1
            curl_intensity = 1.05
            angle_bias = 82 - t * 45
            stroke_w = max(1, int(2.8 * scale))
        elif lash_type == "hybrid":
            fan_count = random.choices([1, 2, 3], weights=[0.35, 0.45, 0.2])[0]
            curl_intensity = 1.15
            angle_bias = 84 - t * 48
            stroke_w = max(1, int(2.2 * scale))
        elif lash_type == "volume":
            fan_count = random.choices([3, 4, 5, 6], weights=[0.2, 0.4, 0.3, 0.1])[0]
            curl_intensity = 1.25
            angle_bias = 86 - t * 50
            stroke_w = max(1, int(1.6 * scale))
            base_len *= 1.16
        elif lash_type == "wispy":
            is_spike = (i % 8 == 0)
            fan_count = 1 if is_spike else random.choice([2, 3])
            base_len = (base_len * 1.42) if is_spike else (base_len * 0.85)
            curl_intensity = 1.32 if is_spike else 1.1
            angle_bias = 83 - t * 46
            stroke_w = max(1, int(3.2 * scale if is_spike else 1.6 * scale))
        else:
            fan_count = 2
            curl_intensity = 1.05
            angle_bias = 82 - t * 45
            stroke_w = max(1, int(2 * scale))

        for f in range(fan_count):
            fan_spread = (f - (fan_count-1)/2) * (6.5 * scale)
            angle = angle_bias + fan_spread + random.uniform(-3.5, 3.5)
            rad = math.radians(angle)
            
            curl = curl_intensity * (26 + t * 16) * scale
            mid_x = lx + math.cos(rad) * (base_len * 0.55) - (curl * 0.45)
            mid_y = ly - math.sin(rad) * (base_len * 0.55)
            
            tip_x = lx + math.cos(rad) * base_len + (curl * 0.85)
            tip_y = ly - math.sin(rad) * base_len
            
            col_tone = random.choice(tones)
            draw.line([(lx, ly), (mid_x, mid_y), (tip_x, tip_y)], fill=col_tone, width=stroke_w)

    # Delicate lower lashes
    lower_count = int(55 * scale)
    for i in range(lower_count):
        t = i / float(lower_count)
        lx = cx - eye_w/2 * 0.8 + t * (eye_w * 0.8)
        ly = cy + (eye_h / 2 * 0.35) + math.sin(t * math.pi) * (18 * scale)
        llen = (16 + math.sin(t * math.pi) * 12) * scale
        draw.line([(lx, ly), (lx + (t - 0.5) * 16 * scale, ly + llen)], fill=(45, 32, 38, 120), width=max(1, int(1.4 * scale)))

def save_dual_assets(img, base_name):
    """Saves both WebP and JPG local assets."""
    jpg_path = os.path.join(OUTPUT_DIR, f"{base_name}.jpg")
    webp_path = os.path.join(OUTPUT_DIR, f"{base_name}.webp")
    
    img.save(jpg_path, "JPEG", quality=95, optimize=True)
    img.save(webp_path, "WEBP", quality=92, method=6)
    print(f"✓ Generated {base_name}.webp and {base_name}.jpg ({img.size[0]}x{img.size[1]})")

# ==============================================================================
# INDIVIDUAL ASSET GENERATORS (12 Bespoke Compositions)
# ==============================================================================

def create_hero():
    """1. Hero: 1920x1200 Ultra-HD Editorial Beauty Close-Up Portrait"""
    w, h = 1920, 1200
    base = create_radiant_background(w, h, (255, 248, 245), (232, 208, 198), angle=35)
    overlay = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    draw = ImageDraw.Draw(overlay)
    
    # Cheekbone & Temple dewy highlight contours
    draw.ellipse([250, 180, 1680, 1160], fill=(255, 246, 242, 140))
    draw.ellipse([650, 420, 1450, 960], fill=(235, 202, 192, 85))
    draw.ellipse([800, 500, 1320, 820], fill=(255, 248, 244, 180))
    
    scale = 1.6
    eye_cx, eye_cy = 980, 680
    
    # Eye anatomy
    render_almond_eye_base(draw, eye_cx, eye_cy, w=440, h=170, scale=scale)
    
    # Feathered Brow
    render_organic_brow(draw, start_x=680, start_y=450, length=490, arch_height=72, density=220, thickness=40, scale=scale)
    
    # Wispy Lash Extensions
    render_bespoke_eyelashes(draw, eye_cx, eye_cy, eye_w=440, eye_h=115, lash_type="wispy", count=190, length_scale=1.3, scale=scale)
    
    # Rose-gold subtle beauty spark / radiance mark
    draw.ellipse([1420, 480, 1426, 486], fill=(200, 154, 139, 220))
    
    base.paste(overlay, (0, 0), overlay)
    img = apply_editorial_finish(base, noise_amount=2.6, glow_pos=(0.68, 0.38), glow_radius=600)
    save_dual_assets(img, "hero")

def create_signature_cards():
    """2. Classic, Hybrid, Volume, Wispy, Brow Styling (1200x1500 each, 4:5 ratio)"""
    card_styles = [
        ("classic", "classic", (255, 249, 247), (236, 214, 206), 0.98, "Clean & Pure 1:1 definition"),
        ("hybrid", "hybrid", (253, 246, 242), (230, 204, 194), 1.12, "Soft multidimensional texture"),
        ("volume", "volume", (248, 236, 232), (222, 192, 182), 1.25, "Rich Russian volume fans"),
        ("wispy", "wispy", (255, 250, 248), (235, 210, 204), 1.22, "Feathery airy Kim K spikes"),
    ]
    
    for base_name, stype, c1, c2, lscale, _ in card_styles:
        w, h = 1200, 1500
        base = create_radiant_background(w, h, c1, c2, angle=random.randint(25, 55))
        overlay = Image.new("RGBA", (w, h), (0, 0, 0, 0))
        draw = ImageDraw.Draw(overlay)
        
        # Soft halo & cheekbone depth
        draw.ellipse([180, 320, 1020, 1220], fill=(255, 246, 242, 150))
        draw.ellipse([280, 460, 920, 1080], fill=(232, 202, 194, 90))
        
        scale = 1.45
        eye_cx, eye_cy = 600, 840
        
        render_almond_eye_base(draw, eye_cx, eye_cy, w=420, h=160, scale=scale)
        render_organic_brow(draw, start_x=320, start_y=580, length=460, arch_height=65, density=170, thickness=34, scale=scale)
        render_bespoke_eyelashes(draw, eye_cx, eye_cy, eye_w=420, eye_h=105, lash_type=stype, count=160, length_scale=lscale, scale=scale)
        
        base.paste(overlay, (0, 0), overlay)
        img = apply_editorial_finish(base, noise_amount=2.8, glow_pos=(0.62, 0.42), glow_radius=480)
        save_dual_assets(img, base_name)

    # 6. Brow Styling Card (1200x1500)
    w, h = 1200, 1500
    base = create_radiant_background(w, h, (255, 248, 245), (230, 206, 198), angle=40)
    overlay = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    draw = ImageDraw.Draw(overlay)
    
    draw.ellipse([140, 260, 1060, 1240], fill=(255, 246, 242, 160))
    scale = 1.68
    
    # High-definition laminated brow focus
    render_organic_brow(draw, start_x=220, start_y=640, length=580, arch_height=85, density=260, thickness=50, scale=scale)
    render_almond_eye_base(draw, cx=600, cy=960, w=400, h=150, scale=1.35)
    render_bespoke_eyelashes(draw, cx=600, cy=960, eye_w=400, eye_h=95, lash_type="classic", count=95, length_scale=0.88, scale=1.35)
    
    # Clean brow bone highlight line
    draw.arc([220, 580, 960, 780], start=190, end=340, fill=(255, 255, 255, 180), width=3)
    
    base.paste(overlay, (0, 0), overlay)
    img = apply_editorial_finish(base, noise_amount=2.8, glow_pos=(0.58, 0.42), glow_radius=500)
    save_dual_assets(img, "brow-styling")

def create_find_your_look():
    """3. Find Your Look: 1400x1600 Editorial Beauty Consultation & Mapping Portrait"""
    w, h = 1400, 1600
    base = create_radiant_background(w, h, (254, 247, 244), (228, 202, 194), angle=135)
    overlay = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    draw = ImageDraw.Draw(overlay)
    
    # Studio mirror frame outline
    draw.rounded_rectangle([90, 90, w-90, h-90], radius=45, outline=(200, 154, 139, 110), width=2)
    draw.ellipse([260, 320, 1140, 1240], fill=(255, 246, 242, 165))
    
    scale = 1.55
    eye_cx, eye_cy = 700, 840
    
    render_almond_eye_base(draw, eye_cx, eye_cy, w=420, h=160, scale=scale)
    render_organic_brow(draw, start_x=390, start_y=590, length=480, arch_height=68, density=180, thickness=36, scale=scale)
    render_bespoke_eyelashes(draw, eye_cx, eye_cy, eye_w=420, eye_h=105, lash_type="hybrid", count=170, length_scale=1.18, scale=scale)
    
    # Golden facial symmetry mapping guidelines
    for r in [280, 340, 400]:
        draw.arc([eye_cx-r, eye_cy-r, eye_cx+r, eye_cy+r], start=210, end=330, fill=(200, 154, 139, 65), width=2)
        
    draw.line([(eye_cx - 300, eye_cy - 120), (eye_cx + 300, eye_cy - 120)], fill=(200, 154, 139, 50), width=1)
    
    base.paste(overlay, (0, 0), overlay)
    img = apply_editorial_finish(base, noise_amount=2.7, glow_pos=(0.54, 0.44), glow_radius=560)
    save_dual_assets(img, "find-your-look")

def create_lumiere_touch():
    """4. Lumière Touch: 1400x1600 Precision Craftsmanship & Artisan Application"""
    w, h = 1400, 1600
    base = create_radiant_background(w, h, (252, 244, 240), (225, 196, 188), angle=145)
    overlay = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    draw = ImageDraw.Draw(overlay)
    
    scale = 1.58
    eye_cx, eye_cy = 760, 850
    
    # Rose-gold precision application tweezers
    tweezer_arm1 = [(360, 180), (735, 795), (745, 805), (460, 160)]
    draw.polygon(tweezer_arm1, fill=(200, 154, 139, 235))
    
    tweezer_arm2 = [(1040, 220), (775, 795), (765, 805), (1100, 240)]
    draw.polygon(tweezer_arm2, fill=(185, 138, 124, 240))
    
    # Hydrogel soothing eye patch
    patch_pts = []
    for i in range(50):
        t = i / 49.0
        px = eye_cx - 240 + t * 480
        py = eye_cy + 40 + math.sin(t * math.pi) * 80
        patch_pts.append((px, py))
    draw.line(patch_pts, fill=(255, 255, 255, 240), width=32)
    
    render_almond_eye_base(draw, eye_cx, eye_cy, w=400, h=155, scale=scale)
    render_bespoke_eyelashes(draw, eye_cx, eye_cy, eye_w=400, eye_h=100, lash_type="volume", count=165, length_scale=1.2, scale=scale)
    
    base.paste(overlay, (0, 0), overlay)
    img = apply_editorial_finish(base, noise_amount=2.7, glow_pos=(0.56, 0.46), glow_radius=550)
    save_dual_assets(img, "lumiere-touch")

def create_transformation_pair():
    """5. Transformation: 1200x1200 Square Conceptual Matching Pair"""
    w, h = 1200, 1200
    scale = 1.48
    eye_cx, eye_cy = 600, 680
    
    # --- BEFORE (Untreated Bare Natural Eye) ---
    base_b = create_radiant_background(w, h, (255, 248, 245), (234, 212, 204), angle=45)
    overlay_b = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    draw_b = ImageDraw.Draw(overlay_b)
    
    draw_b.ellipse([220, 280, 980, 980], fill=(255, 246, 242, 140))
    render_almond_eye_base(draw_b, eye_cx, eye_cy, w=380, h=145, scale=scale)
    # Subtle sparse brow & gentle natural lashes
    render_organic_brow(draw_b, start_x=340, start_y=490, length=440, arch_height=48, density=80, thickness=22, hair_color=(75, 58, 65), scale=scale)
    render_bespoke_eyelashes(draw_b, eye_cx, eye_cy, eye_w=380, eye_h=85, lash_type="classic", count=65, length_scale=0.6, scale=scale)
    
    base_b.paste(overlay_b, (0, 0), overlay_b)
    img_b = apply_editorial_finish(base_b, noise_amount=2.8, glow_pos=(0.6, 0.42), glow_radius=440)
    save_dual_assets(img_b, "transformation-before")
    
    # --- AFTER (Lifted, Sculpted, Enhanced on Same Subject) ---
    base_a = create_radiant_background(w, h, (255, 248, 245), (234, 212, 204), angle=45)
    overlay_a = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    draw_a = ImageDraw.Draw(overlay_a)
    
    draw_a.ellipse([220, 280, 980, 980], fill=(255, 246, 242, 140))
    render_almond_eye_base(draw_a, eye_cx, eye_cy, w=380, h=145, scale=scale)
    # Refined feathered brow & rich wispy lash extensions
    render_organic_brow(draw_a, start_x=340, start_y=490, length=460, arch_height=68, density=200, thickness=38, hair_color=COLOR_LASH_DARK, scale=scale)
    render_bespoke_eyelashes(draw_a, eye_cx, eye_cy, eye_w=380, eye_h=95, lash_type="wispy", count=180, length_scale=1.28, scale=scale)
    
    # Enhanced dewy skin highlight
    draw_a.ellipse([380, 420, 820, 530], fill=(255, 255, 255, 50))
    
    base_a.paste(overlay_a, (0, 0), overlay_a)
    img_a = apply_editorial_finish(base_a, noise_amount=2.8, glow_pos=(0.6, 0.42), glow_radius=440)
    save_dual_assets(img_a, "transformation-after")

def create_appointment():
    """6. Appointment: 1920x1080 Serene Spa Sanctuary Treatment Suite"""
    w, h = 1920, 1080
    base = create_radiant_background(w, h, (255, 252, 250), (230, 208, 202), angle=25)
    overlay = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    draw = ImageDraw.Draw(overlay)
    
    # Warm architectural arched alcove
    draw.ellipse([450, -300, 2300, 1400], fill=(252, 238, 232, 175))
    
    # Minimalist lash bed
    bed_polygon = [(180, 680), (1740, 680), (1660, 860), (250, 860)]
    draw.polygon(bed_polygon, fill=(255, 255, 255, 245))
    
    # Ergonomic headrest
    draw.rounded_rectangle([320, 625, 740, 695], radius=30, fill=(248, 234, 230, 255))
    
    # Folded dusty rose cashmere throw
    draw.rounded_rectangle([1020, 665, 1620, 720], radius=18, fill=(142, 90, 107, 200))
    
    # Ambient warm ring light halo
    for r in range(320, 120, -18):
        alpha = int(45 * (1 - (r - 120)/200))
        draw.ellipse([1260-r, 340-r, 1260+r, 340+r], outline=(200, 154, 139, alpha), width=4)
        
    # Dried botanical pampas grass silhouette
    for angle in [-36, -22, -8, 8, 24]:
        rad = math.radians(90 + angle)
        draw.line([(1680, 1040), (1680 + math.cos(rad)*460, 1040 - math.sin(rad)*460)], fill=(142, 90, 107, 120), width=3)
        
    base.paste(overlay, (0, 0), overlay)
    img = apply_editorial_finish(base, noise_amount=2.6, glow_pos=(0.66, 0.34), glow_radius=620)
    save_dual_assets(img, "appointment")

def create_home_closing():
    """7. Closing: 1400x1600 Moody Deep Espresso-Plum Beauty Portrait"""
    w, h = 1400, 1600
    base = create_radiant_background(w, h, (43, 31, 36), (22, 14, 18), angle=45)
    overlay = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    draw = ImageDraw.Draw(overlay)
    
    # Deep plum glowing spheres
    draw.ellipse([360, 360, 1500, 1500], fill=(72, 46, 56, 150))
    draw.ellipse([520, 520, 1340, 1340], fill=(142, 90, 107, 95))
    
    scale = 1.62
    eye_cx, eye_cy = 780, 850
    
    # Illuminated eye gaze
    render_almond_eye_base(draw, eye_cx, eye_cy, w=420, h=160, scale=scale, iris_color=(120, 85, 70))
    render_organic_brow(draw, start_x=480, start_y=630, length=480, arch_height=70, density=180, thickness=36, hair_color=(215, 175, 165), scale=scale)
    render_bespoke_eyelashes(draw, eye_cx, eye_cy, eye_w=420, eye_h=105, lash_type="volume", count=180, length_scale=1.28, scale=scale)
    
    # Luminous rose-gold halo arc
    draw.arc([220, 220, 1180, 1180], start=175, end=305, fill=(200, 154, 139, 110), width=3)
    
    base.paste(overlay, (0, 0), overlay)
    img = apply_editorial_finish(base, noise_amount=2.8, glow_color=(200, 154, 139), glow_pos=(0.54, 0.44), glow_radius=620)
    save_dual_assets(img, "home-closing")

if __name__ == "__main__":
    print("Synthesizing Bespoke Ultra-HD Local Assets for LUMIÈRE Lash & Brow Studio...")
    create_hero()
    create_signature_cards()
    create_find_your_look()
    create_lumiere_touch()
    create_transformation_pair()
    create_appointment()
    create_home_closing()
    print("\n✓ All 12 Bespoke Local Visual Assets generated successfully in both WebP and JPG formats!")
