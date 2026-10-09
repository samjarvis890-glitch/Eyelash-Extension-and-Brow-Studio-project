"""
LUMIÈRE LASH & BROW - Ultra HD Editorial Asset Generator
Generates all 12 High-Definition (1920px+ landscape, 1600px+ portrait, 1200px+ cards)
custom luxury editorial visuals in assets/images/home/ in both JPG and WebP formats.
"""

import os
import math
import random
import numpy as np
from PIL import Image, ImageDraw, ImageFilter

OUTPUT_DIR = r"assets\images\home"
os.makedirs(OUTPUT_DIR, exist_ok=True)

# Color Palette
COLOR_PRIMARY = (43, 31, 36)        # #2B1F24 Espresso Plum
COLOR_DUSTY_ROSE = (142, 90, 107)    # #8E5A6B
COLOR_ROSE_GOLD = (200, 154, 139)    # #C89A8B
COLOR_BLUSH = (248, 241, 242)        # #F8F1F2
COLOR_WARM_CREAM = (255, 249, 246)   # #FFF9F6
COLOR_HAIR_DARK = (32, 22, 26)       # Rich deep lash pigment
COLOR_HAIR_MED = (45, 32, 38)
COLOR_HAIR_SOFT = (60, 45, 52)

def create_smooth_gradient(w, h, color1, color2, angle=45, center=(0.5, 0.5), radial=False):
    """Creates a smooth 2D gradient array with zero banding."""
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

def add_noise_and_glow(img, noise_level=3.0, glow_color=(255, 242, 236), glow_pos=(0.65, 0.35), glow_radius=500):
    """Adds soft studio ambient glow and realistic editorial film grain."""
    w, h = img.size
    glow = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    gdraw = ImageDraw.Draw(glow)
    gx, gy = int(glow_pos[0] * w), int(glow_pos[1] * h)
    
    # Smooth multi-step radial glow
    for r in range(glow_radius, 0, -15):
        alpha = int(50 * (1 - r / glow_radius)**1.5)
        gdraw.ellipse([gx - r, gy - r, gx + r, gy + r], fill=(glow_color[0], glow_color[1], glow_color[2], alpha))
    img.paste(glow, (0, 0), glow)
    
    # Ultra-fine editorial grain
    arr = np.array(img, dtype=np.int16)
    noise = np.random.normal(0, noise_level, arr.shape)
    arr = np.clip(arr + noise, 0, 255).astype(np.uint8)
    return Image.fromarray(arr)

def draw_feathered_brow(draw, start_x, start_y, length=450, arch_height=65, density=160, thickness=40, hair_color=COLOR_HAIR_DARK, scale=1.0):
    """Draws realistic micro-feathered brow strokes with organic curves."""
    length = int(length * scale)
    arch_height = int(arch_height * scale)
    density = int(density * scale)
    thickness = int(thickness * scale)
    
    for i in range(density):
        t = i / float(density)
        # Baseline arch curve
        bx = start_x + t * length
        by = start_y - math.sin(t * math.pi * 0.88) * arch_height
        
        # Heading angle transitions from vertical at the head to horizontal at tail
        angle_deg = 78 - t * 70 + random.uniform(-9, 9)
        stroke_len = (thickness * (math.sin(t * math.pi) * 0.85 + 0.35)) * random.uniform(0.75, 1.25)
        rad = math.radians(angle_deg)
        
        # Multi-stroke hair filaments
        for _ in range(random.randint(1, 3)):
            ox = random.uniform(-4, 4) * scale
            oy = random.uniform(-5, 5) * scale
            ex = bx + ox + math.cos(rad) * stroke_len
            ey = by + oy - math.sin(rad) * stroke_len
            
            alpha = int(random.uniform(150, 235))
            col = (hair_color[0], hair_color[1], hair_color[2], alpha)
            draw.line([(bx + ox, by + oy), (ex, ey)], fill=col, width=max(1, int(2 * scale)))

