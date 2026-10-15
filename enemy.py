import pygame
import missile
import math

class ship:
    rot = math.radians(90)
    acceleration = .1
    drag = .05
    direct = pygame.Vector2(0, -1)
    s2p = pygame.Vector2(0, -1)
    pos = pygame.Vector2(0, 0)
    shotpos = pygame.Vector2(0, 0)
    vel = pygame.Vector2(0, 0)
    mass = 1
    rad = 20
    maxspeed = 3
    tracking = False
    shotcd = 30
    curshotcd = 0

    shotdot = 0.125
    pursuedot = .425
    pursuedist = 300

    poly = [
        pygame.Vector2(20, 0),
        pygame.Vector2(-20, -10),
        pygame.Vector2(-10, 0),
        pygame.Vector2(-20, 10),
        ]

    def __init__(self, pos, size):
        self.pos = pos
        self.rad = size

    def update(self, plr):
        self.pos += self.vel 
        self.s2p = plr.pos - self.pos
        if(self.curshotcd > 0):
            self.curshotcd -= 1
        self.tracking = self.s2p.magnitude() <= self.pursuedist and pygame.Vector2.dot(self.s2p.normalize(), self.direct) >= self.pursuedot
        if self.tracking:
            self.turn()
            self.accelerate()
        else:
            self.decelerate()


    def accelerate(self):
        if(pygame.Vector2.dot(self.direct, self.vel) < self.maxspeed):
             self.vel += self.direct * self.acceleration * pygame.Vector2.dot(self.s2p.normalize(), self.direct)
    
    def decelerate(self):
        self.vel = self.vel.move_towards(pygame.Vector2(0, 0), self.drag)

    def fire(self, target):
        m = missile.missile(self.pos.xy, 7, target - self.pos, 5)
        return m

    def turn(self):
        turnspeed = 3
        self.rot += math.radians(self.s2p.angle_to(self.direct))
        print(self.rot)
        self.rot %= (2 * math.pi)
        self.direct = pygame.Vector2(math.cos(self.rot), -math.sin(self.rot))

    def draw(self, screen):
        out = tuple(pygame.Vector2(p.x * math.cos(-self.rot) - p.y * math.sin(-self.rot), p.x * math.sin(-self.rot) + p.y * math.cos(-self.rot)) + self.pos for p in self.poly)
        pygame.draw.polygon(screen, (255, 0, 0), out)
        pygame.draw.circle(screen, (255, 0, 0), self.pos, self.pursuedist, 2)
        pygame.draw.line(screen, (255, 0, 0), self.pos, self.pos + self.direct * self.pursuedist)