#!/usr/bin/env python3
"""
Car Racing Game — 10 Levels
Requires: Python 3.13+  |  pip install pygame
Run     : python3 game.py
"""
from __future__ import annotations
import sys, os, random, math
import pygame

if sys.version_info < (3, 13):
    print("Python 3.13+ required. You have:", sys.version); sys.exit(1)

pygame.init()

BASE   = os.path.dirname(os.path.abspath(__file__))
ASSETS = os.path.join(BASE, "assets")

WIDTH, HEIGHT = 400, 700
FPS           = 60
LANES         = [110, 190, 270]

# Colours
WHITE  = (255,255,255); BLACK  = (0,0,0)
YELLOW = (255,220,0);   RED    = (220,40,40)
GREEN  = (40,200,60);   CYAN   = (80,220,220)
ORANGE = (255,140,0);   PURPLE = (180,60,220)
GREY   = (120,120,120)

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Car Racing — 10 Levels")
clock  = pygame.time.Clock()

font_big = pygame.font.SysFont("Arial", 52, bold=True)
font_med = pygame.font.SysFont("Arial", 30, bold=True)
font_sm  = pygame.font.SysFont("Arial", 20)
font_xs  = pygame.font.SysFont("Arial", 15)

# ── loaders ───────────────────────────────────────────────────────────────────
def load_img(name, size=None):
    img = pygame.image.load(os.path.join(ASSETS, name)).convert_alpha()
    return pygame.transform.scale(img, size) if size else img

player_img = load_img("player_car.png", (54,100))
obstacle_img = load_img("obstacle.png", (46,46))
coin_img     = load_img("coin.png",     (28,28))

enemy_imgs = [
    load_img("enemy_car.png",  (54,100)),
    load_img("enemy_car2.png", (54,100)),
    load_img("enemy_car3.png", (54,100)),
    load_img("enemy_car4.png", (54,100)),
    load_img("enemy_car5.png", (54,100)),
    load_img("enemy_car6.png", (54,100)),
    load_img("enemy_car7.png", (54,100)),
    load_img("enemy_car8.png", (54,100)),
]

bg_imgs = [load_img(f"bg_level{i}.png", (WIDTH,HEIGHT)) for i in range(1,11)]

# ── level configs  ────────────────────────────────────────────────────────────
# (name, base_speed, n_enemies, score_goal, enemy_pool_indices, accent_color, hint)
LEVELS = [
    ("City Highway",       3.5, 1, 800,  [0,1],       CYAN,   "Watch out for rocks!"),
    ("Night Desert",       4.5, 2, 1200, [1,2],       ORANGE, "Two enemies — stay alert!"),
    ("Countryside",        5.0, 2, 1500, [0,2,3],     GREEN,  "Coins give +50 bonus!"),
    ("Snow Storm",         5.5, 3, 1800, [1,3,4],     WHITE,  "Icy road — 3 enemies!"),
    ("Sunset Boulevard",   6.0, 3, 2100, [2,4,5],     YELLOW, "Speed is increasing fast!"),
    ("Rainy Night City",   6.5, 4, 2500, [3,5,6],     PURPLE, "Poor visibility — 4 enemies!"),
    ("Mountain Pass",      7.0, 4, 2800, [4,6,7],     WHITE,  "Rough terrain ahead!"),
    ("Neon Tunnel",        7.5, 5, 3200, [5,6,7],     CYAN,   "5 enemies in tight tunnel!"),
    ("Dusk Bridge",        8.0, 5, 3600, [6,7,0],     ORANGE, "Nearly there — stay focused!"),
    ("Space Highway",      9.0, 6, 4000, [7,5,6,4],   PURPLE, "FINAL LEVEL — 6 enemies!"),
]