def draw_luxurious_eyelashes(draw, eye_cx, eye_cy, eye_w=400, eye_h=110, lash_type="hybrid", count=160, length_scale=1.0, scale=1.0):
    """Draws ultra-high-definition individual and fanned eyelash extensions along eyelid margin."""
    eye_w = int(eye_w * scale)
    eye_h = int(eye_h * scale)
    count = int(count * scale)
    
    # Eyelid curvature
    lid_pts = []
    for i in range(60):
        t = i / 59.0
        lx = eye_cx - eye_w/2 + t * eye_w
        ly = eye_cy - math.sin(t * math.pi) * (eye_h / 2)
        lid_pts.append((lx, ly))
    
    # Dark tightline / waterline definition
    draw.line(lid_pts, fill=(30, 20, 24, 240), width=max(2, int(4 * scale)))
    
    tones = [
        (28, 18, 22, 240),
        (38, 26, 30, 210),
        (46, 34, 38, 190)
    ]
    
    for i in range(count):
        t = i / float(count)
        lx = eye_cx - eye_w/2 + t * eye_w + random.uniform(-3, 3) * scale
        ly = eye_cy - math.sin(t * math.pi) * (eye_h / 2)
        
        # Length mapping (cat-eye / natural sweep: shorter inner corner, sweeping outer)
        if t < 0.2:
            base_len = (40 + t * 180) * scale
        elif t < 0.75:
            base_len = (75 + math.sin((t - 0.2)/0.55 * math.pi) * 45) * scale
        else:
            base_len = (85 - (t - 0.75) * 90) * scale
            
        base_len *= length_scale
        
        if lash_type == "classic":
            fan_count = 1
            curl_intensity = 1.05
            angle_bias = 82 - t * 46
            stroke_w = max(1, int(3 * scale))
        elif lash_type == "hybrid":
            fan_count = random.choices([1, 2, 3], weights=[0.35, 0.45, 0.2])[0]
            curl_intensity = 1.15
            angle_bias = 84 - t * 48
            stroke_w = max(1, int(2 * scale))
        elif lash_type == "volume":
            fan_count = random.choices([3, 4, 5, 6], weights=[0.2, 0.4, 0.3, 0.1])[0]
            curl_intensity = 1.25
            angle_bias = 86 - t * 50
            stroke_w = max(1, int(1.5 * scale))
            base_len *= 1.18
        elif lash_type == "wispy":
            is_spike = (i % 8 == 0)
            fan_count = 1 if is_spike else random.choice([2, 3])
            base_len = (base_len * 1.4) if is_spike else (base_len * 0.85)
            curl_intensity = 1.3 if is_spike else 1.1
            angle_bias = 83 - t * 46
            stroke_w = max(1, int(3 * scale if is_spike else 1.5 * scale))
        else:
            fan_count = 2
            curl_intensity = 1.05
            angle_bias = 82 - t * 45
            stroke_w = max(1, int(2 * scale))

        for f in range(fan_count):
            fan_spread = (f - (fan_count-1)/2) * (7 * scale)
            angle = angle_bias + fan_spread + random.uniform(-3.5, 3.5)
            rad = math.radians(angle)
            
            curl = curl_intensity * (28 + t * 16) * scale
            mid_x = lx + math.cos(rad) * (base_len * 0.55) - (curl * 0.45)
            mid_y = ly - math.sin(rad) * (base_len * 0.55)
            
            tip_x = lx + math.cos(rad) * base_len + (curl * 0.85)
            tip_y = ly - math.sin(rad) * base_len
            
            col_tone = random.choice(tones)
            draw.line([(lx, ly), (mid_x, mid_y), (tip_x, tip_y)], fill=col_tone, width=stroke_w)

def save_dual_formats(img, base_name):
    """Saves both JPG and WebP formats."""
    jpg_path = os.path.join(OUTPUT_DIR, f"{base_name}.jpg")
    webp_path = os.path.join(OUTPUT_DIR, f"{base_name}.webp")
    
    img.save(jpg_path, "JPEG", quality=95, optimize=True)
    img.save(webp_path, "WEBP", quality=92, method=6)
    print(f"✓ Saved {base_name}.jpg & {base_name}.webp ({img.size[0]}x{img.size[1]})")

