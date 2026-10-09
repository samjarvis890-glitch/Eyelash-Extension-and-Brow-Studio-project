"""
LUMIÈRE LASH & BROW - Dedicated Services Page Asset Synthesizer
Generates all 7 High-Definition bespoke images for services.html in assets/images/services/
Both .webp and .jpg formats in full HD resolution.
"""

import os
import math
import random
import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageEnhance

OUTPUT_DIR = r"assets\images\services"
os.makedirs(OUTPUT_DIR, exist_ok=True)

# Brand Color Palette
COLOR_ESPRESSO = (43, 31, 36)        # #2B1F24 Deep Espresso Plum
COLOR_DUSTY_ROSE = (142, 90, 107)    # #8E5A6B Dusty Rose
COLOR_ROSE_GOLD = (200, 154, 139)    # #C89A8B Rose Gold
COLOR_BLUSH_IVORY = (248, 241, 242)  # #F8F1F2 Blush Ivory
COLOR_WARM_CREAM = (255, 249, 246)   # #FFF9F6 Warm Cream
COLOR_GOLD_ACCENT = (222, 185, 154)  # Warm Gold
COLOR_LASH_DARK = (26, 18, 22)       # Rich dark pigment
COLOR_LASH_MED = (48, 34, 40)
COLOR_SKIN_PEACH = (246, 228, 220)
COLOR_SKIN_SHADOW = (224, 192, 180)

def create_radiant_background(w, h, color1, color2, angle=35, radial=False, center=(0.5, 0.4)):
    """Creates a smooth continuous-tone studio background."""
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

def apply_editorial_finish(img, noise_amount=2.5, glow_color=(255, 244, 238), glow_pos=(0.65, 0.35), glow_radius=550):
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

def render_organic_brow(draw, start_x, start_y, length=460, arch_height=70, density=200, thickness=42, hair_color=COLOR_LASH_DARK, scale=1.0):
    """Renders multi-layered feathered micro-strokes for high-end brow architecture."""
    length = int(length * scale)
    arch_height = int(arch_height * scale)
    density = int(density * scale)
    thickness = int(thickness * scale)
    
    for i in range(density):
        t = i / float(density)
        bx = start_x + t * length
        by = start_y - math.sin(t * math.pi * 0.88) * arch_height
        
        angle_deg = 82 - t * 72 + random.uniform(-7, 7)
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

def render_fanned_lashes(draw, cx, cy, eye_w=460, eye_h=175, lash_style="hybrid", count=170, length_scale=1.1, scale=1.0):
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
            
            # Flare angle from inner corner (60 deg) to outer sweep (15 deg)
            angle_deg = 62 - t * 50 + random.uniform(-6, 6)
            
            if lash_style == "classic":
                base_len = (42 + math.sin(t * math.pi) * 38) * length_scale * scale
                fan_count = 1
                thickness = 2
            elif lash_style == "hybrid":
                base_len = (44 + math.sin(t * math.pi) * 44) * length_scale * scale
                fan_count = random.choice([1, 2, 3])
                thickness = 2 if fan_count == 1 else 1
            elif lash_style == "volume":
                base_len = (48 + math.sin(t * math.pi) * 46) * length_scale * scale
                fan_count = random.randint(3, 5)
                thickness = 1
            elif lash_style == "wispy":
                is_spike = (i % 14 == 0)
                base_len = (68 if is_spike else 38 + math.sin(t * math.pi) * 34) * length_scale * scale
                fan_count = 1 if is_spike else random.randint(2, 4)
                thickness = 3 if is_spike else 1
            elif lash_style == "lift":
                base_len = (38 + math.sin(t * math.pi) * 32) * length_scale * scale
                fan_count = 1
                thickness = 2
                angle_deg = 80 - t * 45  # high upward curl
            else:
                base_len = (44 + math.sin(t * math.pi) * 40) * length_scale * scale
                fan_count = 2
                thickness = 2
            
            for f in range(fan_count):
                fan_angle = angle_deg + (f - (fan_count - 1) / 2.0) * 9 + random.uniform(-3, 3)
                rad = math.radians(fan_angle)
                
                # Smooth quadratic bezier curve for lash upward sweep
                p0 = (lx, ly)
                ctrl_len = base_len * 0.55
                ctrl_ang = math.radians(fan_angle + 28)
                p1 = (lx + math.cos(ctrl_ang) * ctrl_len, ly - math.sin(ctrl_ang) * ctrl_len)
                p2 = (lx + math.cos(rad) * base_len, ly - math.sin(rad) * base_len)
                
                curve_pts = []
                for s in range(12):
                    st = s / 11.0
                    qx = (1 - st)**2 * p0[0] + 2 * (1 - st) * st * p1[0] + st**2 * p2[0]
                    qy = (1 - st)**2 * p0[1] + 2 * (1 - st) * st * p1[1] + st**2 * p2[1]
                    curve_pts.append((qx, qy))
                
                alpha = int(random.uniform(190, 245))
                for s in range(len(curve_pts) - 1):
                    draw.line([curve_pts[s], curve_pts[s+1]], fill=(COLOR_LASH_DARK[0], COLOR_LASH_DARK[1], COLOR_LASH_DARK[2], alpha), width=max(1, int(thickness * scale)))


