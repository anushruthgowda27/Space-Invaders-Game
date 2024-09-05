#arjun m
import pygame
import random
import math
from pygame import mixer
import time

# game constants
WIDTH = 800
HEIGHT = 600

# global variables
running = True
pause_state = 0
score = 0
highest_score = 0
life = 3
kills = 0
difficulty = 1
level = 1
max_kills_to_difficulty_up = 5
max_difficulty_to_level_up = 5
initial_player_velocity = 3.0
initial_enemy_velocity = 1.0
weapon_shoot_velocity = 5.0
total_time = 0

# game objects
player = type('Player', (), {})()
bullet = type('Bullet', (), {})()
enemies = []
lasers = []

# initialize pygame
pygame.init()

# Input key states (keyboard)
LEFT_ARROW_KEY_PRESSED = 0
RIGHT_ARROW_KEY_PRESSED = 0
UP_ARROW_KEY_PRESSED = 0
SPACE_BAR_PRESSED = 0
ENTER_KEY_PRESSED = 0
ESC_KEY_PRESSED = 0

# create display window
window = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Space Invaders")

# game sounds
pause_sound = None
level_up_sound = None
weapon_annihilation_sound = None
game_over_sound = None

# create background
background_img = pygame.image.load("res/images/background.jpg")
background_music_paths = ["res/sounds/Space_Invaders_Music.ogg",
                          "res/sounds/Space_Invaders_Music_x2.ogg",
                          "res/sounds/Space_Invaders_Music_x4.ogg",
                          "res/sounds/Space_Invaders_Music_x8.ogg",
                          "res/sounds/Space_Invaders_Music_x16.ogg",
                          "res/sounds/Space_Invaders_Music_x32.ogg"]

# create player class
class Player:#ankitha
    def __init__(self, img_path, width, height, x, y, dx, dy, kill_sound_path):
        self.img_path = img_path
        self.img = pygame.image.load(self.img_path)
        self.width = width
        self.height = height
        self.x = x
        self.y = y
        self.dx = dx
        self.dy = dy
        self.kill_sound_path = kill_sound_path
        self.kill_sound = mixer.Sound(self.kill_sound_path)

    def draw(self):
        window.blit(self.img, (self.x, self.y))

# create enemy class
class Enemy:#anushruth
    def __init__(self, img_path, width, height, x, y, dx, dy, kill_sound_path):
        self.img_path = img_path
        self.img = pygame.image.load(self.img_path)
        self.width = width
        self.height = height
        self.x = x
        self.y = y
        self.dx = dx
        self.dy = dy
        self.kill_sound_path = kill_sound_path
        self.kill_sound = mixer.Sound(self.kill_sound_path)

    def draw(self):
        window.blit(self.img, (self.x, self.y))

# create bullet class
class Bullet:#arjun s
    def __init__(self, img_path, width, height, x, y, dx, dy, fire_sound_path):
        self.img_path = img_path
        self.img = pygame.image.load(self.img_path)
        self.width = width
        self.height = height
        self.x = x
        self.y = y
        self.dx = dx
        self.dy = dy
        self.fired = False
        self.fire_sound_path = fire_sound_path
        self.fire_sound = mixer.Sound(self.fire_sound_path)

    #displays the bullet on the screen
    def draw(self):
        if self.fired:
            window.blit(self.img, (self.x, self.y))


# create laser class
class Laser:#arjun m
    def __init__(self, img_path, width, height, x, y, dx, dy, shoot_probability, relaxation_time, beam_sound_path):
        self.img_path = img_path
        self.img = pygame.image.load(self.img_path)
        self.width = width
        self.height = height
        self.x = x
        self.y = y
        self.dx = dx
        self.dy = dy
        self.beamed = False
        self.shoot_probability = shoot_probability
        self.shoot_timer = 0
        self.relaxation_time = relaxation_time
        self.beam_sound_path = beam_sound_path
        self.beam_sound = mixer.Sound(self.beam_sound_path)

    #displays the laser on the screen
    def draw(self):
        if self.beamed:
            window.blit(self.img, (self.x, self.y))


