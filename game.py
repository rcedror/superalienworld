#Game: Super Alien World
#Author: Renato Cedro

###### CONSTANTS ######
TITLE = "Super Alien World"
TILE_SIZE = 64
ROWS = 15
COLS = 30

WIDTH = TILE_SIZE * COLS
HEIGHT = TILE_SIZE * ROWS

SPEED_HERO_H = 2
SPEED_HERO_V = 4
JUMP_FORCE = -14
GRAVITY = 0.5

ALIEN_STAND_SPEED = 0.1
ALIEN_WALK_SPEED = 0.8

BAT_FLY_SPEED = 5
BAT_FLY_ANIMATION_SPEED = 0.1
BAT_ANIMATION_SPEED = 0.1

GHOST_FLY_SPEED = 2
GHOST_FLY_ANIMATION_SPEED = 0.1
GHOST_ANIMATION_SPEED = 0.1

BUTTON_ANIMATION_SPEED = 0.3
BUTTON_START_POSITION = (5 * TILE_SIZE, 5 * TILE_SIZE)

ALIEN_START_POSITION = (50, 785)
BAT_START_POSITION = (WIDTH, 595)
GHOST_START_POSITION = (WIDTH, 785)

###### HERO ######
alien = Actor('alien')
alien.topright = 0, 10
alien.pos = ALIEN_START_POSITION
alien.vx = ALIEN_WALK_SPEED
alien.vy = ALIEN_WALK_SPEED
alien_speed = ALIEN_WALK_SPEED
alien.images = ['alien', 'alien_walk1','alien_walk1']

###### BUTTON ######
button = Actor('buttongreen')
button.left, button.bottom = BUTTON_START_POSITION

###### ENEMY ######
# bat1
bat1 = Actor('bat_1')
bat1.topright = 0, 10
bat1.pos = BAT_START_POSITION
bat1_speed = BAT_FLY_SPEED
bat1.images = ['bat_1', 'bat_2']

# bat2
bat2 = Actor('bat_1')
bat2.topright = 0, 10
bat2.pos = (WIDTH, 160)
bat2_speed = BAT_FLY_SPEED
bat2.images = ['bat_1', 'bat_2']

# GHOST
ghost = Actor('ghost_1')
ghost.topright = 0, 10
ghost.pos = GHOST_START_POSITION
ghost_speed = GHOST_FLY_SPEED
ghost.images = ['ghost_1', 'ghost_2']

###### BUILD STAGE ######

def build(filename, tile_size):
  
    with open(filename, "r") as f:
        contents = f.read().splitlines()
    
    contents = [c.split(",") for c in contents]
    
    for row in range(len(contents)):

        for col in range(len(contents[0])):
            
            val = contents[row][col]
           
            if val.isdigit() or (val[0] == "-" and val[1:].isdigit()):
                contents[row][col] = int(val)
    
    items = []

    for row in range(len(contents)):

        for col in range(len(contents[0])):
 
            tile_num = contents[row][col]
         
            if tile_num != -1:
              
                item = Actor(f"slice{tile_num:02d}_{tile_num:02d}")
                
                item.topleft = (tile_size * col, tile_size * row)
               
                items.append(item)
    return items

platforms = build("platformer.csv", TILE_SIZE)


# ----------------- COLISIONS -----------------------
def collision_platform_x():

    platform_left = False
    platform_right = False 

    for tile in platforms:
        if alien.colliderect(tile):

            if alien.vx < 0:

                alien.left = tile.right
                platform_left = True

            elif alien.vx > 0:

                alien.right = tile.left 
                platform_right = True

    return platform_left, platform_right


def collision_platform_y():

    platform_under = False 
    platform_over = False 

    for tile in platforms:

        if alien.colliderect(tile):
            
            if alien.vy > 0:
                alien.bottom = tile.top
                alien.vy = 0
                platform_under = True

            elif alien.vy < 0:
                alien.top = tile.bottom 
                alien.vy = 0
                platform_over = True

    return platform_under, platform_over


###### VARIABLES ######
lives = 3
game_over = False

###### COLORS ######
white = 255, 255, 255
 
###### ANIMATIONS ######
def set_alien_hurt():
    alien.image = 'alien_hurt'
    sounds.eep.play()
    clock.schedule_unique(set_alien_normal, 1.0)

def set_alien_normal():
    alien.image = 'alien'

def set_alien_walk():
    alien.image = 'alien_walk2'
    clock.schedule_unique(set_alien_normal, 0.05)

###### MOVIMENTATION ######
def update():
    global lives, game_over, BAT_FLY_SPEED, GHOST_FLY_SPEED

    # bat1
    bat1.left -= BAT_FLY_SPEED
    if bat1.left < 0:
        bat1.right = WIDTH
    
    # bat1
    bat2.left -= BAT_FLY_SPEED
    if bat2.left < 0:
        bat2.right = WIDTH

    # GHOST
    ghost.left -= GHOST_FLY_SPEED
    if ghost.left < 0:
        ghost.right = WIDTH
    
    if keyboard.left:
        alien.x -= ALIEN_WALK_SPEED
        set_alien_walk()
    if keyboard.right:
        alien.x += ALIEN_WALK_SPEED
        set_alien_walk()     


    alien.vy = alien.vy + GRAVITY

    alien.y = alien.y + alien.vy

    platform_under, platform_over = collision_platform_y()

    if keyboard.space:

        if platform_under:
            alien.vy = JUMP_FORCE
            sounds.eep.play()

    alien.vx = 0

    if keyboard.left:
        alien.vx = -ALIEN_WALK_SPEED 
    
    if keyboard.right:
        alien.vx = ALIEN_WALK_SPEED 

    alien.x = alien.x + alien.vx

    platform_left, platform_right = collision_platform_x()

    if alien.left < 0:
        alien.left = 0

    if alien.right > WIDTH:
        alien.right = WIDTH

    if alien.colliderect(button):
        alien.pos = ALIEN_START_POSITION

    if alien.colliderect(bat1 or bat2 or ghost):
        lives -= 1
        alien.pos = ALIEN_START_POSITION


def draw():

    if game_over:
        screen.draw.text('GAME OVER', (400,200), color=(white), fontsize=60)
    else:
        screen.clear()
        alien.draw()
        bat1.draw()
        bat2.draw()
        ghost.draw()
        button.draw()
        for platform in platforms:
            platform.draw()
        screen.draw.text('LIFE : ' + str(lives), (15,10), color=(white), fontsize=30)


###### RULES ######
