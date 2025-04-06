import pygame
from math import floor, sqrt, degrees, asin
from random import randint

res = (1000,1000)


class Phys:
    def __init__(self,x,y,w,h,acc,maxV):
        self.x=x
        self.y=y
        self.w=w
        self.h=h
        self.acc=acc
        self.maxV=maxV

        self.j=False
        self.g= 0.8

        self.prevX=x
        self.prevY=y

        self.hV=0
        self.vV=0

        self.hit = pygame.Rect(self.x,self.y,self.w,self.h)

    def physTick(self,beams):
        self.vV += self.g
        self.x += self.hV
        self.y += self.vV
        self.hit = pygame.Rect(self.x,self.y,self.w,self.h)

        for beam in beams:

            if beam.hit.colliderect(self.hit):  # prev frame
                if self.x + self.w >= beam.x + 1 > self.prevX + self.w:  # right ccollide
                    self.x = self.prevX
                    self.hV = 0
                if self.x <= beam.x + beam.w - 1 < self.prevX:  # left col
                    self.x = self.prevX
                    self.hV = 0

                if self.y + self.h >= beam.y + 1 > self.prevY + self.h:  # bottom collide
                    self.y = self.prevY
                    self.vV = 0
                    self.j = False
                if self.y <= beam.x + beam.w - 1 < self.prevY:  # top collide
                    self.y = self.prevY
                    self.vV = 0

        self.prevX = self.x
        self.prevY = self.y

class Player(Phys):
    def __init__(self,x,y):
        self.x = x
        self.y = y
        self.img = pygame.image.load('player.png')
        w = self.img.get_width()
        h = self.img.get_height()

        Phys.__init__(self,x,y,w,h,0.7,15)

        self.walkIn= 0
        self.direct = 1

    def playerTick(self,keys,beams):
        self.physTick(beams)

        if keys[pygame.K_a] and self.hV > self.maxV * -1:
            self.hV -= self.acc
        if keys[pygame.K_d] and self.hV < self.maxV:
            self.hV += self.acc
        if keys[pygame.K_SPACE] and self.j is False:
            self.vV -= 6
            self.j = True
        if keys[pygame.K_w] and self.j is False:
            self.vV -= 10
            self.j = True
        if self.hV > 0:
            self.direct = 1
        elif self.hV < 0:
            self.direct = 0
        if not (keys[pygame.K_d] or keys[pygame.K_a]):
            if self.hV > 0:
                self.hV -= self.acc
            elif self.hV < 0:
                self.hV += self.acc


    def draw(self,screen,bg):
        screen.blit(self.img,(self.x,self.y))
        if bg.w - res[0] / 2 > self.x >= res[0] /2:
            x_s = res[0] /2
        elif self.x >= bg.w - res[0] /2:
            x_s = self.x - bg.w + res[0]
        else:
            x_s = self.x



class Beam:
    def __init__(self,x,y,w,h):
        self.x=x
        self.y=y
        self.w=w
        self.h=h
        self.hit=pygame.Rect(self.x,self.y,self.w,self.h)

    def draw(self,screen,bgX):
        pygame.draw.rect(screen,(100,100,100),(self.x + bgX, self.y, self.w,self.h))

class Exit:
    def __init__(self,x,y):
        self.img = pygame.image.load("exit.png")
        self.x = x
        self.y =y
        self.w = self.img.get_width()
        self.h = self.img.get_height()
        self.hit = pygame.Rect(self.x,self.y,self.w,self.h)

    def draw(self,screen,bg):
        screen.blit(self.img,(self.x,self.y))

class Button:
    def __init__(self,x,y,file):
        self.x = x
        self.y = y
        self.buttImg=pygame.image.load(f"{file}.png")
        self.buttHover=pygame.image.load(f"{file}_hover.png")
        self.hit = pygame.Rect(self.x,self.y,self.buttImg.get_width(),self.buttImg.get_height())

    def tick(self):
        if self.hit.collidepoint(pygame.mouse.get_pos()):
            if pygame.mouse.get_pressed()[0]:
                return True
    def draw(self,screen):
        if self.hit.collidepoint(pygame.mouse.get_pos()):
            screen.blit(self.buttHover,(self.x,self.y))
        else:
            screen.blit(self.buttImg,(self.x,self.y))


class Background:
    def __init__(self):
        self.x = 0
        self.y = 0
        self.img = pygame.image.load('background.png')
        self.w = self.img.get_width()

    def draw(self,screen):

        screen.blit(self.img,(self.x,self.y))


import pygame
import random

pygame.init()
#res = (1000,1000)
screen = pygame.display.set_mode(res)
captions = ['globus','sphere','this game is garbo','ball','boll','kula','kulka','kamuolys','opira','pila','baldge','kura','orb','Faraon Kula Rozpierdala Caly Kosmos 6','bold','balla','glomera','testecle','kulka','sfera','kurwa pryndzypałki','kremuwka papjeska']
caption = random.choice(captions)
pygame.display.set_caption(caption)
clock=pygame.time.Clock()

