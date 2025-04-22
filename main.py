import pgzrun
from pgzero.builtins import Actor
from pgzero.clock import schedule, schedule_interval
import random

# ------------------------------
# EKRAN AYARLARI
# ------------------------------
WIDTH = 800
HEIGHT = 600

# ------------------------------
# OYUN DURUM DEĞİŞKENLERİ
# ------------------------------
menu_active = True           # Ana menü açık mı?
sound_on = True              # Ses açık mı?
sounds_enabled = True        # Ses sistemi aktif mi?
player_visible = False       # Oyuncu görünüyor mu?
game_over = False            # Oyun bitti mi?
game_over_blink = True       # GAME OVER yazısı yanıp sönme durumu

# ------------------------------
# ARKA PLAN VE BUTONLAR
# ------------------------------
background = Actor("background")
button_start = Actor("button_blue", center=(WIDTH // 2, 240))
button_volume = Actor("button_white", center=(WIDTH // 2, 350))
button_exit = Actor("button_white", center=(WIDTH // 2, 420))

# ------------------------------
# OYUNCU AYARLARI
# ------------------------------
player_pos = [WIDTH // 2, HEIGHT - 140]  # Başlangıç konumu
player_state = "idle"                    # 'idle', 'left', 'right'
player_frame = 0                         # Animasyon karesi
can_shoot = True                         # Tek seferlik atış kontrolü
projectiles = []                         # Oyuncudan çıkan taşlar

# Oyuncu görselleri
player_images = {
    "idle": "player_idle",
    "right": ["player_right_01", "player_right_02", "player_right_03"],
    "left": ["player_left_01", "player_left_02", "player_left_03"]
}

# ------------------------------
# DÜŞMAN TANKLAR
# ------------------------------
tanks = []

# ------------------------------
# ÇİZİM FONKSİYONLARI
# ------------------------------
def draw():
    screen.clear()
    background.draw()

    if menu_active:
        draw_menu()
    else:
        if player_visible and not game_over:
            draw_player()
            for p in projectiles:
                p["actor"].draw()
            for tank in tanks:
                tank["actor"].draw()
        elif game_over and game_over_blink:
            screen.draw.text("GAME OVER", center=(WIDTH // 2, HEIGHT // 2), fontsize=64, color="red", owidth=1.0, ocolor="black")

def draw_menu():
    screen.draw.text("CapMan", center=(WIDTH // 2, 100), fontsize=64, color="orange", owidth=1.0, ocolor="black")
    button_start.draw()
    button_volume.draw()
    button_exit.draw()
    screen.draw.text("Start Game", center=button_start.center, fontsize=32, color="white")
    volume_text = "Volume: On" if sound_on else "Volume: Off"
    screen.draw.text(volume_text, center=button_volume.center, fontsize=28, color="black")
    screen.draw.text("Exit Game", center=button_exit.center, fontsize=28, color="black")

# ------------------------------
# MENÜ BUTON TIKLAMA OLAYLARI
# ------------------------------
def on_mouse_down(pos):
    global menu_active, sound_on, player_visible
    if button_start.collidepoint(pos):
        if sounds_enabled: sounds.game_start.play()
        schedule(start_game_music, 1.0)           # 1 sn sonra oyun müziği başlasın
        schedule_interval(spawn_tank, 2.5)        # Her 2.5 sn'de yeni tank gelsin
        menu_active = False
        player_visible = True
    elif button_volume.collidepoint(pos):
        sound_on = not sound_on
        if sounds_enabled: sounds.click.play()
        if not sound_on: sounds.game_music.stop()
    elif button_exit.collidepoint(pos):
        if sounds_enabled: sounds.click.play()
        quit()

# ------------------------------
# MÜZİK KONTROLÜ
# ------------------------------
def start_game_music():
    if sounds_enabled and sound_on:
        sounds.game_music.play()

# ------------------------------
# OYUNCU ÇİZİMİ
# ------------------------------
def draw_player():
    current_image = player_images["idle"] if player_state == "idle" else player_images[player_state][player_frame]
    player = Actor(current_image, center=player_pos)
    player.draw()

# ------------------------------
# GÜNCELLEME FONKSİYONU
# ------------------------------
def update():
    global player_state, player_frame, can_shoot, game_over, projectiles

    if not menu_active and player_visible and not game_over:
        # Karakter hareketi
        if keyboard.right:
            player_state = "right"
            player_pos[0] += 3
        elif keyboard.left:
            player_state = "left"
            player_pos[0] -= 3
        else:
            player_state = "idle"

        # Taş fırlatma
        if keyboard.space and can_shoot:
            direction = 1 if player_state == "right" else -1
            new_projectile = {
                "actor": Actor("projectile", pos=(player_pos[0], player_pos[1] + 15)),
                "dir": direction
            }
            projectiles.append(new_projectile)
            can_shoot = False

        # Taşları hareket ettir
        for p in projectiles:
            p["actor"].x += 8 * p["dir"]

        # Taşları sınır dışı kontrolü
        projectiles = [p for p in projectiles if 0 <= p["actor"].x <= WIDTH]

        # Tankları hareket ettir
        for tank in tanks:
            tank["actor"].x += tank["dir"]

        # Taş - tank çarpışması
        for tank in tanks:
            for p in projectiles:
                if p["actor"].colliderect(tank["actor"]):
                    tank["health"] -= 1
                    projectiles.remove(p)
                    break

        # Canı kalmayan tankları sil
        tanks[:] = [t for t in tanks if t["health"] > 0]

        # Tank - oyuncu çarpışması
        player_rect = Actor(player_images["idle"], center=player_pos)
        for tank in tanks:
            if player_rect.colliderect(tank["actor"]):
                trigger_game_over()

# SPACE tuşunu bırakınca yeniden atış yapabilsin

def on_key_up(key):
    global can_shoot
    if key == keys.SPACE:
        can_shoot = True

# ------------------------------
# OYUNCU ANİMASYONU
# ------------------------------
def animate_player():
    global player_frame
    if player_state in ["left", "right"]:
        player_frame = (player_frame + 1) % 3
    else:
        player_frame = 0

# ------------------------------
# TANK ÜRETİMİ
# ------------------------------
def spawn_tank():
    if menu_active or not player_visible or game_over:
        return
    direction = random.choice(["left", "right"])
    tank_type = random.choice(["weak", "strong"])
    image_name = f"tank_{tank_type}_{direction}"
    y = HEIGHT - 140
    x = -50 if direction == "right" else WIDTH + 50
    velocity = 2 if direction == "right" else -2
    health = 5 if tank_type == "weak" else 10
    tank = {
        "actor": Actor(image_name, (x, y)),
        "dir": velocity,
        "health": health
    }
    tanks.append(tank)

# ------------------------------
# GAME OVER
# ------------------------------
def trigger_game_over():
    global game_over, tanks, projectiles, player_visible
    game_over = True
    player_visible = False
    tanks.clear()
    projectiles.clear()
    if sounds_enabled and sound_on:
        sounds.game_music.stop()
        sounds.game_over.play()
    schedule_interval(toggle_game_over_blink, 0.5)

def toggle_game_over_blink():
    global game_over_blink
    game_over_blink = not game_over_blink

# ------------------------------
schedule_interval(animate_player, 0.2)
pgzrun.go()
