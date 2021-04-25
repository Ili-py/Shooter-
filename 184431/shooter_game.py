
from pygame import *
from random import randint
from time import time as timer

class GameSprite(sprite.Sprite):
    def __init__(self, player_image, player_x, player_y,size_x,size_y,player_speed):
        super().__init__()

        self.image = transform.scale(image.load(player_image), (size_x,size_y))
        self.speed = player_speed

        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y

    def reset(self):
        window.blit(self.image,(self.rect.x, self.rect.y))

class Player(GameSprite):
    def update(self):
        keys = key.get_pressed()

        if keys [K_LEFT]and self.rect.x >10:
            self.rect.x -= self.speed

        if keys [K_RIGHT]and self.rect.x < 630:
            self.rect.x += self.speed

    def fire(self):
        bullet = Bullet('bullet.png', self.rect.centerx, self.rect.top, 20,20,20)
        bullets.add(bullet)

class Enemy(GameSprite):
    def update(self):
        self.rect.y += self.speed
        global lost
        if self.rect.y > 500:
            self.rect.x = randint(0,620)
            self.rect.y = 0
            lost += 1

class Bullet(GameSprite):
    def update(self):
        self.rect.y -= self.speed
        if self.rect.y < 0:
            self.kill()
    
window = display.set_mode((700,500))
display.set_caption('Pygame Window')

background = transform.scale(image.load('fon.jpg'),(700,500))
player = Player('stard.png',500,410,150,150,10)

game = True
finish = False

clock = time.Clock()
FPS = 60

mixer.init()
mixer.music.load('space.ogg')
mixer.music.play()

lost = 0
score = 0

font.init()
font1 = font.SysFont('Arial',36)

bullets = sprite.Group()

num_fire = 0
reck_time = False

life = 5

monsters = sprite.Group()

for i in range(5):
    monster = Enemy('ship2.png',randint(0,620),0,65,65,randint(1,3))
    monsters.add(monster)

while game:
    for e in event.get():
        if e.type == QUIT:
            game = False
        elif e.type == KEYDOWN:
            if e.key == K_SPACE:
                if num_fire <= 5 and reck_time == False:
                    num_fire = num_fire + 1
                    player.fire()
                elif num_fire >= 5 and reck_time == False:
                    last_time = timer()
                    reck_time = True

    if finish != True:
        window.blit(background,(0,0))

        player.update()
        player.reset()

        monsters.draw(window)
        monsters.update()

        bullets.update()
        bullets.draw(window)

        if reck_time == True:
            now_time = timer()
            if now_time - last_time <1:
                text_reload = font1.render('ПЕРЕЗАРЯДКА',1,(255,255,255))
                window.blit(text_reload,(250,450)) 
            else:
                reck_time = False
                num_fire = 0 

        text_life = font1.render('Жизни:'+ str(life), 1,(255,255,255))
        window.blit(text_life,(10,10))

        text_score = font1.render('Сбито:'+ str(score),1,(255,255,255))
        window.blit(text_score,(10,40))

        collides = sprite.groupcollide(monsters,bullets,True,True)
        for coll in collides:
            monster = Enemy('ship2.png',randint(0,620),0,65,65,randint(1,3))
            monsters.add(monster)
            score += 1

        if sprite.spritecollide(player,monsters,True):
            life = life - 1
            monster = Enemy('ship2.png',randint(0,620),0,65,65,randint(1,3))
            monsters.add(monster)

        if score  >=10:
            finish = True
            win = font1.render(' YOU WIN!!! ',1,(255,0,0))
            window.blit(win,(250,250))

        if life == 0:
            finish = True
            text_lose1 = font1.render('You Lose =(',1,(255,0,0))
            window.blit(text_lose1,(250,250))

        display.update()

    else:
        finish = False
        score = 0
        num_fire = 0
        life = 5
        for bullet in bullets:
            bullet.kill()
        for monster in monsters:
            monster.kill()
        for i in range(5):
            monster = Enemy('ship2.png',randint(0,600),0,65,65,randint(1,3))
            monsters.add(monster)

    clock.tick(FPS)