def level_1():
   level = 0
   running=True
   player = Player(1,401)
   clock = 0
   background = Background()
   beams = [Beam(1,501,1000,10),
            ]

   exit1 = Exit(970,470)

   while running:
       delta = pygame.time.Clock().tick(60) / 1000
       clock += delta

       for event in pygame.event.get():
           if event.type == pygame.QUIT:
               pygame.quit()
           elif event.type == pygame.KEYDOWN:
               if event.key == pygame.K_1:
                   level_1()

       background.draw(screen)
       keys = pygame.key.get_pressed()
       exit1.draw(screen,background)
       player.playerTick(keys, beams)
       player.draw(screen, background)

       for beam in beams:
           beam.draw(screen, background.x)

       if exit1.hit.colliderect(player.hit):
           level_2()

       pygame.display.update()

def level_2():
    running = True
    player = Player(1,401)
    clock = 0
    background = Background()
    beams = [Beam(1, 501, 120, 10),
             Beam(251,501,100,10),
             Beam(451,501,100,10),
             Beam(651,501,100,10),
             Beam(851,501,150,10)]

    exit1 = Exit(901, 470)

    while running:
        delta = pygame.time.Clock().tick(60) / 1000
        clock += delta
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    level_2()


        background.draw(screen)
        keys = pygame.key.get_pressed()
        exit1.draw(screen, background)
        player.playerTick(keys, beams)
        player.draw(screen, background)

        for beam in beams:
            beam.draw(screen, background.x)

        if exit1.hit.colliderect(player.hit):

            level_3()

        pygame.display.update()

def level_3():
    running = True
    player = Player(1,401)
    clock = 0
    background = Background()
    beams = [Beam(1, 501, 80, 10),
             Beam(231,501,80,10),
             Beam(431,501,80,10),
             Beam(631,501,80,10),
             Beam(831,501,180,10)]

    exit1 = Exit(901, 470)

    while running:
        delta = pygame.time.Clock().tick(60) / 1000
        clock += delta
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    level_3()


        background.draw(screen)
        keys = pygame.key.get_pressed()
        exit1.draw(screen, background)
        player.playerTick(keys, beams)
        player.draw(screen, background)

        for beam in beams:
            beam.draw(screen, background.x)

        if exit1.hit.colliderect(player.hit):
            level_4()

        pygame.display.update()

def level_4():
    running = True
    player = Player(1,800)
    clock = 0
    background = Background()
    beams = [Beam(1,999,999,30),
             Beam(100,950,150,10),
             Beam(170,900,150,10),
             Beam(220,850,150,10),
             Beam(270,800,150,10),
             Beam(320,750,150,10),
             Beam(370,700,150,10),
             Beam(420,650,150,10),
             Beam(470,600,150,10),
             Beam(520,550,150,10),
             Beam(570,500,150,10),
             Beam(620,450,150,10),
             Beam(670,400,150,10),
             Beam(720,350,150,10),
             Beam(770,300,150,10),
             Beam(820,250,150,10),
             Beam(870,200,300,10),]

    exit1 = Exit(951, 170)

    while running:
        delta = pygame.time.Clock().tick(60) / 1000
        clock += delta
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    level_4()


        background.draw(screen)
        keys = pygame.key.get_pressed()
        exit1.draw(screen, background)
        player.playerTick(keys, beams)
        player.draw(screen, background)

        for beam in beams:
            beam.draw(screen, background.x)

        if exit1.hit.colliderect(player.hit):
            level_5()

        pygame.display.update()

def level_5():
    running = True
    player = Player(1,901)
    clock = 0
    background = Background()
    beams =  [Beam(1,999,999,30),
             Beam(450,950,60,10),
             Beam(550,900,60,10),
             Beam(450,850,60,10),
             Beam(550,800,60,10),
             Beam(450,750,60,10),
             Beam(550,700,60,10),
             Beam(450,650,60,10),
             Beam(550,600,60,10),
             Beam(450,550,60,10),
             Beam(550,500,60,10),
             Beam(450,450,60,10),
             Beam(550,400,60,10),
             Beam(450,350,60,10),
             Beam(550,300,60,10),
             Beam(450,250,60,10),
             Beam(500,200,40,10),]

    exit1 = Exit(502, 170)

    while running:
        delta = pygame.time.Clock().tick(60) / 1000
        clock += delta
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    level_5()


        background.draw(screen)
        keys = pygame.key.get_pressed()
        exit1.draw(screen, background)
        player.playerTick(keys, beams)
        player.draw(screen, background)

        for beam in beams:
            beam.draw(screen, background.x)

        if exit1.hit.colliderect(player.hit):
            level_6()

        pygame.display.update()