def generate_hero():
    """1. Hero: Ultra-HD 1920x1200 Editorial Portrait Beauty Close-Up"""
    w, h = 1920, 1200
    base = create_smooth_gradient(w, h, (254, 247, 244), (235, 212, 204), angle=35)
    overlay = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    draw = ImageDraw.Draw(overlay)
    
    # Cheekbone highlight and soft socket depth
    draw.ellipse([300, 200, 1600, 1150], fill=(248, 228, 222, 130))
    draw.ellipse([600, 400, 1400, 950], fill=(228, 196, 186, 95))
    draw.ellipse([700, 520, 1300, 840], fill=(255, 246, 242, 160))
    
    eye_cx, eye_cy = 960, 680
    scale = 1.6
    
    # Sculpted Feathered Eyebrow
    draw_feathered_brow(draw, start_x=680, start_y=460, length=480, arch_height=70, density=180, thickness=38, scale=scale)
    
    # Ultra-Lush Wispy/Hybrid Lashes
    draw_luxurious_eyelashes(draw, eye_cx, eye_cy, eye_w=400, eye_h=110, lash_type="wispy", count=180, length_scale=1.28, scale=scale)
    
    # Delicate Lower Lashes
    for i in range(65):
        t = i / 65.0
        lx = eye_cx - 160 * scale + t * 320 * scale
        ly = eye_cy + 22 * scale + math.sin(t * math.pi) * (28 * scale)
        draw.line([(lx, ly), (lx + (t - 0.5) * 22 * scale, ly + 20 * scale)], fill=(48, 34, 38, 115), width=max(1, int(1.5 * scale)))

    base.paste(overlay, (0, 0), overlay)
    img = add_noise_and_glow(base, noise_level=2.8, glow_pos=(0.65, 0.4), glow_radius=600)
    save_dual_formats(img, "hero")

def generate_signature_cards():
    """2. Classic, Hybrid, Volume, Wispy, Brow Styling (1200x1200 each)"""
    styles = [
        ("classic", "classic", (255, 248, 246), (236, 216, 208), 0.96),
        ("hybrid", "hybrid", (253, 245, 241), (230, 206, 196), 1.08),
        ("volume", "volume", (248, 238, 234), (224, 194, 186), 1.22),
        ("wispy", "wispy", (255, 249, 247), (234, 208, 202), 1.18),
    ]
    
    for base_name, stype, c1, c2, lscale in styles:
        w, h = 1200, 1200
        base = create_smooth_gradient(w, h, c1, c2, angle=random.randint(25, 60))
        overlay = Image.new("RGBA", (w, h), (0, 0, 0, 0))
        draw = ImageDraw.Draw(overlay)
        
        draw.ellipse([220, 280, 980, 980], fill=(255, 244, 238, 140))
        scale = 1.35
        
        draw_feathered_brow(draw, start_x=340, start_y=450, length=440, arch_height=60, density=150, thickness=32, scale=scale)
        draw_luxurious_eyelashes(draw, eye_cx=600, eye_cy=660, eye_w=380, eye_h=95, lash_type=stype, count=150, length_scale=lscale, scale=scale)
        
        base.paste(overlay, (0, 0), overlay)
        img = add_noise_and_glow(base, noise_level=3.0, glow_pos=(0.6, 0.38), glow_radius=450)
        save_dual_formats(img, base_name)

    # 5. Brow Styling Card
    w, h = 1200, 1200
    base = create_smooth_gradient(w, h, (254, 248, 245), (232, 210, 202), angle=40)
    overlay = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    draw = ImageDraw.Draw(overlay)
    
    draw.ellipse([150, 200, 1050, 980], fill=(255, 246, 242, 150))
    scale = 1.55
    # High-definition laminated brow focus
    draw_feathered_brow(draw, start_x=240, start_y=540, length=560, arch_height=80, density=240, thickness=48, scale=scale)
    draw_luxurious_eyelashes(draw, eye_cx=600, eye_cy=800, eye_w=400, eye_h=85, lash_type="classic", count=90, length_scale=0.85, scale=scale)
    
    base.paste(overlay, (0, 0), overlay)
    img = add_noise_and_glow(base, noise_level=3.0, glow_pos=(0.55, 0.4), glow_radius=500)
    save_dual_formats(img, "brow-styling")

