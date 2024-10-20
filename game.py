import pygame
import sys
from scripts.entities import PhysicsEntity, Player
from scripts.utils import load_image, load_images, Animation
from scripts.tilemap import Tilemap
from scripts.clouds import Clouds

class Game:
  def __init__(self):
    pygame.init()
    pygame.display.set_caption("First Game")

    self.screen = pygame.display.set_mode((640, 480))
    self.display = pygame.Surface((320, 240))
    self.clock = pygame.time.Clock()
    self.movement = [False, False]
    self.assets = {
      "decor" : load_images("tiles/decor"),
      "grass" : load_images("tiles/grass"),
      "large_decor" : load_images("tiles/large_decor"),
      "stone" : load_images("tiles/stone"),
      "player" : load_image("entities/player.png"),
      "background" : load_image("background.png"),
      "clouds" : load_images("clouds"),
      "player/idle" : Animation(load_images("entities/player/idle"), 6),
      "player/run" : Animation(load_images("entities/player/run"), 4),
      "player/jump" : Animation(load_images("entities/player/jump")),
      "player/slide" : Animation(load_images("entities/player/slide")),
      "player/wall_slide" : Animation(load_images("entities/player/wall_slide"))
    }
    self.clouds = Clouds(self.assets["clouds"], count=16)
    self.player = Player(self, (70, 70), (8, 15)) #size może wynosić tylko 16x16 bo tile są sprawdzane do okoła pozycji gracza zakłając, że wszystko jest w 16x16
    self.tilemap = Tilemap(self, tile_size=16)
    self.camera = [0, 0]

  def run(self):
    while True:
      #self.camera[0] += (self.player.hitbox().centerx - self.display.get_width() / 2 - self.camera[0]) / 30
      #self.camera[1] += (self.player.hitbox().centery - self.display.get_height() / 2 - self.camera[1]) / 30
      self.camera[0] += (self.player.hitbox().centerx - self.camera[0] - self.display.get_width() / 2) / 30
      self.camera[1] += (self.player.hitbox().centery - self.camera[1] - self.display.get_height() / 2) / 30

      #może pojawić się ruch poprzez liczby po przecinku dodane jako offset i należy uciąć liczby po przecinku do osobnej zmiennej
      render_offset = [int(self.camera[0]), int(self.camera[1])]

      self.display.fill((119, 56, 255))
      self.player.update(self.tilemap, (self.movement[1] - self.movement[0], 0))
      self.clouds.update()
      self.display.blit(self.assets["background"], (0, 0))
      self.clouds.render(self.display, render_offset)
      self.tilemap.render(self.display, render_offset)
      self.player.render(self.display, render_offset)

      for event in pygame.event.get():
        if event.type == pygame.QUIT:
          sys.exit()
        if event.type == pygame.KEYUP:
          if event.key == pygame.K_ESCAPE:
            sys.exit()
          if event.key == pygame.K_LEFT:
            self.movement[0] = False
          if event.key == pygame.K_RIGHT:
            self.movement[1] = False
        if event.type == pygame.KEYDOWN:
          if event.key == pygame.K_UP:
            self.player.velocity[1] = -3
          if event.key == pygame.K_LEFT:
            self.movement[0] = True
          if event.key == pygame.K_RIGHT:
            self.movement[1] = True

      self.screen.blit(pygame.transform.scale(self.display, self.screen.get_size()), (0, 0))
      pygame.display.update()
      self.clock.tick(60)

Game().run()
