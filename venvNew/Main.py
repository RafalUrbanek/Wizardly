import pygame

pygame.init()

# VARIABLES
windowSize = (1280, 720)
gamePaneSize = (windowSize[0], windowSize[1] - 200)
drawableObjects = []
windowName = 'Game Window'
fpsCounter = 0
fpsFullSec = 0
playerSpeed = 5
initialLife = 100
initialMana = 100

lookDown = False
lookLeft = False
lookRight = False
lookUp = False

run = True

window = pygame.display.set_mode(windowSize)
clock = pygame.time.Clock()


class Button(object):
    def __init__(self, name, pos_x, pos_y, url, url_clicked):
        self.url = url
        self.url_clicked = url_clicked
        self.name = name
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.is_clicked = False
        self.wait_for_release = False

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
        self.direction = 1
        self.fineStep = 1
        self.step = 1
        self.hitbox = (gamePaneSize[0] - 24, gamePaneSize[1] - 32, 64, 48)

    def set_player_direction(self):
        key_pressed = pygame.key.get_pressed()
        mouse_pos = pygame.mouse.get_pos()
        global lookLeft
        global lookRight
        global lookDown
        global lookUp
        moving = False
        mouse_player_dist_x = mouse_pos[0] - gamePaneSize[0] / 2 - 24
        mouse_player_dist_y = mouse_pos[1] - gamePaneSize[1] / 2 - 32

        if key_pressed[pygame.K_SPACE]:
            print("distance to player in X: " + str(mouse_player_dist_x))
            print("distance to player in Y: " + str(mouse_player_dist_y))

        # sets the precedence to walking, not mouse pointing
        if not (key_pressed[pygame.K_RIGHT] or key_pressed[pygame.K_LEFT] or key_pressed[pygame.K_UP] or key_pressed[
            pygame.K_DOWN]):

            if abs(mouse_player_dist_x) - abs(mouse_player_dist_y) > 0:
                if mouse_player_dist_x > 0:
                    self.direction = 3
                else:
                    self.direction = 2
            else:
                if mouse_player_dist_y > 0:
                    self.direction = 1
                else:
                    self.direction = 4

        if key_pressed[pygame.K_LEFT] and not key_pressed[pygame.K_RIGHT]:
            moving = True
            self.direction = 2
            self.fineStep += 1
            if self.fineStep % 10 == 0:
                self.step += 1
            if self.fineStep > 40:
                self.fineStep = 1
                self.step = 1

        if key_pressed[pygame.K_RIGHT] and not key_pressed[pygame.K_LEFT]:
            moving = True
            self.direction = 3
            self.fineStep += 1
            if self.fineStep % 10 == 0:
                self.step += 1
            if self.fineStep > 40:
                self.fineStep = 1
                self.step = 1

        if key_pressed[pygame.K_UP] and not key_pressed[pygame.K_DOWN]:
            moving = True
            self.direction = 4
            self.fineStep += 1
            if self.fineStep % 10 == 0:
                self.step += 1
            if self.fineStep > 40:
                self.fineStep = 1
                self.step = 1

        if key_pressed[pygame.K_DOWN] and not key_pressed[pygame.K_UP]:
            moving = True
            self.direction = 1
            self.fineStep += 1
            if self.fineStep % 10 == 0:
                self.step += 1
            if self.fineStep > 40:
                self.fineStep = 1
                self.step = 1

        if moving is False:
            self.step = 1
            self.fineStep = 1

    def draw(self):
        """Draws the main character in the middle of the screen"""
        window.blit(get_sprite_img('pixels/sprites/13.png', self.direction, self.step), (int(gamePaneSize[0] / 2),
                                                                                         int(gamePaneSize[1] / 2)))