def scoreboard():#anushruth
    x_offset = 10
    y_offset = 10
    # set font type and size
    font = pygame.font.SysFont("arial", 16)

    # render font and text sprites
    score_sprint = font.render("SCORE : " + str(score), True, (255, 255, 255))
    highest_score_sprint = font.render("HI-SCORE : " + str(highest_score), True, (255, 255, 255))
    level_sprint = font.render("LEVEL : " + str(level), True, (255, 255, 255))
    difficulty_sprint = font.render("DIFFICULTY : " + str(difficulty), True, (255, 255, 255))
    life_sprint = font.render("LIFE LEFT : " + str(life) + " | " + ("@ " * life), True, (255, 255, 255))

    # place the font sprites on the screen
    window.blit(score_sprint, (x_offset, y_offset))
    window.blit(highest_score_sprint, (x_offset, y_offset + 20))
    window.blit(level_sprint, (x_offset, y_offset + 40))
    window.blit(difficulty_sprint, (x_offset, y_offset + 60))
    window.blit(life_sprint, (x_offset, y_offset + 80))


#function to check for collision of 2 objects
def collision_check(object1, object2):#arjun s
    x1_cm = object1.x + object1.width / 2
    y1_cm = object1.y + object1.width / 2
    x2_cm = object2.x + object2.width / 2
    y2_cm = object2.y + object2.width / 2
    distance = math.sqrt(math.pow((x2_cm - x1_cm), 2) + math.pow((y2_cm - y1_cm), 2))
    return distance < ((object1.width + object2.width) / 2)

def level_up():#ankitha
    global life
    global level
    global difficulty
    global max_difficulty_to_level_up
    level_up_sound.play()
    level += 1
    life += 1       # grant a life
    difficulty = 1  # reset difficulty
    if level % 3 == 0:
        player.dx += 1
        bullet.dy += 1
        max_difficulty_to_level_up += 1
        for each_laser in lasers:
            each_laser.shoot_probability += 0.1
            if each_laser.shoot_probability > 1.0:
                each_laser.shoot_probability = 1.0
    if max_difficulty_to_level_up > 7:
        max_difficulty_to_level_up = 7

    font = pygame.font.SysFont("freesansbold", 64)
    gameover_sprint = font.render("LEVEL UP", True, (255, 255, 255))
    window.blit(gameover_sprint, (WIDTH / 2 - 120, HEIGHT / 2 - 32))
    pygame.display.update()
    init_game()
    time.sleep(1.0)


def respawn(enemy_obj):#anushruth
    enemy_obj.x = random.randint(0, (WIDTH - enemy_obj.width))
    enemy_obj.y = random.randint(((HEIGHT / 10) * 1 - (enemy_obj.height / 2)),
                                 ((HEIGHT / 10) * 4 - (enemy_obj.height / 2)))


def kill_enemy(player_obj, bullet_obj, enemy_obj):#anushruth
    global score
    global kills
    global difficulty
    bullet_obj.fired = False
    enemy_obj.kill_sound.play()
    bullet_obj.x = player_obj.x + player_obj.width / 2 - bullet_obj.width / 2
    bullet_obj.y = player_obj.y + bullet_obj.height / 2
    score = score + 10 * difficulty * level
    kills += 1
    if kills % max_kills_to_difficulty_up == 0:
        difficulty += 1
        if (difficulty == max_difficulty_to_level_up) and (life != 0):
            level_up()
        #init_background_music()
    print("Score:", score)
    print("level:", level)
    print("difficulty:", difficulty)
    respawn(enemy_obj)


def rebirth(player_obj):#ankitha
    player_obj.x = (WIDTH / 2) - (player_obj.width / 2)
    player_obj.y = (HEIGHT / 10) * 9 - (player_obj.height / 2)


