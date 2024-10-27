import pygame
class PhysicsEntity:
  def __init__(self, game, e_type, pos, size):
    self.type = e_type
    self.pos = list(pos) #lista nie jest referencyjna, a tablica tak i tablica nie może być zmieniana
    self.size = size
    self.velocity = [0, 0]
    self.game = game
    self.action = ""
    self.set_action("idle")
    self.anim_offset = (-3, -3)
    self.flip = False
    self.collisions = {"down" : False, "up" : False, "right" : False, "left" : False}

  def hitbox(self):
    return pygame.Rect(self.pos[0], self.pos[1], self.size[0], self.size[1])

  def set_action(self, action):
    if self.action != action:
      self.action = action
      self.animation = self.game.assets[self.type + "/" + action].copy()

  def update(self, tilemap, movement = (0, 0)):
    self.collisions = {"down" : False, "up" : False, "right" : False, "left" : False}
    frame_movement = (movement[0] + self.velocity[0], movement[1] + self.velocity[1])
    #movement[0] - movement (1 do (-1)) na osi x
    #movement[1] - movement (1 do (-1)) na osi y
    #frame_movement - movement z dodanym velocity który się zmienia

    self.pos[0] += frame_movement[0]
    entity_rect = self.hitbox()
    for rect in tilemap.physics_rects_around(self.pos):
      if entity_rect.colliderect(rect):
        if frame_movement[0] > 0:
          self.collisions["right"] = True
          entity_rect.right = rect.left
        if frame_movement[0] < 0:
          self.collisions["left"] = True
          entity_rect.left = rect.right
        self.pos[0] = entity_rect.x

    self.pos[1] += frame_movement[1]
    entity_rect = self.hitbox()
    for rect in tilemap.physics_rects_around(self.pos):
      if entity_rect.colliderect(rect):
        if frame_movement[1] > 0:
          self.collisions["down"] = True
          entity_rect.bottom = rect.top
        if frame_movement[1] < 0:
          self.collisions["up"] = True
          entity_rect.top = rect.bottom
        self.pos[1] = entity_rect.y

    self.velocity[1] = min(5, self.velocity[1] + 0.1)

    self.animation.update()
    if movement[0] > 0:
      self.flip = False
    if movement[0] < 0:
      self.flip = True

  def render(self, surf, offset = (0, 0)):
    surf.blit(pygame.transform.flip(self.animation.img(), self.flip, False), (self.pos[0] - offset[0] + self.anim_offset[0], self.pos[1] - offset[1] + self.anim_offset[1]))


class Player(PhysicsEntity):
  def __init__(self, game, pos, size):
    super().__init__(game, "player", pos, size)
    self.air_time = 0
    self.jumps = 0
    self.wall_slide = False

  def update(self, tilemap, movement = (0, 0)):
    super().update(tilemap, movement) 
    self.wall_slide = False

    if self.velocity[0] > 0:
      self.velocity[0] = max(0, self.velocity[0] - 0.1)
    else:
      self.velocity[0] = min(0, self.velocity[0] + 0.1)

    self.air_time += 1
    if self.collisions["down"]:
      self.air_time = 0
      self.jumps = 1

    if (self.collisions["right"] or self.collisions["left"]) and self.air_time > 4:
      self.wall_slide = True
      self.velocity[1] = min(0.5, self.velocity[1])
      if self.collisions["right"]:
        self.flip = False
      if self.collisions["left"]:
        self.flip = True
      
    if self.wall_slide:
      self.set_action("wall_slide")
    elif self.air_time > 4:
      self.set_action("jump")
    elif movement[0] != 0:
      self.set_action("run")
    else:
      self.set_action("idle")

  def jump(self):
    if self.wall_slide:
      if self.flip:
        self.velocity[0] = 3.5
        self.velocity[1] = -2.5
      else:
        self.velocity[0] = -3.5
        self.velocity[1] = -2.5
    elif self.jumps > 0:
      self.velocity[1] = -3
      self.jumps -= 1