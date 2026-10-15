import pygame

class asteroid:
    pos = pygame.Vector2(0, 0)
    vel = pygame.Vector2(0, 0)
    mass = 1
    rad = 1

    def __init__(self, pos, vel, mass):
        self.pos = pos
        self.vel = vel
        self.mass = mass
        self.rad = mass * 1

    def update(self):
        self.pos += self.vel
    
    def collision(self, other):
        norm = pygame.Vector2.normalize(other.pos - self.pos)
        mdif = self.mass - other.mass
        msum = self.mass + other.mass
        svnorm = self.vel.project(norm)
        ovnorm = other.vel.project(norm)
        rsum = (self.rad + other.rad)
        
        self.vel -= ((mdif * svnorm) + (2 * other.mass * ovnorm)) / msum 
        other.vel += ((mdif * ovnorm) + (2 * self.mass * svnorm)) / msum 
        if(self.mass >= other.mass):
            other.pos = self.pos + norm * rsum
        else:
            self.pos = other.pos - norm * rsum

    def draw(self, screen):
        pygame.draw.circle(screen, (125, 125, 125), self.pos, self.rad)