# ── helpers ───────────────────────────────────────────────────────────────────
def draw_center(surf, text, font, color, cy):
    s = font.render(text, True, color)
    surf.blit(s, (WIDTH//2 - s.get_width()//2, cy))

def draw_shadow(surf, text, font, color, shadow, cy):
    sh = font.render(text, True, shadow)
    tx = WIDTH//2 - sh.get_width()//2
    surf.blit(sh, (tx+2, cy+2))
    surf.blit(font.render(text, True, color), (tx, cy))

# ══════════════════════════════════════════════════════════════════════════════
# GAME OBJECTS
# ══════════════════════════════════════════════════════════════════════════════
class PlayerCar:
    W, H = 54, 100
    def __init__(self):
        self.lane = 1
        self.x = float(LANES[1] - self.W//2)
        self.y = float(HEIGHT - self.H - 20)
        self.hp = 3; self.invincible = 0
        self.rect = pygame.Rect(int(self.x), int(self.y), self.W, self.H)

    def move_left(self):
        if self.lane > 0: self.lane -= 1
    def move_right(self):
        if self.lane < 2: self.lane += 1

    def update(self):
        tx = float(LANES[self.lane] - self.W//2)
        self.x += (tx - self.x) * 0.18
        if self.invincible > 0: self.invincible -= 1
        self.rect.update(int(self.x), int(self.y), self.W, self.H)

    def draw(self, surf):
        if self.invincible > 0 and (self.invincible//5) % 2 == 0: return
        surf.blit(player_img, (int(self.x), int(self.y)))

    def hit(self):
        if self.invincible > 0: return
        self.hp -= 1; self.invincible = 90


class Obstacle:
    W, H = 46, 46
    def __init__(self, speed):
        self.lane = random.randint(0,2)
        self.x = float(LANES[self.lane] - self.W//2)
        self.y = float(-self.H); self.speed = speed
        self.rect = pygame.Rect(int(self.x), int(self.y), self.W, self.H)
    def update(self):
        self.y += self.speed
        self.rect.update(int(self.x), int(self.y), self.W, self.H)
    def draw(self, surf): surf.blit(obstacle_img, (int(self.x), int(self.y)))
    def off_screen(self): return self.y > HEIGHT + 10


class Coin:
    W, H = 28, 28
    def __init__(self, speed):
        self.lane = random.randint(0,2)
        self.x = float(LANES[self.lane] - self.W//2)
        self.y = float(-self.H); self.speed = speed
        self.rect = pygame.Rect(int(self.x), int(self.y), self.W, self.H)
    def update(self):
        self.y += self.speed
        self.rect.update(int(self.x), int(self.y), self.W, self.H)
    def draw(self, surf): surf.blit(coin_img, (int(self.x), int(self.y)))
    def off_screen(self): return self.y > HEIGHT + 10


class EnemyCar:
    W, H = 54, 100
    def __init__(self, speed, img):
        self.lane = random.randint(0,2)
        self.x = float(LANES[self.lane] - self.W//2)
        self.y = float(-self.H - random.randint(0,300))
        self.speed = speed; self.img = img
        self.change_timer = random.randint(60,180)
        self.rect = pygame.Rect(int(self.x), int(self.y), self.W, self.H)
    def update(self):
        self.y += self.speed
        self.change_timer -= 1
        if self.change_timer <= 0:
            self.lane = random.randint(0,2)
            self.change_timer = random.randint(60,180)
        self.x += (float(LANES[self.lane] - self.W//2) - self.x) * 0.10
        self.rect.update(int(self.x), int(self.y), self.W, self.H)
    def draw(self, surf): surf.blit(self.img, (int(self.x), int(self.y)))
    def off_screen(self): return self.y > HEIGHT + 10


class ScrollBG:
    def __init__(self, img, speed):
        self.img = img; self.speed = speed
        self.y1 = 0.0; self.y2 = float(-HEIGHT)
    def update(self):
        self.y1 += self.speed; self.y2 += self.speed
        if self.y1 >= HEIGHT: self.y1 = float(-HEIGHT)
        if self.y2 >= HEIGHT: self.y2 = float(-HEIGHT)
    def draw(self, surf):
        surf.blit(self.img, (0, int(self.y1)))
        surf.blit(self.img, (0, int(self.y2)))
    def set_speed(self, s): self.speed = s


# ── HUD ───────────────────────────────────────────────────────────────────────
def draw_hud(surf, score, coins, hp, level_num, score_goal, speed_kmh, accent):
    bar = pygame.Surface((WIDTH,48), pygame.SRCALPHA)
    bar.fill((0,0,0,165)); surf.blit(bar,(0,0))
    surf.blit(font_sm.render(f"Score: {score}", True, YELLOW), (10,12))
    surf.blit(coin_img, (160,12))
    surf.blit(font_sm.render(f"x{coins}", True, YELLOW), (192,12))
    surf.blit(font_sm.render(f"{speed_kmh}km/h", True, CYAN), (WIDTH-110,12))
    lv = font_xs.render(f"LV {level_num}/10", True, accent)
    surf.blit(lv, (WIDTH//2 - lv.get_width()//2, 14))
    # lives
    for i in range(hp):
        pygame.draw.circle(surf, RED, (10+i*22, HEIGHT-20), 8)
        pygame.draw.circle(surf, (255,100,100), (8+i*22, HEIGHT-22), 4)
    # progress bar
    pw = int((score/score_goal)*(WIDTH-20))
    pygame.draw.rect(surf,(50,50,50),(10,HEIGHT-40,WIDTH-20,10),border_radius=5)
    pygame.draw.rect(surf, accent, (10,HEIGHT-40,max(0,pw),10), border_radius=5)
    gt = font_xs.render(f"{score}/{score_goal}", True, WHITE)
    surf.blit(gt, (WIDTH//2 - gt.get_width()//2, HEIGHT-56))


# ══════════════════════════════════════════════════════════════════════════════
# LEVEL TRANSITION SCREEN
# ══════════════════════════════════════════════════════════════════════════════
def level_transition(surf, level_num, name, hint, accent):
    bg_surf = bg_imgs[level_num-1].copy()
    ov = pygame.Surface((WIDTH,HEIGHT), pygame.SRCALPHA)
    ov.fill((0,0,0,200)); bg_surf.blit(ov,(0,0))
    surf.blit(bg_surf,(0,0))
    draw_shadow(surf, f"LEVEL {level_num}", font_big, accent, BLACK, HEIGHT//2-100)
    draw_center(surf, name, font_med, WHITE, HEIGHT//2-30)
    draw_center(surf, hint, font_sm,  GREY,  HEIGHT//2+20)
    draw_center(surf, "Press ENTER to start", font_sm, YELLOW, HEIGHT//2+70)
    pygame.display.flip()
    while True:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT: pygame.quit(); sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN: return
                if event.key == pygame.K_ESCAPE: pygame.quit(); sys.exit()


# ══════════════════════════════════════════════════════════════════════════════
# RUN ONE LEVEL
# ══════════════════════════════════════════════════════════════════════════════
def run_level(level_num: int) -> str:
    """Returns: 'next' | 'dead' | 'quit' | 'restart'"""
    name, base_spd, n_enemies, goal, epool, accent, hint = LEVELS[level_num-1]
    level_transition(screen, level_num, name, hint, accent)

    bg        = ScrollBG(bg_imgs[level_num-1], base_spd)
    player    = PlayerCar()
    # level 5+ give player an extra life
    if level_num >= 5:  player.hp = 4
    if level_num >= 8:  player.hp = 5

    obstacles: list[Obstacle]  = []
    coins:     list[Coin]      = []

    def fresh_enemy():
        img = enemy_imgs[random.choice(epool)]
        spd = base_spd + random.uniform(0.3, 1.8 + level_num*0.1)
        return EnemyCar(spd, img)

    enemies: list[EnemyCar] = [fresh_enemy() for _ in range(n_enemies)]

    score = 0; coin_count = 0; frame = 0
    speed = base_spd; speed_inc = 0.001 + level_num*0.0005
    obs_interval  = max(35, 100 - level_num*5)
    coin_interval = 65
    game_over = False; won = False; end_timer = 0

    while True:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT: pygame.quit(); sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE: return "quit"
                if game_over:
                    if event.key == pygame.K_r: return "restart"
                    if event.key == pygame.K_RETURN and won: return "next"
                else:
                    if event.key in (pygame.K_LEFT,  pygame.K_a): player.move_left()
                    if event.key in (pygame.K_RIGHT, pygame.K_d): player.move_right()

        # ── logic ─────────────────────────────────────────────────────────────
        if not game_over:
            frame += 1; speed += speed_inc; score += 1
            bg.set_speed(speed); bg.update(); player.update()

            if frame % obs_interval == 0:
                obstacles.append(Obstacle(speed * 0.85))
            if frame % coin_interval == 0:
                coins.append(Coin(speed * 0.65))

            # extra enemy spawns as level progresses
            max_e = n_enemies + frame//(500 - level_num*20)
            while len(enemies) < max_e:
                enemies.append(fresh_enemy())

            for o in obstacles[:]:
                o.update()
                if o.off_screen(): obstacles.remove(o)
                elif player.rect.colliderect(o.rect):
                    player.hit(); obstacles.remove(o)

            for c in coins[:]:
                c.update()
                if c.off_screen(): coins.remove(c)
                elif player.rect.colliderect(c.rect):
                    coins.remove(c); coin_count += 1; score += 50

            for e in enemies[:]:
                e.update()
                if e.off_screen():
                    enemies.remove(e); enemies.append(fresh_enemy())
                elif player.rect.colliderect(e.rect):
                    player.hit()
                    e.lane = (e.lane + 1) % 3; e.change_timer = 45

            if player.hp <= 0: game_over = True; won = False; end_timer = 300
            if score >= goal:   game_over = True; won = True;  end_timer = 300
        else:
            bg.update(); end_timer -= 1

        # ── draw ──────────────────────────────────────────────────────────────
        bg.draw(screen)
        for o in obstacles: o.draw(screen)
        for c in coins:     c.draw(screen)
        for e in enemies:   e.draw(screen)
        player.draw(screen)

        speed_kmh = int(80 + (speed - base_spd) * 35)
        draw_hud(screen, score, coin_count, player.hp,
                 level_num, goal, speed_kmh, accent)

        if game_over:
            ov = pygame.Surface((WIDTH,HEIGHT), pygame.SRCALPHA)
            ov.fill((0,0,0,145)); screen.blit(ov,(0,0))
            if won:
                draw_shadow(screen, "Level Clear! 🏆", font_big, YELLOW, BLACK, HEIGHT//2-80)
                draw_center(screen, f"Score {score}  |  Coins {coin_count}", font_sm, WHITE, HEIGHT//2)
                if level_num < 10:
                    draw_center(screen, "ENTER = Next Level   R = Restart   ESC = Quit",
                                font_xs, GREY, HEIGHT//2+50)
                else:
                    draw_center(screen, "YOU BEAT ALL 10 LEVELS! 🎉", font_med, YELLOW, HEIGHT//2+55)
                    draw_center(screen, "R = Play Again   ESC = Quit", font_xs, GREY, HEIGHT//2+95)
            else:
                draw_shadow(screen, "GAME OVER", font_big, RED, BLACK, HEIGHT//2-80)
                draw_center(screen, f"Level {level_num} — Score {score}", font_sm, WHITE, HEIGHT//2)
                draw_center(screen, "R = Retry from Level 1   ESC = Quit",
                            font_xs, GREY, HEIGHT//2+50)

        pygame.display.flip()


# ══════════════════════════════════════════════════════════════════════════════
# TITLE SCREEN
# ══════════════════════════════════════════════════════════════════════════════
def title_screen():
    bg = ScrollBG(bg_imgs[0], 2.5)
    timer = 0
    scroll_y = 0

    # build level list surface
    list_surf = pygame.Surface((WIDTH-40, 10*36+10), pygame.SRCALPHA)
    for i,(name,_,ne,goal,_,col,_) in enumerate(LEVELS):
        y = i*36
        row = pygame.Surface((WIDTH-40, 32), pygame.SRCALPHA)
        row.fill((0,0,0,140))
        list_surf.blit(row,(0,y))
        t = font_xs.render(f"Lv{i+1:02d}  {name:<20} enemies:{ne}  goal:{goal}", True, col)
        list_surf.blit(t,(8, y+8))

    while True:
        clock.tick(FPS); timer += 1
        scroll_y = (scroll_y + 0.4) % (10*36+10)

        for event in pygame.event.get():
            if event.type == pygame.QUIT: pygame.quit(); sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN: return
                if event.key == pygame.K_ESCAPE: pygame.quit(); sys.exit()

        bg.update(); bg.draw(screen)
        ov = pygame.Surface((WIDTH,HEIGHT),pygame.SRCALPHA)
        ov.fill((0,0,0,175)); screen.blit(ov,(0,0))

        draw_shadow(screen, "CAR RACING",   font_big, YELLOW, BLACK, 55)
        draw_shadow(screen, "10 LEVELS",    font_med, CYAN,   BLACK, 120)

        # scrolling level list
        clip = pygame.Surface((WIDTH-40, 180), pygame.SRCALPHA)
        clip.blit(list_surf, (0, -int(scroll_y)))
        if scroll_y > (10*36+10)-180:
            clip.blit(list_surf,(0, (10*36+10)-int(scroll_y)))
        screen.blit(clip,(20,165))

        controls = ["← →  /  A D  —  Change Lane",
                    "Reach score goal  →  next level",
                    "Collect 💰 coins for +50 bonus",
                    "","ENTER to Start   |   ESC to Quit"]
        for i,line in enumerate(controls):
            col = YELLOW if i==len(controls)-1 else (210,210,210)
            t = font_xs.render(line, True, col)
            screen.blit(t,(WIDTH//2-t.get_width()//2, 365+i*25))

        pulse = int(abs(math.sin(timer*0.05))*10)
        screen.blit(player_img,(WIDTH//2-27, HEIGHT-160-pulse))
        if (timer//30)%2==0:
            t = font_sm.render("Press ENTER", True, WHITE)
            screen.blit(t,(WIDTH//2-t.get_width()//2, HEIGHT-55))

        pygame.display.flip()


# ══════════════════════════════════════════════════════════════════════════════
# MAIN
# ══════════════════════════════════════════════════════════════════════════════
def main():
    title_screen()
    level = 1
    while True:
        result = run_level(level)
        match result:
            case "quit":    break
            case "restart": level = 1
            case "dead":    level = 1
            case "next":
                if level < 10:
                    level += 1
                else:
                    # Victory screen
                    screen.fill(BLACK)
                    draw_shadow(screen,"ALL LEVELS COMPLETE!",font_big,YELLOW,BLACK,150)
                    draw_center(screen,"You are the ultimate racer 🏆",font_med,WHITE,230)
                    draw_center(screen,"R = Play Again   ESC = Quit",font_sm,GREY,310)
                    pygame.display.flip()
                    done = False
                    while not done:
                        clock.tick(FPS)
                        for e in pygame.event.get():
                            if e.type==pygame.QUIT: done=True; result="quit"
                            if e.type==pygame.KEYDOWN:
                                if e.key==pygame.K_r: level=1; done=True
                                if e.key==pygame.K_ESCAPE: done=True; result="quit"
                    if result=="quit": break

    pygame.quit(); sys.exit()

if __name__=="__main__":
    main()