def draw_bottom_Pane():
    """Draws the bottom panel, including all text and buttons"""
    bottom_pane = pygame.image.load('pixels/backgrounds/bottomMainPanel.png')

    life_bar_width = int((player.maxLife / player.life) * 314)
    mana_bar_width = int((player.maxMana / player.mana) * 314)
    window.blit(bottom_pane, (0, windowSize[1] - 150))  # bottom panel
    pygame.draw.rect(window, (200, 0, 0), (23, 593, life_bar_width, 24))  # Life bar
    pygame.draw.rect(window, (0, 0, 200), (945, 593, mana_bar_width, 24))  # mana bar
    bottom_panel_btn1.draw()
    bottom_panel_btn2.draw()
    bottom_panel_btn3.draw()
    bottom_panel_btn4.draw()


def redraw_game_window():
    pygame.display.update()
    window.fill((0, 200, 0))


def get_sprite_img(source, direction, frame):
    image = pygame.image.load(source)

    if frame == 1:
        pic_pos_x = 0
    elif frame == 2:
        pic_pos_x = int(image.get_width() * 0.25)
    elif frame == 3:
        pic_pos_x = int(image.get_width() * 0.5)
    else:
        pic_pos_x = int(image.get_width() * 0.75)

    if direction == 1:
        pic_pos_y = 0
    elif direction == 2:
        pic_pos_y = int(image.get_height() * 0.25)
    elif direction == 3:
        pic_pos_y = int(image.get_height() * 0.5)
    else:
        pic_pos_y = int(image.get_height() * 0.75)

    surface = pygame.Surface((48, 64))
    surface.blit(image, (0, 0), (pic_pos_x, pic_pos_y, 48, 64))
    return surface


def mouseClickListener():
    mouse_position = pygame.mouse.get_pos()
    mouse_click = pygame.mouse.get_pressed()
    if mouse_click[0] == 1:
        if bottom_panel_btn1.pos_y <= mouse_position[1] <= bottom_panel_btn1.pos_y + 40:
            if bottom_panel_btn1.pos_x <= mouse_position[0] <= bottom_panel_btn1.pos_x + 70:
                bottom_panel_btn1.is_clicked = True
            else:
                bottom_panel_btn1.is_clicked = False
            if bottom_panel_btn2.pos_x <= mouse_position[0] <= bottom_panel_btn2.pos_x + 70:
                bottom_panel_btn2.is_clicked = True
            else:
                bottom_panel_btn2.is_clicked = False

            if bottom_panel_btn3.pos_x <= mouse_position[0] <= bottom_panel_btn3.pos_x + 70:
                bottom_panel_btn3.is_clicked = True
            else:
                bottom_panel_btn3.is_clicked = False

            if bottom_panel_btn4.pos_x <= mouse_position[0] <= bottom_panel_btn4.pos_x + 70:
                bottom_panel_btn4.is_clicked = True
            else:
                bottom_panel_btn4.is_clicked = False
    else:
        unclick_buttons()


def unclick_buttons():
    bottom_panel_btn1.is_clicked = False
    bottom_panel_btn2.is_clicked = False
    bottom_panel_btn3.is_clicked = False
    bottom_panel_btn4.is_clicked = False


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
bottom_panel_btn1 = Button('INVENTORY', 418, 660, 'pixels/backgrounds/buttonUnpressedInventory.png',
                           'pixels/backgrounds/buttonPressedInventory.png')
bottom_panel_btn2 = Button('SPELLBOOK', 542, 660, 'pixels/backgrounds/buttonUnpressedSpellbook.png',
                           'pixels/backgrounds/buttonPressedSpellbook.png')
bottom_panel_btn3 = Button('CHARACTER', 666, 660, 'pixels/backgrounds/buttonUnpressedCharacter.png',
                           'pixels/backgrounds/buttonPressedCharacter.png')
bottom_panel_btn4 = Button('OPTIONS', 790, 660, 'pixels/backgrounds/buttonUnpressedOptions.png',
                           'pixels/backgrounds/buttonPressedOptions.png')

# MAIN LOOP
while run is True:
    clock.tick(60)
    redraw_game_window()
    show_title_and_fps()
    player.set_player_direction()
    player.draw()
    draw_bottom_Pane()
    mouseClickListener()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

pygame.quit()
