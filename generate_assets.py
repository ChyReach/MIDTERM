"""Run this once to generate all PNG assets for the car game."""
from PIL import Image, ImageDraw
import os

ASSETS = os.path.join(os.path.dirname(os.path.abspath(__file__)), "assets")
os.makedirs(ASSETS, exist_ok=True)

# ── Helper ────────────────────────────────────────────────────────────────────
def save(img, name):
    img.save(os.path.join(ASSETS, name))
    print(f"  saved {name}")

# ══════════════════════════════════════════════════════════════
# PLAYER CAR  (60×110, top-down, blue racing car)
# ══════════════════════════════════════════════════════════════
def make_player_car():
    img = Image.new("RGBA", (60, 110), (0,0,0,0))
    d = ImageDraw.Draw(img)
    # Body
    d.rounded_rectangle([5,10,55,100], radius=8, fill=(30,90,220))
    # Windshield
    d.polygon([(12,20),(48,20),(44,38),(16,38)], fill=(180,220,255,200))
    # Rear window
    d.polygon([(14,72),(46,72),(44,85),(16,85)], fill=(180,220,255,180))
    # Hood stripes
    d.rectangle([22,10,26,40], fill=(255,255,255,120))
    d.rectangle([34,10,38,40], fill=(255,255,255,120))
    # Headlights
    d.ellipse([8,8,22,18],  fill=(255,255,180))
    d.ellipse([38,8,52,18], fill=(255,255,180))
    # Taillights
    d.ellipse([8,94,22,104],  fill=(255,60,60))
    d.ellipse([38,94,52,104], fill=(255,60,60))
    # Wheels
    for wx,wy in [(0,15),(44,15),(0,82),(44,82)]:
        d.ellipse([wx,wy,wx+16,wy+22], fill=(30,30,30))
        d.ellipse([wx+3,wy+3,wx+13,wy+19], fill=(80,80,80))
    # Number
    d.ellipse([20,46,40,66], fill=(255,255,255,200))
    d.text((26,49), "1", fill=(20,60,200))
    return img

save(make_player_car(), "player_car.png")

# ══════════════════════════════════════════════════════════════
# ENEMY CAR  (60×110, red)
# ══════════════════════════════════════════════════════════════
def make_enemy_car(color=(200,30,30), number="X"):
    img = Image.new("RGBA", (60, 110), (0,0,0,0))
    d = ImageDraw.Draw(img)
    d.rounded_rectangle([5,10,55,100], radius=8, fill=color)
    d.polygon([(12,20),(48,20),(44,38),(16,38)], fill=(180,220,255,200))
    d.polygon([(14,72),(46,72),(44,85),(16,85)], fill=(180,220,255,180))
    d.ellipse([8,8,22,18],  fill=(255,255,100))
    d.ellipse([38,8,52,18], fill=(255,255,100))
    d.ellipse([8,94,22,104],  fill=(255,80,80))
    d.ellipse([38,94,52,104], fill=(255,80,80))
    for wx,wy in [(0,15),(44,15),(0,82),(44,82)]:
        d.ellipse([wx,wy,wx+16,wy+22], fill=(30,30,30))
        d.ellipse([wx+3,wy+3,wx+13,wy+19], fill=(80,80,80))
    d.ellipse([20,46,40,66], fill=(255,255,255,200))
    d.text((24,49), number, fill=(180,20,20))
    return img

save(make_enemy_car((200,30,30), "X"),   "enemy_car.png")
save(make_enemy_car((180,80,20), "2"),   "enemy_car2.png")
save(make_enemy_car((120,20,160), "3"),  "enemy_car3.png")

# ══════════════════════════════════════════════════════════════
# OBSTACLE (rock / barrel, 50×50)
# ══════════════════════════════════════════════════════════════
def make_obstacle():
    img = Image.new("RGBA", (50, 50), (0,0,0,0))
    d = ImageDraw.Draw(img)
    d.ellipse([2,2,48,48], fill=(100,70,40), outline=(60,40,20), width=3)
    d.ellipse([10,10,40,40], fill=(120,90,55))
    d.line([(25,5),(25,45)], fill=(80,55,30), width=2)
    d.line([(5,25),(45,25)], fill=(80,55,30), width=2)
    return img

save(make_obstacle(), "obstacle.png")

# ══════════════════════════════════════════════════════════════
# COIN / BOOST  (30×30)
# ══════════════════════════════════════════════════════════════
def make_coin():
    img = Image.new("RGBA", (30, 30), (0,0,0,0))
    d = ImageDraw.Draw(img)
    d.ellipse([2,2,28,28], fill=(255,215,0), outline=(200,160,0), width=2)
    d.ellipse([6,6,24,24], fill=(255,230,80))
    d.text((10,8), "$", fill=(180,130,0))
    return img

save(make_coin(), "coin.png")

