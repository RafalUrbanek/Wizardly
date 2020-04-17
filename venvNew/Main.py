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
playerSpeed = 5
initialLife = 100
initialMana = 100
windowCenter = (640, 385)
playerAngle = 0
selectTool = (0, 0, 0, 0, 0, 0, 0, 0, 0)
buttonsDictionary = {}

lookDown = False
lookLeft = False
lookRight = False
lookUp = False

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
    def __init__(self, pos_x, pos_y, pic_id):
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.pic_id = pic_id

    def background_move(self):
        """Moves all of the background objects when the player moves"""

        if lookDown is True:
            self.pos_y -= playerSpeed
        if lookLeft is True:
            self.pos_x += playerSpeed
        if lookRight is True:
            self.pos_x -= playerSpeed
        if lookUp is True:
            self.pos_y += playerSpeed

    def get_obj_graphics(self):
        print("given ID: " + str(self.pic_id))
        # method should return surface with the correct picture for specific id


class Player(object):
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.vel = playerSpeed
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
    window.fill((0, 200, 0))


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
                print("button pressed")
                command = btn + ".is_clicked = True"
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


# OBJECTS

player = Player(48, 64)
testObj = GameObj(20, 20, 2)
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
    show_title_and_fps()
    (get_mouse_angle())
    player.draw()
    draw_bottom_Pane()
    mouseClickListener()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

pygame.quit()
