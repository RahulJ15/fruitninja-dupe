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

# INITIALIZING PYGAME WINDOW

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
professor_image = pygame.image.load('professor.png')
professor_rect = professor_image.get_rect()
professor_rect.topleft = (20, HEIGHT / 2)
fruit_facts = [
    "Did you know that bananas are berries?",
    "Grapes can be used to make wine.",
    "Melons are an excellent choice for staying hydrated.",
    "Guavas are sometimes called 'the poor man's apple'.",
    "Each pomegranate can contain hundreds of juicy seeds, known as arils.",
    "Oranges are a good source of vitamin C.",
    "Cranberries can bounce!",
    "Orange trees can live for up to 100 years and continue to produce fruit throughout their long lives.",
    "Guavas are often referred to as superfruits because of their high nutritional value.",
    "Pomegranates are known as 'nature's candy' due to their sweet and tart flavor.",
    "Some oranges can be fully ripe while still green in color.",
    "The world's heaviest melon on record weighed over 350 pounds!"
]

#DISPLAYING RANDOM FRUIT FACTS
def display_random_fact(facts_displayed):

    # Shuffle the facts list to ensure randomness

    random.shuffle(fruit_facts)
    fact_font = pygame.font.Font(os.path.join(os.getcwd(), 'mario.otf'), 14)
    text_x = WIDTH // 1.6  # Initial x-coordinate for the text
    text_y = professor_rect.bottom + 0.25  # Position the text below the professor
    scroll_speed=0.125 # Adjust this value to control the scrolling speed

    # A smaller value will slow down the scrolling speed
    # while a larger value will speed it up.

    for fact in fruit_facts:

        if fact not in facts_displayed:
            # Display the fact

            text_height = fact_font.size(fact)[1]
            fact_text = fact_font.render(fact, True, (255, 255, 255))
            text_rect = fact_text.get_rect()
            text_rect.topleft = (text_x, text_y)
            gameDisplay.blit(fact_text, text_rect)
            pygame.display.update()

            while text_rect.right > 0:
                gameDisplay.blit(background, text_rect, text_rect)  # Clear previous text
                text_x -= scroll_speed  # Adjust the scrolling speed
                text_rect.topleft = (text_x, text_y)
                gameDisplay.blit(fact_text, text_rect)
                pygame.display.update()

            # Add the displayed fact to the list to prevent repeats

            facts_displayed.append(fact)
            text_x = WIDTH // 1.6

            pygame.draw.rect(gameDisplay, (0, 0, 0), text_rect)
            gameDisplay.blit(fact_text, text_rect)

            pygame.display.update()
            pygame.time.delay(1000)  # Wait for 1 seconds before displaying the next fact

            # Clear the fact from the screen

            pygame.draw.rect(gameDisplay, BLACK, text_rect)
            pygame.display.update()
            # Add the displayed fact to the list to prevent repeats

            facts_displayed.append(fact)
            break 

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



# DICTIONARY TO HOLD FRUITS

data = {}

for fruit in fruits:
    generate_random_fruits(fruit)

def hide_cross_lives(x, y):
    gameDisplay.blit(pygame.image.load("images/red_lives.png"), (x, y))


# DISPLAY FONT ON SCREEN

font_name = pygame.font.match_font('mario.otf')
def draw_text(display, text, size, x, y):

    font = pygame.font.Font(os.path.join(os.getcwd(), 'mario.otf'), size)
    text_surface = font.render(text, True, WHITE)
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x, y)
    gameDisplay.blit(text_surface, text_rect)



# PLAYER LIVES 

def draw_lives(display, x, y, lives, image) :

    for i in range(lives) :
        img = pygame.image.load(image)
        img_rect = img.get_rect()       #gets the (x,y) coordinates of the cross icons (lives on the the top rightmost side)
        img_rect.x = int(x + 35 * i)    #sets the next cross icon 35pixels awt from the previous one
        img_rect.y = y                  #takes care of how many pixels the cross icon should be positioned from top of the screen
        display.blit(img, img_rect)


#THEME SELECTION:


def load_theme_background(theme):
    if theme == "Summer":
        return pygame.image.load('summer.jpg')

    elif theme == "Winter":
        return pygame.image.load('winter.jpg')

    # Default to summer if theme is not recognized
    return pygame.image.load('summer.jpg')



