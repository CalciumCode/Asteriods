import pygame 

class missile:
    direct = pygame.Vector2(0,0)
    pos = pygame.Vector2(0, 0)
    spd = 1
    rad = 1

    def __init__(self, pos, spd, direction, rad):
        self.pos = pos
        self.spd = spd
        self.direct = pygame.Vector2.normalize(direction)
        self.rad = rad

    def update(self):
        self.pos += self.spd * self.direct

    def draw(self, screen):
        pygame.draw.circle(screen, (255, 0, 0), self.pos, self.rad)