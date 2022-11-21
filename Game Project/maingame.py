import pygame
import random
import os
import button
from pygame import mixer
from spritesheet import Spritesheet
from enemy import Enemy

mixer.init()
pygame.init()

SCREEN_WIDTH = 400
SCREEM_HEIGHT = 600

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEM_HEIGHT))
pygame.display.set_caption('65010869')

clock = pygame.time.Clock()
FPS = 60

#load music amd sound
pygame.mixer.music.load(r'D:/coding/Game Project/PIC/game2/sound_game.mp3')
pygame.mixer.music.set_volume(0.5)
pygame.mixer.music.play(-1, 0.0)
jump_fx = pygame.mixer.Sound(r'D:/coding/Game Project/PIC/game2/jump.mp3')
jump_fx.set_volume(0.2)
death_fx = pygame.mixer.Sound(r'D:/coding/Game Project/PIC/game2/death.mp3')
death_fx.set_volume(0.4)
#define color
WHITE = (255,255,255)
BLACK  = (0, 0, 0)

#define font
font_small = pygame.font.SysFont('Lucida Sans', 18)
font_big = pygame.font.SysFont('Lucida Sans', 24)
font = pygame.font.SysFont('arialblack', 20)
#define variable for game
GRAVITY = 1
MAX_PLATFORMS = 10
SCROLL_THRESH = 200
scroll = 0
bg_scroll = 0
game_over = False
score = 0
fade_counter = 0
music_event = 0
game_paused = False
file_score = 'score.txt'

#load button image
start_img = pygame.image.load(r'D:/coding/Game Project/PIC/game2/start_button.png').convert_alpha()
option_img = pygame.image.load(r'D:/coding/Game Project/PIC/game2/option_button.png').convert_alpha()
leaderboard_img = pygame.image.load(r'D:/coding/Game Project/PIC/game2/leaderboard_button.png').convert_alpha()
exit_img = pygame.image.load(r'D:/coding/Game Project/PIC/game2/exit_button.png').convert_alpha()

#create button 
start_button = button.Button(110, 200, start_img, 0.25)
option_button = button.Button(110, 300, option_img, 0.25)
leaderboard_button = button.Button(110, 400, leaderboard_img, 0.25)
exit_button = button.Button(110, 500, exit_img, 0.25)

#function for menu
def draw_text_menu(text , font, text_col, x, y):
    img = font.render(text, True, text_col)
    screen.blit(img, (x, y))

if os.path.exists('file_score'):
    with open ('file_score','r') as file:
        high_score = int(file.read())
else:
    high_score = 0

#load image
bg = pygame.image.load(r'D:/coding/Game Project/PIC/game2/bg_new.png').convert_alpha()
cat_image = pygame.image.load(r'D:/coding/Game Project/PIC/game2/stdcat.png').convert_alpha()
plantform_image = pygame.image.load(r'D:/coding/Game Project/PIC/game2/platform.png').convert_alpha()
bird_image = pygame.image.load(r'D:/coding/Game Project/PIC/game2/bird.png').convert_alpha()
bird_sheet = Spritesheet(bird_image)
#function show text 
def draw_text(text, font, text_col, x, y):
    img = font.render(text, True, text_col)
    screen.blit(img, (x, y))

def draw_bg(scroll):
    screen.blit(bg, (0,0 + bg_scroll))
    screen.blit(bg, (0,-600 + bg_scroll))

def draw_info():
    pygame.draw.rect(screen, BLACK, (0,0,SCREEN_WIDTH,30))
    pygame.draw.line(screen, WHITE, (0,30), (SCREEN_WIDTH,30), 2)
    draw_text('SCORE : ' + str(score), font_small, WHITE, 0, 0) 

