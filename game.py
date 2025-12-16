import pygame
import random
import math

pygame.init()

screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Mon premier jeu")

clock = pygame.time.Clock()

def draw_button(rect, text):
    pygame.draw.rect(screen, (30,30,30), rect)
    if rect.collidepoint(mouse_pos):
        pygame.draw.rect(screen, (255,255,255), rect, 3)
    else:
        pygame.draw.rect(screen, (120,120,120), rect, 2)

    label = font.render(text, True, (255,255,255))
    screen.blit(
        label,
        (
         rect.centerx - label.get_width() // 2,
         rect.centery - label.get_height() // 2
        ) 
    )        

def draw_health_bar(x, y, w, h, hp, hp_max):
    pygame.draw.rect(screen, (20, 20, 20), (x, y, w, h), border_radius=6)
    pygame.draw.rect(screen, (120, 120, 120), (x, y, w, h), 2, border_radius=6)
    ratio = max(0, min(1, hp/ hp_max))
    fill_w = int((w - 4) * ratio)
    pygame.draw.rect(screen, (200, 40, 40), (x + 2, y + 2, fill_w, h - 4), border_radius=6)

def draw_bar(x, y, w, h, val, val_max, color):
    pygame.draw.rect(screen, (20, 20, 20), (x, y, w, h), border_radius=6)
    pygame.draw.rect(screen, (120, 120, 120), (x, y, w, h), 2, border_radius=6)
    ratio = max(0, min(1, val / val_max))
    fill_w = int((w - 4) * ratio)
    pygame.draw.rect(screen, color, (x + 2, y + 2, fill_w, h - 4), border_radius=6)

def draw_cooldown_bar(x, y, w, h, last_time, cooldown_ms):
    pygame.draw.rect(screen, (20, 20, 20), (x, y, w, h), border_radius=6)
    pygame.draw.rect(screen, (120, 120, 120), (x, y, w, h), 2, border_radius=6)
    now = pygame.time.get_ticks()
    ratio = (now - last_time) / cooldown_ms
    ratio = max(0, min(1, ratio))
    fill_w = int((w - 4) * ratio)
    pygame.draw.rect(screen, (60, 120, 255), (x + 2, y + 2, fill_w, h - 4), border_radius=6)

def angle_diff(a, b):
    d = (a - b + math.pi) % (2 * math.pi) - math.pi
    return abs(d)

def spawn_enemy():
   
    min_dist = 220
    px = x + size // 2
    py = y + size // 2

    for _ in range(20): 
        side = random.choice (["top", "bottom", "left", "right"])
        if side == "top":
            ex, ey = random.randint(0, W - enemy_size), -enemy_size
        elif side == "bottom":
            ex, ey = random.randint(0, W - enemy_size), H + enemy_size
        elif side == "left":
            ex, ey = -enemy_size, random.randint(0, H - enemy_size)
        else:
            ex, ey = W + enemy_size, random.randint(0, H - enemy_size)

        ex_c = ex + enemy_size // 2
        ey_c = ey + enemy_size // 2
        dist = ((px -ex_c) ** 2 + (py - ey_c) ** 2) ** 0.5    
    
        if dist >= min_dist:
            enemies.append({
                "x": ex,
                "y": ey,
                "hp": enemy_hp_max,
                "hp_max": enemy_hp_max,
                "alive": True
            })    
            return

font = pygame.font.Font(None, 48)
small_font = pygame.font.Font(None, 28)
x = 400
y = 300
speed = 3
size = 50

W, H = 800, 600

btn_w, btn_h = 260, 60
btn_x = (W - btn_w) // 2

btn_play = pygame.Rect(btn_x, 220, btn_w, btn_h)
btn_options = pygame.Rect(btn_x, 300, btn_w, btn_h)
btn_quit = pygame.Rect(btn_x, 380, btn_w, btn_h)
btn_back = pygame.Rect(30, 30, 160, 50)

cube_color = (255, 255, 255)

colors = [
    ((255, 255, 255), pygame.Rect(220, 300, 60, 60)),
    ((255, 60, 60), pygame.Rect(320, 300, 60, 60)),
    ((60, 255, 60), pygame.Rect(420, 300, 60, 60)),
    ((60, 60, 255), pygame.Rect(520, 300, 60, 60)),
]

