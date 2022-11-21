import pygame
import button

pygame.init()

SCREEN_WIDTH = 400
SCREEM_HEIGHT = 600

screen = pygame.display.set_mode((SCREEN_WIDTH,SCREEM_HEIGHT))
pygame.display.set_caption('Main Menu')

#variable
game_paused = False

#define font
font = pygame.font.SysFont('arialblack', 20)

#define color
WHITE = (255, 255, 255)

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

def draw_text(text , font, text_col, x, y):
    img = font.render(text, True, text_col)
    screen.blit(img, (x, y))

#main loop
run = True
while run:
    
    screen.fill((52, 78, 91))

    #check if game is paused
    if game_paused == False:
        if start_button.draw(screen):
            game_paused = True
        if option_button.draw(screen):
            pass
        if leaderboard_button.draw(screen):
            pass
        if exit_button.draw(screen):
            run = False

    #display menu
    else:
        draw_text('Press SPACE to pause', font, WHITE, 100, 300)

    #event handler
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                print('pause')
                game_paused = True
        if event.type == pygame.QUIT:
            run = False

    pygame.display.update()

pygame.quit()