class player():
    def __init__(self, x, y):
        self.image = pygame.transform.scale(cat_image, (70, 70))
        self.width = 40
        self.height = 40
        self.rect = pygame.Rect(0, 0, self.width, self.height)
        self.rect.center = (x, y)
        self.flip = False
        self.vel_y = 0

    def move(self):

        scroll = 0
        dx = 0
        dy = 0

        key = pygame.key.get_pressed()
        if key[pygame.K_LEFT]:
            dx = -10
            self.flip = True
        if key[pygame.K_RIGHT]:
            dx = 10
            self.flip = False

        #gravity
        self.vel_y += GRAVITY
        dy += self.vel_y

        if self.rect.left + dx < 0:
            dx = -self.rect.left
        if self.rect.right + dx > SCREEN_WIDTH:
            dx = SCREEN_WIDTH - self.rect.right

        

        #check bounce top screen
        if self.rect.top <= SCROLL_THRESH:
            if self.vel_y < 0:
                 scroll = -dy

        #check collusion w/ platform
        for platform in platform_group:
            if platform.rect.colliderect(self.rect.x, self.rect.y + dy, self.width, self.height):
                if self.rect.bottom < platform.rect.centery:
                    if self.vel_y > 0:
                        self.rect.bottom = platform.rect.top
                        dy = 0
                        self.vel_y = -20
                        jump_fx.play()

            
        self.rect.x += dx
        self.rect.y += dy + scroll

        #update mask
        self.mask = pygame.mask.from_surface(self.image)

        return scroll

    def draw(self):
        screen.blit(pygame.transform.flip(self.image, self.flip, False), (self.rect.x - 10, self.rect.y - 30))

class Platform(pygame.sprite.Sprite):
    def __init__(self,x ,y, width, moving):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(plantform_image, (width, 10))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.moving = moving
        self.move_counter = random.randint(0, 50)
        self.direction = random.choice([-1, 1])
        self.speed = random.randint(1, 3)

    def update(self, scroll):
        #move platform
        if self.moving == True:
            self.move_counter += 1
            self.rect.x += self.direction * self.speed

        #change platform direction if it move fully
        if self.move_counter >= 100 or self.rect.left < 0 or self.rect.right > SCREEN_WIDTH:
            self.direction *= -1
            self.move_counter = 0
        #update platform pos
        self.rect.y += scroll

        #check if platform hs gone off screen
        if self.rect.top > SCREEM_HEIGHT:
            self.kill()
    
    
