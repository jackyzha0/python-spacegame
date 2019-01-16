# !/usr/local/bin/python
import pygame
import spritesheet
import random
import math

"""
TODO
-Add PAUSE
-Make asteroids destructable
-Take damage from asteroids
"""

pygame.init()
pygame.font.init()
pygame.display.set_caption('HyperDrive')
pygame.mouse.set_visible(False)
screen = pygame.display.set_mode((1920, 1080))
ss = spritesheet.spritesheet('lib/tex/playerspritesheet.png')
cur = pygame.image.load('lib/tex/cur.png').convert_alpha()
bul = pygame.image.load('lib/tex/bul1.png').convert_alpha()
rocksprites = spritesheet.spritesheet('lib/tex/rocks.jpg')
maintitlefont = pygame.font.Font("lib/font/pixel font-7.ttf", 112)
titlefont = pygame.font.Font("lib/font/pixel font-7.ttf", 42)
subfont = pygame.font.Font("lib/font/SFPixelate-Bold.ttf", 16)
font = pygame.font.Font("lib/font/SFPixelate-Bold.ttf", 12)
hbar  = pygame.image.load("lib/tex/H.png").convert_alpha()
fbar = pygame.image.load("lib/tex/F.png").convert_alpha()

logo = pygame.image.load('lib/tex/logo.png').convert_alpha()
sprites = []
asteroidssprites = []
pb = []
xdim = 50
ydim = 54
rows = 6
done = False
col = 5
xvel = 0.00
yvel = 0.00
cycle = 0
deg = 0.00
__GLOBALX = 0.00
__GLOBALY = 0.00
theta = random.uniform(0,1)
theta1 = random.uniform(0,1)
theta2 = random.uniform(0,1)
TITLE,RUNNING,PAUSED,INTRO = 0,1,2,3
GAMESTATE = INTRO

#Player Stats
__hp = 1000
__hpmax = 1000
__speedmult = 1
__atk = 100
__curcd = 0
__weaponcd = 8
__weaponspeedmult = 115
__numguns = 1
__fuel = 250
__fuelrecharge = (1/25)
__maxfuel = 250

#STRINGS


stars = []
fumes = []
asteroids = []
clock = pygame.time.Clock()
def rot_center(image, _center, angle):
        """rotate an image while keeping its center"""
        rot_image = pygame.transform.rotate(image, angle)
        rot_rect = rot_image.get_rect(center=_center)
        return rot_image,rot_rect
def getPlayerSprite(xvel,cycle):
    if int(xvel/2) == 0:
        adjustedState = 2
    elif (xvel > 0):
        if xvel > 5:
            adjustedState = 4
        else:
            adjustedState = 3
    else:
        if xvel < -5:
            adjustedState = 0
        else:
            adjustedState = 1
    sprite = sprites[((adjustedState+1)+(cycle*5))-1]
    return sprite

class star(object):
    def __init__(self,x,y,colour=None,radius=None,life=None):
        self.x = x
        self.y = y
        if colour:
            self.colour = colour
        else:
            self.colour = (random.randint(230, 255),random.randint(240, 255),random.randint(200, 255))
        if radius:
            self.radius = radius
        else:
            self.radius = random.randint(1, 4)
        if life:
            self.life = life
        else:
            self.life = random.randint(180,1200)
    def update(self,xvel,yvel):
        self.x += xvel
        self.y += yvel
        if self.x > 2880 or self.x < -960 or self.y > 1620 or self.y < -540:
            self.life = -1
        else:
            self.life -= 1
        return int(self.x),int(self.y),self.radius,self.colour,self.life

class asteroid(object):
    def __init__(self):
        self.type = random.randint(0,15)
        if random.randint(0,1) == 1:
            self.x = random.randint(-1920,0)
        else:
            self.x = random.randint(1920,3840)
        if random.randint(0,1) == 1:
            self.y = random.randint(-1080,0)
        else:
            self.y = random.randint(1080,2160)
        self.rotatespeed = random.uniform(-0.4,-0.4)
        self.rotation = random.uniform(0,360)
        self.size = random.randint(10,110)
        self.sprite = asteroidssprites[self.type]
        self.gmovex = random.uniform(-3,3)
        self.gmovey = random.uniform(-3,3)
    def update(self,xvel,yvel):
        self.x += xvel+self.gmovex
        self.y += yvel+self.gmovey
        self.rotation += self.rotatespeed
        if self.x > 3840 or self.x < -1920 or self.y > 2160 or self.y < -1080:
            self.size = 0
        return self.x,self.y,self.rotation,96*(self.size/100),self.sprite,self.size

class bullet(object):
    def __init__(self,deg,xvel,yvel,damage,x,y,__weaponspeedmult):
        self.xvel = -xvel*__weaponspeedmult
        self.yvel = -yvel*__weaponspeedmult
        self.deg = deg
        self.x = x
        self.y = y
        self.damage = damage
        self.kill = 0
        self.sprite,self.rect = rot_center(bul, (6,15), deg)
    def update(self,_xvel,_yvel):
        self.x += self.xvel+_xvel
        self.y += self.yvel+_yvel
        if self.x > 3840 or self.x < -1920 or self.y > 2160 or self.y < -1080:
            self.kill = 1
        return self.x,self.y,self.sprite,self.rect,self.kill