def save_image(img, base_name):
    """Saves high-definition asset in both .webp and .jpg formats."""
    webp_path = os.path.join(OUTPUT_DIR, f"{base_name}.webp")
    jpg_path = os.path.join(OUTPUT_DIR, f"{base_name}.jpg")
    
    img.save(webp_path, format="WEBP", quality=92, method=6)
    img.save(jpg_path, format="JPEG", quality=92, optimize=True)
    print(f"Generated: {webp_path} ({img.size[0]}x{img.size[1]})")


# ==============================================================================
# 1. SERVICES INTRO - Editorial Studio Flatlay & Artistry Tools (1920x1080)
# ==============================================================================
def gen_services_intro():
    w, h = 1920, 1080
    bg = create_radiant_background(w, h, COLOR_WARM_CREAM, COLOR_BLUSH_IVORY, angle=30)
    draw = ImageDraw.Draw(bg, "RGBA")
    
    # Soft rose gold silk wave backdrop
    for i in range(18):
        y_off = 350 + i * 40
        draw.arc([-200, y_off, w + 300, y_off + 450], start=10, end=170, fill=(200, 154, 139, 22), width=18)
    
    # Precision lash map grid & tray
    tray_x, tray_y, tray_w, tray_h = 980, 260, 780, 560
    draw.rounded_rectangle([tray_x, tray_y, tray_x + tray_w, tray_y + tray_h], radius=24, fill=(255, 255, 255, 240), outline=(200, 154, 139, 140), width=3)
    
    # Lash strips on tray (C, CC, D curls in varying lengths 8mm - 14mm)
    lengths = ["8mm Natural", "9mm Inner", "10mm Contour", "11mm Balance", "12mm Flutter", "13mm Drama", "14mm Wispy"]
    for idx, label in enumerate(lengths):
        sy = tray_y + 60 + idx * 68
        draw.rounded_rectangle([tray_x + 40, sy, tray_x + tray_w - 40, sy + 44], radius=8, fill=(248, 241, 242, 220), outline=(230, 216, 218, 180), width=1)
        # Render miniature lash fans along the strip
        for lx in range(tray_x + 180, tray_x + tray_w - 60, 14):
            for _ in range(3):
                fa = math.radians(random.uniform(70, 110))
                fl = random.uniform(16, 24)
                draw.line([(lx, sy + 38), (lx + math.cos(fa) * fl, sy + 38 - math.sin(fa) * fl)], fill=(COLOR_LASH_DARK[0], COLOR_LASH_DARK[1], COLOR_LASH_DARK[2], 210), width=1)
    
    # Precision golden isolation tweezers
    t_start = (520, 780)
    t_tip = (960, 480)
    draw.line([t_start, t_tip], fill=(212, 175, 120, 230), width=7)
    draw.line([(t_start[0] + 15, t_start[1] - 8), t_tip], fill=(235, 205, 160, 240), width=4)
    
    # Macro almond eye contour in left focal area
    render_almond_eye_base(draw, 580, 460, w=440, h=165, scale=1.1)
    render_organic_brow(draw, 340, 310, length=460, arch_height=65, scale=1.1)
    render_fanned_lashes(draw, 580, 460, eye_w=440, eye_h=165, lash_style="hybrid", scale=1.1)
    
    final_img = apply_editorial_finish(bg, noise_amount=2.2, glow_pos=(0.35, 0.45), glow_radius=600)
    save_image(final_img, "services-intro")


