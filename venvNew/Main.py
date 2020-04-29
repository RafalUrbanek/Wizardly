import random

import pygame
import math

pygame.init()

# VARIABLES
windowSize = (1280, 920)
gamePaneSize = (windowSize[0], windowSize[1] - 200)
drawableObjects = []
windowName = 'Game Window'
fpsCounter = 0
fpsFullSec = 0
player_default_speed = 10
initialLife = 100
initialMana = 100
windowCenter = (640, 385)
playerAngle = 0
selectTool = (0, 0, 0, 0, 0, 0, 0, 0, 0)
game_level = 1
buttonsDictionary = {}
key_pressed = {"left": False, "right": False, "up": False, "down": False}

run = True

window = pygame.display.set_mode(windowSize)
clock = pygame.time.Clock()


class Button(object):
    def __init__(self, name, pos_x, pos_y, pos_x2, pos_y2, url, url_clicked):
        self.url = url
        self.url_clicked = url_clicked
        self.name = name
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.pos_x2 = pos_x2
        self.pos_y2 = pos_y2
        self.is_clicked = False
        self.wait_for_release = False

        buttonsDictionary[self.name] = ((pos_x, pos_y), (pos_x2, pos_y2))

    def draw(self):

        if self.is_clicked is False:
            window.blit(pygame.image.load(self.url), (self.pos_x, self.pos_y))
            if self.wait_for_release:
                self.activate()
        else:
            window.blit(pygame.image.load(self.url_clicked), (self.pos_x, self.pos_y))
            self.clicked()

    def clicked(self):
        self.wait_for_release = True

    def activate(self):
        print('Button ' + self.name + ' activated')
        # what to do, when a button has been pressed
        self.wait_for_release = False


class GameObj(object):
    def __init__(self, map_tile_pos_x, map_tile_pos_y, pic_url, direction=0):
        self.map_pos_x = map_tile_pos_x
        self.map_pos_y = map_tile_pos_y
        self.abs_pos_x = -64
        self.abs_pos_y = -64
        self.pic_url = pic_url
        self.direction = direction
        self.img = self.get_obj_img()

    def get_obj_img(self):
        img = pygame.image.load(self.pic_url)
        if self.direction == 1:
            rotated_img = pygame.transform.rotate(img, 90).convert()
        elif self.direction == 2:
            rotated_img = pygame.transform.rotate(img, 180).convert()
        elif self.direction == 3:
            rotated_img = pygame.transform.rotate(img, 270).convert()
        else:
            rotated_img = img.convert()
        return rotated_img

    def background_move(self):
        """Moves all of the background objects when the player moves"""
        if key_pressed["right"]:
            self.abs_pos_x -= player.speed // 5
        if key_pressed["left"]:
            self.abs_pos_x += player.speed // 5
        if key_pressed["up"]:
            self.abs_pos_y += player.speed // 5
        if key_pressed["down"]:
            self.abs_pos_y -= player.speed // 5

    def draw(self):
        window.blit(self.img, (self.map_pos_x * 64 + windowCenter[0] + self.abs_pos_x - 32,
                               self.map_pos_y * 64 + windowCenter[1] + self.abs_pos_y - 32))


def create_map_file(map_load):
    file = open("maps/map.txt", "w+")
    for line in range(len(map_load)):
        for tile in range(len(map_load[line])):
            file.write(str(map_load[line][tile]))
        file.write("\n")
    file.close()


def path_clear(hitbox):
    tile_type = None
    corners = []
    types = []
    corners.append((gameMap.player_pos_x - player.hitbox, gameMap.player_pos_y - player.hitbox))
    corners.append((gameMap.player_pos_x + player.hitbox, gameMap.player_pos_y - player.hitbox))
    corners.append((gameMap.player_pos_x + player.hitbox, gameMap.player_pos_y + player.hitbox))
    corners.append((gameMap.player_pos_x - player.hitbox, gameMap.player_pos_y + player.hitbox))
    for point in corners:
        tile_pos_x = point[0] // 64
        tile_pos_y = point[1] // 64
        tile_type = gameMap.map_matrix[tile_pos_x][tile_pos_y]
        types.append(tile_type)
    return tile_type


