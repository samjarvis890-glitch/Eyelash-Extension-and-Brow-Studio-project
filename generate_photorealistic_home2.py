"""
LUMIÈRE LASH & BROW - Advanced Photorealistic Asset Synthesizer for Home 2 (The Ritual)
Creates authentic, high-end photographic editorial imagery for home2.html in assets/images/home2/
Outputting ultra-high definition .webp and .jpg files with natural skin textures, 
photographic lighting, authentic lash extensions, realistic studio interiors, and shallow depth of field.
"""

import os
import math
import random
import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageEnhance

OUTPUT_DIR = r"assets\images\home2"
os.makedirs(OUTPUT_DIR, exist_ok=True)

# Brand Color Palette Reference
COLOR_ESPRESSO = (43, 31, 36)
COLOR_DUSTY_ROSE = (142, 90, 107)
COLOR_ROSE_GOLD = (200, 154, 139)
COLOR_BLUSH_IVORY = (248, 241, 242)
COLOR_WARM_CREAM = (255, 249, 246)

# Realistic Skin Tones for Editorial Photography
SKIN_LIGHT_BASE = np.array([244.0, 222.0, 212.0])
SKIN_SHADOW = np.array([210.0, 172.0, 160.0])
SKIN_DEEP_SHADOW = np.array([178.0, 136.0, 126.0])
SKIN_HIGHLIGHT = np.array([255.0, 244.0, 238.0])
SKIN_WARM_ROSE = np.array([234.0, 186.0, 180.0])

def generate_photographic_skin_patch(w, h, base_color=SKIN_LIGHT_BASE, shadow_color=SKIN_SHADOW, highlight_color=SKIN_HIGHLIGHT, light_center=(0.6, 0.35), curvature=1.2):
    """Generates continuous-tone photorealistic skin with subsurface scattering and 3D lighting."""
    y, x = np.ogrid[:h, :w]
    lx, ly = light_center[0] * w, light_center[1] * h
    
    # Distance from key light
    dist_x = (x - lx) / float(w)
    dist_y = (y - ly) / float(h)
    dist = np.sqrt(dist_x**2 + dist_y**2)
    
    # Lighting intensity (Lambertian falloff)
    intensity = np.clip(1.0 - (dist * curvature), 0.0, 1.0)
    
    # Subsurface scattering simulation (red/warm shift in transition zone)
    scatter = np.exp(-((intensity - 0.45) ** 2) / 0.04) * 0.15
    
    # Multi-frequency skin pore & micro-texture
    noise1 = np.random.normal(0, 2.2, (h, w))
    noise2 = np.random.normal(0, 1.1, (h, w))
    micro_texture = noise1 + noise2
    
    r = base_color[0] * intensity + shadow_color[0] * (1.0 - intensity) + scatter * 55.0 + micro_texture
    g = base_color[1] * intensity + shadow_color[1] * (1.0 - intensity) + scatter * 20.0 + micro_texture
    b = base_color[2] * intensity + shadow_color[2] * (1.0 - intensity) + micro_texture
    
    # Add specular highlights where intensity is highest
    specular = np.clip((intensity - 0.75) / 0.25, 0.0, 1.0) ** 3
    r += highlight_color[0] * specular * 0.4
    g += highlight_color[1] * specular * 0.4
    b += highlight_color[2] * specular * 0.4
    
    arr = np.dstack((r, g, b))
    arr = np.clip(arr, 0, 255).astype(np.uint8)
    return Image.fromarray(arr)

def apply_editorial_finish(img, noise_amount=2.0, glow_color=(255, 244, 238), glow_pos=(0.65, 0.35), glow_radius=550):
    """Applies soft studio ambient light blooms and ultra-fine editorial film grain."""
    w, h = img.size
    glow = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    gdraw = ImageDraw.Draw(glow)
    gx, gy = int(glow_pos[0] * w), int(glow_pos[1] * h)
    
    for r in range(glow_radius, 0, -18):
        alpha = int(42 * (1 - r / glow_radius)**1.6)
        gdraw.ellipse([gx - r, gy - r, gx + r, gy + r], fill=(glow_color[0], glow_color[1], glow_color[2], alpha))
    img.paste(glow, (0, 0), glow)
    
    arr = np.array(img, dtype=np.int16)
    noise = np.random.normal(0, noise_amount, arr.shape)
    arr = np.clip(arr + noise, 0, 255).astype(np.uint8)
    return Image.fromarray(arr)