for i in range(0,rows):
    for j in range(0,col):
        sprites.append(ss.image_at((j*xdim, i*ydim, xdim, ydim)).convert())
for i in range(0,4):
    for j in range(0,4):
        asteroidssprites.append(rocksprites.image_at((j*96, i*96, 96, 96)))

def genFume(xvel,yvel,deg,boost=None):
    velavg = abs(int((xvel+yvel)))
    fumearr = []
    for i in range(0,velavg):
        if (boost):
            fumearr.append(star(960-27+random.randint(-4,4),540-25+random.randint(-4,4),colour = (random.randint(240,255),random.randint(180,240),random.randint(49,80)),radius=random.randint(2,5),life=random.randint(30,60)))
        else:
            rand = random.randint(140,230)
            fumearr.append(star(960-27+random.randint(-14,14),540-25+random.randint(-14,14),colour = (rand,rand,rand),radius=random.randint(3,6),life=random.randint(30,120)))
    return fumearr


background = pygame.Surface(screen.get_size())
background = background.convert()
background.fill((255, 255, 255))
chgy = 0
chgx = 0
olddeg = 0
randflicker = random.randint(180,255)

logo = pygame.transform.scale(logo, (256, 256))
brect = pygame.Surface(screen.get_size(), pygame.SRCALPHA, 32)
screen.blit(background,(0,0))
screen.blit(logo,(832,412))
pygame.display.update()
dt = clock.tick(1)
col = ((math.sin(theta)+1)*30,(math.sin(theta1)+1)*20,(math.sin(theta2)+1)*28)
for i in range(0, 55):
    brect.fill((col[0], col[1], col[2],i))
    screen.blit(brect, (0,0))
    pygame.display.update()
GAMESTATE = TITLE
while len(stars) < 500:
    stars.append(star(random.randint(-960, 2880),random.randint(-540, 1620)))