#object
cat = player(SCREEN_WIDTH//2, SCREEM_HEIGHT - 150)
platform_group = pygame.sprite.Group()
enemy_group = pygame.sprite.Group()
#star platform
platform = Platform(SCREEN_WIDTH // 2 - 50, SCREEM_HEIGHT - 50, 100, False)
platform_group.add(platform)

#main loop
run = True
while run:
    
    clock.tick(FPS)

    if game_over == False:
        
        scroll = cat.move()
        
        #draw bg
        bg_scroll += scroll
        if bg_scroll >= 600:
            bg_scroll = 0
        draw_bg(bg_scroll)

        #generate platform
        if len(platform_group) < MAX_PLATFORMS:
            p_w = random.randint(40, 60)
            p_x = random.randint(0, SCREEN_WIDTH - p_w)
            p_y = platform.rect.y - random.randint(80, 110)
            p_type = random.randint(1, 2)
            if p_type == 1 and score > 500 :
                p_moving = True
            else:
                p_moving = False
            platform = Platform(p_x , p_y, p_w, p_moving)
            platform_group.add(platform)

        #score
        if scroll > 0:
            score += scroll

        #draw line previous high score
        pygame.draw.line(screen, WHITE, (0, score - high_score + SCROLL_THRESH), (SCREEN_WIDTH, score - high_score + SCROLL_THRESH), 2 )
        draw_text('HIGHEST SCORE :' + str(high_score), font_small, BLACK, SCREEN_WIDTH - 140,  score - high_score + SCROLL_THRESH )

        platform_group.update(scroll)

        #generate enemy
        if len(enemy_group) == 0 and score > 1000:
            enemy = Enemy(SCREEN_WIDTH, 100, bird_sheet, 1.5)
            enemy_group.add(enemy)

        #update enemy
        enemy_group.update(scroll ,SCREEN_WIDTH)
        #draw sprite
        platform_group.draw(screen)
        enemy_group.draw(screen)
        cat.draw()
        draw_info()

        #check game end
        if cat.rect.top > SCREEM_HEIGHT:
            game_over = True
            death_fx.play() 
        #check for collision with enemy
        if pygame.sprite.spritecollide(cat, enemy_group, False):
            if pygame.sprite.spritecollide(cat, enemy_group, False, pygame.sprite.collide_mask):
                game_over = True
                death_fx.play()
    else:
        if fade_counter <= SCREEN_WIDTH:
            fade_counter += 5
            pygame.draw.rect(screen, BLACK, (0, 0, fade_counter,SCREEM_HEIGHT / 2))
            pygame.draw.rect(screen, BLACK, (SCREEN_WIDTH - fade_counter, SCREEM_HEIGHT / 2, SCREEN_WIDTH,SCREEM_HEIGHT ))
        else:
            pygame.mixer.music.pause()
            draw_text('GAME OVER', font_big, WHITE, 130, 200)
            draw_text('SCORE ' + str(score), font_big, WHITE, 130, 250)
            draw_text('PRESS SPACE TO PLAY AGAIN', font_big, WHITE, 40, 300)
            if score > high_score:
                high_score = score
                with open('file_score','w') as file:
                    file.write(str(high_score))
            key = pygame.key.get_pressed()
            if key[pygame.K_SPACE]:
                pygame.mixer.music.unpause()
                game_over = False
                score = 0
                scroll = 0
                fade_counter = 0 
                cat.rect.center = (SCREEN_WIDTH//2, SCREEM_HEIGHT - 150) 
                platform_group.empty()
                enemy_group.empty()
                platform = Platform(SCREEN_WIDTH // 2 - 50, SCREEM_HEIGHT - 50, 100, False)
                platform_group.add(platform)

    #คำสั่งปิดเกม
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
         run = False
         
         

    pygame.display.update()

pygame.quit()


'''
#main loop 
run = True
while run:
    
    clock.tick(FPS)

    if game_over == False:
        
        scroll = cat.move()
        
        #draw bg
        bg_scroll += scroll
        if bg_scroll >= 600:
            bg_scroll = 0
        draw_bg(bg_scroll)

        #generate platform
        if len(platform_group) < MAX_PLATFORMS:
            p_w = random.randint(40, 60)
            p_x = random.randint(0, SCREEN_WIDTH - p_w)
            p_y = platform.rect.y - random.randint(80, 110)
            p_type = random.randint(1, 2)
            if p_type == 1 and score > 500 :
                p_moving = True
            else:
                p_moving = False
            platform = Platform(p_x , p_y, p_w, p_moving)
            platform_group.add(platform)

        #score
        if scroll > 0:
            score += scroll

        #draw line previous high score
        pygame.draw.line(screen, WHITE, (0, score - high_score + SCROLL_THRESH), (SCREEN_WIDTH, score - high_score + SCROLL_THRESH), 2 )
        draw_text('HIGHEST SCORE :' + str(high_score), font_small, BLACK, SCREEN_WIDTH - 140,  score - high_score + SCROLL_THRESH )

        platform_group.update(scroll)

        #generate enemy
        if len(enemy_group) == 0 and score > 1000:
            enemy = Enemy(SCREEN_WIDTH, 100, bird_sheet, 1.5)
            enemy_group.add(enemy)

        #update enemy
        enemy_group.update(scroll ,SCREEN_WIDTH)
        #draw sprite
        platform_group.draw(screen)
        enemy_group.draw(screen)
        cat.draw()
        draw_info()

        #check game end
        if cat.rect.top > SCREEM_HEIGHT:
            game_over = True
            death_fx.play() 
        #check for collision with enemy
        if pygame.sprite.spritecollide(cat, enemy_group, False):
            if pygame.sprite.spritecollide(cat, enemy_group, False, pygame.sprite.collide_mask):
                game_over = True
                death_fx.play()
    else:
        if fade_counter <= SCREEN_WIDTH:
            fade_counter += 5
            pygame.draw.rect(screen, BLACK, (0, 0, fade_counter,SCREEM_HEIGHT / 2))
            pygame.draw.rect(screen, BLACK, (SCREEN_WIDTH - fade_counter, SCREEM_HEIGHT / 2, SCREEN_WIDTH,SCREEM_HEIGHT ))
        else:
            pygame.mixer.music.pause()
            draw_text('GAME OVER', font_big, WHITE, 130, 200)
            draw_text('SCORE ' + str(score), font_big, WHITE, 130, 250)
            draw_text('PRESS SPACE TO PLAY AGAIN', font_big, WHITE, 40, 300)
            if score > high_score:
                high_score = score
                with open('file_score','w') as file:
                    file.write(str(high_score))
            key = pygame.key.get_pressed()
            if key[pygame.K_SPACE]:
                pygame.mixer.music.unpause()
                game_over = False
                score = 0
                scroll = 0
                fade_counter = 0 
                cat.rect.center = (SCREEN_WIDTH//2, SCREEM_HEIGHT - 150) 
                platform_group.empty()
                enemy_group.empty()
                platform = Platform(SCREEN_WIDTH // 2 - 50, SCREEM_HEIGHT - 50, 100, False)
                platform_group.add(platform)

    #คำสั่งปิดเกม
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
         run = False
         
         

    pygame.display.update()

pygame.quit()
'''  