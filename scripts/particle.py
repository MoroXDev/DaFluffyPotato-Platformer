class Particle:
  def __init__(self, game, p_type, pos, velocity = (0, 0), frame = 0):
    self.game = game
    self.pos = list(pos)
    self.velocity = velocity
    self.animation = game.assets["particle/" + p_type].copy()
    self.animation.frame = frame
    self.type = p_type

  def update(self):
    self.animation.update()
    kill = self.animation.done

    self.pos[0] += self.velocity[0]
    self.pos[1] += self.velocity[1]

    return kill
  
  def render(self, surf, offset = (0, 0)):
    img = self.animation.img()
    surf.blit(img, (self.pos[0] - offset[0] - img.get_width() // 2, self.pos[1] - offset[1] - img.get_height() // 2))

    