class Map:
    def __init__(self, tile_width, tile_height, tile_spawn_x, tile_spawn_y):
        self.tile_width = tile_width
        self.tile_height = tile_height
        self.tile_spawn_x = tile_spawn_x
        self.tile_spawn_y = tile_spawn_y
        self.player_pos_x = (tile_spawn_x * 64) - 32
        self.player_pos_y = (tile_spawn_y * 64) - 32
        self.row = []
        self.map_matrix = []
        self.map_img = []
        self.initialize_map()
        self.line = None
        self.line_counter = None

    def load_map(self, map_pointer):
        """Loads map from the given map_pointer"""
        self.line_counter = 0
        with open(map_pointer, 'r') as mapFile:
            while True:
                self.line = mapFile.readline()
                for y in range(self.line.__len__() - 1):
                    self.map_matrix[self.line_counter][y] = int(self.line[y])
                self.line_counter += 1
                if self.line == "":
                    print("loaded all lines from map file")
                    break

                #print(self.map_matrix)

    def initialize_map(self):
        """builds initial map template"""
        for y in range(self.tile_height):
            for x in range(self.tile_width):
                self.row.append(0)
            self.map_matrix.append(self.row)
            self.row = []

    def generate_new_map(self, wall_count=3):
        """generates new random map"""
        for y in range(self.tile_height):
            for x in range(self.tile_width):
                if random.randint(0, wall_count) == wall_count:
                    self.row.append(0)
                else:
                    self.row.append(1)
            self.map_matrix.append(self.row)
            self.row = []

    def background_move(self):
        """Moves all of the background objects when the player moves"""
        if key_pressed["left"]:
            self.player_pos_x -= player.speed // 5
        if key_pressed["right"]:
            self.player_pos_x += player.speed // 5
        if key_pressed["down"]:
            self.player_pos_y += player.speed // 5
        if key_pressed["up"]:
            self.player_pos_y -= player.speed // 5

    def initialize(self):
        """method loads background images into memory for later use in draw() method"""
        self.map_img.append(self.get_bkg_surface(0))
        self.map_img.append(self.get_bkg_surface(1))

    def draw(self):
        """Draws the background based on the map_matrix"""
        for y in range(self.tile_height):
            for x in range(self.tile_width):
                if self.map_matrix[y][x] != 0:
                    window.blit(self.map_img[self.map_matrix[y][x]],
                                ((x * 64) - self.player_pos_x + windowCenter[0],
                                 (y * 64) - self.player_pos_y + windowCenter[1]))

    def get_bkg_surface(self, tile_id):
        """implementation of different tiles based on title_id required"""
        if tile_id == 0:
            pic = None
        elif tile_id == 1:
            pic = pygame.image.load('pixels/backgrounds/temp_tiles.png').convert()
        return pic


class Player(object):
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.hitbox = 16
        self.speed = player_default_speed
        self.life = initialLife
        self.maxLife = initialLife
        self.mana = initialMana
        self.maxMana = initialMana
        self.exp = 0
        self.direction = 0
        self.player_img = pygame.image.load('pixels/sprites/tempMainChar.png')

    def draw(self):
        """Draws the main character in the middle of the screen"""
        rotated_img = pygame.transform.rotate(self.player_img, self.direction)
        img_size = rotated_img.get_rect().size
        window.blit(rotated_img, (int(windowCenter[0] - img_size[0] / 2), int(windowCenter[1] - img_size[1] / 2)))
        self.direction = get_mouse_angle()