def level_6():
    running = True
    player = Player(1,800)
    clock = 0
    background = Background()
    beams = [Beam(1, 901, 30, 10),
             Beam(231,901,50,10),
             Beam(331,901,30,10),
             Beam(431,901,50,10),
             Beam(531,901,20,10),
             Beam(631,901,20,10),
             Beam(731,901,20,10),
             Beam(831,851,80,10),
             Beam(740,811,40,10),
             Beam(670,771,40,10),
             Beam(630,731,40,10),
             Beam(530,681,80,10),
             Beam(480,631,40,10),
             Beam(420,591,40,10),
             Beam(340, 591, 40, 10),
             Beam(280, 541, 40, 10),
             Beam(340, 491, 30, 10),
             Beam(280, 441, 40, 10),
             Beam(340, 391, 30, 10),
             Beam(280, 341, 40, 10),
             Beam(340, 291, 30, 10),
             Beam(280, 241, 40, 10),
             Beam(340, 191, 30, 10),
             Beam(440, 191, 30, 10),
             Beam(560, 181, 30, 10),
             Beam(640, 181, 30, 10),
             Beam(740, 171, 30, 10),
             Beam(800, 171, 300, 10),]

    exit1 = Exit(951, 140)

    while running:
        delta = pygame.time.Clock().tick(60) / 1000
        clock += delta
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    level_6()


        background.draw(screen)
        keys = pygame.key.get_pressed()
        exit1.draw(screen, background)
        player.playerTick(keys, beams)
        player.draw(screen, background)

        for beam in beams:
            beam.draw(screen, background.x)

        if exit1.hit.colliderect(player.hit):
            level_7()

        pygame.display.update()

def level_7():
    running = True
    player = Player(1,11)
    clock = 0
    background = Background()
    beams =  [Beam(1,50,50,10),
             Beam(850,950,70,10)]

    exit1 = Exit(852, 920)

    while running:
        delta = pygame.time.Clock().tick(60) / 1000
        clock += delta
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    level_7()


        background.draw(screen)
        keys = pygame.key.get_pressed()
        exit1.draw(screen, background)
        player.playerTick(keys, beams)
        player.draw(screen, background)

        for beam in beams:
            beam.draw(screen, background.x)

        if exit1.hit.colliderect(player.hit):
            level_8()

        pygame.display.update()


def level_8():
    running = True
    player = Player(1,11)
    clock = 0
    background = Background()
    beams =  [Beam(1,50,50,10),
             Beam(950,950,70,10)]

    exit1 = Exit(952, 920)

    while running:
        delta = pygame.time.Clock().tick(60) / 1000
        clock += delta
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    level_8()


        background.draw(screen)
        keys = pygame.key.get_pressed()
        exit1.draw(screen, background)
        player.playerTick(keys, beams)
        player.draw(screen, background)

        for beam in beams:
            beam.draw(screen, background.x)

        if exit1.hit.colliderect(player.hit):
            level_9()

        pygame.display.update()


def level_9():
    running = True
    player = Player(1,11)
    clock = 0
    background = Background()
    beams =  [Beam(1,999,999,30),
             Beam(450,950,30,10),
             Beam(550,900,30,10),
             Beam(450,850,30,10),
             Beam(550,800,30,10),
             Beam(450,750,30,10),
             Beam(550,700,30,10),
             Beam(450,650,30,10),
             Beam(550,600,30,10),
             Beam(450,550,30,10),
             Beam(550,500,30,10),
             Beam(450,450,30,10),
             Beam(550,400,30,10),
             Beam(450,350,30,10),
             Beam(550,300,30,10),
             Beam(450,250,30,10),
             Beam(550,200,30,10),
             Beam(450, 150, 30, 10),
             Beam(500, 100, 40, 10) ]

    exit1 = Exit(502, 70)

    while running:
        delta = pygame.time.Clock().tick(60) / 1000
        clock += delta
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    level_9()


        background.draw(screen)
        keys = pygame.key.get_pressed()
        exit1.draw(screen, background)
        player.playerTick(keys, beams)
        player.draw(screen, background)

        for beam in beams:
            beam.draw(screen, background.x)

        if exit1.hit.colliderect(player.hit):
            winScreen()

        pygame.display.update()

def winScreen():
    running = True
    winBg = pygame.image.load("EndScreen.png")
    boobieButton = Button(400,800,"button_Boobie")
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

        if boobieButton.tick():
            boobie()

        screen.blit(winBg,(0,0))
        boobieButton.draw(screen)

        pygame.display.update()



def boobie():
    running = True
    boobieBg = pygame.image.load("Boobie.gif")
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

        screen.blit(boobieBg,(400,400))
        pygame.display.update()


def main():
    run = True
    clock = 0
    bg = pygame.image.load("TitleScreen.png")
    playButton= Button(220,800,"button_Play")

    while run:

        events = pygame.event.get()
        for event in events:

            if event.type == pygame.QUIT:
                pygame.quit()

        if playButton.tick():
            level_1()

        screen.blit(bg,(0,0))
        playButton.draw(screen)

        pygame.display.update()

if __name__ == "__main__":
    main()