# ==============================================================================
# 2. LASH EXTENSIONS MENU - Macro Multistyle Lash Architecture (1600x1200)
# ==============================================================================
def gen_services_lashes():
    w, h = 1600, 1200
    bg = create_radiant_background(w, h, (252, 245, 242), (242, 230, 232), angle=45)
    draw = ImageDraw.Draw(bg, "RGBA")
    
    # Deep plum & soft gold aesthetic circular aura
    draw.ellipse([w//2 - 480, h//2 - 400, w//2 + 480, h//2 + 400], fill=(200, 154, 139, 45))
    draw.ellipse([w//2 - 360, h//2 - 280, w//2 + 360, h//2 + 280], fill=(255, 255, 255, 160))
    
    # Centerpiece: High-definition open eye with full hybrid/volume lash mapping
    cx, cy = w // 2, int(h * 0.52)
    render_almond_eye_base(draw, cx, cy, w=580, h=220, scale=1.35)
    render_organic_brow(draw, cx - 320, cy - 200, length=640, arch_height=90, scale=1.35)
    render_fanned_lashes(draw, cx, cy, eye_w=580, eye_h=220, lash_style="wispy", count=240, length_scale=1.2, scale=1.35)
    
    # Editorial focal annotations & subtle geometry
    draw.ellipse([cx - 290, cy - 80, cx - 270, cy - 60], outline=(200, 154, 139, 200), width=2)
    draw.line([(cx - 270, cy - 70), (cx - 180, cy - 70)], fill=(200, 154, 139, 180), width=1)
    
    draw.ellipse([cx + 270, cy - 90, cx + 290, cy - 70], outline=(200, 154, 139, 200), width=2)
    draw.line([(cx + 180, cy - 80), (cx + 270, cy - 80)], fill=(200, 154, 139, 180), width=1)
    
    final_img = apply_editorial_finish(bg, noise_amount=2.0, glow_pos=(0.5, 0.45), glow_radius=500)
    save_image(final_img, "services-lashes")


# ==============================================================================
# 3. LASH LIFT - Natural Uplift & Keratin Gloss (1600x1100)
# ==============================================================================
def gen_services_lift():
    w, h = 1600, 1100
    bg = create_radiant_background(w, h, COLOR_WARM_CREAM, (244, 235, 238), angle=60)
    draw = ImageDraw.Draw(bg, "RGBA")
    
    # Soft upward radiant rays
    for i in range(12):
        ang = math.radians(20 + i * 12)
        draw.line([(w * 0.2, h * 0.8), (w * 0.2 + math.cos(ang) * 900, h * 0.8 - math.sin(ang) * 900)], fill=(200, 154, 139, 25), width=3)
    
    # Side-profile elegant upward curl
    cx, cy = int(w * 0.58), int(h * 0.52)
    render_almond_eye_base(draw, cx, cy, w=520, h=190, scale=1.25, iris_color=(62, 72, 80))
    render_organic_brow(draw, cx - 280, cy - 170, length=560, arch_height=80, scale=1.25)
    render_fanned_lashes(draw, cx, cy, eye_w=520, eye_h=190, lash_style="lift", count=180, length_scale=1.1, scale=1.25)
    
    # Dewy catchlight glints (keratin nourishment)
    for _ in range(8):
        gx = cx + random.randint(-180, 180)
        gy = cy - random.randint(30, 90)
        draw.ellipse([gx - 4, gy - 4, gx + 4, gy + 4], fill=(255, 255, 255, 220))
        draw.line([(gx - 8, gy), (gx + 8, gy)], fill=(255, 255, 255, 180), width=1)
        draw.line([(gx, gy - 8), (gx, gy + 8)], fill=(255, 255, 255, 180), width=1)
    
    final_img = apply_editorial_finish(bg, noise_amount=2.3, glow_pos=(0.6, 0.4), glow_radius=520)
    save_image(final_img, "services-lift")


# ==============================================================================
# 4. BROW SERVICES - The Brow Edit Architecture & Styling (1600x1200)
# ==============================================================================
def gen_services_brow():
    w, h = 1600, 1200
    bg = create_radiant_background(w, h, (249, 243, 240), COLOR_WARM_CREAM, angle=35)
    draw = ImageDraw.Draw(bg, "RGBA")
    
    # Golden ratio brow mapping guides
    cx, cy = w // 2, int(h * 0.48)
    
    # Facial golden ratio arches (subtle dashed lines)
    for r in range(180, 520, 80):
        draw.arc([cx - r, cy - r + 80, cx + r, cy + r + 80], start=200, end=340, fill=(200, 154, 139, 60), width=2)
    
    # Vertical brow alignment markers
    draw.line([(cx - 260, cy - 220), (cx - 260, cy + 180)], fill=(142, 90, 107, 70), width=2) # Head alignment
    draw.line([(cx + 60, cy - 240), (cx + 60, cy + 180)], fill=(142, 90, 107, 70), width=2)   # Arch peak
    draw.line([(cx + 310, cy - 200), (cx + 310, cy + 180)], fill=(142, 90, 107, 70), width=2) # Tail finish
    
    # Main feathered brow presentation (high density, laminated texture)
    render_organic_brow(draw, cx - 290, cy - 110, length=620, arch_height=95, density=340, thickness=52, scale=1.35)
    
    # Eye contour underneath for anatomical context
    render_almond_eye_base(draw, cx, cy + 80, w=520, h=180, scale=1.2)
    render_fanned_lashes(draw, cx, cy + 80, eye_w=520, eye_h=180, lash_style="classic", count=140, scale=1.2)
    
    final_img = apply_editorial_finish(bg, noise_amount=2.2, glow_pos=(0.5, 0.38), glow_radius=500)
    save_image(final_img, "services-brow")


# ==============================================================================
# 5. CUSTOM CONSULTATION - Studio Style Guidance & Consultation (1600x1100)
# ==============================================================================
def gen_services_consultation():
    w, h = 1600, 1100
    bg = create_radiant_background(w, h, COLOR_WARM_CREAM, (246, 236, 238), angle=120)
    draw = ImageDraw.Draw(bg, "RGBA")
    
    # Consultation visual mood cards & palette chips
    card_configs = [
        {"x": 220, "y": 280, "w": 340, "h": 500, "rot": -6, "label": "NATURAL LIFT"},
        {"x": 620, "y": 220, "w": 360, "h": 560, "rot": 0, "label": "HYBRID FLUTTER"},
        {"x": 1040, "y": 300, "w": 340, "h": 480, "rot": 6, "label": "STATEMENT VOLUME"},
    ]
    
    for c in card_configs:
        draw.rounded_rectangle([c["x"], c["y"], c["x"] + c["w"], c["y"] + c["h"]], radius=18, fill=(255, 255, 255, 245), outline=(200, 154, 139, 160), width=2)
        # Inner thumbnail framing
        draw.rounded_rectangle([c["x"] + 20, c["y"] + 20, c["x"] + c["w"] - 20, c["y"] + c["h"] - 100], radius=12, fill=(248, 241, 242, 255))
        
        # Draw eyes on cards
        card_cx = c["x"] + c["w"] // 2
        card_cy = c["y"] + (c["h"] - 80) // 2
        render_almond_eye_base(draw, card_cx, card_cy, w=220, h=80, scale=0.6)
        render_organic_brow(draw, card_cx - 120, card_cy - 70, length=240, arch_height=35, scale=0.6)
        style_type = "lift" if "LIFT" in c["label"] else ("hybrid" if "HYBRID" in c["label"] else "volume")
        render_fanned_lashes(draw, card_cx, card_cy, eye_w=220, eye_h=80, lash_style=style_type, scale=0.6)
    
    # Soft warm ambient light bloom
    final_img = apply_editorial_finish(bg, noise_amount=2.4, glow_pos=(0.5, 0.45), glow_radius=580)
    save_image(final_img, "services-consultation")


# ==============================================================================
# 6. AFTERCARE - Clean Care Botanicals & Spoolie Routine (1600x1100)
# ==============================================================================
def gen_services_aftercare():
    w, h = 1600, 1100
    bg = create_radiant_background(w, h, COLOR_BLUSH_IVORY, COLOR_WARM_CREAM, angle=45)
    draw = ImageDraw.Draw(bg, "RGBA")
    
    # Clean minimalist marble pedestal
    draw.ellipse([w//2 - 450, h - 340, w//2 + 450, h - 80], fill=(255, 255, 255, 230), outline=(230, 216, 218, 180), width=2)
    
    # Foaming lash cleanser bottle (matte plum & rose gold dispenser)
    bx, by, bw, bh = 540, 360, 180, 420
    draw.rounded_rectangle([bx, by, bx + bw, by + bh], radius=24, fill=(43, 31, 36, 240), outline=(200, 154, 139, 200), width=3)
    # Gold pump cap
    draw.rounded_rectangle([bx + 45, by - 70, bx + bw - 45, by], radius=8, fill=(212, 175, 120, 255))
    draw.line([(bx + bw // 2, by - 70), (bx + bw // 2 - 40, by - 95)], fill=(212, 175, 120, 255), width=10)
    
    # Luxury metallic rose-gold spoolie brush
    sp_start = (840, 720)
    sp_end = (1120, 320)
    draw.line([sp_start, sp_end], fill=(200, 154, 139, 255), width=12)
    # Bristle head
    for s in range(40):
        t = s / 39.0
        px = sp_end[0] - (sp_end[0] - sp_start[0]) * (t * 0.28)
        py = sp_end[1] - (sp_end[1] - sp_start[1]) * (t * 0.28)
        # Radial bristles
        for _ in range(8):
            ba = math.radians(random.uniform(0, 360))
            bl = random.uniform(14, 28)
            draw.line([(px, py), (px + math.cos(ba) * bl, py + math.sin(ba) * bl)], fill=(142, 90, 107, 190), width=2)
    
    # Soft botanical mist droplets
    for _ in range(25):
        dx = random.randint(350, 1250)
        dy = random.randint(250, 680)
        dr = random.randint(3, 8)
        draw.ellipse([dx - dr, dy - dr, dx + dr, dy + dr], fill=(255, 255, 255, 180))
    
    final_img = apply_editorial_finish(bg, noise_amount=2.3, glow_pos=(0.55, 0.42), glow_radius=520)
    save_image(final_img, "services-aftercare")


# ==============================================================================
# 7. SERVICES CLOSING - Studio Finish & Appointment Invitation (1920x1080)
# ==============================================================================
def gen_services_closing():
    w, h = 1920, 1080
    bg = create_radiant_background(w, h, COLOR_ESPRESSO, (28, 19, 24), angle=135)
    draw = ImageDraw.Draw(bg, "RGBA")
    
    # Glowing warm studio rim light and ambient vignette
    draw.ellipse([w - 650, -100, w + 350, 900], fill=(200, 154, 139, 35))
    draw.ellipse([-200, 300, 600, 1100], fill=(142, 90, 107, 30))
    
    # Center-right editorial beauty portrait
    cx, cy = int(w * 0.65), int(h * 0.52)
    render_almond_eye_base(draw, cx, cy, w=540, h=195, scale=1.3, iris_color=(85, 55, 48))
    render_organic_brow(draw, cx - 290, cy - 180, length=580, arch_height=85, scale=1.3, hair_color=(18, 12, 14))
    render_fanned_lashes(draw, cx, cy, eye_w=540, eye_h=195, lash_style="hybrid", count=220, length_scale=1.2, scale=1.3)
    
    # Subtle geometric decorative ring
    draw.ellipse([cx - 420, cy - 350, cx + 420, cy + 350], outline=(200, 154, 139, 80), width=2)
    
    final_img = apply_editorial_finish(bg, noise_amount=2.1, glow_pos=(0.65, 0.45), glow_radius=650)
    save_image(final_img, "services-closing")


if __name__ == "__main__":
    print("=== Generating High-Definition Assets for Services Page ===")
    gen_services_intro()
    gen_services_lashes()
    gen_services_lift()
    gen_services_brow()
    gen_services_consultation()
    gen_services_aftercare()
    gen_services_closing()
    print("=== All 7 Services Assets Generated Successfully ===")
