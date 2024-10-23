import pygame
import sys
from scripts.utils import load_images
from scripts.tilemap import Tilemap

RENDER_SCALE = 2.0

class Editor:
  def __init__(self):
    pygame.init()
    pygame.display.set_caption("editor")
    monitor = pygame.display.Info()
    self.screen = pygame.display.set_mode((monitor.current_w / 2, monitor.current_h / 2))
    self.display = pygame.Surface((monitor.current_w / 4, monitor.current_h / 4))
    self.clock = pygame.time.Clock()
    self.movement = [False, False, False, False]
    self.tilemap = Tilemap(self, 16)
    self.camera = [0, 0]
    self.on_grid = True

    self.assets = {
      "decor" : load_images("tiles/decor"),
      "grass" : load_images("tiles/grass"),
      "stone" : load_images("tiles/stone"),
      "large_decor" : load_images("tiles/large_decor")
    }    

    self.tile_list = list(self.assets)
    self.tile_group = 0
    self.tile_variant = 0
    self.left_clicking = False
    self.right_clicking = False
    self.shifting = False

    try:
      self.tilemap.load("map.json")
    except FileNotFoundError:
      pass
  
  def run(self):
    while True:
      self.display.fill((0, 0, 0))

      render_camera = (int(self.camera[0]), int(self.camera[1]))
      mouse_pos = pygame.mouse.get_pos()
      mouse_pos = (mouse_pos[0] / RENDER_SCALE, mouse_pos[1] / RENDER_SCALE)
      tile_pos = (int((mouse_pos[0] + render_camera[0]) // self.tilemap.tile_size), int((mouse_pos[1] + render_camera[1]) // self.tilemap.tile_size))
      self.camera[0] += self.movement[1] - self.movement[0]
      self.camera[1] += self.movement[3] - self.movement[2]

      if self.left_clicking and self.on_grid:
        self.tilemap.tilemap[str(tile_pos[0]) + ";" + str(tile_pos[1])] = {"type" : self.tile_list[self.tile_group], "variant" : self.tile_variant, "pos" : tile_pos}
      
      if self.right_clicking and self.on_grid:
        tile_loc = str(tile_pos[0]) + ";" + str(tile_pos[1])
        if tile_loc in self.tilemap.tilemap:
          del self.tilemap.tilemap[tile_loc]

      if self.right_clicking and not self.on_grid:
        for tile in self.tilemap.offgrid_tiles.copy():
          tile_img = self.assets[tile["type"]][tile["variant"]]
          tile_rect = pygame.Rect(tile["pos"][0], tile["pos"][1], tile_img.get_width(), tile_img.get_height())
          if tile_rect.collidepoint((mouse_pos[0] + self.camera[0], mouse_pos[1] + self.camera[1])):
            self.tilemap.offgrid_tiles.remove(tile)

      current_tile_img = self.assets[self.tile_list[self.tile_group]][self.tile_variant].copy()
      current_tile_img.set_alpha(100)

      self.tilemap.render(self.display, render_camera)
      if self.on_grid:
        self.display.blit(current_tile_img, (tile_pos[0] * self.tilemap.tile_size - render_camera[0], tile_pos[1] * self.tilemap.tile_size - render_camera[1]))
      else:
        self.display.blit(current_tile_img, mouse_pos)

      for event in pygame.event.get():
        if event.type == pygame.QUIT:
          sys.exit()

        if event.type == pygame.KEYUP:
          if event.key == pygame.K_a:
            self.movement[0] = False
          if event.key == pygame.K_d:
            self.movement[1] = False
          if event.key == pygame.K_w:
            self.movement[2] = False
          if event.key == pygame.K_s:
            self.movement[3] = False
          if event.key == pygame.K_LSHIFT:
            self.shifting = False

        if event.type == pygame.KEYDOWN:
          if event.key == pygame.K_ESCAPE:
            sys.exit()
          if event.key == pygame.K_a:
            self.movement[0] = True
          if event.key == pygame.K_d:
            self.movement[1] = True
          if event.key == pygame.K_w:
            self.movement[2] = True
          if event.key == pygame.K_s:
            self.movement[3] = True
          if event.key == pygame.K_LSHIFT:
            self.shifting = True
          if event.key == pygame.K_g:
            self.on_grid = not self.on_grid
          if event.key == pygame.K_o:
            self.tilemap.save("map.json")
          if event.key == pygame.K_t:
            self.tilemap.autotile()

        if event.type == pygame.MOUSEBUTTONDOWN:
          if event.button == pygame.BUTTON_LEFT:
            self.left_clicking = True
            if not self.on_grid:
              self.tilemap.offgrid_tiles.append({"type" : self.tile_list[self.tile_group], "variant" : self.tile_variant, "pos" : (mouse_pos[0] + self.camera[0], mouse_pos[1] + self.camera[1])})

          if event.button == pygame.BUTTON_RIGHT:
            self.right_clicking = True

          if self.shifting:
            if event.button == pygame.BUTTON_WHEELUP:
              self.tile_variant = (self.tile_variant - 1) % len(self.assets[self.tile_list[self.tile_group]])
            if event.button == pygame.BUTTON_WHEELDOWN:
              self.tile_variant = (self.tile_variant + 1) % len(self.assets[self.tile_list[self.tile_group]])
          else:
            if event.button == pygame.BUTTON_WHEELUP:
              self.tile_group = (self.tile_group - 1) % len(self.assets)
              self.tile_variant = 0
            if event.button == pygame.BUTTON_WHEELDOWN:
              self.tile_group = (self.tile_group + 1) % len(self.assets)
              self.tile_variant = 0 

        if event.type == pygame.MOUSEBUTTONUP:
          if event.button == pygame.BUTTON_LEFT:
            self.left_clicking = False
          if event.button == pygame.BUTTON_RIGHT:
            self.right_clicking = False

      self.screen.blit(pygame.transform.scale(self.display, self.screen.get_size()), (0, 0))
      pygame.display.update()
      self.clock.tick(60)

editor = Editor()
editor.run()


