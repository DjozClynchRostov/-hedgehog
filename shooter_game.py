from pygame import *
from random import randint
from time import sleep, time as timer
init()
mixer.init()

WIDTH = 700
HEIGHT = 500
FPS = 60

font.init()
font2 = font.Font(None, 70)

win = font2.render("YOU WIN", True, (230,120,46))
lose = font2.render("YOU LOSE", True, (230,120,46))
fire_sound = mixer.Sound('fire.ogg')

lost = 0
score = 0
#картинки:
img_back = "galaxy.jpg" #фон игры
img_hero = "rocket.png" #герой
img_enemy = "kakashka.png" # враг
img_bullet = 'bullet.png' #пуля
img_asteroid = "asteroid.png"
class GameSprite(sprite.Sprite):
    def __init__(self, player_image, player_x, player_y, player_speed):
        super().__init__()
        self.image = transform.scale(image.load(player_image),(65,65)).convert_alpha() 
        self.speed = player_speed 
        self.rect = self.image.get_rect() 
        self.rect.x = player_x
        self.rect.y = player_y
    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

class Player(GameSprite):
    def update(self):
        keys_pressed = key.get_pressed()
        if (keys_pressed[K_UP] or keys_pressed[K_w]) and self.rect.y > 5:
            self.rect.y -= self.speed
        if (keys_pressed[K_DOWN] or keys_pressed[K_s]) and self.rect.y < 450:
            self.rect.y += self.speed
        if (keys_pressed[K_LEFT] or keys_pressed[K_a]) and self.rect.x > 5:
            self.rect.x -= self.speed
        if (keys_pressed[K_RIGHT] or keys_pressed[K_d]) and self.rect.x < 595:
            self.rect.x += self.speed
    def fire(self):
        bullet = Bullet(img_bullet, self.rect.centerx, self.rect.top, -15)
        bullets.add(bullet)

class Enemy(GameSprite):
    def update(self):
        global lost
        self.rect.y += self.speed
        if self.rect.y > HEIGHT:
            self.rect.x = randint(80, WIDTH - 80)
            self.rect.y = 0
            lost = lost + 1

class Bullet(GameSprite):
    def __init__(self, player_image, player_x, player_y, player_speed):
        super().__init__(player_image, player_x, player_y, player_speed)
        self.image = transform.scale(image.load(player_image), (15,15))
    def update(self):
        self.rect.y += self.speed
        if self.rect.y < 0:
            self.kill()

window = display.set_mode((WIDTH, HEIGHT))
display.set_caption("MAZE")
bg = transform.scale(image.load("cosmos.jpg"), (WIDTH, HEIGHT)) 
clock = time.Clock()

player = Player('Toilet.png', 5, HEIGHT-80, 5) 

mixer.music.load('space.ogg')
#mixer.music.play()

monsters = sprite.Group()
for i in range(1, 6):
    monster = Enemy(img_enemy, randint(80, WIDTH - 80), -40, randint(1, 3))
    monsters.add(monster)
asteroids = sprite.Group()
for i in range(3):
    asteroid = Enemy(img_asteroid, randint(80, WIDTH - 80), -40, randint(1, 7))
    asteroids.add(asteroid)
bullets = sprite.Group()
fire = mixer.Sound('fire.ogg')
rel_time =False
num_fire = 0
game = True
finish = False

while game:
    for e in event.get():
      if e.type == QUIT:
          game = False
      elif e.type == KEYDOWN:
          if e.key == K_SPACE:
              if num_fire < 5 and rel_time == False:
                  num_fire += 1
                  fire_sound.play()
                  player.fire()
              if num_fire >= 5 and rel_time == False:
                  last_time = timer()
                  rel_time = True  
    if finish != True:
        window.blit(bg, (0, 0))
        text = font2.render("СБИТО:" + str(score), 1, (255, 255, 255))
        window.blit(text, (5, 20))
        text_lose = font2.render("ПРОПУШЧЕНО:" + str(lost), 1, (255, 255, 255))
        window.blit(text_lose, (5, 60))
        player.update()
        bullets.update()
        monsters.update()
        asteroids.update()
        player.reset()
        monsters.draw(window)
        bullets.draw(window)
        if rel_time == True:
            now_timer = timer()
            if now_timer - last_time < 3:
                reload = font2.render("RELOAD", True, (150,0,0))
                window.blit(reload, (350, 500))
            else:
                num_fire = 0
                rel_time = False
        asteroids.draw(window)
        collides = sprite.groupcollide(monsters, bullets, True, True)
        for c in collides:
            score += 1
            monster = Enemy(img_enemy, randint(80, WIDTH - 80), -40, randint(1, 3))
            monsters.add(monster)
        if sprite.spritecollide(player, monsters, True):
            finish = True
            window.blit(lose, (200,200))
        if score > 9:
            finish = True
            window.blit(win, (200,200))
        display.update()
    else:
        sleep(5)
        finish = False
        score = 0
        lost = 0
        for b in bullets:
            b.kill()
        for m in monsters:
            m.kill()
        for i in range(1, 6):
            monster = Enemy(img_enemy, randint(80, WIDTH - 80), -40, randint(1, 3))
            monsters.add(monster)
        for i in range(3):
            asteroid =Enemy(img_asteroid, randint(80, WIDTH - 80), -40, randint(1, 1))



    display.update()
    clock.tick(FPS)