while not done:
    __curcd+= 1
    theta += random.uniform(0,((xvel+yvel)/2000))
    theta1 += random.uniform(0,((xvel+yvel)/2000))
    theta2 += random.uniform(0,((xvel+yvel)/2000))
    col = ((math.sin(theta)+1)*30,(math.sin(theta1)+1)*20,(math.sin(theta2)+1)*28)
    mx, my = pygame.mouse.get_pos()
    mdist = math.sqrt((540-mx)**2+(960-my)**2)

    background.fill((col[0], col[1], col[2]))

    if GAMESTATE == RUNNING:
        if __hp > __hpmax:
            __hp = __hpmax
        if __hp < 0:
            pygame.display.quit()
            pygame.quit()
            sys.exit()
        cycle+=1
        if cycle > 40:
            cycle = 0
    mouseX, mouseY = pygame.mouse.get_pos()
    olddeg = deg
    deg = math.atan2(960-mouseX, 547-mouseY)*(180/(3.1415))
    degchange = deg-olddeg
    xvel *= 0.995
    yvel *= 0.995
    if xvel > __speedmult*12:
        xvel = __speedmult*10
    if xvel < -__speedmult*12:
        xvel = -__speedmult*10
    if yvel > __speedmult*12:
        yvel = __speedmult*10
    if yvel < -__speedmult*12:
        yvel = -__speedmult*10

    __GLOBALX += xvel/10
    __GLOBALY += yvel/10
    screen.blit(background,(0, 0))

    for s in stars:
        tmp = s.update(xvel,yvel)
        st = pygame.Surface((tmp[2],tmp[2]))
        pygame.draw.circle(st,tmp[3],(int(tmp[2]/2),int(tmp[2]/2)),tmp[2])
        st.set_alpha(255-tmp[2]*30)
        screen.blit(st,(tmp[0],tmp[1]))
        if tmp[4] < 0:
            stars.remove(s)
            stars.append(star(random.randint(-960, 2880),random.randint(-540, 1620)))
    for f in fumes:
        if not f:
            fumes.remove(f)
        else:
            for fu in f:
                tmp = fu.update(xvel,yvel)
                st = pygame.Surface((tmp[2],tmp[2]))
                pygame.draw.circle(st,tmp[3],(int(tmp[2]/2),int(tmp[2]/2)),tmp[2])
                st.set_alpha(255-tmp[2]*40)
                screen.blit(st,(tmp[0],tmp[1]))
                if tmp[4] < 0:
                    f.remove(fu)
    if len(asteroids) < 4:
        asteroids.append(asteroid())

    for a in asteroids:
        tmp = a.update(xvel,yvel)
        st = pygame.Surface((tmp[3],tmp[3]))
        _sprite = tmp[4]
        if int(tmp[3]) != 0:
            _sprite = pygame.transform.scale(_sprite, (int(tmp[3]), int(tmp[3])))
        _sprite,rect = rot_center(_sprite, (tmp[3],tmp[3]), tmp[2])
        _sprite.set_colorkey((47,72,78))
        if tmp[5] < 1:
            asteroids.remove(a)
        screen.blit(_sprite,(tmp[0],tmp[1]))
    screen.blit(cur,pygame.mouse.get_pos())
    if GAMESTATE == RUNNING:
        for b in pb:
            tmp = b.update(xvel,yvel)
            st = pygame.Surface((abs(tmp[3][0]-tmp[3][2]),abs(tmp[3][1]-tmp[3][3])))
            _sprite = tmp[2]
            screen.blit(_sprite,(tmp[0],tmp[1]))
            if tmp[4] == 1:
                pb.remove(b)
        sprite = getPlayerSprite(int(degchange*2),int(cycle/10))
        sprite,rect = rot_center(sprite, (933,515), deg)
        sprite.set_colorkey((0,0,0))
        screen.blit(sprite, rect)
        if pygame.mouse.get_pressed()[0] and __curcd > __weaponcd:
            __curcd = 0
            for i in range(0,__numguns):
                degran = deg+(random.uniform(-5,5))
                _raddeg = (degran*3.14159265359)/180
                xvel -= (math.sin(_raddeg))/10
                yvel -= (math.sin(1.5708-_raddeg))/10
                pb.append(bullet(degran,(math.sin(_raddeg))/10,(math.sin(1.5708-_raddeg))/10,__atk+random.randint(-10,10),933,515,__weaponspeedmult))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True

    if cycle%5 == 0:
        randflicker = random.randint(120,255)
    if GAMESTATE == TITLE:
        titletext = maintitlefont.render('Hyper', False, (randflicker, randflicker, randflicker))
        titletext1 = maintitlefont.render('Drive', False, (randflicker, randflicker, randflicker))
        subtext = subfont.render('Press \'SPACE\' to begin.', False, (randflicker, randflicker, randflicker))
        screen.blit(titletext,(800,355))
        screen.blit(titletext1,(800,445))
        screen.blit(subtext,(820,600))
        dt = clock.tick(60)
    if GAMESTATE == RUNNING:
        hud = pygame.Surface(screen.get_size(), pygame.SRCALPHA, 32)
        hud.blit(hbar,(10,10))
        baramt = int((__hp/__hpmax)*274)
        pygame.draw.rect(hud,(140,15,15),(12,12,baramt,16))
        hptext = font.render("%d / %d" % (__hp, __hpmax), False, (randflicker, randflicker, randflicker))
        hud.blit(hptext,(100,15))

        hud.blit(fbar,(10,40))
        baramt = int((__fuel/__maxfuel)*198)
        pygame.draw.rect(hud,(40,80,150),(12,42,baramt,16))
        hptext = font.render("%d / %d" % (int(__fuel), __maxfuel), False, (randflicker, randflicker, randflicker))
        hud.blit(hptext,(100,45))

        veltotal = math.sqrt((xvel)**2+(yvel)**2)
        xtext = font.render("X: %12.4f" % __GLOBALX, False, (randflicker, randflicker, randflicker))
        ytext = font.render("Y: %12.4f" % __GLOBALY, False, (randflicker, randflicker, randflicker))
        veltext = font.render("%2.2fkm/s" % veltotal, False, (randflicker, randflicker, randflicker))
        fps = font.render("%2.1f FPS" % clock.get_fps(), False, (randflicker, randflicker, randflicker))
        hud.blit(xtext,(12,75))
        hud.blit(ytext,(12,95))
        hud.blit(fps,(1810,10))
        hud.blit(veltext,(12,115))

        screen.blit(hud,(0,0))

    keys = pygame.key.get_pressed()
    if GAMESTATE == TITLE:
        if keys[pygame.K_SPACE]:
            rect = pygame.Surface(screen.get_size(), pygame.SRCALPHA, 32)
            i = 0
            for i in range(0,40):
                rect.fill((0, 0, 0, i))
                screen.blit(rect, (0,0))
                pygame.display.update()
            GAMESTATE = RUNNING
            for i in range(40,0,-1):
                dt = clock.tick(60)
                rect.fill((0, 0, 0, i))
                screen.blit(rect, (0,0))
                pygame.display.update()
    if GAMESTATE == RUNNING:
        if keys[pygame.K_w]:
            raddeg = (deg*3.14159265359)/180
            chgx = (math.sin(raddeg))/(50/__speedmult)
            chgy = (math.sin(1.5708-raddeg))/(50/__speedmult)
            if keys[pygame.K_SPACE] and __fuel > 0:
                chgx = chgx*3
                chgy = chgy*3
                fumes.append(genFume(xvel,yvel,deg,boost=1))
                __fuel -= (1/4)
            xvel += chgx
            yvel += chgy
        fumes.append(genFume(xvel,yvel,deg))
    if __fuel < __maxfuel:
        __fuel += __fuelrecharge
    if __fuel > __maxfuel:
        __fuel = __maxfuel
    dt = clock.tick(60)
    pygame.display.update()