# ══════════════════════════════════════════════════════════════
# BACKGROUND LEVEL 1: City Highway (day)
# ══════════════════════════════════════════════════════════════
def make_bg_city():
    W, H = 400, 700
    img = Image.new("RGBA", (W, H), (0,0,0,0))
    d = ImageDraw.Draw(img)
    # Sky
    for y in range(H):
        t = y/H
        r = int(100*(1-t)+50*t); g = int(160*(1-t)+80*t); b = int(220*(1-t)+120*t)
        d.line([(0,y),(W,y)], fill=(r,g,b))
    # Road
    d.rectangle([60,0,340,H], fill=(60,60,65))
    # Road edges
    d.rectangle([60,0,75,H],  fill=(255,255,255))
    d.rectangle([325,0,340,H],fill=(255,255,255))
    # Lane dashes (repeating)
    for y in range(0, H, 60):
        d.rectangle([197,y,203,y+35], fill=(255,220,0))
    # Sidewalks
    d.rectangle([0,0,60,H],  fill=(140,130,120))
    d.rectangle([340,0,W,H], fill=(140,130,120))
    # Buildings left
    import random; random.seed(7)
    for i in range(5):
        bh = random.randint(100,250)
        bx = random.randint(0,30)
        by = random.randint(0,H-bh)
        bw = random.randint(20,45)
        bc = (random.randint(80,160),random.randint(80,140),random.randint(90,160))
        d.rectangle([bx,by,bx+bw,by+bh], fill=bc, outline=(40,40,40))
        # windows
        for wy in range(by+10, by+bh-10, 20):
            for wx2 in range(bx+5, bx+bw-5, 14):
                wc = (255,240,150) if random.random()<0.6 else (60,80,120)
                d.rectangle([wx2,wy,wx2+8,wy+12], fill=wc)
    # Buildings right
    for i in range(5):
        bh = random.randint(100,250)
        bx = random.randint(345,370)
        by = random.randint(0,H-bh)
        bw = random.randint(20,45)
        bc = (random.randint(80,160),random.randint(80,140),random.randint(90,160))
        d.rectangle([bx,by,bx+bw,by+bh], fill=bc, outline=(40,40,40))
        for wy in range(by+10, by+bh-10, 20):
            for wx2 in range(bx+5, bx+bw-5, 14):
                wc = (255,240,150) if random.random()<0.6 else (60,80,120)
                d.rectangle([wx2,wy,wx2+8,wy+12], fill=wc)
    return img

save(make_bg_city(), "bg_level1.png")

# ══════════════════════════════════════════════════════════════
# BACKGROUND LEVEL 2: Night Desert Highway
# ══════════════════════════════════════════════════════════════
def make_bg_desert():
    import random; random.seed(13)
    W, H = 400, 700
    img = Image.new("RGBA", (W, H), (0,0,0,0))
    d = ImageDraw.Draw(img)
    # Sky (dark night)
    for y in range(H):
        t = y/H
        r = int(5+15*t); g = int(5+10*t); b = int(20+30*t)
        d.line([(0,y),(W,y)], fill=(r,g,b))
    # Stars
    for _ in range(80):
        sx = random.randint(0,W); sy = random.randint(0,int(H*0.5))
        br = random.randint(150,255)
        d.ellipse([sx,sy,sx+2,sy+2], fill=(br,br,br))
    # Moon
    d.ellipse([320,30,360,70], fill=(240,235,200))
    d.ellipse([330,32,368,68], fill=(5,5,20))  # crescent
    # Desert sand
    d.rectangle([0,0,60,H],  fill=(180,140,80))
    d.rectangle([340,0,W,H], fill=(180,140,80))
    # Sand texture
    for _ in range(30):
        sx = random.randint(0,55); sy = random.randint(0,H)
        d.ellipse([sx,sy,sx+8,sy+3], fill=(160,120,60,120))
    for _ in range(30):
        sx = random.randint(342,W-5); sy = random.randint(0,H)
        d.ellipse([sx,sy,sx+8,sy+3], fill=(160,120,60,120))
    # Road
    d.rectangle([60,0,340,H], fill=(40,40,45))
    d.rectangle([60,0,75,H],  fill=(255,255,255))
    d.rectangle([325,0,340,H],fill=(255,255,255))
    # Lane dashes
    for y in range(0, H, 60):
        d.rectangle([197,y,203,y+35], fill=(255,180,0))
    # Cacti
    for cx in [20,42,350,372]:
        for cy in [80,230,400,560]:
            cy2 = cy + random.randint(-20,20)
            d.rectangle([cx+8,cy2,cx+16,cy2+50], fill=(40,120,40))
            d.rectangle([cx,  cy2+15,cx+8, cy2+25],  fill=(40,120,40))
            d.rectangle([cx+16,cy2+20,cx+24,cy2+30], fill=(40,120,40))
    # Road glow (headlight reflection)
    for y in range(0,H,120):
        glow = Image.new("RGBA", (W,40), (0,0,0,0))
        gd = ImageDraw.Draw(glow)
        gd.ellipse([150,5,250,35], fill=(255,220,100,18))
        img.alpha_composite(glow, (0,y))
    return img

save(make_bg_desert(), "bg_level2.png")

print("\nAll assets generated successfully!")