player_hp = 100
player_hp_max = 100
player_dmg = 25

attack_cooldown_ms = 350
last_attack_time = 0
attack_range = 180
attack_effects = []
attack_ready = True
attack_cone = 0.9

stamina = 100
stamina_max = 100

stamina_regen_per_sec = 22
dash_cost = 35
dash_speed = 10
dash_duration_ms = 130

dash_end_time = 0
dash_vx = 0.0
dash_vy = 0.0

enemies = []
enemy_size = 40
enemy_hp_max = 60
enemy_dmg = 10

spawn_cooldown_ms = 1200
last_spawn_time = 0
max_enemies = 6


mode = "menu"

running = True
while running:
    mouse_pos = pygame.mouse.get_pos()
    dt = clock.get_time() / 1000
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if mode == "menu":
                if btn_play.collidepoint(event.pos):
                    mode = "game"
                elif btn_options.collidepoint(event.pos):
                    mode = "options"
                elif btn_quit.collidepoint(event.pos):
                    running = False 
                
            elif mode == "options":
                if btn_back.collidepoint(event.pos):
                    mode = "menu"
                else:
                    for col, rect in colors:
                        if rect.collidepoint(event.pos):
                            cube_color = col    
                
            elif mode == "game":
                now = pygame.time.get_ticks()
                if now - last_attack_time >= attack_cooldown_ms:
                    last_attack_time = now
                    px = x + size // 2
                    py = y + size // 2
                    
                    target_angle = 0.0
                    
                    mx, my = event.pos
                    px = x + size // 2
                    py = y + size // 2
                    target_angle = math.atan2(my - py, mx - px)

                    attack_effects.append({
                        "t": now,
                        "duration": 140,
                        "cx": px,
                        "cy": py,
                       "angle": target_angle
                    })
                    
                    px = x + size // 2
                    py = y + size // 2
                    for e in enemies:
                        if not e["alive"]:
                            continue
                        ex = e["x"] + enemy_size // 2
                        ey = e["y"] + enemy_size // 2

                        dx = ex - px
                        dy = ey - py
                        dist = (dx*dx + dy*dy) ** 0.5
                        
                        if dist <= attack_range:
                            enemy_angle = math.atan2(dy, dx)

                            if angle_diff(enemy_angle, target_angle) <= attack_cone:
                                e["hp"] -= player_dmg
                                if e["hp"] <= 0:
                                    e["alive"] = False
                          
    if event.type ==pygame.KEYDOWN:
        if event.key == pygame.K_RETURN:
            if mode == "menu":
                mode = "game"
            elif mode == "gameover":
                player_hp = player_hp_max
                enemies.clear()
                attack_effects.clear()
                x, y = 400, 300
                mode = "game"

        elif event.key == pygame.K_ESCAPE:
            if mode == "gameover":
                mode = "menu"
            elif mode in ("game", "options"):
                mode = "menu"
            else:
                running = False
    
        elif event.key == pygame.K_e and mode == "game":
            now = pygame.time.get_ticks()

        if stamina >= dash_cost and now >= dash_end_time:
            stamina -= dash_cost

            keys = pygame.key.get_pressed()
            dx = 0
            dy = 0
            if keys[pygame.K_q] or keys[pygame.K_LEFT]:
                dx -= 1
            if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
                dx += 1
            if keys[pygame.K_z] or keys[pygame.K_UP]:
                dy -= 1
            if keys[pygame.K_s] or keys[pygame.K_DOWN]:
                dy += 1

            if dx == 0 and dy == 0:
                mx, my = pygame.mouse.get_pos()
                px = x + size // 2
                py = y + size // 2
                dx = mx - px
                dy = my - py

            dist = (dx*dx + dy*dy) ** 0.5
            if dist != 0:
                dash_vx = (dx / dist) * dash_speed
                dash_vy = (dy / dist) * dash_speed
            else:
                dash_vx = dash_vy = 0

            dash_end_time = now + dash_duration_ms                          

            if mode == "game":
                now = pygame.time.get_ticks()

                if now < dash_end_time:
                    x += dash_vx
                    y += dash_vy
            else:
                keys = pygame.key.get_pressed()
                if keys[pygame.K_LEFT] or keys[pygame.K_q]:
                    x -= speed
                if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
                    x += speed
                if keys[pygame.K_UP] or keys[pygame.K_z]:
                    y -= speed
                if keys[pygame.K_DOWN] or keys[pygame.K_s]:
                    y += speed
    
            if x < 0:
                x = 0
            if x > 800 - size:
                x = 800 - size
            if y < 0:                                   
                y = 0
            if y > 600 - size:
                y = 600 - size
            stamina = min(stamina_max, stamina + stamina_regen_per_sec * dt)
    
    
    screen.fill((0, 0, 0))
    
    if mode == "menu":
       title = font.render("The Slasher", True, (255, 255, 255))
       screen.blit(
           title,
           (W // 2 - title.get_width() // 2, 120)
       ) 
       draw_button(btn_play, "Jouer")
       draw_button(btn_options, "Options")
       draw_button(btn_quit, "Quitter")
    elif mode == "options":
        title = font.render("Options", True, (255, 255, 255))
        screen.blit(
            title,
            (W // 2 - title.get_width() // 2, 100)
        )
        for col, rect in colors :
            pygame.draw.rect(screen, col, rect)
            if rect.collidepoint(mouse_pos):
                pygame.draw.rect(screen, (255, 255, 255), rect, 3)
            if col == cube_color:
                pygame.draw.rect(screen, (255, 255, 255), rect.inflate(8, 8), 2)
        draw_button(btn_back, "Retour")        
    elif mode == "game":
        pygame.draw.rect(screen, cube_color, (x, y, size, size))

        now = pygame.time.get_ticks()

        alive_count = 0
        for e in enemies:
            if e["alive"]:
                alive_count += 1

        if now - last_spawn_time >= spawn_cooldown_ms and alive_count < max_enemies:
            last_spawn_time = now
            spawn_enemy()

        px = x + size // 2
        py = y + size // 2
        player_rect = pygame.Rect(x, y, size, size)

        for e in enemies:
            if not e["alive"]:
                continue

            ex = e["x"] + enemy_size // 2
            ey = e["y"] + enemy_size // 2

            dx = px - ex
            dy = py - ey
            dist = (dx*dx + dy*dy) ** 0.5

            if dist != 0:
                vx = dx / dist
                vy = dy / dist
            else:
                vx = vy = 0

            e["x"] += vx * 1.6
            e["y"] += vy * 1.6

            enemy_rect = pygame.Rect(int(e["x"]), int(e["y"]), enemy_size, enemy_size)
            if player_rect.colliderect(enemy_rect):
                player_hp -= 0.35
                if player_hp <= 0:
                    player_hp = 0
                    mode = "gameover"

            pygame.draw.rect(screen, (180, 180, 180), (int(e["x"]), int(e["y"]), enemy_size, enemy_size))
            draw_health_bar(int(e["x"]), int(e["y"]) - 12, enemy_size, 8, e["hp"], e["hp_max"])
            draw_cooldown_bar(20, 58, 300, 10, last_attack_time, attack_cooldown_ms)
            draw_bar(20, 42, 300, 12, stamina, stamina_max, (60, 220, 80))

        for eff in attack_effects[:]:
            age = now - eff["t"]
            if age > eff["duration"]:
                attack_effects.remove(eff)
                continue

            cx, cy = eff["cx"], eff["cy"]
            radius = 55 + age * 0.15
            base = eff.get("angle", 0.0)
            arc = 1.0
            start_angle = base - arc
            end_angle = base + arc
            steps = 18

            points = []
            for i in range(steps + 1):
                a = start_angle + (end_angle - start_angle) * (i / steps)
                px2 = cx + math.cos(a) * radius
                py2 = cy + math.sin(a) * radius
                points.append((px2, py2))

            pygame.draw.lines(screen, (220, 220, 255), False, points, 6)
            pygame.draw.lines(screen, (120, 120, 200), False, points, 2)

        draw_health_bar(20, 20, 300, 18, player_hp, player_hp_max)

    elif mode == "gameover":
        screen.fill((0, 0, 0))
        title = font.render("GAME OVER", True, (200, 40, 40))
        hint = small_font.render("ENTRÉE = recommencer | ÉCHAP = menu", True, (200, 200, 200))
        screen.blit(title, (W//2 - title.get_width()//2, 220))
        screen.blit(hint, (W//2 - hint.get_width()//2, 280))    

    pygame.display.flip()
    clock.tick(60)
pygame.quit()
