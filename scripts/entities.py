import pygame
class PhysicsEntity:
  def __init__(self, game, e_type, pos, size):
    self.type = e_type
    self.pos = list(pos) #lista nie jest referencyjna, a tablica tak i tablica nie może być zmieniana
    self.size = size
    self.velocity = [0, 0]
    self.game = game

  def hitbox(self):
    return pygame.Rect(self.pos[0], self.pos[1], self.size[0], self.size[1])

  def update(self, tilemap, movement = (0, 0)):
    frame_movement = (movement[0] + self.velocity[0], movement[1] + self.velocity[1])
    #frame_movement[0] - movement (1 do (-1)) na osi x
    #frame_movement[1] - movement (1 do (-1)) na osi y

    self.pos[0] += frame_movement[0]
    entity_rect = self.hitbox()
    for rect in tilemap.physics_rects_around(self.pos):
      if entity_rect.colliderect(rect):
        if frame_movement[0] > 0:
          entity_rect.right = rect.left
        if frame_movement[0] < 0:
          entity_rect.left = rect.right
        self.pos[0] = entity_rect.x

    self.pos[1] += frame_movement[1]
    entity_rect = self.hitbox()
    for rect in tilemap.physics_rects_around(self.pos):
      if entity_rect.colliderect(rect):
        if frame_movement[1] > 0:
          entity_rect.bottom = rect.top
        if frame_movement[1] < 0:
          entity_rect.top = rect.bottom
        self.pos[1] = entity_rect.y


    self.velocity[1] = min(5, self.velocity[1] + 0.1)

  def render(self, surf, offset = (0, 0)):
    surf.blit(self.game.assets['player'], (self.pos[0] - offset[0], self.pos[1] - offset[1]))