def show_theme_selection_screen():
    facts_displayed = [] 
    gameDisplay.blit(background, (0, 0))

    draw_text(gameDisplay, "FRUIT NINJA!", 70, WIDTH / 2, HEIGHT / 5)
    draw_text(gameDisplay, "Select a Theme", 35, WIDTH / 2, HEIGHT / 2 - 45)

    # THEME SELECTION BUTTONS

    summer_button = pygame.Rect(WIDTH / 4, HEIGHT / 2, 150, 55)
    winter_button = pygame.Rect(3 * WIDTH / 4 - 150, HEIGHT / 2, 150, 55)

    pygame.draw.rect(gameDisplay, GREEN, summer_button)
    pygame.draw.rect(gameDisplay, BLUE, winter_button)

    draw_text(gameDisplay, "Summer", 20, WIDTH / 4 + 75, HEIGHT / 2 + 25)
    draw_text(gameDisplay, "Winter", 20, 3 * WIDTH / 4 - 75, HEIGHT / 2 + 25)

    gameDisplay.blit(professor_image, professor_rect)
    pygame.display.flip()

    theme_selected = False

    while not theme_selected:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                if summer_button.collidepoint(mouse_x, mouse_y):
                    theme_selected = "Summer"
                elif winter_button.collidepoint(mouse_x, mouse_y):
                    theme_selected = "Winter"
                elif professor_rect.collidepoint(mouse_x, mouse_y):
                    display_random_fact(facts_displayed)

    return theme_selected


# FRONT DISPLAY AND GAME OVER SCREEN

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

#DISPLAY TIMER

def update_timer_display():

    timer_font_size = 27
    timer_font = pygame.font.Font(os.path.join(os.getcwd(), 'mario.otf'), timer_font_size)
    timer_text = timer_font.render("Time: " + str(game_duration - current_time), True, (255, 255, 255))
    timer_text_rect = timer_text.get_rect()
    timer_text_rect.topleft = (10, 50)  # Adjust the position here
    gameDisplay.blit(timer_text, timer_text_rect)



# FUNCTION TO DISPLAY DIFFICULTY LEVEL

def display_difficulty_level(display, current_difficulty):

    difficulty_font = pygame.font.Font(os.path.join(os.getcwd(), 'mario.otf'), 16)
    difficulty_text = difficulty_font.render("Difficulty: " + current_difficulty, True, WHITE)
    difficulty_rect = difficulty_text.get_rect()
    difficulty_rect.bottomright = (WIDTH - 10, HEIGHT - 10)  # Adjust the position here
    display.blit(difficulty_text, difficulty_rect)

start_time = pygame.time.get_ticks()

# MAIN GAME LOOP

first_round = True
game_over = True        #terminates the game While loop if more than 3-Bombs are cut
game_running = True     #used to manage the game loop
game_duration = 60
current_time = 0  
theme="Summer" #default 

while game_running:

    if game_over:

        if first_round:

            theme = show_theme_selection_screen()  # Get the selected theme
            background = load_theme_background(theme)
            show_gameover_screen()
            first_round = False
        game_over = False

        player_lives = 3
        score = 0
        fruit_spawn_rate = 0.2  # Reset initial fruit spawn rate
        bomb_frequency = 0.1   # Reset initial bomb spawn frequency
        draw_lives(gameDisplay, 690, 5, player_lives, 'images/red_lives.png')
        start_time = pygame.time.get_ticks()

    

    current_time = (pygame.time.get_ticks() - start_time) // 1000  
    for event in pygame.event.get():

        # checking for closing window

        if event.type == pygame.QUIT:

            game_running = False

    gameDisplay.blit(background, (0, 0))

    if current_time >= game_duration:
        # Game over or round end logic here
        show_gameover_screen()

        game_over = True
        start_time = pygame.time.get_ticks()



    update_timer_display()

    gameDisplay.blit(score_text, (0, 0))

    draw_lives(gameDisplay, 690, 5, player_lives, 'images/red_lives.png')

    # Track player performance (you can modify this logic)
    player_accuracy = (score + 1) / (score + 2)

    # Adjust game parameters based on player performance

    if player_accuracy > 0.8:

        fruit_spawn_rate = 0.03  # Decrease fruit spawn rate for skilled players
        bomb_frequency = 0.2  # Increase bomb frequency for skilled players
        if current_difficulty != "Hard":
            current_difficulty = "Hard"

    elif player_accuracy < 0.3:

        fruit_spawn_rate = 0.3 # Increase fruit spawn rate for struggling players
        bomb_frequency = 0.02   # Decrease bomb frequency for struggling players
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