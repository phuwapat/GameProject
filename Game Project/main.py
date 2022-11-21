import pygame
import random
import os
import button
import re
from pygame import mixer
from spritesheet import Spritesheet
from enemy import Enemy


mixer.init()
pygame.init()

SCREEN_WIDTH = 400
SCREEN_HEIGHT = 600

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('65010869')

clock = pygame.time.Clock()
FPS = 60
user = ''
score_list = []
score = 0
global item_use 
item_use = False

#load image
bg = pygame.image.load(r'D:/coding/Game Project/PIC/game2/bgnew1.png').convert_alpha()
cat_image = pygame.image.load(r'D:/coding/Game Project/PIC/game2/stdcat.png').convert_alpha()
plantform_image = pygame.image.load(r'D:/coding/Game Project/PIC/game2/platform.png').convert_alpha()
bird_image = pygame.image.load(r'D:/coding/Game Project/PIC/game2/bird.png').convert_alpha()
item1_image = pygame.image.load(r'D:/coding/Game Project/PIC/game2/item1.png').convert_alpha()
bombup_image = pygame.image.load(r'D:/coding/Game Project/PIC/game2/bombup.png').convert_alpha()
bombdown_image = pygame.image.load(r'D:/coding/Game Project/PIC/game2/bombdown.png').convert_alpha()
bird_sheet = Spritesheet(bird_image)

#load music amd sound
jump_fx = pygame.mixer.Sound(r'D:/coding/Game Project/PIC/game2/jump.mp3')
jump_fx.set_volume(0.2)
death_fx = pygame.mixer.Sound(r'D:/coding/Game Project/PIC/game2/death.mp3')
death_fx.set_volume(0.4)
item_fx = pygame.mixer.Sound(r'D:/coding/Game Project/PIC/game2/item.mp3')
item_fx.set_volume(0.5)

#define font
font_small = pygame.font.Font(r'D:/coding/Game Project/FONT/PressStart2P.ttf', 12)
font_big = pygame.font.Font(r'D:/coding/Game Project/FONT/PressStart2P.ttf', 18)
font_menu = pygame.font.Font(r'D:/coding/Game Project/FONT/PressStart2P.ttf', 24)

#define color
WHITE = (255,255,255)
BLACK  = (0, 0, 0)

def music_game():
    pygame.mixer.music.load(r'D:/coding/Game Project/PIC/game2/sound_game.mp3')
    pygame.mixer.music.set_volume(0.5)
    pygame.mixer.music.play(-1, 0.0)

def music_menu():
    pygame.mixer.music.load(r'D:/coding/Game Project/PIC/game2/sound_menu.mp3')
    pygame.mixer.music.set_volume(0.5)
    pygame.mixer.music.play(-1, 0.0)


def music_menu():
    pygame.mixer.music.load(r'D:/coding/Game Project/PIC/game2/sound_menu.mp3')
    pygame.mixer.music.set_volume(1)
    pygame.mixer.music.play(-1, 0.0)


