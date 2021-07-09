import numpy as np
from tcod.console import Console
from tcod.tileset import CHARMAP_CP437

import tile_types

class GameMap:
    def __init__(self, width: int, height: int):
        self.width, self.height = width, height
        self.tiles = np.full((width, height), fill_value = tile_types.wall, order = "F")

    def in_bounds(self, x: int, y: int) -> bool:
        """ Return True if x and y are inside of the bounds of this map. """
        return 0 <= x < self.width and 0 <= y < self.height

    # Really unoptimized bitmask renderer based on the RLTK Tutorial
    def render(self, console: Console) -> None:
        # The original, FAST, NumPy renderer
        # console.tiles_rgb[0: self.width, 0: self.height] = self.tiles["dark"]

        # The new, SLOW, bitmask renderer
        
        for x in range(0, self.width):
            for y in range(0, self.height):
                console.tiles_rgb[x, y] = self.tiles[x, y]["dark"]
                if self.tiles[x, y] == tile_types.wall:
                    console.tiles_rgb[x, y][0] = self.wall_glyph(x, y)

    def is_revealed_and_wall(self, x: int, y: int) -> bool:
        return self.tiles[x, y] == tile_types.wall

    def wall_glyph(self, x: int, y: int) -> int:
        if x < 1 or x > self.width - 2 or y < 1 or y > self.height - 2:
            return CHARMAP_CP437[35]

        mask = 0
        if self.is_revealed_and_wall(x, y - 1):
            mask += 1
        if self.is_revealed_and_wall(x, y + 1):
            mask += 2
        if self.is_revealed_and_wall(x - 1, y):
            mask += 4
        if self.is_revealed_and_wall(x + 1, y):
            mask += 8

        tiles = {
            0: 9,       # No neighbors
            1: 186,     # Wall N
            2: 186,     # Wall S
            3: 186,     # Wall NS
            4: 205,     # Wall W
            5: 188,     # Wall NW
            6: 187,     # Wall SW
            7: 185,     # Wall NSW
            8: 205,     # Wall E
            9: 200,     # Wall NE
            10: 201,    # Wall SE
            11: 204,    # Wall NSE
            12: 205,    # Wall EW
            13: 202,    # Wall SWE
            14: 203,    # Wall NWE
            15: 206     # Wall on all sides
        }

        return CHARMAP_CP437[tiles.get(mask, 35)]
