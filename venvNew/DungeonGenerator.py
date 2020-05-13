import math
import random


class DungeonMap:

    def __init__(self, width, height, spawn_x, spawn_y):
        self.width = width
        self.height = height
        self.spawn_x = spawn_x
        self.spawn_y = spawn_y
        self.row = []
        self.map_matrix = []
        self.stairs_pos = []
        self.initialize()
        self.generate()

    def initialize(self):
        """builds initial map template"""
        for y in range(self.height):
            for x in range(self.width):
                self.row.append(Cell(0, False))
            self.map_matrix.append(self.row)
            self.row = []
        print("map initialized, size: rows " + str(len(self.map_matrix)) + "  lines " + str(len(self.map_matrix[0])))

    def percent_used(self):
        used = 0

        for line in range(len(self.map_matrix)):
            for cell in range(len(self.map_matrix[line])):
                field = self.map_matrix[line][cell]
                if field.passable:
                    used += 1
        return (used * 100) // (self.width * self.height)

    def generate(self):

        # generate 3x3 spawn room around spawn point
        spawn_room = [[self.spawn_x - 1, self.spawn_y - 1],
                      [self.spawn_x, self.spawn_y - 1],
                      [self.spawn_x + 1, self.spawn_y - 1],
                      [self.spawn_x - 1, self.spawn_y],
                      [self.spawn_x, self.spawn_y],
                      [self.spawn_x + 1, self.spawn_y],
                      [self.spawn_x - 1, self.spawn_y + 1],
                      [self.spawn_x, self.spawn_y + 1],
                      [self.spawn_x + 1, self.spawn_y + 1]]

        for tile in spawn_room:
            if 0 <= tile[0] <= self.width - 1:
                if 0 <= tile[1] <= self.height - 1:
                    self.map_matrix[tile[1]][tile[0]] = Cell()
        print("spawn room generated")

        # generate random rooms
        attempts = 100
        while attempts > 0 and self.percent_used() < 70:
            room_size = self.get_room_size()
            room_spawn_x = random.randint(room_size // 2 + 1, self.width - room_size // 2 - 1)
            room_spawn_y = random.randint(room_size // 2 + 1, self.height - room_size // 2 - 1)

            if self.test_room_position(room_spawn_x, room_spawn_y, room_size):
                self.build_room(room_spawn_x, room_spawn_y, room_size)
            attempts -= 1
        print("rooms generated")

        while True:
            valid = True
            position = (random.randint(0, self.width-4), random.randint(0, self.height-4))
            for y in range(position[1], position[1] + 4):
                for x in range(position[0], position[0] + 4):
                    if self.map_matrix[y][x].tile_id == 0:
                        valid = False
                        break
            if valid:
                self.stairs_pos = [position[0] + 2, position[1] + 2]
                self.map_matrix[self.stairs_pos[1]][self.stairs_pos[0]] = Cell(3)
                break

    def test_room_position(self, room_spawn_x, room_spawn_y, room_size):
        valid = True
        for y in range(room_spawn_y - (room_size // 2) - 1, room_spawn_y + (room_size // 2) + 1):
            for x in range(room_spawn_x - (room_size // 2) - 1, room_spawn_x + (room_size // 2) + 1):
                if x < len(self.map_matrix[0]) and y < (len(self.map_matrix)):
                    if self.map_matrix[y][x].tile_id != 0:
                        valid = False
                        break
        return valid

    def build_room(self, room_spawn_x, room_spawn_y, room_size):
        for y in range(room_spawn_y - (room_size // 2), room_spawn_y + (room_size // 2)):
            for x in range(room_spawn_x - (room_size // 2), room_spawn_x + (room_size // 2)):
                self.map_matrix[y][x] = Cell()

    def get_room_size(self):
        if self.width < 20 or self.height < 20:
            return random.randint(2, 3) * 2
        elif self.width < 40 or self.height < 40:
            return random.randint(3, 5) * 2
        elif self.width < 80 or self.height < 80:
            return random.randint(3, 7) * 2
        else:
            return random.randint(4, 9) * 2


class Cell:
    def __init__(self, tile_id=1, passable=True, item_id=0):
        self.tile_id = tile_id
        self.passable = passable
        self.item_id = item_id


class PrintMap:
    """Temporary class for visualising generated data"""
    map = DungeonMap(40, 19, 1, 1)
    for line in range(len(map.map_matrix)):
        for cell in range(len(map.map_matrix[line])):
            if map.map_matrix[line][cell].tile_id == 1:
                print(" ", end='')
            elif map.map_matrix[line][cell].tile_id == 0:
                print(u'\u2588', end='')
            elif map.map_matrix[line][cell].tile_id == 3:  # temporary symbol for stairs
                print(u'\u2599', end='')
            elif map.map_matrix[line][cell].tile_id == 2:  # temporary symbol for corridor
                print(u'\u2591', end='')
        print()


PrintMap()
