class DungeonMap:

    def __init__(self, width, height, spawn_x, spawn_y):
        self.width = width
        self.height = height
        self.spawn_x = spawn_x
        self.spawn_y = spawn_y
        self.row = []
        self.map_matrix = []
        self.initialize()
        self.generate()

    def initialize(self):
        """builds initial map template"""
        for y in range(self.height):
            for x in range(self.width):
                self.row.append(0)
            self.map_matrix.append(self.row)
            self.row = []

    def generate(self):

        # generate spawn room around spawn point
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
            if 0 <= tile[0] <= self.width-1:
                if 0 <= tile[1] <= self.height-1:
                    self.map_matrix[tile[1]][tile[0]] = Cell()


class Cell:
    def __init__(self, tile_id=1, passable=True, item_id=0):
        self.tile_id = tile_id
        self.passable = passable
        self.item_id = item_id


class Test:
    map = DungeonMap(10, 5, 1, 1)
    for line in range(len(map.map_matrix)):
        for cell in range(len(map.map_matrix[line])):
            if map.map_matrix[line][cell] != 0:
                print(map.map_matrix[line][cell].tile_id, end='')
            else:
                print(map.map_matrix[line][cell], end='')
        print()


Test()
