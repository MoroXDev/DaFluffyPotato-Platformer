import pygame
import json
AUTOTILE_MAP = {
    tuple(sorted([(1, 0), (0, 1)])): 0,
    tuple(sorted([(1, 0), (0, 1), (-1, 0)])): 1,
    tuple(sorted([(-1, 0), (0, 1)])): 2, 
    tuple(sorted([(-1, 0), (0, -1), (0, 1)])): 3,
    tuple(sorted([(-1, 0), (0, -1)])): 4,
    tuple(sorted([(-1, 0), (0, -1), (1, 0)])): 5,
    tuple(sorted([(1, 0), (0, -1)])): 6,
    tuple(sorted([(1, 0), (0, -1), (0, 1)])): 7,
    tuple(sorted([(1, 0), (-1, 0), (0, 1), (0, -1)])): 8,
}
NEIGHBOUR_OFFSET = [(0, 0), (1, 1), (-1, -1), (-1, 1), (1, -1), (1, 0), (0, 1), (0, -1), (-1, 0)]
PHYSCIS_TILES = {"grass", "stone"}
AUTOTILE_TYPES = {"grass", "stone"}

class Tilemap:
  def __init__(self, game, tile_size = 16):
    self.game = game
    self.tile_size = tile_size
    self.tilemap = {}
    self.offgrid_tiles = []

  def extract(self, id_pairs, keep = False):
    matches = []
    for tile in self.offgrid_tiles.copy():
      if (tile["type"], tile["variant"]) in id_pairs:
        matches.append(tile.copy())
        if not keep:
          self.offgrid_tiles.remove(tile)

    for loc in self.tilemap.copy():
      tile = self.tilemap[loc]
      if (tile["type"], tile["variant"]) in id_pairs:
        matches.append(tile.copy())
        matches[-1]["pos"] = matches[-1]["pos"].copy()
        matches[-1]["pos"][0] *= self.tile_size
        matches[-1]["pos"][1] *= self.tile_size
        if not keep:
          del self.tilemap[loc]

    return matches

  def tile_around(self, pos):
    tiles = []
    tile_loc = (int(pos[0] // self.tile_size), int(pos[1] // self.tile_size))
    for offset in NEIGHBOUR_OFFSET:
      check_loc = str(tile_loc[0] + offset[0]) + ";" + str(tile_loc[1] + offset[1])
      if check_loc in self.tilemap:
        tiles.append(self.tilemap[check_loc])
    return tiles
  
  def solid_check(self, pos):
    tile_loc = str(int(pos[0] // self.tile_size)) + ";" + str(int(pos[1] // self.tile_size))
    if tile_loc in self.tilemap:
      if self.tilemap[tile_loc]["type"] in PHYSCIS_TILES:
        return self.tilemap[tile_loc]

  def physics_rects_around(self, pos):
    rects = []
    for tile in self.tile_around(pos):
      if tile["type"] in PHYSCIS_TILES:
        rects.append(pygame.Rect(tile["pos"][0] * self.tile_size, tile["pos"][1] * self.tile_size, self.tile_size, self.tile_size))
    return rects

  def render(self, surf, offset = (0, 0)):
    for tile in self.offgrid_tiles:
      surf.blit(self.game.assets[tile["type"]][tile["variant"]], (tile["pos"][0] - offset[0], tile["pos"][1] - offset[1]))

    for x in range(offset[0] // self.tile_size, (offset[0] + surf.get_width()) // self.tile_size + 1):
      for y in range(offset[1] // self.tile_size, (offset[1] + surf.get_height()) // self.tile_size + 1):
        loc = str(x) + ";" + str(y)
        if loc in self.tilemap:
          tile = self.tilemap[loc]
          surf.blit(self.game.assets[tile["type"]][tile["variant"]], (tile["pos"][0] * self.tile_size - offset[0], tile["pos"][1] * self.tile_size - offset[1]))

  def save(self, path):
    file = open(path, "w")
    json.dump({"tilemap" : self.tilemap, "offgrid" : self.offgrid_tiles, "tile_size" : self.tile_size}, file)
    file.close()
  
  def load(self, path):
    file = open(path, "r")
    json_data = json.load(file)
    file.close()
    self.tilemap = json_data["tilemap"]
    self.offgrid_tiles = json_data["offgrid"]
    self.tile_size = json_data["tile_size"]

  def autotile(self):
    for loc in self.tilemap:
      tile = self.tilemap[loc]
      neighbours = set()
      for shift in ((0, 1), (0, -1), (1, 0), (-1, 0)):
        check_loc = str(tile["pos"][0] + shift[0]) + ";" + str(tile["pos"][1] + shift[1])
        if check_loc in self.tilemap:
          if self.tilemap[check_loc]["type"] == tile["type"]:
            neighbours.add(shift)
      neighbours = tuple(sorted(neighbours))
      if (tile["type"] in AUTOTILE_TYPES) and (neighbours in AUTOTILE_MAP):
        tile["variant"] = AUTOTILE_MAP[neighbours]