def generate_find_your_look():
    """3. Find Your Look: 1400x1600 Editorial Portrait & Mapping Consultation"""
    w, h = 1400, 1600
    base = create_smooth_gradient(w, h, (253, 246, 243), (228, 204, 196), angle=125)
    overlay = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    draw = ImageDraw.Draw(overlay)
    
    # Soft mirror frame accent
    draw.rounded_rectangle([100, 100, w-100, h-100], radius=40, outline=(200, 154, 139, 100), width=2)
    draw.ellipse([300, 350, 1100, 1150], fill=(255, 246, 241, 160))
    
    scale = 1.5
    draw_feathered_brow(draw, start_x=400, start_y=600, length=460, arch_height=65, density=160, thickness=35, scale=scale)
    draw_luxurious_eyelashes(draw, eye_cx=700, eye_cy=820, eye_w=380, eye_h=95, lash_type="hybrid", count=160, length_scale=1.15, scale=scale)
    
    # Golden consultation geometric mapping guides
    for r in [260, 320, 380]:
        draw.arc([700-r, 820-r, 700+r, 820+r], start=210, end=330, fill=(200, 154, 139, 50), width=2)
        
    base.paste(overlay, (0, 0), overlay)
    img = add_noise_and_glow(base, noise_level=3.0, glow_pos=(0.52, 0.42), glow_radius=550)
    save_dual_formats(img, "find-your-look")

def generate_lumiere_touch():
    """4. Lumière Touch: 1400x1600 Precision Tweezers & Artist Craftsmanship"""
    w, h = 1400, 1600
    base = create_smooth_gradient(w, h, (250, 241, 238), (224, 198, 190), angle=145)
    overlay = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    draw = ImageDraw.Draw(overlay)
    
    scale = 1.55
    # Luxury tweezers
    tweezer_pts1 = [(380, 200), (740, 780), (748, 788), (480, 180)]
    draw.polygon(tweezer_pts1, fill=(200, 154, 139, 230))
    
    tweezer_pts2 = [(1020, 240), (778, 780), (770, 788), (1080, 260)]
    draw.polygon(tweezer_pts2, fill=(185, 138, 124, 235))
    
    draw.ellipse([480, 560, 1020, 1100], fill=(255, 246, 242, 160))
    draw_luxurious_eyelashes(draw, eye_cx=760, eye_cy=830, eye_w=360, eye_h=90, lash_type="volume", count=150, length_scale=1.15, scale=scale)
    
    # Soft hydrogel soothing eye patch curve
    draw.arc([520, 810, 1000, 990], start=20, end=160, fill=(255, 255, 255, 230), width=26)
    
    base.paste(overlay, (0, 0), overlay)
    img = add_noise_and_glow(base, noise_level=2.8, glow_pos=(0.55, 0.45), glow_radius=550)
    save_dual_formats(img, "lumiere-touch")

def generate_transformation_pair():
    """5. Transformation: 1200x1200 Natural Bare vs Sculpted Enhanced Pair"""
    w, h = 1200, 1200
    scale = 1.45
    
    # --- BEFORE ---
    base_b = create_smooth_gradient(w, h, (254, 248, 245), (234, 212, 204), angle=45)
    overlay_b = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    draw_b = ImageDraw.Draw(overlay_b)
    
    draw_b.ellipse([220, 300, 980, 980], fill=(255, 246, 242, 135))
    draw_feathered_brow(draw_b, start_x=340, start_y=480, length=440, arch_height=45, density=75, thickness=22, hair_color=(75, 58, 65), scale=scale)
    draw_luxurious_eyelashes(draw_b, eye_cx=600, eye_cy=680, eye_w=360, eye_h=85, lash_type="classic", count=60, length_scale=0.55, scale=scale)
    
    base_b.paste(overlay_b, (0, 0), overlay_b)
    img_b = add_noise_and_glow(base_b, noise_level=3.0, glow_pos=(0.6, 0.4), glow_radius=420)
    save_dual_formats(img_b, "transformation-before")
    
    # --- AFTER ---
    base_a = create_smooth_gradient(w, h, (254, 248, 245), (234, 212, 204), angle=45)
    overlay_a = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    draw_a = ImageDraw.Draw(overlay_a)
    
    draw_a.ellipse([220, 300, 980, 980], fill=(255, 246, 242, 135))
    draw_feathered_brow(draw_a, start_x=340, start_y=480, length=460, arch_height=65, density=190, thickness=38, hair_color=(35, 24, 28), scale=scale)
    draw_luxurious_eyelashes(draw_a, eye_cx=600, eye_cy=680, eye_w=360, eye_h=85, lash_type="wispy", count=170, length_scale=1.25, scale=scale)
    
    base_a.paste(overlay_a, (0, 0), overlay_a)
    img_a = add_noise_and_glow(base_a, noise_level=3.0, glow_pos=(0.6, 0.4), glow_radius=420)
    save_dual_formats(img_a, "transformation-after")