def gameover_screen():#arjun srinivas
    scoreboard()
    font = pygame.font.SysFont("freesansbold", 64)
    gameover_sprint = font.render("GAME OVER", True, (255, 255, 255))
    window.blit(gameover_sprint, (WIDTH / 2 - 140, HEIGHT / 2 - 32))
    pygame.display.update()

    mixer.music.stop()
    game_over_sound.play()
    time.sleep(5.0)
    mixer.quit()


def gameover():#arjun s
    global running
    global score
    global highest_score

    if score > highest_score:
        highest_score = score

    # console display
    print("----------------")
    print("GAME OVER !!")
    print("----------------")
    print("you died at")
    print("Level:", level)
    print("difficulty:", difficulty)
    print("Your Score:", score)
    print("----------------")
    print("Try Again !!")
    print("----------------")
    running = False
    gameover_screen()


def kill_player(player_obj, enemy_obj, laser_obj):#ankitha
    global life
    laser_obj.beamed = False
    player_obj.kill_sound.play()
    laser_obj.x = enemy_obj.x + enemy_obj.width / 2 - laser_obj.width / 2
    laser_obj.y = enemy_obj.y + laser_obj.height / 2
    life -= 1
    print("Life Left:", life)
    if life > 0:
        rebirth(player_obj)
    else:
        gameover()


def destroy_weapons(player_obj, bullet_obj, enemy_obj, laser_obj):#arjun m
    bullet_obj.fired = False
    laser_obj.beamed = False
    weapon_annihilation_sound.play()
    bullet_obj.x = player_obj.x + player_obj.width / 2 - bullet_obj.width / 2
    bullet_obj.y = player_obj.y + bullet_obj.height / 2
    laser_obj.x = enemy_obj.x + enemy_obj.width / 2 - laser_obj.width / 2
    laser_obj.y = enemy_obj.y + laser_obj.height / 2


def pause_game():#arjun m 
    pause_sound.play()
    scoreboard()
    font = pygame.font.SysFont("freesansbold", 64)
    gameover_sprint = font.render("PAUSED", True, (255, 255, 255))
    window.blit(gameover_sprint, (WIDTH / 2 - 80, HEIGHT / 2 - 32))
    pygame.display.update()
    mixer.music.pause()


def init_game():#arjun m
    global pause_sound
    global level_up_sound
    global game_over_sound
    global weapon_annihilation_sound

    pause_sound = mixer.Sound("res/sounds/pause.wav")
    level_up_sound = mixer.Sound("res/sounds/1up.wav")
    game_over_sound = mixer.Sound("res/sounds/gameover.wav")
    weapon_annihilation_sound = mixer.Sound("res/sounds/annihilation.wav")

    # player
    player_img_path = "res/images/spaceship.png"  # 64 x 64 px image
    player_width = 64
    player_height = 64
    player_x = (WIDTH / 2) - (player_width / 2)
    player_y = (HEIGHT / 10) * 9 - (player_height / 2)
    player_dx = initial_player_velocity
    player_dy = 0
    player_kill_sound_path = "res/sounds/explosion.wav"

    global player
    player = Player(player_img_path, player_width, player_height, player_x, player_y, player_dx, player_dy,
                    player_kill_sound_path)

    # bullet
    bullet_img_path = "res/images/bullet.png"  # 32 x 32 px image
    bullet_width = 32
    bullet_height = 32
    bullet_x = player_x + player_width / 2 - bullet_width / 2
    bullet_y = player_y + bullet_height / 2
    bullet_dx = 0
    bullet_dy = weapon_shoot_velocity
    bullet_fire_sound_path = "res/sounds/gunshot.wav"

    global bullet
    bullet = Bullet(bullet_img_path, bullet_width, bullet_height, bullet_x, bullet_y, bullet_dx, bullet_dy,
                    bullet_fire_sound_path)

    # enemy (number of enemy = level number)
    enemy_img_path = "res/images/enemy.png"  # 64 x 64 px image
    enemy_width = 64
    enemy_height = 64
    enemy_dx = initial_enemy_velocity
    enemy_dy = (HEIGHT / 10) / 2
    enemy_kill_sound_path = "res/sounds/enemykill.wav"

    # laser beam (equals number of enemies and retains corresponding enemy position)
    laser_img_path = "res/images/beam.png"  # 24 x 24 px image
    laser_width = 24
    laser_height = 24
    laser_dx = 0
    laser_dy = weapon_shoot_velocity
    shoot_probability = 0.3
    relaxation_time = 100
    laser_beam_sound_path = "res/sounds/laser.wav"

    global enemies
    global lasers

    enemies.clear()
    lasers.clear()

    for lev in range(level):
        enemy_x = random.randint(0, (WIDTH - enemy_width))
        enemy_y = random.randint(((HEIGHT / 10) * 1 - (enemy_height / 2)), ((HEIGHT / 10) * 4 - (enemy_height / 2)))
        laser_x = enemy_x + enemy_width / 2 - laser_width / 2
        laser_y = enemy_y + laser_height / 2

        enemy_obj = Enemy(enemy_img_path, enemy_width, enemy_height, enemy_x, enemy_y, enemy_dx, enemy_dy,
                          enemy_kill_sound_path)
        enemies.append(enemy_obj)

        laser_obj = Laser(laser_img_path, laser_width, laser_height, laser_x, laser_y, laser_dx, laser_dy,
                          shoot_probability, relaxation_time, laser_beam_sound_path)
        lasers.append(laser_obj)

