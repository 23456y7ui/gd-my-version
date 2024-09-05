import pygame
import random
import sys
from pygame.locals import QUIT

pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((1535, 800))
clock = pygame.time.Clock()
font = pygame.font.Font(None,50)
sound_effect_jump = pygame.mixer.Sound('8bit-synth-bounce-short.wav')
sound_effect_jump.set_volume(0.5)
pygame.mixer.music.load("Dimrain47_-_At_the_Speed_of_Light_Full_62880084.mp3")
pygame.mixer.music.set_volume(0.6)
pygame.mixer.music.play(-1)
player_image = pygame.image.load('гд2_1.png').convert_alpha()
player_image = pygame.transform.scale(player_image,(50,50))
spike = pygame.image.load('гд3.png')
spike = pygame.transform.scale(spike,(40,40))
ground = pygame.image.load('Фото земли.png').convert_alpha()
ground = pygame.transform.scale(ground,(3060,250))
background = pygame.image.load('Без названия.png').convert_alpha()
background = pygame.transform.scale(background,(1535,800))
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = player_image
        self.rect = self.image.get_rect(topleft=(100, 500))  # создание персонажа
        self.velocity_y = 0  # вертикальная скорость
        self.gravity = 0.5  # сила гравитации
        self.jump_strength = -11  # сила прыжка
        self.on_ground = False  # проверка нахождения на земле

    def update(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE] and self.on_ground:  # проверка прыжка
            sound_effect_jump.play()  # звук прыжка
            self.velocity_y = self.jump_strength  # сила прыжка
            self.on_ground = False

        # Применение гравитации
        self.velocity_y += self.gravity
        self.rect.y += self.velocity_y

        # Проверка коллизий с полом
        if self.rect.bottom >= 550:
            self.rect.bottom = 550
            self.velocity_y = 0
            self.on_ground = True


class Ground(pygame.sprite.Sprite):
    def __init__(self,img,y,speed):
        super().__init__()
        self.image = img
        self.rect = self.image.get_rect(topleft=(0, y))
        self.speed = speed
        self.x1 = 0
        self.x2 = self.rect.width

    def update(self):
        self.x1 -= self.speed
        self.x2 -= self.speed
        if self.x1 <= -self.rect.width:
            self.x1 = self.rect.width
        if self.x2 <= -self.rect.width:
            self.x2 = self.rect.width

    def draw(self, screen):
        screen.blit(self.image, (self.x1, self.rect.y))
        screen.blit(self.image, (self.x2, self.rect.y))


class Triangle(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = spike
        self.rect = self.image.get_rect(topleft=(x, y))
        self.speed = 5

    def update(self):
        self.rect.x -= self.speed
        # Удаление треугольника, если он выходит за пределы экрана
        if self.rect.right < 0:
            self.kill()


player = Player()
dirt = Ground(ground,550,5)
bg = Ground(background,0,5)
all_sprites = pygame.sprite.Group()
all_sprites.add(player)
triangles = pygame.sprite.Group()


def spawn():
    start_x = 1570
    for i in range(random.randint(1,3)):
        triangle = Triangle(start_x + i*30 , 515)
        all_sprites.add(triangle)
        triangles.add(triangle)
def timer(screen,start_ticks,font):
    elapsed_time = (pygame.time.get_ticks() - start_ticks) / 1000
    timer_surface = font.render(f'time : {int(elapsed_time)}',True,(0,0,0))
    screen.blit(timer_surface,(10,10))


spawn_event = pygame.USEREVENT + 1
pygame.time.set_timer(spawn_event, random.randint(1, 3) * 1000)
running = True
start_ticks = pygame.time.get_ticks()
fps = 30
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == spawn_event:
            spawn()
            pygame.time.set_timer(spawn_event, random.randint(2, 5) * 1000)
    all_sprites.update()
    dirt.update()
    bg.update()
    if pygame.sprite.spritecollide(player, triangles, False):
        print('you die')
        running = False
    bg.draw(screen)
    all_sprites.draw(screen)
    dirt.draw(screen)
    timer(screen, start_ticks, font)
    pygame.display.flip()
    fps += 0.1
    clock.tick(int(fps))
    print(fps)


pygame.quit()
sys.exit()