def generate_appointment():
    """6. Appointment: 1920x1080 Immersive Spa Treatment Suite"""
    w, h = 1920, 1080
    base = create_smooth_gradient(w, h, (255, 251, 249), (228, 206, 200), angle=25)
    overlay = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    draw = ImageDraw.Draw(overlay)
    
    # Warm architectural alcove
    draw.ellipse([500, -250, 2200, 1350], fill=(250, 236, 230, 170))
    
    # Ergonomic lash bed
    bed_pts = [(200, 680), (1720, 680), (1650, 850), (270, 850)]
    draw.polygon(bed_pts, fill=(255, 255, 255, 240))
    
    # Plush memory-foam headrest
    draw.rounded_rectangle([340, 630, 720, 695], radius=28, fill=(245, 230, 225, 250))
    
    # Dusty rose folded cashmere throw
    draw.rounded_rectangle([1050, 670, 1600, 715], radius=16, fill=(142, 90, 107, 190))
    
    # Soft warm ring-light halo
    for r in range(300, 140, -18):
        alpha = int(45 * (1 - (r - 140)/160))
        draw.ellipse([1240-r, 360-r, 1240+r, 360+r], outline=(200, 154, 139, alpha), width=4)
        
    # Dried botanical pampas silhouette
    for angle in [-35, -20, -5, 10, 25]:
        rad = math.radians(90 + angle)
        draw.line([(1650, 1020), (1650 + math.cos(rad)*440, 1020 - math.sin(rad)*440)], fill=(142, 90, 107, 115), width=3)
        
    base.paste(overlay, (0, 0), overlay)
    img = add_noise_and_glow(base, noise_level=2.8, glow_pos=(0.65, 0.35), glow_radius=600)
    save_dual_formats(img, "appointment")

def generate_home_closing():
    """7. Closing: 1400x1600 Moody Plum Portrait Accent"""
    w, h = 1400, 1600
    base = create_smooth_gradient(w, h, (43, 31, 36), (24, 15, 19), angle=45)
    overlay = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    draw = ImageDraw.Draw(overlay)
    
    draw.ellipse([380, 380, 1480, 1480], fill=(68, 44, 52, 145))
    draw.ellipse([540, 540, 1320, 1320], fill=(142, 90, 107, 85))
    
    scale = 1.55
    draw_feathered_brow(draw, start_x=500, start_y=640, length=460, arch_height=65, density=160, thickness=34, hair_color=(210, 170, 160), scale=scale)
    draw_luxurious_eyelashes(draw, eye_cx=780, eye_cy=830, eye_w=380, eye_h=95, lash_type="volume", count=160, length_scale=1.24, scale=scale)
    
    draw.arc([240, 240, 1160, 1160], start=180, end=300, fill=(200, 154, 139, 95), width=3)
    
    base.paste(overlay, (0, 0), overlay)
    img = add_noise_and_glow(base, noise_level=3.0, glow_color=(200, 154, 139), glow_pos=(0.55, 0.45), glow_radius=600)
    save_dual_formats(img, "home-closing")

if __name__ == "__main__":
    print("Generating Ultra-HD local image assets in JPG and WebP formats...")
    generate_hero()
    generate_signature_cards()
    generate_find_your_look()
    generate_lumiere_touch()
    generate_transformation_pair()
    generate_appointment()
    generate_home_closing()
    print("All 12 Ultra-HD image assets in JPG & WebP generated successfully!")