def draw_bottom_Pane():
    """Draws the bottom panel, including all text and buttons"""
    bottom_pane = pygame.image.load('pixels/backgrounds/bottomMainPanel.png')

    life_bar_width = int((player.maxLife / player.life) * 314)
    mana_bar_width = int((player.maxMana / player.mana) * 314)
    window.blit(bottom_pane, (0, windowSize[1] - 150))  # bottom panel
    pygame.draw.rect(window, (200, 0, 0), (23, 793, life_bar_width, 24))  # Life bar
    pygame.draw.rect(window, (0, 0, 200), (945, 793, mana_bar_width, 24))  # mana bar

    inventory.draw()
    character.draw()
    spellbook.draw()
    options.draw()


def redraw_game_window():
    pygame.display.update()
    window.fill((0, 0, 0))


def get_mouse_angle():
    mouse_pos = pygame.mouse.get_pos()
    x = mouse_pos[0] - windowCenter[0]
    y = -(mouse_pos[1] - windowCenter[1])
    mouse_angle = (math.atan2(y, x) * 180) / math.pi

    return int(mouse_angle + 180)


def mouseClickListener():
    mouse_position = pygame.mouse.get_pos()
    mouse_click = pygame.mouse.get_pressed()
    if mouse_click[0]:
        for btn in buttonsDictionary:
            if buttonsDictionary[btn][0][0] < mouse_position[0] < buttonsDictionary[btn][1][0] and \
                    buttonsDictionary[btn][0][1] < mouse_position[1] < buttonsDictionary[btn][1][1]:
                command = btn + ".is_clicked = True"
                exec(command)
            else:
                command = btn + ".is_clicked = False"
                exec(command)
    else:
        unclick_buttons()


def unclick_buttons():
    inventory.is_clicked = False
    spellbook.is_clicked = False
    character.is_clicked = False
    options.is_clicked = False


def show_title_and_fps():
    global fpsFullSec
    global fpsCounter
    if fpsFullSec + 1000 > pygame.time.get_ticks():
        fpsCounter += 1
    else:
        fpsFullSec += 1000
        pygame.display.set_caption(windowName + '    FPS: ' + str(fpsCounter))
        fpsCounter = 0


def keyListener():
    key = pygame.key.get_pressed()
    if key[pygame.K_RIGHT]:
        key_pressed["right"] = True
    else:
        key_pressed["right"] = False

    if key[pygame.K_LEFT]:
        key_pressed["left"] = True
    else:
        key_pressed["left"] = False

    if key[pygame.K_UP]:
        key_pressed["up"] = True
    else:
        key_pressed["up"] = False

    if key[pygame.K_DOWN]:
        key_pressed["down"] = True
    else:
        key_pressed["down"] = False


# OBJECT INSTANTIATION
player = Player(48, 64)
gameMap = Map(10, 10, 1, 1)
gameMap.initialize()
gameMap.load_map("maps/map.txt")
# create_map_file(gameMap.map_matrix)
obstacle = GameObj(3, 3, 'pixels/pack/props n decorations/generic-rpg-bridge.png')

inventory = Button('inventory', 418, 860, 488, 900, 'pixels/backgrounds/buttonUnpressedInventory.png',
                   'pixels/backgrounds/buttonPressedInventory.png')
spellbook = Button('spellbook', 542, 860, 612, 900, 'pixels/backgrounds/buttonUnpressedSpellbook.png',
                   'pixels/backgrounds/buttonPressedSpellbook.png')
character = Button('character', 666, 860, 736, 900, 'pixels/backgrounds/buttonUnpressedCharacter.png',
                   'pixels/backgrounds/buttonPressedCharacter.png')
options = Button('options', 790, 860, 860, 900, 'pixels/backgrounds/buttonUnpressedOptions.png',
                 'pixels/backgrounds/buttonPressedOptions.png')

# MAIN LOOP
while run is True:
    clock.tick(60)
    redraw_game_window()
    keyListener()
    gameMap.background_move()
    gameMap.draw()
    show_title_and_fps()
    get_mouse_angle()
    obstacle.background_move()
    obstacle.draw()
    player.draw()
    path_clear(player.hitbox)
    draw_bottom_Pane()

    mouseClickListener()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

pygame.quit()