def game():
    GRAVITY = 1
    MAX_PLATFORMS = 10
    MAX = 1
    SCROLL_THRESH = 200
    scroll = 0
    bg_scroll = 0
    game_over = False
    global score 
    item_use = False
    score = 0
    fade_counter = 0
    game_paused = False
    file_score = 'score1.txt'
    file_highscore = 'highsocre.txt'
    
    if os.path.exists(file_highscore):
        with open(file_highscore,'r') as file:
            high_score = int(file.read())
    else:
        high_score = 0   

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
        draw_text('SCORE : ' + str(score), font_small, WHITE, 0, 10)
        draw_text('HIGHSCORE : ' + str(high_score), font_small, WHITE, 200, 10)
        

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
            global dx 
            global dy 
            dx = 0 
            dy = 0
            item_use = False

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
            
            #auto jump
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
            if self.rect.top > SCREEN_HEIGHT + 100:
                self.kill()
    
    class Item(pygame.sprite.Sprite):
        def __init__(self, x, y, moving):
            pygame.sprite.Sprite.__init__(self)
            self.image = pygame.transform.scale(item1_image, (40, 40))
            self.rect = self.image.get_rect()
            self.rect.x = x
            self.rect.y = y
            self.moving = moving
            self.move_counter = random.randint(0, 50)
            self.direction = 1
            self.speed = random.randint(4, 5)
        
        def update(self, scroll):
            
            if self.moving == True:
                self.move_counter += 1
                self.rect.y += self.direction * self.speed

            self.rect.y += scroll

            if self.rect.top > SCREEN_HEIGHT + 100:
                self.kill()
    
    class BombDown(pygame.sprite.Sprite):
        def __init__(self, x, y, moving):
            pygame.sprite.Sprite.__init__(self)
            self.image = pygame.transform.scale(bombdown_image, (40, 40))
            self.rect = self.image.get_rect()
            self.rect.x = x
            self.rect.y = y
            self.moving = moving
            self.move_counter = random.randint(0, 50)
            self.direction = 1
            self.speed = random.randint(5, 7)
        
        def update(self, scroll):
            
            if self.moving == 1:
                self.move_counter += 1
                self.rect.y += self.direction * self.speed
                if self.rect.top > SCREEN_HEIGHT + 100:
                    self.kill()

            self.rect.y += scroll
    
    class BombUp(pygame.sprite.Sprite):
        def __init__(self, x, y, moving):
            pygame.sprite.Sprite.__init__(self)
            self.image = pygame.transform.scale(bombup_image, (40, 40))
            self.rect = self.image.get_rect()
            self.rect.x = x
            self.rect.y = y
            self.moving = moving
            self.move_counter = random.randint(0, 50)
            self.direction = 1
            self.speed = random.randint(5, 7)
        
        def update(self, scroll):

            if self.moving == 2:
                self.move_counter += 1
                self.rect.y -= self.direction * self.speed
                if self.rect.bottom < 0:
                    self.kill()

            self.rect.y += scroll


    #object
    cat = player(SCREEN_WIDTH//2, SCREEN_HEIGHT - 150)
    platform_group = pygame.sprite.Group()
    enemy_group = pygame.sprite.Group()
    item_group = pygame.sprite.Group()
    bomb_group = pygame.sprite.Group()
    #start platform
    platform = Platform(SCREEN_WIDTH // 2 - 50, SCREEN_HEIGHT - 50, 100, False)
    platform_group.add(platform)

    music_game()

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
                p_y = platform.rect.y - random.randint(80, 115)
                p_type = random.randint(1, 2)
                if p_type == 1 and score > 500 :
                    p_moving = True
                else:
                    p_moving = False
                platform = Platform(p_x , p_y, p_w, p_moving)
                platform_group.add(platform)

            #generate item
            if len(item_group) < MAX:
                if item_use == False and score > 700:
                    p_x = random.randint(0, SCREEN_WIDTH - 50)
                    p_y = 0
                    p_type = 1
                    if p_type == 1:
                        p_moving = True
                    item = Item(p_x, p_y,p_moving)
                    item_group.add(item)

            #generate bomb
            if len(bomb_group) < MAX and score > 300 :
                if item_use == False:
                    p_x = random.randint(0, SCREEN_WIDTH - 50)
                    p_type = random.choice([1, 2])
                    if p_type == 1:
                        p_y = -100
                        p_moving = 1
                        bomb = BombDown(p_x, p_y,p_moving)
                    if p_type == 2:
                        p_y = SCREEN_HEIGHT
                        p_moving = 2 
                        bomb = BombUp(p_x, p_y,p_moving)
                    bomb_group.add(bomb)

            #score
            if scroll > 0:
                score += scroll

            #draw line previous high score
            pygame.draw.line(screen, WHITE, (0, score - high_score + SCROLL_THRESH), (SCREEN_WIDTH, score - high_score + SCROLL_THRESH), 2 )
            draw_text('HIGHEST SCORE :' + str(high_score), font_small, BLACK, SCREEN_WIDTH - 160,  score - high_score + SCROLL_THRESH )


            #generate enemy
            if len(enemy_group) == 0 and score > 1000:
                enemy = Enemy(SCREEN_WIDTH, 100, bird_sheet, 1.5)
                enemy_group.add(enemy)

            #update enemy
            enemy_group.update(scroll ,SCREEN_WIDTH)
            #update item
            item_group.update(scroll)
            bomb_group.update(scroll)
            #update platform
            platform_group.update(scroll)
            #draw sprite
            platform_group.draw(screen)
            item_group.draw(screen)
            enemy_group.draw(screen)
            bomb_group.draw(screen)
            cat.draw()
            draw_info()
            #check collision item
            if pygame.sprite.spritecollide(cat, item_group, False):
                item.kill()
                item_fx.play()
                item_use = False
                p_w = random.randint(40 * 3, 60 * 3)
                p_x = random.randint(0, SCREEN_WIDTH - p_w)
                p_y = platform.rect.y - random.randint(80, 120)
                platform = Platform(p_x , p_y, p_w, None)
                platform_group.add(platform)
            #check collision
            if pygame.sprite.spritecollide(cat, bomb_group, False):
                game_over = True
                death_fx.play()
            #check game end
            if cat.rect.top > SCREEN_HEIGHT:
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
                pygame.draw.rect(screen, BLACK, (0, 0, fade_counter,SCREEN_HEIGHT / 2))
                pygame.draw.rect(screen, BLACK, (SCREEN_WIDTH - fade_counter, SCREEN_HEIGHT / 2, SCREEN_WIDTH,SCREEN_HEIGHT ))
            else:
                pygame.mixer.music.pause()
                draw_text('GAME OVER', font_big, WHITE, 120, 200)
                draw_text('SCORE ', font_big, WHITE, 100, 250)
                draw_text(str(score), font_big, WHITE, 250, 250)
                draw_text('PRESS SPACE TO PLAY ', font_big, WHITE, 30, 300)
                draw_text('PRESS ESC TO EXIT', font_big, WHITE, 50, 350 )
                if score > high_score:
                    high_score = score
                    with open(file_highscore,'w') as file:
                        file.write(str(high_score))
                key = pygame.key.get_pressed()
                if key[pygame.K_SPACE]:
                    save_score(user, score)
                    pygame.mixer.music.unpause()
                    item_use = False
                    game_over = False
                    bg_scroll = 0
                    score = 0
                    scroll = 0
                    fade_counter = 0 
                    cat.rect.center = (SCREEN_WIDTH//2, SCREEN_HEIGHT - 150) 
                    platform_group.empty()
                    item_group.empty()
                    enemy_group.empty()
                    bomb_group.empty()
                    platform = Platform(SCREEN_WIDTH // 2 - 50, SCREEN_HEIGHT - 50, 100, False)
                    platform_group.add(platform)
                if key[pygame.K_ESCAPE]:
                    save_score(user, score)
                    main_menu()

        #คำสั่งปิดเกม
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

        pygame.display.update()

#variable
game_paused = False

#define color
WHITE = (255, 255, 255)

#load button image
start_img = pygame.image.load(r'D:/coding/Game Project/PIC/game2/start_button.png').convert_alpha()
credit_img = pygame.image.load(r'D:/coding/Game Project/PIC/game2/credit_button.png').convert_alpha()
leaderboard_img = pygame.image.load(r'D:/coding/Game Project/PIC/game2/leaderboard_button.png').convert_alpha()
exit_img = pygame.image.load(r'D:/coding/Game Project/PIC/game2/exit_button.png').convert_alpha()
enter_img = pygame.image.load(r'D:/coding/Game Project/PIC/game2/enter_button.png').convert_alpha()
backward_img = pygame.image.load(r'D:/coding/Game Project/PIC/game2/backward_button.png').convert_alpha()

#create button 
start_button = button.Button(110, 200, start_img, 0.25)
credit_button = button.Button(110, 300, credit_img, 0.25)
leaderboard_button = button.Button(110, 400, leaderboard_img, 0.25)
exit_button = button.Button(110, 500, exit_img, 0.25)
enter_button = button.Button(110, 500, enter_img, 0.25)
backward_button = button.Button(110, 500, backward_img, 0.25)

def draw_text(text , font, text_col, x, y):
    img = font.render(text, True, text_col)
    screen.blit(img, (x, y))

def insert_name():
    text_box = pygame.Rect(98, 300, 200, 32)
    global user
    user = ''
    run = True
    while run:
        screen.blit(bg, (0, 0))
        backward_button = button.Button(0, 0, backward_img, 0.15)
        enter_button = button.Button(145, 330, enter_img, 0.15)
        draw_text('ENTER NAME', font_big, WHITE, 107, 249)
        draw_text('ENTER NAME', font_big, BLACK, 110, 250)
        text_surface = font_big.render(user, True, WHITE)
        screen.blit(text_surface, (98, 305))
        pygame.draw.rect(screen, BLACK, text_box, 2)
        if backward_button.draw(screen):
            main_menu()
        if enter_button.draw(screen):
            if user == '':
                user = 'GUEST'
            print(user)
            game()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_BACKSPACE:
                    user = user[:-1]
                else:
                    if len(user) == 6:
                        break
                    user += event.unicode
    
            
        pygame.display.update()

    return user

def save_score(user, score):
    global score_list 
    sorted_file = 'sortedscore.txt'
    leaderboard = open("score1.txt",'a+')
    leaderboard.write(f"{score} {user}\n")
    leaderboard.close()
    
       
def sort_score(user, score):
    global score_list
    leaderboard = open("score1.txt",'r')
    readthefile = leaderboard.readlines()
    readthefile.sort(key=lambda s: int(re.search(r'\d+', s).group()), reverse=True)
    for i in readthefile:
        score_list.append(i.strip())    
    
def credit():
    run = True
    while run:
        screen.blit(bg, (0, 0))
        backward_button = button.Button(0, 0, backward_img, 0.15)
        draw_text('CREATED BY', font_big, WHITE, 107, 249)
        draw_text('CREATED BY', font_big, BLACK, 110, 250)
        draw_text('PHUWAPAT JAISIN', font_big, WHITE, 67, 309)
        draw_text('PHUWAPAT JAISIN', font_big, BLACK, 70, 310)
        draw_text('65010869', font_big, WHITE, 127, 369)
        draw_text('65010869', font_big, BLACK, 130, 370)
        if backward_button.draw(screen):
            main_menu()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

        pygame.display.update()


def lederboard():
    sort_score(user, score)
    # sorted_file = 'sortedscore.txt'
    run = True
    while run:
        screen.blit(bg, (0, 0))
        backward_button = button.Button(0, 0, backward_img, 0.15)
        draw_text('TOP 5 SCORES', font_big, BLACK, 95, 100)

        top1 = score_list[0]
        top_1 = draw_text(f"1.{top1}", font_big, BLACK, 95, 150)

        top2 = score_list[1]
        top_2 = draw_text(f"2.{top2}", font_big, BLACK, 95, 200)

        top3 = score_list[2]
        top_3 = draw_text(f"3.{top3}", font_big, BLACK, 95, 250)

        top4 = score_list[3]
        top_4 = draw_text(f"4.{top4}", font_big, BLACK, 95, 300)

        top5 = score_list[4]
        top_5 = draw_text(f"5.{top5}", font_big, BLACK, 95, 350)
        
        if backward_button.draw(screen):
            main_menu()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

        pygame.display.update()


#main loop
def main_menu():
    game_over = False
    game_paused = False
    run = True
    music_menu()
    while run:
        
        screen.blit(bg, (0, 0))

        #check if game is paused
        if game_paused == False:
            draw_text('ANGRY MAD CAT', font_menu, WHITE, 50, 108)
            draw_text('ANGRY MAD CAT', font_menu, BLACK, 51, 110)
            if start_button.draw(screen):
                game_paused = True
                pygame.mixer.music.pause()
                insert_name()
            if credit_button.draw(screen):
                credit()
            if leaderboard_button.draw(screen):
                lederboard()
            if exit_button.draw(screen):
                run = False

        #event handler
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    game_paused = True
            if event.type == pygame.QUIT:
                run = False

        pygame.display.update()

    pygame.quit()

main_menu()

