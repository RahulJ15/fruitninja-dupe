
import sys
import os
import random
import pygame

player_lives = 3                                                #keep track of lives
score = 0                                                       #keeps track of score
fruits = ['melon', 'orange', 'pomegranate', 'guava', 'bomb']    #entities in the game
game_duration = 60  # Time limit for each game round in seconds
current_time = 0   # Initialize the timer to zero  
fruit_spawn_rate = 0.2  # Initial fruit spawn rate
bomb_frequency = 0.1   # Initial bomb spawn frequency
current_difficulty = "Easy"  # Initialize difficulty level

# initialize pygame and create window
WIDTH = 800
HEIGHT = 500
FPS = 10                                               #controls how often the gameDisplay should refresh. In our case, it will refresh every 1/12th second
pygame.init()
pygame.display.set_caption('Fruit-Ninja Game -- DataFlair')
gameDisplay = pygame.display.set_mode((WIDTH, HEIGHT))   #setting game display size
clock = pygame.time.Clock()

# Define colors
WHITE = (255,255,255)
BLACK = (0,0,0)
RED = (255,0,0)
GREEN = (0,255,0)
BLUE = (0,0,255)

background = pygame.image.load('summer.jpg')                                  #game background
font = pygame.font.Font(os.path.join(os.getcwd(), 'mario.otf'), 42)
score_text = font.render('Score : ' + str(score), True, (255, 255, 255))    #score display
lives_icon = pygame.image.load('images/white_lives.png')                    #images that shows remaining lives


# Generalized structure of the fruit Dictionary
def generate_random_fruits(fruit):
    fruit_path = "images/" + fruit + ".png"
    data[fruit] = {
        'img': pygame.image.load(fruit_path),
        'x' : random.randint(100,500),          #where the fruit should be positioned on x-coordinate
        'y' : 800,
        'speed_x': random.randint(-10,10),      #how fast the fruit should move in x direction. Controls the diagonal movement of fruits
        'speed_y': random.randint(-80, -60),    #control the speed of fruits in y-directionn ( UP )
        'throw': False,                         #determines if the generated coordinate of the fruits is outside the gameDisplay or not. If outside, then it will be discarded
        't': 0,                                 #manages the
        'hit': False
    }

    if random.random() >= 0.75:     #Return the next random floating point number in the range [0.0, 1.0) to keep the fruits inside the gameDisplay
        data[fruit]['throw'] = True
    else:
        data[fruit]['throw'] = False

# Dictionary to hold the data the random fruit generation
data = {}
for fruit in fruits:
    generate_random_fruits(fruit)

def hide_cross_lives(x, y):
    gameDisplay.blit(pygame.image.load("images/red_lives.png"), (x, y))

# Generic method to draw fonts on the screen
font_name = pygame.font.match_font('mario.otf')
def draw_text(display, text, size, x, y):
    font = pygame.font.Font(os.path.join(os.getcwd(), 'mario.otf'), size)
    text_surface = font.render(text, True, WHITE)
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x, y)
    gameDisplay.blit(text_surface, text_rect)

# draw players lives
def draw_lives(display, x, y, lives, image) :
    for i in range(lives) :
        img = pygame.image.load(image)
        img_rect = img.get_rect()       #gets the (x,y) coordinates of the cross icons (lives on the the top rightmost side)
        img_rect.x = int(x + 35 * i)    #sets the next cross icon 35pixels awt from the previous one
        img_rect.y = y                  #takes care of how many pixels the cross icon should be positioned from top of the screen
        display.blit(img, img_rect)

# show game over display & front display
def show_gameover_screen():
    gameDisplay.blit(background, (0,0))
    draw_text(gameDisplay, "FRUIT NINJA!", 70, WIDTH / 2, HEIGHT / 4)
    draw_text(gameDisplay, "Made by Vanshika & Rahul :)", 20, WIDTH / 2, HEIGHT / 2.4)
    
    if not game_over :
        draw_text(gameDisplay,"Score : " + str(score), 35, WIDTH / 2, HEIGHT /2)

    draw_text(gameDisplay, "Press Enter to begin!", 35, WIDTH / 2, HEIGHT * 3 / 4)
    pygame.display.flip()
    waiting = True
    while waiting:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.KEYUP:
                waiting = False
