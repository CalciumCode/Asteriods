import pygame
import missile
import math

class ship:
    rot = math.radians(90)
    acceleration = .05
    drag = .025
    direct = pygame.Vector2(0, -1)
    pos = pygame.Vector2(0, 0)
    shotpos = pygame.Vector2(0, 0)
    vel = pygame.Vector2(0, 0)
    mass = 1
    rad = 1
    maxspeed = 5

    poly = [
        pygame.Vector2(20, 0),
        pygame.Vector2(-20, -10),
        pygame.Vector2(-10, 0),
        pygame.Vector2(-20, 10),
        ]

    def __init__(self, pos, size):
        self.pos = pos
        self.rad = size

    def update(self):
        self.pos += self.vel 
    
    def accelerate(self):
        if(pygame.Vector2.dot(self.direct, self.vel) < self.maxspeed):
            self.vel += self.direct * self.acceleration
    
    def decelerate(self):
        self.vel = self.vel.move_towards(pygame.Vector2(0, 0), self.drag)
        
    def fire(self, target):
        m = missile.missile(self.pos.xy, 7, target - self.pos, 5)
        return m

    def turn(self, r):
        turnspeed = 3
        if(r):
            self.rot -= math.radians(turnspeed)
        else:
            self.rot += math.radians(turnspeed)

        self.rot %= (2 * math.pi)
        self.direct = pygame.Vector2(math.cos(self.rot), -math.sin(self.rot))

    def draw(self, screen):
        out = tuple(pygame.Vector2(p.x * math.cos(-self.rot) - p.y * math.sin(-self.rot), p.x * math.sin(-self.rot) + p.y * math.cos(-self.rot)) + self.pos for p in self.poly)
        pygame.draw.polygon(screen, (255, 255, 0), out)