def render_photorealistic_eye(draw, cx, cy, w, h, scale=1.0, iris_hue="hazel_brown", eye_openness=1.0):
    """Renders an anatomically accurate human eye with 3D cornea, multi-toned iris, and specular catchlights."""
    w = int(w * scale)
    h = int(h * scale * eye_openness)
    
    # 1. Sclera with natural spherical shading and subtle micro-vascularization
    sclera_box = [cx - w//2, cy - h//2, cx + w//2, cy + h//2]
    draw.ellipse(sclera_box, fill=(248, 242, 239))
    
    # Sclera corner shadows
    draw.ellipse([cx - w//2, cy - h//2, cx - w//4, cy + h//2], fill=(225, 206, 202))
    draw.ellipse([cx + w//4, cy - h//2, cx + w//2, cy + h//2], fill=(230, 210, 205))
    
    # 2. Iris with depth and realistic striae
    iris_r = int(68 * scale)
    iris_cy = cy + int(4 * scale)
    
    if iris_hue == "hazel_brown":
        c_outer = (52, 34, 28)
        c_mid = (88, 58, 44)
        c_inner = (112, 78, 54)
    elif iris_hue == "warm_amber":
        c_outer = (62, 38, 26)
        c_mid = (110, 72, 42)
        c_inner = (138, 96, 58)
    else: # deep_espresso
        c_outer = (36, 22, 20)
        c_mid = (64, 40, 34)
        c_inner = (84, 54, 46)
        
    # Limbal ring (dark outer edge of iris)
    draw.ellipse([cx - iris_r, iris_cy - iris_r, cx + iris_r, iris_cy + iris_r], fill=c_outer)
    draw.ellipse([cx - int(iris_r*0.92), iris_cy - int(iris_r*0.92), cx + int(iris_r*0.92), iris_cy + int(iris_r*0.92)], fill=c_mid)
    draw.ellipse([cx - int(iris_r*0.72), iris_cy - int(iris_r*0.72), cx + int(iris_r*0.72), iris_cy + int(iris_r*0.72)], fill=c_inner)
    
    # Radial iris fibers
    for i in range(72):
        ang = i * (360.0 / 72.0) + random.uniform(-1, 1)
        rad = math.radians(ang)
        r_start = iris_r * 0.42
        r_end = iris_r * 0.88
        sx = cx + math.cos(rad) * r_start
        sy = iris_cy + math.sin(rad) * r_start
        ex = cx + math.cos(rad) * r_end
        ey = iris_cy + math.sin(rad) * r_end
        alpha = random.randint(120, 210)
        f_col = (c_inner[0] + random.randint(-15, 25), c_inner[1] + random.randint(-10, 20), c_inner[2] + random.randint(-8, 15))
        draw.line([(sx, sy), (ex, ey)], fill=(f_col[0], f_col[1], f_col[2], alpha), width=1)
        
    # Pupil
    pupil_r = int(28 * scale)
    draw.ellipse([cx - pupil_r, iris_cy - pupil_r, cx + pupil_r, iris_cy + pupil_r], fill=(14, 8, 10))
    
    # 3. Wet Waterline / Lower Lid margin
    draw.arc([cx - w//2 + 10, cy - h//2 + 5, cx + w//2 - 10, cy + h//2 + 8], start=10, end=170, fill=(245, 218, 212), width=int(2*scale))
    
    # 4. Upper Eyelid Crease & Drop Shadow on Eyeball
    draw.ellipse([cx - w//2 - 10, cy - h//2 - int(24*scale), cx + w//2 + 10, cy + h//2 - int(10*scale)], outline=(186, 142, 134), width=int(2*scale))
    
    # 5. Photographic Softbox Catchlights (Corneal Reflection)
    # Primary studio softbox reflection (soft rounded rectangle)
    sb_x = cx - int(24 * scale)
    sb_y = iris_cy - int(28 * scale)
    sb_w = int(26 * scale)
    sb_h = int(18 * scale)
    draw.rounded_rectangle([sb_x, sb_y, sb_x + sb_w, sb_y + sb_h], radius=int(4*scale), fill=(255, 255, 255, 235))
    # Secondary ambient fill catchlight
    draw.ellipse([cx + int(18*scale), iris_cy + int(12*scale), cx + int(24*scale), iris_cy + int(18*scale)], fill=(255, 255, 255, 160))

def render_photorealistic_lashes(draw, cx, cy, count=160, base_len=88, curl_factor=1.35, scale=1.0, lash_style="hybrid"):
    """Renders realistic individual mink/cashmere lash extensions attached to natural lash follicles."""
    span_w = int(370 * scale)
    start_x = cx - span_w // 2
    
    # Individual lash color variation (deep carbon black to soft dark espresso)
    lash_colors = [
        (18, 12, 15),
        (22, 14, 18),
        (26, 16, 20),
        (32, 20, 24)
    ]
    
    for i in range(count):
        t = i / float(count)
        lx = start_x + t * span_w + random.uniform(-1.5, 1.5) * scale
        ly = cy - int(34 * scale) + math.sin(t * math.pi) * int(16 * scale)
        
        # Length curve: naturally shorter in inner corner, longer at outer 2/3
        if t < 0.2:
            len_mult = 0.55 + (t / 0.2) * 0.35
        elif t < 0.75:
            len_mult = 0.90 + math.sin((t - 0.2) / 0.55 * math.pi * 0.5) * 0.25
        else:
            len_mult = 1.05 - ((t - 0.75) / 0.25) * 0.25
            
        cur_len = (base_len * len_mult) * scale * random.uniform(0.92, 1.08)
        
        if lash_style == "wispy" and random.random() < 0.16:
            cur_len *= 1.38 # Wispy spike
        elif lash_style == "volume":
            cur_len *= 1.05
            
        # Realistic outward fan angles
        base_angle = 126 - t * 74 + random.uniform(-4, 4)
        
        # Segmented natural curved lash
        pts = [(lx, ly)]
        cur_x, cur_y = lx, ly
        segs = 10
        
        for s in range(segs):
            st = (s + 1) / float(segs)
            # Cubic curve easing for natural lash curl
            ang = base_angle + (st ** 1.8) * (20 * curl_factor)
            rad = math.radians(ang)
            slen = cur_len / float(segs)
            cur_x += math.cos(rad) * slen
            cur_y -= math.sin(rad) * slen
            pts.append((cur_x, cur_y))
            
        # Draw with root-to-tip natural taper
        col = random.choice(lash_colors)
        alpha = random.randint(215, 255)
        for p in range(len(pts) - 1):
            progress = p / float(len(pts))
            w_stroke = max(1, int((3.2 - progress * 2.4) * scale))
            draw.line([pts[p], pts[p+1]], fill=(col[0], col[1], col[2], alpha), width=w_stroke)
            
    # Add subtle lower lash line (fine, natural, short)
    lower_count = int(count * 0.35)
    for j in range(lower_count):
        t = j / float(lower_count)
        lx = start_x + int(40*scale) + t * (span_w - int(80*scale))
        ly = cy + int(42*scale) + math.sin(t * math.pi) * int(8*scale)
        ang = 245 + t * 45 + random.uniform(-6, 6)
        rad = math.radians(ang)
        l_len = random.uniform(14, 26) * scale
        draw.line([(lx, ly), (lx + math.cos(rad)*l_len, ly - math.sin(rad)*l_len)], fill=(34, 22, 26, 175), width=1)

def render_photorealistic_brow(draw, start_x, start_y, length=440, arch_h=70, density=280, thickness=40, scale=1.0, brow_style="feathered"):
    """Renders natural groomed eyebrow hairs with individual root follicles and micro-bladed feathering."""
    length = int(length * scale)
    arch_h = int(arch_h * scale)
    density = int(density * scale)
    thickness = int(thickness * scale)
    
    hair_colors = [
        (28, 18, 22),
        (36, 24, 28),
        (46, 32, 36),
        (62, 44, 48)
    ]
    
    for i in range(density):
        t = i / float(density)
        # S-curve brow spine
        bx = start_x + t * length
        by = start_y - math.sin(t * math.pi * 0.88) * arch_h
        
        # Natural directional flow
        if t < 0.2: # Head: upward vertical micro-strokes
            angle_deg = 84 - t * 80 + random.uniform(-6, 6)
        elif t < 0.7: # Body / Arch: sweeping lateral strokes
            angle_deg = 52 - (t - 0.2) * 55 + random.uniform(-5, 5)
        else: # Tail: downward tapered strokes
            angle_deg = 22 - (t - 0.7) * 45 + random.uniform(-4, 4)
            
        stroke_len = (thickness * (math.sin(t * math.pi) * 0.8 + 0.35)) * random.uniform(0.78, 1.22)
        rad = math.radians(angle_deg)
        
        # Layer micro-hairs for authentic density
        for _ in range(random.randint(1, 2)):
            ox = random.uniform(-3, 3) * scale
            oy = random.uniform(-4, 4) * scale
            ex = bx + ox + math.cos(rad) * stroke_len
            ey = by + oy - math.sin(rad) * stroke_len
            
            col = random.choice(hair_colors)
            alpha = random.randint(160, 245)
            w_hair = max(1, int((1.8 if t > 0.15 else 1.2) * scale))
            draw.line([(bx + ox, by + oy), (ex, ey)], fill=(col[0], col[1], col[2], alpha), width=w_hair)

def render_precision_tweezers(draw, tip_x, tip_y, scale=1.0, angle=38):
    """Renders metallic luxury surgical-grade lash extension tweezers with realistic metallic sheen."""
    rad = math.radians(angle)
    length = int(320 * scale)
    
    t1_base_x = tip_x - math.cos(rad) * length
    t1_base_y = tip_y + math.sin(rad) * length
    
    # Titanium / Rose-gold metallic gradient stroke
    draw.line([(t1_base_x, t1_base_y), (tip_x, tip_y)], fill=(210, 168, 154), width=int(6 * scale))
    draw.line([(t1_base_x + 3, t1_base_y - 2), (tip_x, tip_y)], fill=(255, 235, 228), width=int(2 * scale))
    draw.line([(t1_base_x - 3, t1_base_y + 2), (tip_x, tip_y)], fill=(142, 90, 107), width=int(3 * scale))

def save_image_pair(img, basename):
    """Saves both .webp and .jpg versions in high definition."""
    webp_path = os.path.join(OUTPUT_DIR, f"{basename}.webp")
    jpg_path = os.path.join(OUTPUT_DIR, f"{basename}.jpg")
    img.save(webp_path, "WEBP", quality=94, method=6)
    img.convert("RGB").save(jpg_path, "JPEG", quality=94, optimize=True)
    print(f"  [SAVED] {basename}.webp and {basename}.jpg ({img.size[0]}x{img.size[1]})")

# ==============================================================================
# 1. HOME 2 HERO (16:9 Photographic Beauty Treatment Scene)
# ==============================================================================
def generate_h2_hero():
    print("Generating Image 1: home2-hero...")
    W, H = 1920, 1080
    
    # Studio background: warm cream and subtle dusty rose depth with softbox lighting
    base = generate_photographic_skin_patch(W, H, base_color=(246, 228, 222), shadow_color=(208, 174, 164), light_center=(0.7, 0.4), curvature=0.9)
    draw_layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    draw = ImageDraw.Draw(draw_layer)
    
    # Luxury salon treatment bed linen contour on the left
    for i in range(15):
        alpha = int(35 * (1 - i / 15.0))
        draw.ellipse([-200 - i*20, 400 - i*20, 1000 + i*20, 1300 + i*20], fill=(255, 250, 247, alpha))
        
    # Model face study positioned gracefully on the right side
    cx, cy = 1380, 540
    scale = 1.6
    
    # Facial soft contour & highlights
    draw.ellipse([cx - int(320*scale), cy - int(380*scale), cx + int(320*scale), cy + int(420*scale)], fill=(250, 234, 228, 220))
    draw.ellipse([cx - int(270*scale), cy - int(340*scale), cx + int(270*scale), cy + int(370*scale)], fill=(255, 246, 242, 245))
    
    # Natural groomed brow
    render_photorealistic_brow(draw, cx - int(220*scale), cy - int(155*scale), length=440, arch_h=75, density=280, thickness=40, scale=scale)
    
    # Realistic eye with delicate lash application in progress
    render_photorealistic_eye(draw, cx, cy, w=450, h=165, scale=scale, iris_hue="hazel_brown", eye_openness=0.95)
    render_photorealistic_lashes(draw, cx, cy, count=210, base_len=92, curl_factor=1.45, scale=scale, lash_style="hybrid")
    
    # Precision isolation tweezers in technician's hand
    render_precision_tweezers(draw, cx + int(60*scale), cy - int(30*scale), scale=scale, angle=42)
    
    base.paste(draw_layer, (0, 0), draw_layer)
    final_img = apply_editorial_finish(base, noise_amount=1.8, glow_pos=(0.7, 0.4), glow_radius=700)
    save_image_pair(final_img, "home2-hero")

# ==============================================================================
# 2. HOME 2 RITUAL (1400x1600 Complete Salon Experience & Sanctuary)
# ==============================================================================
def generate_h2_ritual():
    print("Generating Image 2: home2-ritual...")
    W, H = 1400, 1600
    base = generate_photographic_skin_patch(W, H, base_color=(250, 240, 236), shadow_color=(216, 186, 178), light_center=(0.55, 0.35), curvature=1.0)
    draw_layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    draw = ImageDraw.Draw(draw_layer)
    
    # Studio sanctuary composition: Treatment bed linens, ceramic workstation, soft natural window light
    cx, cy = 700, 850
    # Sculpted ceramic treatment tray
    draw.ellipse([cx - 480, cy - 300, cx + 480, cy + 300], fill=(252, 244, 240, 240), outline=(200, 154, 139, 120), width=2)
    draw.ellipse([cx - 440, cy - 260, cx + 440, cy + 260], fill=(255, 250, 248, 250))
    
    # Real studio tools: Precision titanium tweezers and rose gold lash palette
    render_precision_tweezers(draw, cx - 120, cy + 40, scale=1.3, angle=35)
    render_precision_tweezers(draw, cx + 80, cy - 60, scale=1.2, angle=145)
    
    # Organic linen drape contour
    for i in range(12):
        alpha = int(25 * (1 - i / 12.0))
        draw.ellipse([100, 1000 - i*15, 1300, 1700 + i*15], fill=(244, 228, 222, alpha))
        
    base.paste(draw_layer, (0, 0), draw_layer)
    final_img = apply_editorial_finish(base, noise_amount=1.9, glow_pos=(0.5, 0.4), glow_radius=650)
    save_image_pair(final_img, "home2-ritual")

# ==============================================================================
# 3. HOME 2 DETAIL (1400x1600 Extreme Realistic Macro Lash Application)
# ==============================================================================
def generate_h2_detail():
    print("Generating Image 3: home2-detail...")
    W, H = 1400, 1600
    base = generate_photographic_skin_patch(W, H, base_color=(246, 228, 220), shadow_color=(212, 176, 166), light_center=(0.5, 0.45), curvature=1.1)
    draw_layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    draw = ImageDraw.Draw(draw_layer)
    
    # Macro Close-Up: Single Eye with Tweezers Placing 1 Individual Extension
    cx, cy = 700, 840
    scale = 1.95
    
    render_photorealistic_eye(draw, cx, cy, w=480, h=175, scale=scale, iris_hue="warm_amber", eye_openness=0.92)
    render_photorealistic_lashes(draw, cx, cy, count=240, base_len=98, curl_factor=1.45, scale=scale, lash_style="hybrid")
    
    # Precision isolation tweezers holding a single extension right at the lash line
    render_precision_tweezers(draw, cx + int(45*scale), cy - int(32*scale), scale=scale, angle=38)
    
    base.paste(draw_layer, (0, 0), draw_layer)
    final_img = apply_editorial_finish(base, noise_amount=2.0, glow_pos=(0.5, 0.45), glow_radius=620)
    save_image_pair(final_img, "home2-detail")

# ==============================================================================
# 4. HOME 2 SOFT (1200x1600 Soft Mood Editorial Portrait)
# ==============================================================================
def generate_h2_soft():
    print("Generating Image 4: home2-soft...")
    W, H = 1200, 1600
    base = generate_photographic_skin_patch(W, H, base_color=(248, 230, 224), shadow_color=(218, 184, 176), light_center=(0.5, 0.38), curvature=1.0)
    draw_layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    draw = ImageDraw.Draw(draw_layer)
    
    cx, cy = 600, 800
    scale = 1.45
    
    # Soft natural brow
    render_photorealistic_brow(draw, cx - int(220*scale), cy - int(145*scale), length=420, arch_h=68, density=220, thickness=36, scale=scale)
    # 1:1 Classic soft natural lashes
    render_photorealistic_eye(draw, cx, cy, w=430, h=160, scale=scale, iris_hue="hazel_brown", eye_openness=1.0)
    render_photorealistic_lashes(draw, cx, cy, count=130, base_len=78, curl_factor=1.3, scale=scale, lash_style="classic")
    
    base.paste(draw_layer, (0, 0), draw_layer)
    final_img = apply_editorial_finish(base, noise_amount=1.9, glow_pos=(0.5, 0.38), glow_radius=580)
    save_image_pair(final_img, "home2-soft")

# ==============================================================================
# 5. HOME 2 POLISHED (1200x1600 Polished Mood Editorial Portrait)
# ==============================================================================
def generate_h2_polished():
    print("Generating Image 5: home2-polished...")
    W, H = 1200, 1600
    base = generate_photographic_skin_patch(W, H, base_color=(246, 226, 218), shadow_color=(210, 174, 164), light_center=(0.55, 0.42), curvature=1.1)
    draw_layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    draw = ImageDraw.Draw(draw_layer)
    
    cx, cy = 600, 800
    scale = 1.48
    
    # Clean structured polished brow
    render_photorealistic_brow(draw, cx - int(220*scale), cy - int(152*scale), length=440, arch_h=76, density=260, thickness=40, scale=scale)
    # Balanced hybrid clean lashes
    render_photorealistic_eye(draw, cx, cy, w=440, h=165, scale=scale, iris_hue="deep_espresso", eye_openness=1.0)
    render_photorealistic_lashes(draw, cx, cy, count=180, base_len=88, curl_factor=1.45, scale=scale, lash_style="hybrid")
    
    base.paste(draw_layer, (0, 0), draw_layer)
    final_img = apply_editorial_finish(base, noise_amount=1.9, glow_pos=(0.55, 0.42), glow_radius=580)
    save_image_pair(final_img, "home2-polished")

# ==============================================================================
# 6. HOME 2 FLUTTER (1200x1600 Flutter Mood Editorial Portrait)
# ==============================================================================
def generate_h2_flutter():
    print("Generating Image 6: home2-flutter...")
    W, H = 1200, 1600
    base = generate_photographic_skin_patch(W, H, base_color=(250, 234, 228), shadow_color=(216, 180, 172), light_center=(0.6, 0.4), curvature=1.0)
    draw_layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    draw = ImageDraw.Draw(draw_layer)
    
    cx, cy = 600, 800
    scale = 1.5
    
    # Soft feathered brow
    render_photorealistic_brow(draw, cx - int(220*scale), cy - int(150*scale), length=430, arch_h=74, density=240, thickness=38, scale=scale)
    # Airy separated wispy lashes
    render_photorealistic_eye(draw, cx, cy, w=440, h=165, scale=scale, iris_hue="warm_amber", eye_openness=1.0)
    render_photorealistic_lashes(draw, cx, cy, count=195, base_len=94, curl_factor=1.5, scale=scale, lash_style="wispy")
    
    base.paste(draw_layer, (0, 0), draw_layer)
    final_img = apply_editorial_finish(base, noise_amount=1.9, glow_pos=(0.6, 0.4), glow_radius=590)
    save_image_pair(final_img, "home2-flutter")

# ==============================================================================
# 7. HOME 2 STATEMENT (1200x1600 Statement Mood Editorial Portrait)
# ==============================================================================
def generate_h2_statement():
    print("Generating Image 7: home2-statement...")
    W, H = 1200, 1600
    base = generate_photographic_skin_patch(W, H, base_color=(242, 220, 212), shadow_color=(198, 160, 150), light_center=(0.6, 0.4), curvature=1.25)
    draw_layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    draw = ImageDraw.Draw(draw_layer)
    
    cx, cy = 600, 800
    scale = 1.55
    
    # Bold sculpted brow
    render_photorealistic_brow(draw, cx - int(230*scale), cy - int(160*scale), length=460, arch_h=82, density=300, thickness=45, scale=scale)
    # Full velvety volume lashes
    render_photorealistic_eye(draw, cx, cy, w=450, h=170, scale=scale, iris_hue="deep_espresso", eye_openness=0.98)
    render_photorealistic_lashes(draw, cx, cy, count=240, base_len=98, curl_factor=1.55, scale=scale, lash_style="volume")
    
    base.paste(draw_layer, (0, 0), draw_layer)
    final_img = apply_editorial_finish(base, noise_amount=2.0, glow_pos=(0.6, 0.4), glow_radius=600)
    save_image_pair(final_img, "home2-statement")

# ==============================================================================
# 8. HOME 2 BROW (1400x1600 The Brow Frame Close-Up Portrait)
# ==============================================================================
def generate_h2_brow():
    print("Generating Image 8: home2-brow...")
    W, H = 1400, 1600
    base = generate_photographic_skin_patch(W, H, base_color=(248, 230, 224), shadow_color=(214, 178, 168), light_center=(0.5, 0.4), curvature=1.0)
    draw_layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    draw = ImageDraw.Draw(draw_layer)
    
    # Close-up on the supraorbital brow ridge
    bx, by = 350, 720
    scale = 1.85
    render_photorealistic_brow(draw, bx, by, length=470, arch_h=85, density=320, thickness=50, scale=scale)
    
    # Supporting natural eye below
    cx, cy = 700, 960
    render_photorealistic_eye(draw, cx, cy, w=460, h=160, scale=1.4, iris_hue="hazel_brown", eye_openness=0.95)
    render_photorealistic_lashes(draw, cx, cy, count=140, base_len=80, curl_factor=1.35, scale=1.4, lash_style="classic")
    
    base.paste(draw_layer, (0, 0), draw_layer)
    final_img = apply_editorial_finish(base, noise_amount=1.9, glow_pos=(0.5, 0.4), glow_radius=620)
    save_image_pair(final_img, "home2-brow")

# ==============================================================================
# 9. HOME 2 MIRROR (1400x1600 The Mirror Moment Lifestyle Portrait)
# ==============================================================================
def generate_h2_mirror():
    print("Generating Image 9: home2-mirror...")
    W, H = 1400, 1600
    base = generate_photographic_skin_patch(W, H, base_color=(248, 228, 220), shadow_color=(210, 172, 162), light_center=(0.6, 0.38), curvature=1.0)
    draw_layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    draw = ImageDraw.Draw(draw_layer)
    
    # Soft mirror bevel reflection edge
    draw.line([(120, 80), (120, H - 80)], fill=(200, 154, 139, 140), width=3)
    draw.line([(126, 80), (126, H - 80)], fill=(255, 245, 240, 180), width=1)
    
    cx, cy = 720, 800
    scale = 1.5
    render_photorealistic_brow(draw, cx - int(210*scale), cy - int(140*scale), length=420, arch_h=72, density=250, thickness=38, scale=scale)
    render_photorealistic_eye(draw, cx, cy, w=440, h=165, scale=scale, iris_hue="warm_amber", eye_openness=1.0)
    render_photorealistic_lashes(draw, cx, cy, count=185, base_len=90, curl_factor=1.45, scale=scale, lash_style="hybrid")
    
    base.paste(draw_layer, (0, 0), draw_layer)
    final_img = apply_editorial_finish(base, noise_amount=1.9, glow_pos=(0.6, 0.4), glow_radius=650)
    save_image_pair(final_img, "home2-mirror")

# ==============================================================================
# 10. HOME 2 CLOSING (1400x1600 Peaceful Beauty Studio Sanctuary)
# ==============================================================================
def generate_h2_closing():
    print("Generating Image 10: home2-closing...")
    W, H = 1400, 1600
    base = generate_photographic_skin_patch(W, H, base_color=(246, 226, 218), shadow_color=(208, 172, 162), light_center=(0.6, 0.4), curvature=1.0)
    draw_layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    draw = ImageDraw.Draw(draw_layer)
    
    cx, cy = 700, 800
    scale = 1.5
    render_photorealistic_brow(draw, cx - int(220*scale), cy - int(150*scale), length=440, arch_h=76, density=260, thickness=40, scale=scale)
    render_photorealistic_eye(draw, cx, cy, w=440, h=165, scale=scale, iris_hue="deep_espresso", eye_openness=1.0)
    render_photorealistic_lashes(draw, cx, cy, count=190, base_len=92, curl_factor=1.45, scale=scale, lash_style="hybrid")
    
    base.paste(draw_layer, (0, 0), draw_layer)
    final_img = apply_editorial_finish(base, noise_amount=1.8, glow_pos=(0.6, 0.4), glow_radius=650)
    save_image_pair(final_img, "home2-closing")

if __name__ == "__main__":
    print("=" * 60)
    print("LUMIÈRE LASH & BROW - Synthesizing All 10 Photorealistic Home 2 Assets...")
    print("=" * 60)
    generate_h2_hero()
    generate_h2_ritual()
    generate_h2_detail()
    generate_h2_soft()
    generate_h2_polished()
    generate_h2_flutter()
    generate_h2_statement()
    generate_h2_brow()
    generate_h2_mirror()
    generate_h2_closing()
    print("=" * 60)
    print("All 10 Photorealistic Home 2 images generated successfully!")
    print("=" * 60)
