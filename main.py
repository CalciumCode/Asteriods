import pygame
import asteroid
import ship
import enemy
import missile
import random

s_wid = 1280
s_hgh = 720
s_run = True
screen = pygame.display.set_mode((s_wid, s_hgh))
pygame.display.set_caption("ASTERIODS")
clock = pygame.time.Clock()

plr = ship.ship(pygame.Vector2(s_wid/2, s_hgh/2), 10)
enms = [
    enemy.ship(pygame.Vector2(500, s_hgh/2), 10),
]
ast = []
pmis = []
emis = []

asrate = 120
asc = 0

def newAsteriod():
    s = random.randint(1,4)
    m = random.randint(5,50)
    a = asteroid.asteroid(pygame.Vector2(0, 0), pygame.Vector2(random.randint(-1, 1), random.randint(-1, 1)) * 2, m)
    if s == 1:
        a.pos = pygame.Vector2(0, random.randint(0, s_hgh))
        if a.vel.x < 0:
            a.vel = pygame.Vector2(-a.vel.x, a.vel.y)
    if s == 2:
        a.pos = pygame.Vector2(s_wid, random.randint(0, s_hgh))
        if a.vel.x > 0:
            a.vel = pygame.Vector2(-a.vel.x, a.vel.y)
    if s == 3:
        a.pos = pygame.Vector2(random.randint(0, s_wid), 0)
        if a.vel.y < 0:
            a.vel = pygame.Vector2(a.vel.x, -a.vel.y)

    if(s == 4):
        a.pos = pygame.Vector2(random.randint(0, s_wid), s_hgh)
        if a.vel.y > 0:
            a.vel = pygame.Vector2(a.vel.x, -a.vel.y)

    ast.append(a)

while(s_run):
    keys = pygame.key.get_pressed()

    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            s_run = False
        if e.type == pygame.MOUSEBUTTONDOWN:
            pmis.append(plr.fire(plr.pos + plr.direct))

    screen.fill((0, 0, 0)) 

    if(keys[pygame.K_RIGHT]):
        plr.turn(True)
    if(keys[pygame.K_LEFT]):
        plr.turn(False)
    if(keys[pygame.K_UP]):
        plr.accelerate()
    else:
        plr.decelerate()
    if(plr.pos.x < 0):
        plr.pos = pygame.Vector2(s_wid, plr.pos.y)
    if(plr.pos.x > s_wid):
        plr.pos = pygame.Vector2(0, plr.pos.y)
    if(plr.pos.y > s_hgh):
        plr.pos = pygame.Vector2(plr.pos.x, 0)
    if(plr.pos.y < 0):
        plr.pos = pygame.Vector2(plr.pos.x, s_hgh) 
    plr.update()
    plr.draw(screen)

    for e in enms:
        e.update(plr)
        if(e.pos.x < 0):
            e.pos = pygame.Vector2(s_wid, e.pos.y)
        if(e.pos.x > s_wid):
            e.pos = pygame.Vector2(0, e.pos.y)
        if(e.pos.y > s_hgh):
            e.pos = pygame.Vector2(e.pos.x, 0)
        if(e.pos.y < 0):
            e.pos = pygame.Vector2(e.pos.x, s_hgh) 
        if(e.tracking and pygame.Vector2.dot(e.s2p.normalize(), e.direct) >= e.shotdot and e.curshotcd == 0):
            emis.append(e.fire(plr.pos))
            e.curshotcd = e.shotcd
        e.draw(screen)
    for pm in pmis[:]:
        pm.update()
        if(pm.pos.x < 0 or pm.pos.x > s_wid or pm.pos.y < 0 or pm.pos.y > s_hgh):
            pmis.remove(pm)
        for e in enms:
            if (pm.pos - e.pos).magnitude() <= pm.rad + e.rad:
                e.vel += (pm.direct * pm.spd)
                pmis.remove(pm)
        for a in ast[:]:
            if (pm.pos - a.pos).magnitude() <= pm.rad + a.rad:
                ast.remove(a)
                pmis.remove(pm)
        pm.draw(screen)
    for em in emis[:]:
        em.update()
        if(em.pos.x < 0 or em.pos.x > s_wid or em.pos.y < 0 or em.pos.y > s_hgh):
            emis.remove(em)
        if (em.pos - plr.pos).magnitude() <= plr.rad + em.rad:
                plr.vel += (em.direct * em.spd)
                emis.remove(em)
        for a in ast[:]:
            if (em.pos - a.pos).magnitude() <= em.rad + a.rad:
                ast.remove(a)
                emis.remove(em)
        em.draw(screen)
    for a in ast[:]:
        a.update()
        for b in ast:
            if(a == b):
                continue
            if((a.pos - b.pos).length() < a.rad + b.rad):
                a.collision(b)
        if(a.pos.x  > s_wid + a.rad or a.pos.x < 0 - a.rad or a.pos.y > s_hgh + a.rad or a.pos.y < 0 - a.rad):
            ast.remove(a)
            continue
        if (a.pos - plr.pos).magnitude() <= plr.rad + a.rad:
                plr.vel += a.vel * .5
                a.vel = a.vel * .5
        for e in enms:
            if (a.pos - e.pos).magnitude() <= a.rad + e.rad:
                e.vel += a.vel * .5
                a.vel = a.vel * .5      
        a.draw(screen)
   
    asc += 1
    if (asc % asrate == 0):  
        newAsteriod()
        asc = 0

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