#display timer
def update_timer_display():
    timer_font_size = 27
    timer_font = pygame.font.Font(os.path.join(os.getcwd(), 'mario.otf'), timer_font_size)
    timer_text = timer_font.render("Time: " + str(game_duration - current_time), True, (255, 255, 255))
    timer_text_rect = timer_text.get_rect()
    timer_text_rect.topleft = (10, 50)  # Adjust the position here
    gameDisplay.blit(timer_text, timer_text_rect)

# Function to display the difficulty level
def display_difficulty_level(display, current_difficulty):
    difficulty_font = pygame.font.Font(None, 36)
    difficulty_text = difficulty_font.render("Difficulty: " + current_difficulty, True, WHITE)
    difficulty_rect = difficulty_text.get_rect()
    difficulty_rect.bottomright = (WIDTH - 10, HEIGHT - 10)  # Adjust the position here
    display.blit(difficulty_text, difficulty_rect)

# Game Loop
first_round = True
game_over = True        #terminates the game While loop if more than 3-Bombs are cut
game_running = True     #used to manage the game loop
game_duration = 60
current_time = 0   
while game_running:
    if game_over:
        if first_round:
            show_gameover_screen()
            first_round = False
        game_over = False
        player_lives = 3
        score = 0
        fruit_spawn_rate = 0.2  # Reset initial fruit spawn rate
        bomb_frequency = 0.1   # Reset initial bomb spawn frequency
        draw_lives(gameDisplay, 690, 5, player_lives, 'images/red_lives.png')


    for event in pygame.event.get():
        # checking for closing window
        if event.type == pygame.QUIT:
            game_running = False

    gameDisplay.blit(background, (0, 0))
    current_time = pygame.time.get_ticks() // 1000 
    if current_time >= game_duration:
        # Game over or round end logic here
        show_gameover_screen()
        game_over = True

    update_timer_display()

    gameDisplay.blit(score_text, (0, 0))
    draw_lives(gameDisplay, 690, 5, player_lives, 'images/red_lives.png')

    # Track player performance (you can modify this logic)
    player_accuracy = (score + 1) / (score + 2)

    # Adjust game parameters based on player performance
    if player_accuracy > 0.8:
        fruit_spawn_rate = 0.3  # Increase fruit spawn rate for skilled players
        bomb_frequency = 0.05  # Decrease bomb frequency for skilled players
        if current_difficulty != "Hard":
            current_difficulty = "Hard"
    elif player_accuracy < 0.3:
        fruit_spawn_rate = 0.1  # Decrease fruit spawn rate for struggling players
        bomb_frequency = 0.2   # Increase bomb frequency for struggling players
        if current_difficulty != "Easy":
            current_difficulty = "Easy"
    
    display_difficulty_level(gameDisplay, current_difficulty)  # Display difficulty level


    for key, value in data.items():
        if value['throw']:
            value['x'] += value['speed_x']          #moving the fruits in x-coordinates
            value['y'] += value['speed_y']          #moving the fruits in y-coordinate
            value['speed_y'] += (1 * value['t'])    #increasing y-corrdinate
            value['t'] += 1                         #increasing speed_y for next loop

            if value['y'] <= 800:
                gameDisplay.blit(value['img'], (value['x'], value['y']))    #displaying the fruit inside screen dynamically
            else:
                generate_random_fruits(key)

            current_position = pygame.mouse.get_pos()   #gets the current coordinate (x, y) in pixels of the mouse

            if not value['hit'] and current_position[0] > value['x'] and current_position[0] < value['x']+60 \
                    and current_position[1] > value['y'] and current_position[1] < value['y']+60:
                if key == 'bomb':
                    player_lives -= 1
                    if player_lives == 0:
                        
                        hide_cross_lives(690, 15)
                    elif player_lives == 1 :
                        hide_cross_lives(725, 15)
                    elif player_lives == 2 :
                        hide_cross_lives(760, 15)
                    #if the user clicks bombs for three time, GAME OVER message should be displayed and the window should be reset
                    if player_lives == 0 :
                        show_gameover_screen()
                        game_over = True

                    half_fruit_path = "images/explosion.png"
                else:
                    half_fruit_path = "images/" + "half_" + key + ".png"

                value['img'] = pygame.image.load(half_fruit_path)
                value['speed_x'] += 10
                if key != 'bomb' :
                    score += 1
                score_text = font.render('Score : ' + str(score), True, (255, 255, 255))
                value['hit'] = True
        else:
            generate_random_fruits(key)

    pygame.display.update()
    clock.tick(FPS)      # keep loop running at the right speed (manages the frame/second. The loop should update afer every 1/12th pf the sec
                        

pygame.quit()
