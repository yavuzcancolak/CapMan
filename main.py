# Gerekli kütüphaneleri yüklüyoruz
import pgzrun
import random
import sys
from pgzero.actor import Actor
from pgzero.keyboard import keyboard, keys
from pgzero.clock import schedule, schedule_interval

# ------------------------------
# EKRAN AYARLARI
# ------------------------------
WIDTH = 800
HEIGHT = 600

# ------------------------------
# OYUN DURUM DEĞİŞKENLERİ
# ------------------------------
menu_active = True          # Menü açık mı?
sound_on = True             # Ses açık mı?
player_visible = False      # Oyuncu görünüyor mu?
game_over = False           # Oyun bitti mi?
game_over_blink = True      # GAME OVER yazısı yanıp sönüyor mu?
restart_button_active = False  # Restart butonu aktif mi?

# ------------------------------
# ARKA PLAN VE BUTONLAR
# ------------------------------
background = Actor("background")

button_start = Actor("button_blue", center=(WIDTH // 2, 240))
button_volume = Actor("button_white", center=(WIDTH // 2, 350))
button_exit = Actor("button_white", center=(WIDTH // 2, 420))
button_restart = Actor("button_white", center=(WIDTH // 2, 400))

# ------------------------------
# PLAYER SINIFI
# Oyuncunun özelliklerini ve hareketlerini tanımlar
# ------------------------------
class Player:
    def __init__(self):
        self.images = {
            "idle": "player_idle",
            "left": ["player_left_01", "player_left_02", "player_left_03"],
            "right": ["player_right_01", "player_right_02", "player_right_03"]
        }
        self.pos = [WIDTH // 2, HEIGHT - 140]
        self.state = "idle"
        self.frame = 0
        self.can_shoot = True
        self.projectiles = []  # Oyuncudan çıkan mermiler

    def draw(self):
        # Oyuncuyu ekrana çizer
        if self.state == "idle":
            image = self.images["idle"]
        else:
            image = self.images[self.state][self.frame]
        player_actor = Actor(image, center=self.pos)
        player_actor.draw()

    def update(self):
        # Oyuncunun sağa sola hareketi
        if keyboard.right:
            self.state = "right"
            self.pos[0] += 3
        elif keyboard.left:
            self.state = "left"
            self.pos[0] -= 3
        else:
            self.state = "idle"

        # Sadece hareket ederken ateş edebilir
        if keyboard.space and self.can_shoot and self.state in ["left", "right"]:
            self.shoot()

        # Mermileri hareket ettir
        for p in self.projectiles:
            p.actor.x += 8 * p.dir

        # Ekran dışına çıkan mermileri sil
        self.projectiles = [p for p in self.projectiles if 0 <= p.actor.x <= WIDTH]

    def shoot(self):
        # Yeni mermi oluştur
        new_proj = Projectile(self.pos[0], self.pos[1] + 15, 1 if self.state == "right" else -1)
        self.projectiles.append(new_proj)
        self.can_shoot = False

# ------------------------------
# PROJECTILE SINIFI
# Oyuncudan çıkan mermileri temsil eder
# ------------------------------
class Projectile:
    def __init__(self, x, y, direction):
        self.actor = Actor("projectile", center=(x, y))
        self.dir = direction

# ------------------------------
# ENEMY SINIFI
# Düşmanları tanımlar ve hareket ettirir
# ------------------------------
class Enemy:
    def __init__(self, enemy_type, direction):
        self.type = enemy_type
        self.direction = direction
        self.images = self.load_images()
        self.actor = Actor(self.images[0])

        # Düşmanın başlangıç pozisyonu
        if direction == "left":
            self.actor.pos = (WIDTH + 50, HEIGHT - 140)
            self.speed = -2
        else:
            self.actor.pos = (-50, HEIGHT - 140)
            self.speed = 2

        self.frame = 0
        self.health = 8 if enemy_type == "strong" else 5  # Güçlü düşman 8, zayıf düşman 5 can

    def load_images(self):
        # Düşman için resimleri yükle
        return [f"tank_{self.type}_{self.direction}_1", f"tank_{self.type}_{self.direction}_2"]

    def draw(self):
        self.actor.image = self.images[self.frame]
        self.actor.draw()

    def update(self):
        # Düşmanı hareket ettir
        self.actor.x += self.speed

    def animate(self):
        # Düşmanın animasyon karesini değiştir
        self.frame = (self.frame + 1) % 2

# ------------------------------
# NESNELERİ OLUŞTUR
# ------------------------------
player = Player()
enemies = []

# ------------------------------
# ÇİZİM FONKSİYONLARI
# ------------------------------
def draw():
    screen.clear()
    background.draw()

    if menu_active:
        draw_menu()
    elif game_over:
        if game_over_blink:
            screen.draw.text("GAME OVER", center=(WIDTH//2, HEIGHT//2 - 50), fontsize=64, color="red")
        button_restart.draw()
        screen.draw.text("Start Again", center=button_restart.center, fontsize=32, color="black")
    else:
        player.draw()
        for p in player.projectiles:
            p.actor.draw()
        for e in enemies:
            e.draw()

def draw_menu():
    screen.draw.text("CapMan", center=(WIDTH // 2, 100), fontsize=64, color="orange")
    button_start.draw()
    button_volume.draw()
    button_exit.draw()
    screen.draw.text("Start Game", center=button_start.center, fontsize=32, color="white")
    volume_text = "Volume: On" if sound_on else "Volume: Off"
    screen.draw.text(volume_text, center=button_volume.center, fontsize=28, color="black")
    screen.draw.text("Exit Game", center=button_exit.center, fontsize=28, color="black")

# ------------------------------
# GÜNCELLEME FONKSİYONLARI
# ------------------------------
def update():
    if not menu_active and not game_over:
        player.update()
        for e in enemies:
            e.update()
        check_collisions()

def check_collisions():
    global game_over

    # Oyuncu ile düşman çarpışmasını kontrol et
    player_actor = Actor(player.images["idle"], center=player.pos)
    for e in enemies:
        if player_actor.colliderect(e.actor):
            trigger_game_over()

    # Mermi ile düşman çarpışmasını kontrol et
    for e in enemies:
        for proj in player.projectiles:
            if proj.actor.colliderect(e.actor):
                e.health -= 1
                if proj in player.projectiles:
                    player.projectiles.remove(proj)

    # Canı biten düşmanları listeden çıkar
    enemies[:] = [e for e in enemies if e.health > 0]

# ------------------------------
# OYUN MEKANİKLERİ
# ------------------------------
def spawn_enemy():
    # Yeni düşman oluştur
    enemy_type = random.choice(["strong", "weak"])
    direction = random.choice(["left", "right"])
    enemy = Enemy(enemy_type, direction)
    enemies.append(enemy)

def animate_enemies():
    # Düşman animasyonlarını çalıştır
    for e in enemies:
        e.animate()

def toggle_game_over_blink():
    # GAME OVER yazısını yanıp söndür
    global game_over_blink
    game_over_blink = not game_over_blink

def trigger_game_over():
    # Oyunu bitir
    global game_over, player_visible, enemies, restart_button_active
    game_over = True
    player_visible = False
    restart_button_active = True
    enemies.clear()
    if sound_on:
        sounds.game_music.stop()
        sounds.game_over.play()
    schedule_interval(toggle_game_over_blink, 0.8)

# ------------------------------
# OYUNU YENİDEN BAŞLAT
# ------------------------------
def delayed_restart():
    global game_over, player_visible, restart_button_active, player, enemies
    game_over = False
    player_visible = True
    restart_button_active = False
    player = Player()
    enemies = []
    if sound_on:
        sounds.game_music.play()

# ------------------------------
# OYUNDAN ÇIKIŞ
# ------------------------------
def delayed_exit():
    sys.exit()

# ------------------------------
# MOUSE TIKLAMASI
# ------------------------------
def on_mouse_down(pos):
    global menu_active, player_visible, sound_on
    if menu_active:
        if button_start.collidepoint(pos):
            if sound_on:
                sounds.game_start.play()
                sounds.game_music.play()
            menu_active = False
            player_visible = True
        elif button_volume.collidepoint(pos):
            if sound_on:
                sounds.click.play()
            sound_on = not sound_on
        elif button_exit.collidepoint(pos):
            if sound_on:
                sounds.click.play()
            schedule(delayed_exit, 1.0)
    elif game_over:
        if button_restart.collidepoint(pos):
            if sound_on:
                sounds.click.play()
            schedule(delayed_restart, 1.0)

# ------------------------------
# KLAVYE TUŞU BIRAKMA
# ------------------------------
def on_key_up(key):
    if key == keys.SPACE:
        player.can_shoot = True

# ------------------------------
# ANİMASYONLARI ÇALIŞTIR
# ------------------------------
def animate_player():
    if not menu_active and player_visible and not game_over:
        if player.state in ["left", "right"]:
            player.frame = (player.frame + 1) % 3
        else:
            player.frame = 0

# ------------------------------
# TAKVİMLER (Periyodik İşler)
# ------------------------------
schedule_interval(spawn_enemy, 2.5)
schedule_interval(animate_enemies, 0.3)
schedule_interval(animate_player, 0.1)

# ------------------------------
# OYUNU BAŞLAT
# ------------------------------
pgzrun.go()