init_game()

runned_once = False

# main game loop begins
while running:#anushruth
    # background
    window.fill((0, 0, 0))
    window.blit(background_img, (0, 0))

    # register events
    for event in pygame.event.get():
        # Quit Event
        if event.type == pygame.QUIT:
            running = False

        # Keypress Down Event #anushruth
        if event.type == pygame.KEYDOWN:
            # Left Arrow Key down
            if event.key == pygame.K_LEFT:
                print("LOG: Left Arrow Key Pressed Down")
                LEFT_ARROW_KEY_PRESSED = 1
            # Right Arrow Key down
            if event.key == pygame.K_RIGHT:
                print("LOG: Right Arrow Key Pressed Down")
                RIGHT_ARROW_KEY_PRESSED = 1
            # Up Arrow Key down
            if event.key == pygame.K_UP:
                print("LOG: Up Arrow Key Pressed Down")
                UP_ARROW_KEY_PRESSED = 1
            # Space Bar down
            if event.key == pygame.K_SPACE:
                print("LOG: Space Bar Pressed Down")
                SPACE_BAR_PRESSED = 1
            # Enter Key down ("Carriage RETURN key" from old typewriter lingo)
            if event.key == pygame.K_RETURN:
                print("LOG: Enter Key Pressed Down")
                ENTER_KEY_PRESSED = 1
                pause_state += 1
            # Esc Key down
            if event.key == pygame.K_ESCAPE:
                print("LOG: Escape Key Pressed Down")
                ESC_KEY_PRESSED = 1
                pause_state += 1

        # Keypress Up Event #anushruth
        if event.type == pygame.KEYUP:
            # Right Arrow Key up
            if event.key == pygame.K_RIGHT:
                print("LOG: Right Arrow Key Released")
                RIGHT_ARROW_KEY_PRESSED = 0
            # Left Arrow Key up
            if event.key == pygame.K_LEFT:
                print("LOG: Left Arrow Key Released")
                LEFT_ARROW_KEY_PRESSED = 0
            # Up Arrow Key up
            if event.key == pygame.K_UP:
                print("LOG: Up Arrow Key Released")
                UP_ARROW_KEY_PRESSED = 0
            # Space Bar up
            if event.key == pygame.K_SPACE:
                print("LOG: Space Bar Released")
                SPACE_BAR_PRESSED = 0
            # Enter Key up ("Carriage RETURN key" from old typewriter lingo)
            if event.key == pygame.K_RETURN:
                print("LOG: Enter Key Released")
                ENTER_KEY_PRESSED = 0
            # Esc Key up
            if event.key == pygame.K_ESCAPE:
                print("LOG: Escape Key Released")
                ESC_KEY_PRESSED = 0

    # check for pause game event #ankitha
    if pause_state == 2:
        pause_state = 0
        runned_once = False
        mixer.music.unpause()
    if pause_state == 1:
        if not runned_once:
            runned_once = True
            pause_game()
        continue
    # manipulate game objects based on events and player actions
    # player spaceship movement
    if RIGHT_ARROW_KEY_PRESSED:
        player.x += player.dx
    if LEFT_ARROW_KEY_PRESSED:
        player.x -= player.dx
    # bullet firing #arjun s
    if (SPACE_BAR_PRESSED or UP_ARROW_KEY_PRESSED) and not bullet.fired:
        bullet.fired = True
        bullet.fire_sound.play()
        bullet.x = player.x + player.width / 2 - bullet.width / 2
        bullet.y = player.y + bullet.height / 2
    # bullet movement
    if bullet.fired:
        bullet.y -= bullet.dy

    # iter through every enemies and lasers #arjun m
    for i in range(len(enemies)):
        # laser beaming
        if not lasers[i].beamed:
            lasers[i].shoot_timer += 1
            if lasers[i].shoot_timer == lasers[i].relaxation_time:
                lasers[i].shoot_timer = 0
                random_chance = random.randint(0, 100)
                if random_chance <= (lasers[i].shoot_probability * 100):
                    lasers[i].beamed = True
                    lasers[i].beam_sound.play()
                    lasers[i].x = enemies[i].x + enemies[i].width / 2 - lasers[i].width / 2
                    lasers[i].y = enemies[i].y + lasers[i].height / 2
        # enemy movement
        enemies[i].x += enemies[i].dx * float(2 ** (difficulty - 1))
        # laser movement
        if lasers[i].beamed:
            lasers[i].y += lasers[i].dy

    # collision check
    for i in range(len(enemies)):
        bullet_enemy_collision = collision_check(bullet, enemies[i])
        if bullet_enemy_collision:
            kill_enemy(player, bullet, enemies[i])

    for i in range(len(lasers)):
        laser_player_collision = collision_check(lasers[i], player)
        if laser_player_collision:
            kill_player(player, enemies[i], lasers[i])

    for i in range(len(enemies)):
        enemy_player_collision = collision_check(enemies[i], player)
        if enemy_player_collision:
            kill_enemy(player, bullet, enemies[i])
            kill_player(player, enemies[i], lasers[i])

    for i in range(len(lasers)):
        bullet_laser_collision = collision_check(bullet, lasers[i])
        if bullet_laser_collision:
            destroy_weapons(player, bullet, enemies[i], lasers[i])

    # boundary check: 0 <= x <= WIDTH, 0 <= y <= HEIGHT
    # player spaceship
    if player.x < 0:
        player.x = 0
    if player.x > WIDTH - player.width:
        player.x = WIDTH - player.width
    # enemy
    for enemy in enemies:
        if enemy.x <= 0:
            enemy.dx = abs(enemy.dx) * 1
            enemy.y += enemy.dy
        if enemy.x >= WIDTH - enemy.width:
            enemy.dx = abs(enemy.dx) * -1
            enemy.y += enemy.dy
    # bullet
    if bullet.y < 0:
        bullet.fired = False
        bullet.x = player.x + player.width / 2 - bullet.width / 2
        bullet.y = player.y + bullet.height / 2
    # laser
    for i in range(len(lasers)):
        if lasers[i].y > HEIGHT:
            lasers[i].beamed = False
            lasers[i].x = enemies[i].x + enemies[i].width / 2 - lasers[i].width / 2
            lasers[i].y = enemies[i].y + lasers[i].height / 2

    # create frame by placing objects on the surface
    scoreboard()
    for laser in lasers:
        laser.draw()
    for enemy in enemies:
        enemy.draw()
    bullet.draw()
    player.draw()

    # render the display
    pygame.display.update()