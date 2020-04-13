import pygame

pygame.init()

# VARIABLES
windowSize = (1280, 720)
drawableObjects = []
windowName = 'Game Window'
fpsCounter = 0
fpsFullSec = 0
playerSpeed = 5

lookDown = False
lookLeft = False
lookRight = False
lookUp = False

run = True

window = pygame.display.set_mode(windowSize)
clock = pygame.time.Clock()


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
        self.direction = 1
        self.fineStep = 1
        self.step = 1
        self.hitbox = (windowSize[0] - 24, windowSize[1] - 32, 64, 48)

    def set_player_direction(self):
        key_pressed = pygame.key.get_pressed()
        mouse_pos = pygame.mouse.get_pos()
        global lookLeft
        global lookRight
        global lookDown
        global lookUp
        moving = False
        mouse_player_dist_x = mouse_pos[0] - windowSize[0] / 2 - 24
        mouse_player_dist_y = mouse_pos[1] - windowSize[1] / 2 - 32

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
        window.blit(get_img('pixels/sprites/13.png', self.direction, self.step), (int(windowSize[0] / 2),
                                                                                  int(windowSize[1] / 2)))


def redraw_game_window():
    pygame.display.update()
    window.fill((0, 200, 0))


def get_img(source, direction, frame):
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
# MAIN LOOP
while run is True:
    clock.tick(60)
    redraw_game_window()
    show_title_and_fps()
    player.set_player_direction()
    player.draw()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

pygame.quit()
