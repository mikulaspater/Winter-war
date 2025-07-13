#made by Mikulas Pater 2025
#POkud toto někdo čte, tak vítej, poutníče
import pygame
import json
import random
import math
import sys
import copy
hitboxes=0
pygame.init()
pygame.mixer.init()
pygame.mixer.set_num_channels(48)
pygame.display.set_caption("Zimní válka")
VOLUME=100
WIDTH,HEIGHT=pygame.display.get_desktop_sizes()[0]
MWIDTH,MHEIGHT=1920, 1080
if WIDTH-(48/27*HEIGHT)>3:
    WIDTH=int(48/27*HEIGHT)
    print(f"Resize --> New width: {WIDTH}, height: {HEIGHT}")
elif HEIGHT-(27/48*WIDTH)>3:
    HEIGHT=int(27/48*WIDTH)
    print(f"Resize --> width: {WIDTH}, New height: {HEIGHT}")
fullscreen=True
pygame.mouse.set_visible(0)
clock=pygame.time.Clock()
#screen=pygame.display.set_mode((WIDTH,HEIGHT))
def copygun(g):return Gun(g.firerate, g.maxspread, g.texturename, g.firespeed, g.angle, g.WIDTH, g.HEIGHT, g.twidth, g.theight, g.increments, g.rounds, g.shotsound, g.reloadsound, g.maxrw)
class Supertarget:
    def __init__(self,x,y,texture,hp=100):
        self.x=x
        self.y=y
        self.texture=texture
        self.hp=hp
    def render(self,screen,cmrx,cmry):
        rect=self.texture.get_rect()
        rect.center=(self.x-cmrx, self.y-cmry)
        screen.blit(self.texture, rect)
    def got_hit(self,bullet):
        rect=self.texture.get_rect()
        rect.center=(self.x,self.y)
        return rect.collidepoint(bullet.x,bullet.y)
class Bullet:
    def __init__(self,x,y,vx,vy,pe):
        self.x=x
        self.y=y
        self.vx=vx
        self.vy=vy
        self.pe=pe
    def update(self):
        self.x+=self.vx
        self.y+=self.vy
        self.vx=0.995*self.vx
        self.vy=0.995*self.vy
    def render(self, screen,cmrx,cmry):
        screen.set_at((int(self.x-cmrx), int(self.y)),(0,0,0))
        screen.set_at((int(self.x+1-cmrx), int(self.y-cmry)),(0,0,0))
        screen.set_at((int(self.x-1-cmrx), int(self.y-cmry)),(0,0,0))
        screen.set_at((int(self.x-cmrx), int(self.y+1-cmry)),(0,0,0))
        screen.set_at((int(self.x-cmrx), int(self.y-1-cmry)),(0,0,0))
        screen.set_at((int(self.x+1-cmrx), int(self.y+1-cmry)),(5,5,5))
        screen.set_at((int(self.x-1-cmrx), int(self.y-1-cmry)),(5,5,5))
        screen.set_at((int(self.x-1-cmrx), int(self.y+1-cmry)),(5,5,5))
        screen.set_at((int(self.x+1-cmrx), int(self.y-1-cmry)),(5,5,5))
        screen.set_at((int(self.x+2-cmrx), int(self.y-cmry)),(5,5,5))
        screen.set_at((int(self.x-2-cmrx), int(self.y-cmry)),(5,5,5))
        screen.set_at((int(self.x-cmrx), int(self.y+2-cmry)),(5,5,5))
        screen.set_at((int(self.x-cmrx), int(self.y-2-cmry)),(5,5,5))
        screen.set_at((int(self.x+2-cmrx), int(self.y-1-cmry)),(5,5,5))
        screen.set_at((int(self.x-2-cmrx), int(self.y+1-cmry)),(5,5,5))
        screen.set_at((int(self.x+1-cmrx), int(self.y+2-cmry)),(5,5,5))
        screen.set_at((int(self.x-1-cmrx), int(self.y-2-cmry)),(5,5,5))
        screen.set_at((int(self.x+2-cmrx), int(self.y+1-cmry)),(5,5,5))
        screen.set_at((int(self.x-2-cmrx), int(self.y-1-cmry)),(5,5,5))
        screen.set_at((int(self.x-1-cmrx), int(self.y+2-cmry)),(5,5,5))
        screen.set_at((int(self.x+1-cmrx), int(self.y-2-cmry)),(5,5,5))
sound=1
screen=pygame.display.set_mode((0,0),pygame.FULLSCREEN)
class Player:
    def __init__(self, x, y,WIDTH,HEIGHT,posguns,hp=100,molotovcount=0):
        self.x=x
        self.y=y
        self.relativex=x
        self.relativey=y
        self.posguns=posguns
        self.gun=self.posguns[0]
        self.gunind=0
        self.sizex=int(54*(WIDTH/1920))
        self.sizey=int(78*(HEIGHT/1080))
        self.facing="r"
        self.imgidl1r=pygame.transform.scale(pygame.image.load("resources/idle1rp.png").convert_alpha(),(self.sizex, self.sizey))
        self.imgidl2r=pygame.transform.scale(pygame.image.load("resources/idle2rp.png").convert_alpha(),(self.sizex, self.sizey))
        self.imgidl1l=pygame.transform.scale(pygame.image.load("resources/idle1lp.png").convert_alpha(),(self.sizex, self.sizey))
        self.imgidl2l=pygame.transform.scale(pygame.image.load("resources/idle2lp.png").convert_alpha(),(self.sizex, self.sizey))
        self.drp=pygame.transform.scale(pygame.image.load("resources/drp.png").convert_alpha(),(int(78*(WIDTH/1920)), int(42*(HEIGHT/1080))))
        self.dlp=pygame.transform.scale(pygame.image.load("resources/dlp.png").convert_alpha(),(int(78*(WIDTH/1920)), int(42*(HEIGHT/1080))))
        self.hp=hp
        self.molotovcount=molotovcount
    def chnggun(self,dir):
        ang=self.gun.angle
        if dir==-1:
            self.gunind-=1
            if self.gunind<0:
                self.gunind=len(self.posguns)-1
        if dir==1:
            self.gunind+=1
            if self.gunind==len(self.posguns):self.gunind=0
        self.gun=self.posguns[self.gunind]
        self.gun.angle=ang
    def update(self, dir, gundir,cmrx,cmry,r_boundary=WIDTH):
        global WIDTH, HEIGHT
        if self.hp<=0:return [cmrx,cmry]
        prf=self.facing
        if dir[0]==1:self.facing="r"
        if dir[0]==-1:self.facing="l"
        if self.gun.reloading and self.facing!=prf:
            self.gun.prevangle=360-self.gun.prevangle
        speed=9/4
        if self.x>-WIDTH//2 and dir[0]==-1:
            self.x+=speed*dir[0]
            relativex,relativey=self.x-cmrx,self.y-cmry
            if relativex<WIDTH//7 or relativex>6*WIDTH//7 or self.gun.firerate>150:cmrx+=speed*dir[0]
        if self.x<r_boundary and dir[0]==1:
            self.x+=speed*dir[0]
            relativex,relativey=self.x-cmrx,self.y-cmry
            if relativex<WIDTH//7 or relativex>6*WIDTH//7 or self.gun.firerate>150:cmrx+=speed*dir[0]
        if dir[1]==1:
            if self.y<1.25*HEIGHT:
                self.y+=speed*dir[1]
                relativex,relativey=self.x-cmrx,self.y-cmry
                if relativey<HEIGHT//5 or relativey>4*HEIGHT//5 or self.gun.firerate>150:cmry+=speed*dir[1]
        if dir[1]==-1:
            if self.y>-0.25*HEIGHT:
                self.y+=speed*dir[1]
                relativex,relativey=self.x-cmrx,self.y-cmry
                if relativey<HEIGHT//5 or relativey>4*HEIGHT//5 or self.gun.firerate>150:cmry+=speed*dir[1]
        
        
        if (self.facing=="r") == (self.gun.angle>180):
            self.gun.angle=360-self.gun.angle
        targangle=""
        #klij
        if self.gun.reloading==1:
            targangle=0
        elif self.gun.reloading==2:
            targangle=self.gun.prevangle
        elif gundir[0]:
            targangle=180-45*(self.facing=="r" and gundir[1])+45*(self.facing=="l" and gundir[3])
        elif gundir[2]:
            targangle=360+45*(self.facing=="r" and gundir[1])-45*(self.facing=="l" and gundir[3])
            targangle=targangle%360
        elif gundir[1] and self.facing=="r":
            targangle=90
        elif gundir[3] and self.facing=="l":
            targangle=270
        if targangle!="" and self.gun.angle!=targangle:
            if abs(targangle-self.gun.angle)<=5:
                self.gun.angle=targangle
            elif abs(targangle-self.gun.angle)<=180:
                self.gun.angle+=5*(targangle>self.gun.angle)-5*(targangle<self.gun.angle)
            else:
                targangle=360-targangle
                if abs(targangle-self.gun.angle)<=5:
                    self.gun.angle=targangle
                elif abs(targangle-self.gun.angle)<=180:
                    self.gun.angle+=5*(targangle>self.gun.angle)-5*(targangle<self.gun.angle)
        if self.gun.reloading==1 and self.gun.angle in [0,360]:
            if self.gun.rldwait>=self.gun.maxrw:
                self.gun.reloading=2
                self.gun.bullets=self.gun.rounds
            else:
                self.gun.rldwait+=1
        if self.gun.reloading==2 and self.gun.angle==self.gun.prevangle:
            self.gun.reloading=0
            self.gun.rldwait=0
        return cmrx,cmry
    def reload(self):
        global VOLUME
        if self.gun.reloading!=0 or self.gun.bullets==self.gun.rounds:return
        self.gun.prevangle=self.gun.angle
        self.gun.reloading=1
        channel=pygame.mixer.find_channel()
        self.gun.reload.set_volume(VOLUME/100)
        if channel:
            self.gun.reload.play()
    def render(self,screen, WIDTH,HEIGHT,frame,cmrx,cmry):
        if self.hp<=0:
            if self.facing=="r":
                screen.blit(self.drp, (self.x-int(78*(WIDTH/1920))/2-cmrx, self.y-int(42*(WIDTH/1920))//2-cmry))
            else:
                screen.blit(self.dlp, (self.x-int(78*(WIDTH/1920))//2-cmrx, self.y-int(42*(WIDTH/1920))/2-cmry))
        else:
            if frame%30<15:
                exec("screen.blit(self.imgidl1"+self.facing+", (self.x-self.sizex//2-cmrx, self.y-self.sizey//2-cmry))")
            else:
                exec("screen.blit(self.imgidl2"+self.facing+", (self.x-self.sizex//2-cmrx, self.y-self.sizey//2-cmry))")
    def got_hit(self,bx,by,frame):
        global hitboxes, screen
        if frame%30<15:
            if self.facing=="l":
                rect=self.imgidl1l.get_rect(center=(self.x, self.y))
            else:
                rect=self.imgidl1r.get_rect(center=(self.x, self.y))
        else:
            if self.facing=="l":
                rect=self.imgidl2l.get_rect(center=(self.x,self.y))
            else:
                rect=self.imgidl2r.get_rect(center=(self.x, self.y))
        if hitboxes:
            pygame.draw.rect(screen, (0,255,0),rect,2)
            screen.set_at((self.x,self.y),(255,0,0))
        return rect.collidepoint((bx,by))
class NPC:
    def __init__(self, x, y,WIDTH,HEIGHT,posguns,hp=100,targetx="N",targety="N"):
        self.x=x
        self.y=y
        self.relativex=x
        self.relativey=y
        self.posguns=posguns
        self.gun=self.posguns[0]
        self.gunind=0
        self.sizex=int(54*(WIDTH/1920))
        self.sizey=int(78*(HEIGHT/1080))
        self.facing="l"
        self.imgidl1r=pygame.transform.scale(pygame.image.load("resources/idle1re.png").convert_alpha(),(self.sizex, self.sizey))
        self.imgidl2r=pygame.transform.scale(pygame.image.load("resources/idle2re.png").convert_alpha(),(self.sizex, self.sizey))
        self.imgidl1l=pygame.transform.scale(pygame.image.load("resources/idle1le.png").convert_alpha(),(self.sizex, self.sizey))
        self.imgidl2l=pygame.transform.scale(pygame.image.load("resources/idle2le.png").convert_alpha(),(self.sizex, self.sizey))
        self.dre=pygame.transform.scale(pygame.image.load("resources/dre.png").convert_alpha(),(int(78*(WIDTH/1920)), int(42*(HEIGHT/1080))))
        self.dle=pygame.transform.scale(pygame.image.load("resources/dle.png").convert_alpha(),(int(78*(WIDTH/1920)), int(42*(HEIGHT/1080))))
        self.runnin=0
        self.seesplayer=0
        if targetx=="N":targetx=self.x+100
        if targety=="N":targety=self.y+100
        self.target=[targetx,targety]
        self.hp=hp
        self.ontarget=0
        self.wandering=1
    def aimatplayer(self,player):
        plrl=["r","l"][player.x<self.x]
        diffx=abs(self.x-player.x)
        diffy=abs(self.y-player.y)
        if self.facing!=plrl or diffy==0:return [90,270][self.facing=="l"]
        if self.y>player.y:
            if self.x<=player.x:
                return int(math.degrees(math.atan(diffx/diffy)))
            else:
                return 360-int(math.degrees(math.atan(diffx/diffy)))
        else:
            if self.x<=player.x:
                return 180-int(math.degrees(math.atan(diffx/diffy)))
            else:
                return 180+int(math.degrees(math.atan(diffx/diffy)))
    def update(self, player,WIDTH,HEIGHT,frames,supertarget=None):
        global screen
        targangle=""
        bul=0
        if self.hp<=0:return 0
        if self.gun.bullets==0:self.reload()
        pdist=math.sqrt((player.x-self.x)**2+(player.y-self.y)**2)
        plrl=["r","l"][player.x<self.x]
        try:q=abs(self.x-player.x)/abs(self.y-player.y)
        except ZeroDivisionError:q=100
        if pdist<WIDTH//20 and plrl==self.facing:
            self.seesplayer=1
        elif pdist<WIDTH//5 and plrl==self.facing and abs(self.x-player.x)>abs(self.y-player.y):
            self.seesplayer=1
        elif pdist<WIDTH and plrl==self.facing and q>4:
            self.seesplayer=1
        if self.seesplayer and player.hp>0:
            if (not supertarget) or pdist<math.sqrt((supertarget.x-self.x)**2+(supertarget.y-self.y)**2):
                if pdist<WIDTH//3:
                    if player.x<self.x:self.facing="l"
                    else:self.facing="r"
                    self.target=[self.x,self.y]
                    targangle=self.aimatplayer(player)
                    if abs(targangle-self.gun.angle)<5:
                        bul=self.gun.fire(frames,self.x,self.y, screen, self.facing)
                        if type(bul)==Bullet:
                            bul.pe=1
                        else:bul=0
                else:
                    self.target=[player.x,player.y]
            elif not supertarget:
                if (abs(self.x-self.target[0])<5 and abs(self.y-self.target[1])<5) or self.ontarget:
                    self.target=[int(self.target[0]-250*(WIDTH/1920)+random.randrange(int(500*(WIDTH/1920)))),int(self.target[1]-250*(WIDTH/1920)+random.randrange(int(500*(WIDTH/1920))))]
                    self.ontarget=0
                    self.wandering=1
                    self.gun.angle=[90,270][self.facing=="l"]
            else:
                sdist=math.sqrt((self.x-supertarget.x)**2+(self.y-supertarget.y)**2)
                if sdist<WIDTH//3:
                    if supertarget.x<self.x:self.facing="l"
                    else:self.facing="r"
                    self.target=[self.x,self.y]
                    targangle=self.aimatplayer(supertarget)
                    if abs(targangle-self.gun.angle)<5 and random.randrange(2):
                        bul=self.gun.fire(frames,self.x,self.y, screen, self.facing)
                        if type(bul)==Bullet:
                            bul.pe=1
                        else:bul=0
                else:
                    self.target=[supertarget.x,supertarget.y]
            self.wandering=0
        elif supertarget:
            sdist=math.sqrt((self.x-supertarget.x)**2+(self.y-supertarget.y)**2)
            if sdist<WIDTH//3:
                if supertarget.x<self.x:self.facing="l"
                else:self.facing="r"
                self.target=[self.x,self.y]
                targangle=self.aimatplayer(supertarget)
                if abs(targangle-self.gun.angle)<5:
                    bul=self.gun.fire(frames,self.x,self.y, screen, self.facing)
                    if type(bul)==Bullet:
                        bul.pe=1
                    else:bul=0
            else:
                self.target=[supertarget.x,supertarget.y]
            self.wandering=0
        elif (abs(self.x-self.target[0])<5 and abs(self.y-self.target[1])<5) or self.ontarget:
            self.target=[int(self.target[0]-250*(WIDTH/1920)+random.randrange(int(500*(WIDTH/1920)))),int(self.target[1]-250*(WIDTH/1920)+random.randrange(int(500*(WIDTH/1920))))]
            self.ontarget=0
            self.wandering=1
            self.gun.angle=[90,270][self.facing=="l"]
        


        """dir=[0,0]
        if abs(self.x-self.target[0])>5:
            if self.x<self.target[0]:
                dir[0]=1
            elif self.x>self.target[0]:
                dir[0]=-1
        if abs(self.y-self.target[1])>5:
            if self.y<self.target[1]:
                dir[1]=1
            elif self.y>self.target[1]:
                dir[1]=-1
        if dir==[0,0]:self.ontarget=1"""
        if self.wandering:speed=HEIGHT/1080
        else:speed=3*(HEIGHT/1080)
        if math.sqrt((self.target[0]-self.x)**2+(self.target[1]-self.y)**2)>speed:
            dx=abs(self.target[0]-self.x)
            dy=abs(self.target[1]-self.y)
            if dx!=0:
                fx=speed/math.sqrt(1+(dy**2)/(dx**2))
                fy=(dy/dx)*fx
            else:
                fx=0
                fy=speed
            prf=self.facing
            if self.x>self.target[0]:
                self.facing="l"
                self.x-=fx
            elif self.x<self.target[0]:
                self.facing="r"
                self.x+=fx
            if self.y>self.target[1]:
                self.y-=fy
            else:
                self.y+=fy
            if self.gun.reloading and self.facing!=prf:
                self.gun.prevangle=360-self.gun.prevangle
            if (self.facing=="r") == (self.gun.angle>180):
                self.gun.angle=360-self.gun.angle
        else:
            self.x=self.target[0]
            self.y=self.target[1]
        if self.gun.reloading==1:
            targangle=0
        elif self.gun.reloading==2:
            targangle=self.gun.prevangle
        if targangle!="" and self.gun.angle!=targangle:
            if abs(targangle-self.gun.angle)<=5:
                self.gun.angle=targangle
            elif abs(targangle-self.gun.angle)<=180:
                self.gun.angle+=5*(targangle>self.gun.angle)-5*(targangle<self.gun.angle)
            else:
                targangle=360-targangle
                if abs(targangle-self.gun.angle)<=5:
                    self.gun.angle=targangle
                elif abs(targangle-self.gun.angle)<=180:
                    self.gun.angle+=5*(targangle>self.gun.angle)-5*(targangle<self.gun.angle)
        if self.gun.reloading==1 and self.gun.angle in [0,360]:
            if self.gun.rldwait>=self.gun.maxrw:
                self.gun.reloading=2
                self.gun.bullets=self.gun.rounds
            else:
                self.gun.rldwait+=1
        if self.gun.reloading==2 and self.gun.angle==self.gun.prevangle:
            self.gun.reloading=0
            self.gun.rldwait=0
        return bul
    def reload(self):
        global VOLUME
        if self.gun.reloading!=0 or self.gun.bullets==self.gun.rounds:return
        self.gun.prevangle=self.gun.angle
        self.gun.reloading=1
        channel=pygame.mixer.find_channel()
        self.gun.reload.set_volume(VOLUME/100)
        if channel:
            self.gun.reload.play()
    def render(self,screen, WIDTH,HEIGHT,frame,cmrx,cmry):
        if self.hp<=0:
            if self.facing=="r":
                screen.blit(self.dre, (self.x-int(112*(WIDTH/1920))/2-cmrx, self.y-int(56*(WIDTH/1920))//2-cmry))
            else:
                screen.blit(self.dle, (self.x-int(112*(WIDTH/1920))//2-cmrx, self.y-int(56*(WIDTH/1920))/2-cmry))
        elif self.runnin and 0:
            screen.blit(pygame.transform.scale(pygame.image.load("resources/run"+self.facing+(frame%8)+".png").convert(),(self.sizex, self.sizey)), (self.x-self.sizex//2, self.y-self.sizey//2))
        else:
            if frame%30<15:
                exec("screen.blit(self.imgidl1"+self.facing+", (self.x-self.sizex//2-cmrx, self.y-self.sizey//2-cmry))")
            else:
                exec("screen.blit(self.imgidl2"+self.facing+", (self.x-self.sizex//2-cmrx, self.y-self.sizey//2-cmry))")
    def got_hit(self,bx,by,frame,cmrx,cmry):
        global screen,hitboxes
        if self.hp<=0:
            rect=self.dre.get_rect(center=(self.x,self.y))
        elif frame%30<15:
                if self.facing=="l":
                    rect=self.imgidl1l.get_rect(center=(self.x, self.y))
                else:
                    rect=self.imgidl1r.get_rect(center=(self.x, self.y))
        else:
            if self.facing=="l":
                rect=self.imgidl2l.get_rect(center=(self.x, self.y))
            else:
                rect=self.imgidl2r.get_rect(center=(self.x, self.y))
        if hitboxes:
            pygame.draw.rect(screen, (255,0,0),rect,2)
        return rect.collidepoint((bx,by))

class vlocka:
    def __init__(self,WIDTH,HEIGHT,randomy=0):
        if not randomy:
            self.y=0
        else:
            self.y=random.randrange(HEIGHT)
        self.x=random.randrange(WIDTH)
        self.color=(255-random.randrange(100),255,255)
    def render(self,display):
        display.set_at((self.x, int(self.y)), self.color)
PHASE="menu"
class Text:
    def __init__(self, x, y, text,color):
        self.x=x
        self.y=y
        self.text=text
        self.color=color
    def render(self,screen,fontsize):
        font=pygame.font.Font("resources/font/SHPinscher-Regular.otf",fontsize)
        text=font.render(self.text, True, self.color)
        textRect=text.get_rect()
        textRect.center=(self.x,self.y)
        screen.blit(text, textRect)
class TemporaryText:
    def __init__(self, x, y, text,color,start,end):
        self.x=x
        self.y=y
        self.text=text
        self.color=color
        self.elapsed=0
        self.start=start
        self.end=end
    def render(self,screen,fontsize,fadein=1):
        self.elapsed+=1
        font=pygame.font.Font("resources/font/SHPinscher-Regular.otf",fontsize)
        text=font.render(self.text, True, self.color).convert_alpha()
        if self.elapsed<self.start or self.elapsed>self.end:return
        if fadein:
            textRect=text.get_rect()
            textRect.center=(self.x,self.y)
            if 4*(self.elapsed-self.start)<255:
                text.set_alpha(4*(self.elapsed-self.start))
            elif 4*(self.end-self.elapsed)<255:
                text.set_alpha(4*(self.end-self.elapsed))
            else:
                text.set_alpha(255)
            screen.blit(text, textRect)
        else:
            textRect=text.get_rect()
            textRect.center=(self.x,self.y)
            screen.blit(text, textRect)
class Button:
    def __init__(self, x, y, text, marked,pressfunc):
        self.x=x
        self.y=y
        self.text=text
        self.marked=marked
        self.pressfunc=pressfunc
    def press(self):
        self.pressfunc()
    def render(self,screen,fontsize):
        font=pygame.font.Font("resources/font/SHPinscher-Regular.otf",fontsize)
        if self.marked:
            color=(115,0,0)
        else:
            color=(255,255,255)
        text=font.render(self.text, True, color)
        textRect=text.get_rect()
        textRect.center=(self.x,self.y)
        screen.blit(text, textRect)
class Gun:
    def __init__(self, firerate, maxspread, texturename, firespeed,angle,WIDTH, HEIGHT,twidth,theight, increments,rounds,shotsound,reloadsound,maxrw):
        self.firerate=firerate
        self.maxspread=maxspread
        self.texturename=texturename
        self.texturel=pygame.transform.scale(pygame.image.load("resources/"+texturename+"l.png").convert_alpha(),(twidth, theight))
        self.texturer=pygame.transform.scale(pygame.image.load("resources/"+texturename+"r.png").convert_alpha(),(twidth, theight))
        self.firespeed=firespeed
        self.angle=angle
        self.lastfire=-firerate
        self.WIDTH=WIDTH
        self.HEIGHT=HEIGHT
        self.twidth=twidth
        self.theight=theight
        self.increments=increments
        self.cxil, self.cyil, self.cxir, self.cyir=increments
        self.rounds=rounds
        self.bullets=rounds
        self.reloading=0
        self.prevangle=0
        self.shotsound=shotsound
        self.shot=pygame.mixer.Sound(shotsound)
        self.reloadsound=reloadsound
        self.reload=pygame.mixer.Sound(reloadsound)
        self.rldwait=0
        self.maxrw=maxrw
    def render(self,screen,px,py,facing,cmrx,cmry):
        angle=360-self.angle
        if facing=="r":
            rotimg=pygame.transform.rotate(self.texturer, angle)
            rect=rotimg.get_rect(center=self.texturer.get_rect(center=(px+self.cxir-cmrx,py+self.cyir-cmry)).center)
        elif facing=="l":
            rotimg=pygame.transform.rotate(self.texturel, angle)
            rect=rotimg.get_rect(center=self.texturel.get_rect(center=(px+self.cxil-cmrx,py+self.cyil-cmry)).center)
        screen.blit(rotimg, rect)
    def fire(self,frames,px,py, screen, facing,molotov=0):
        global VOLUME
        if (frames-self.lastfire<self.firerate or self.reloading!=0 or self.bullets==0) and not molotov:return 0
        halfgun=0.5*math.sqrt(self.twidth**2+self.theight**2)
        if self.angle<90:
            centerx, centery=px+self.cxir,py+self.cyir
            xtip=centerx+halfgun*math.sin(math.radians(self.angle))
            ytip=centery-halfgun*math.cos(math.radians(self.angle))
        elif self.angle<180:
            centerx, centery=px+self.cxir,py+self.cyir
            xtip=centerx+halfgun*math.sin(math.radians(180-self.angle))
            ytip=centery+halfgun*math.cos(math.radians(180-self.angle))
        elif self.angle==180 and facing=="r":
            centerx, centery=px+self.cxir,py+self.cyir
            xtip=centerx+halfgun*math.sin(math.radians(180-self.angle))
            ytip=centery+halfgun*math.cos(math.radians(180-self.angle))
        elif self.angle<270:
            centerx, centery=px+self.cxil,py+self.cyil
            xtip=centerx-halfgun*math.sin(math.radians(self.angle-180))
            ytip=centery+halfgun*math.cos(math.radians(self.angle-180))
        else:
            centerx, centery=px+self.cxil,py+self.cyil
            xtip=centerx-halfgun*math.sin(math.radians(360-self.angle))
            ytip=centery-halfgun*math.cos(math.radians(360-self.angle))
        if self.maxspread>0:x=random.randrange(2*self.maxspread)-self.maxspread
        else:x=0
        angle=self.angle+x
        if angle<0:angle=360-angle
        angle=angle%360
        if angle>180:
            if angle>270:
                vx=-self.firespeed*math.sin(math.radians(360-angle))
                vy=-self.firespeed*math.cos(math.radians(360-angle))
            else:
                vx=-self.firespeed*math.sin(math.radians(360-angle))
                vy=-self.firespeed*math.cos(math.radians(360-angle))
        else:
            if angle<90:
                vx=self.firespeed*math.sin(math.radians(angle))
                vy=-self.firespeed*math.cos(math.radians(angle))
            else:
                vx=self.firespeed*math.sin(math.radians(angle))
                vy=-self.firespeed*math.cos(math.radians(angle))
        if not molotov:
            self.lastfire=frames
            self.bullets-=1
            channel=pygame.mixer.find_channel()
            self.shot.set_volume(VOLUME/100)
            if channel:
                self.shot.play()
            return Bullet(xtip, ytip, vx, vy,0)
        else:return [xtip,ytip,vx,vy]
class Tile:
    def __init__(self,x,y,texture):
        self.x=x
        self.y=y
        self.texture=texture
    def render(self,screen,cmrx,cmry):
        screen.blit(self.texture, (self.x-cmrx, self.y-cmry))
class Molotov:
    def __init__(self,x,y,vx,vy):
        self.x=x
        self.y=y
        self.vx=vx
        self.vy=vy
        self.updcounter=0
    def update(self):
        self.x+=self.vx
        self.y+=self.vy
        if self.updcounter>60:return 1
        self.updcounter+=1
    def render(self,screen,frames,cmrx,cmry):
        img=pygame.transform.rotate(pygame.transform.scale(pygame.image.load("resources/molotov.png"),(16,28)),(10*frames)%360)
        screen.blit(img, (self.x-cmrx, self.y-cmry))
class Fire:
    def __init__(self,x,y):
        self.x=x
        self.y=y
        self.frstart=-1
    def render(self,screen,frames,cmrx,cmry):
        if self.frstart==-1:self.frstart=frames
        if frames-self.frstart>600:return 1
        if frames//7%3==0:
            img=pygame.transform.scale(pygame.image.load('resources/fire1.png'),(200*(WIDTH/1920),308*(HEIGHT/1080)))
        elif frames//7%3==1:
            img=pygame.transform.scale(pygame.image.load('resources/fire2.png'),(200*(WIDTH/1920),308*(HEIGHT/1080)))
        else:
            img=pygame.transform.scale(pygame.image.load('resources/fire3.png'),(150*(WIDTH/1920),308*(HEIGHT/1080)))
        rect=img.get_rect()
        rect.center=(self.x-cmrx, self.y-cmry)
        screen.blit(img, rect)
    def hurts(self,obj):
        img=pygame.transform.scale(pygame.image.load('resources/fire1.png'),(200*(WIDTH/1920),308*(HEIGHT/1080)))
        rect=img.get_rect()
        rect.center=(self.x, self.y)
        return rect.collidepoint(obj.x, obj.y)
def readdatabase():
    with open("databtest.json","r") as db:
        return json.load(db)

def resumegame():
    while 1:
        db=readdatabase()
        for i in range(1,10):#počet kapitol
            if db[str(i)]["finished"]=="0":
                LEVELFUNC="level"+str(i)+"()"
                break
        ret={}
        exec("LVLRETURN="+LEVELFUNC,globals(),ret)
        LVLRETURN=ret["LVLRETURN"]
        if LVLRETURN=="MENU":
            break
    mainmenu()
        
def navod():
    global screen, WIDTH, HEIGHT, MWIDTH, MHEIGHT,fullscreen,VOLUME
    nadpis=Text(WIDTH//2, HEIGHT//20, "NÁVOD", (255,255,255))
    t1=Text(WIDTH//2,2*HEIGHT//8,"Pohyb hráče je ovládán klávesami WSAD.",(189,255,255))
    t2=Text(WIDTH//2,3*HEIGHT//8,"Pohyb střelných zbraní je ovládán IK.",(189,255,255))
    t3=Text(WIDTH//2,4*HEIGHT//8,"Střílí se mezerníkem, přebíjí se O.",(189,255,255))
    t4=Text(WIDTH//2,5*HEIGHT//8,"Zbraně se mění U.",(189,255,255))
    t5=Text(WIDTH//2,6*HEIGHT//8,"Hráč může několikrát za hru použít molotov M nebo pervitin P.",(189,255,255))
    t6=Text(WIDTH//2,7*HEIGHT//8,"Do menu se hráč dostane ESC, zvuk hry se vypne Q.",(189,255,255))
    while 1:
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key==pygame.K_ESCAPE:
                    return
                elif event.key==pygame.K_q:
                    pygame.mixer.music.set_volume([0,100][VOLUME==0])
                    VOLUME=[0,100][VOLUME==0]
                    
        screen.fill((0,0,0))
        nadpis.render(screen, HEIGHT//10)
        t1.render(screen, HEIGHT//15)
        t2.render(screen, HEIGHT//15)
        t3.render(screen, HEIGHT//15)
        t4.render(screen, HEIGHT//15)
        t5.render(screen, HEIGHT//15)
        t6.render(screen, HEIGHT//15)
        pygame.display.update()
        clock.tick(60)
def about():
    global screen, WIDTH, HEIGHT, MWIDTH, MHEIGHT,fullscreen,VOLUME
    nadpis=Text(WIDTH//2, HEIGHT//20, "O HŘE",(255,255,255))
    ohre=Text(WIDTH//2,HEIGHT//3, "Celá anotace je na stránce", (189,255,255))
    ohre2=Text(WIDTH//2, 2*HEIGHT//3, "https://github.com/mikulaspater/Winter-war", (189,255,255))
    while 1:
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key==pygame.K_ESCAPE:
                    return
                elif event.key==pygame.K_q:
                    pygame.mixer.music.set_volume([0,100][VOLUME==0])
                    VOLUME=[0,100][VOLUME==0]
                    
        screen.fill((0,0,0))
        nadpis.render(screen, HEIGHT//10)
        ohre.render(screen, HEIGHT//15)
        ohre2.render(screen, HEIGHT//15)
        pygame.display.update()
        clock.tick(60)
def mainmenu():
    global screen, WIDTH, HEIGHT, MWIDTH, MHEIGHT,fullscreen,VOLUME
    nadpis=Text(WIDTH//2, HEIGHT//10, "ZIMNÍ VÁLKA", (189, 255,255))
    button1=Button(2.5*WIDTH/5,2*HEIGHT//7+HEIGHT//20,"Pokračovat ve hře", True, resumegame)
    button2=Button(2.5*WIDTH/5,3*HEIGHT//7+HEIGHT//20,"Levely",0,levelmenu)
    button3=Button(2.5*WIDTH/5,4*HEIGHT//7+HEIGHT//20,"Návod",0,navod)
    button4=Button(2.5*WIDTH/5,5*HEIGHT//7+HEIGHT//20,"O hře",0,about)
    button5=Button(2.5*WIDTH/5,6*HEIGHT//7+HEIGHT//20,"Exit",0,sys.exit)
    pozadi=pygame.transform.scale(pygame.image.load("resources/menupozadi.png").convert(),(WIDTH,HEIGHT))
    marked=1
    VLOCKY=[]
    for i in range(WIDTH//4):
        VLOCKY.append(vlocka(WIDTH, HEIGHT, 1))
    pygame.mixer.music.load("resources/menumusic.mp3")
    pygame.mixer.music.play(-1,0.0)
    while 1:
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key==pygame.K_DOWN:
                    exec("button"+str(marked)+".marked=0")
                    marked+=1
                    marked=(marked-1)%5+1
                    exec("button"+str(marked)+".marked=1")
                elif event.key==pygame.K_UP:
                    exec("button"+str(marked)+".marked=0")
                    marked-=1
                    if marked==0:
                        marked=5
                    exec("button"+str(marked)+".marked=1")
                elif event.key==13:
                    if marked==1:
                        pygame.mixer.music.stop()
                    exec("button"+str(marked)+".press()")
                elif event.key==pygame.K_q:
                    pygame.mixer.music.set_volume([0,100][VOLUME==0])
                    VOLUME=[0,100][VOLUME==0]
                else:
                    ...#print(event.key)
            elif event.type==pygame.MOUSEBUTTONDOWN and 0:
                print(pygame.mouse.get_pos())
        screen.fill((0,0,0))
        screen.blit(pozadi,(0,0))
        button1.render(screen,HEIGHT//20)
        button2.render(screen,HEIGHT//20)
        button3.render(screen,HEIGHT//20)
        button4.render(screen,HEIGHT//20)
        button5.render(screen,HEIGHT//20)
        nadpis.render(screen, HEIGHT//7)
        iter=0
        if random.randrange(5)==0:
            VLOCKY.append(vlocka(WIDTH,HEIGHT))
        while 1:
            try:
                VLOCKY[iter].y+=HEIGHT/1080
                VLOCKY[iter].render(screen)
                if VLOCKY[iter].y<HEIGHT:
                    iter+=1
                else:
                    del(VLOCKY[iter])
            except IndexError:
                break
        pygame.display.update()
        clock.tick(60)

def levelmenu():
    global screen, WIDTH, HEIGHT, MWIDTH, MHEIGHT,fullscreen,VOLUME
    nadpis=Text(WIDTH//2, HEIGHT//14, "Levely", (189, 255,255))
    button1=Button(2.5*WIDTH/5,2*HEIGHT//11,"O prvním útoku", True, level1)#lvl 2
    button2=Button(2.5*WIDTH/5,3*HEIGHT//11,"První útok", 0, level2)#lvl 2
    button3=Button(2.5*WIDTH/5,4*HEIGHT//11,"O molotovu", 0, level3)#lvl 2
    button4=Button(2.5*WIDTH/5,5*HEIGHT//11,"Koktejl",0,level4)#lvl 4
    button5=Button(2.5*WIDTH/5,6*HEIGHT//11,"O motti", 0, level5)#lvl 2
    button6=Button(2.5*WIDTH/5,7*HEIGHT//11,"Motti",0,level6)#lvl 6
    button7=Button(2.5*WIDTH/5,8*HEIGHT//11,"Sekání dřeva",0,level7)#lvl7
    button8=Button(2.5*WIDTH/5,9*HEIGHT//11,"O Finských podmínkách", 0, level8)#lvl 2
    button9=Button(2.5*WIDTH/5,10*HEIGHT//11,"Prosekej se k vítězství",0,level9)#lvl 9
    marked=1
    warntext=TemporaryText(WIDTH//2,10*HEIGHT//11,"Tento level není odemčen.",(255,255,255), 0, 0)
    VLOCKY=[]
    lst=range(10)
    for i in range(WIDTH//4):
        VLOCKY.append(vlocka(WIDTH, HEIGHT, 1))
    frames=0
    while 1:
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key==pygame.K_DOWN:
                    exec("button"+str(marked)+".marked=0")
                    marked+=1
                    marked=(marked-1)%9+1
                    exec("button"+str(marked)+".marked=1")
                elif event.key==pygame.K_ESCAPE:return
                elif event.key==pygame.K_UP:
                    exec("button"+str(marked)+".marked=0")
                    marked-=1
                    if marked==0:
                        marked=9
                    exec("button"+str(marked)+".marked=1")
                elif event.key==13:
                    with open("databtest.json") as db:
                        mydb=json.load(db)
                    pygame.mixer.music.stop()
                    if marked==1:
                        exec("button"+str(marked)+".press()")
                    elif mydb[str(lst[marked-1])]["finished"]=="3":
                        exec("button"+str(marked)+".press()")
                    else:
                        warntext=TemporaryText(WIDTH//2,HEIGHT//2,"Tento level není odemčen.",(255,0,0), 0, 180)
                elif event.key==pygame.K_q:
                    pygame.mixer.music.set_volume([0,100][VOLUME==0])
                    VOLUME=[0,100][VOLUME==0]
                else:
                    ...#print(event.key)
            elif event.type==pygame.MOUSEBUTTONDOWN and 0:
                print(pygame.mouse.get_pos())
        screen.fill((0,0,0))
        button1.render(screen,HEIGHT//20)
        button2.render(screen,HEIGHT//20)
        button3.render(screen,HEIGHT//20)
        button4.render(screen,HEIGHT//20)
        button5.render(screen,HEIGHT//20)
        button6.render(screen,HEIGHT//20)
        button7.render(screen,HEIGHT//20)
        button8.render(screen,HEIGHT//20)
        button9.render(screen,HEIGHT//20)
        nadpis.render(screen, HEIGHT//7)
        warntext.render(screen,HEIGHT//10)
        iter=0
        if random.randrange(5)==0:
            VLOCKY.append(vlocka(WIDTH,HEIGHT))
        while 1:
            try:
                VLOCKY[iter].y+=HEIGHT/1080
                VLOCKY[iter].render(screen)
                if VLOCKY[iter].y<HEIGHT:
                    iter+=1
                else:
                    del(VLOCKY[iter])
            except IndexError:
                break
        pygame.display.update()
        clock.tick(60)
        frames+=1
def level1():
    global screen, WIDTH, HEIGHT, MWIDTH, MHEIGHT,fullscreen,VOLUME
    text1=TemporaryText(WIDTH//2,HEIGHT//2,"Okolo roku 1939 si Sověti kladli nárok na území kolem Finské hranice, hlavně blízko Leningradu.",(255,255,255), 30, 330)
    text2=TemporaryText(WIDTH//2,HEIGHT//2,"Tvrdili, že území je nutné pro jejich bezpečnost.",(255,255,255), 330, 630)
    text3=TemporaryText(WIDTH//2,HEIGHT//2,"Celkem padlo několik Sovětských návrhů a jeden Finský protinávrh na novou hranici, ani na jednom se však obě strany neshodly.",(255,255,255), 630, 930)
    text4=TemporaryText(WIDTH//2,HEIGHT//2,"26.11.1939 Sovětské dělostřelectvo pod Finskou vlajkou napadlo sovětskou přihraniční vesnici Manila.",(255,255,255), 930, 1230)
    text5=TemporaryText(WIDTH//2,HEIGHT//2,"Tato akce, známá jako Manilský incident, se stala záminkou k útoku.",(255,255,255), 1230, 1530)
    text6=TemporaryText(WIDTH//2,HEIGHT//2,"30. listopadu 1939 začali Sověti vojenskou invazi do Finska.",(255,255,255), 1530, 1830)
    frames=0
    VLOCKY=[]
    for i in range(WIDTH//4):
        VLOCKY.append(vlocka(WIDTH, HEIGHT, 1))
    pygame.mixer.music.load("resources/music1.mp3")
    pygame.mixer.music.play(-1,0.0)
    while 1:
        if frames==1830:
            with open("databtest.json") as db:
                mydb=json.load(db)
            mydb["1"]["finished"]="3"
            with open("databtest.json","w") as db:
                json.dump(mydb,db)
            return
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key==pygame.K_ESCAPE:
                    return "MENU"
                elif event.key==pygame.K_q:
                    pygame.mixer.music.set_volume([0,100][VOLUME==0])
                    VOLUME=[0,100][VOLUME==0]
        screen.fill((0,0,0))
        text1.render(screen, HEIGHT//20)
        text2.render(screen, HEIGHT//20)
        text3.render(screen, HEIGHT//27)
        text4.render(screen, HEIGHT//25)
        text5.render(screen, HEIGHT//20)
        text6.render(screen, HEIGHT//20)
        iter=0
        if random.randrange(5)==0:
            VLOCKY.append(vlocka(WIDTH,HEIGHT))
        while 1:
            try:
                VLOCKY[iter].y+=HEIGHT/1080
                VLOCKY[iter].render(screen)
                if VLOCKY[iter].y<HEIGHT:
                    iter+=1
                else:
                    del(VLOCKY[iter])
            except IndexError:
                break
        pygame.display.update()
        frames+=1
        clock.tick(60)
def level2():
    global screen, WIDTH, HEIGHT, MWIDTH, MHEIGHT,fullscreen,VOLUME
    cmrx,cmry=0,0#topleftcorner
    TARGETTIME=180*60
    BULLETS=[]
    inversespawnrate=1200
    SUPERTARGET=Supertarget(WIDTH//25,HEIGHT//2,pygame.image.load("resources/chajda.png"),hp=999)
    kp_increments=[-int(23*(HEIGHT/1080)),int(9*(HEIGHT/1080)), int(22*(HEIGHT/1080)),int(9*(HEIGHT/1080))]
    l_increments=[-int(21*(HEIGHT/1080)),int(9*(HEIGHT/1080)), int(22*(HEIGHT/1080)),int(9*(HEIGHT/1080))]
    kp31=Gun(4, 3, "suomi_kp31", int(16*(HEIGHT/1080)),90,WIDTH,HEIGHT, int(15*WIDTH/1920), int(67*HEIGHT/1080), kp_increments,71,"resources/kp.mp3","resources/ppl40rld.mp3",0)
    l35=Gun(30, 2, "l35", int(32*(HEIGHT/1080)),90,WIDTH,HEIGHT, int(21*WIDTH/1920), int(57*HEIGHT/1080),l_increments,8,"resources/l35.mp3","resources/tt33_rld.mp3",0)
    m28=Gun(200, 0, "m28", int(70*(HEIGHT/1080)),90,WIDTH,HEIGHT, int(12*WIDTH/1920), int(75*HEIGHT/1080),l_increments,5,"resources/m28.mp3","resources/m28_rld.mp3",300)
    m28e=Gun(400, 5, "m28", int(49*(HEIGHT/1080)),270,WIDTH,HEIGHT, int(12*WIDTH/1920), int(75*HEIGHT/1080),l_increments,5,"resources/m28.mp3","resources/m28_rld.mp3",300)
    ppd40e=Gun(7, 3, "suomi_kp31", int(16*(HEIGHT/1080)),270,WIDTH,HEIGHT, int(15*WIDTH/1920), int(67*HEIGHT/1080), kp_increments,71,"resources/kp.mp3","resources/ppl40rld.mp3",0)
    tt33e=Gun(60, 5, "tt33", int(19*(HEIGHT/1080)),90,WIDTH,HEIGHT, int(18*WIDTH/1920), int(36*HEIGHT/1080),l_increments,8,"resources/l35.mp3","resources/tt33_rld.mp3",0)
    #machine gun kp31
    #firerate cca 750-900 rounds/min--> cca 12.5-15 rps  --> delay 4 framy
    #firespeed cca 396 m/s --> panacek vysokej 180 cm je 128(HEIGHT/1080) takže cca pro x =HEIGHT/1080 je 1.8m 128x tudíž 1m=71*x px tudíž 396m je 28116*x px děleno 60 fps je 468.8x px/f což je mga rychlý
    #proto firespeed bude 64x
    pygame.mixer.music.load("resources/music1.mp3")
    pygame.mixer.music.play(-1,0.0)
    PLAYER=Player(WIDTH//2,HEIGHT//2, WIDTH,HEIGHT,[l35])
    started=0
    nadpis=Text(WIDTH//2, HEIGHT//10, "Level 1", (189, 255,255))
    nadpis2=Text(WIDTH//2, HEIGHT//5, "PRVNÍ ÚTOK", (189, 255,255))
    info=Text(WIDTH//2, HEIGHT//2, "Pohyb WSAD, miř IK, přebíjej O, střílej mezerníkem.", (189, 255,255))
    info2=Text(WIDTH//2, HEIGHT//3, "Ubraň základnu!", (189, 255,255))
    info3=Text(WIDTH//2, 2*HEIGHT//3, "K dispozici máš pistoli Finské výroby Lahti L35.", (189, 255,255))
    cont=Text(WIDTH//2, 8*HEIGHT//10, "Mezerník pro spuštění", (189, 255,255))
    contsize=10
    contphase="RETROGRADE"
    gameover=0
    frames=0
    fires=[]
    VLOCKY=[]
    npcs=[]
    tiles=[]
    """tilesize=64*(WIDTH/1920)
    for i in range(-math.ceil(WIDTH/tilesize),2*math.ceil(WIDTH/tilesize)):
        for j in range(-math.ceil(HEIGHT/tilesize),2*math.ceil(HEIGHT/tilesize)):
            if random.randrange(10)==1:
                tiles.append(Tile(i*tilesize, j*tilesize, pygame.transform.scale(pygame.image.load("resources/tile"+str(random.randrange(10))+".png"),(tilesize, tilesize))))"""
    for i in range(WIDTH//4):
        VLOCKY.append(vlocka(WIDTH, HEIGHT, 1))
    molotovs=[]
    infotext=TemporaryText(WIDTH//2,7*HEIGHT//8,"Odemkl jsi samopal Finské výroby KP31. Měníš zbraně U.",(0,0,0), 60*100, 60*100+300)
    while 1:
        if frames>=TARGETTIME:gameover=1
        if frames==60*100:
            PLAYER.posguns=[l35,kp31];inversespawnrate=300
        if gameover:
            pygame.mixer.stop()
            with open("databtest.json") as db:
                mydb=json.load(db)
            mydb["2"]["finished"]="3"
            with open("databtest.json","w") as db:
                json.dump(mydb,db)
            return
        if SUPERTARGET:
            if SUPERTARGET.hp<=0:pygame.mixer.stop();return
        keys=pygame.key.get_pressed()
        dir=[0,0]
        if keys[pygame.K_w]:dir[1]=-1
        elif keys[pygame.K_s]:dir[1]=1
        if keys[pygame.K_a]:dir[0]=-1
        elif keys[pygame.K_d]:dir[0]=1
        x=keys[pygame.K_k]
        #y=keys[pygame.K_l]
        z=keys[pygame.K_i]
        #a=keys[pygame.K_j]
        y=0
        a=0
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key==pygame.K_ESCAPE:
                    return "MENU"
                elif event.key==pygame.K_q:
                    pygame.mixer.music.set_volume([0,100][VOLUME==0])
                    VOLUME=[0,100][VOLUME==0]
                elif event.key==pygame.K_SPACE:
                    if not started:started=1
                elif event.key==pygame.K_u:
                    PLAYER.chnggun(1)
                elif event.key==pygame.K_z:
                    PLAYER.chnggun(-1)
                elif event.key==pygame.K_o:
                    PLAYER.reload()
                elif event.key==pygame.K_m and started and PLAYER.hp>0 and PLAYER.molotovcount>0:
                    pf=PLAYER.gun.firespeed
                    PLAYER.gun.firespeed=7*(HEIGHT/1080)
                    x=PLAYER.gun.fire(frames, PLAYER.x, PLAYER.y, screen, PLAYER.facing, molotov=1)
                    molotovs.append(Molotov(x[0],x[1],x[2],x[3]))
                    PLAYER.gun.firespeed=pf
                    PLAYER.molotovcount-=1
        if keys[pygame.K_SPACE] and frames>60 and PLAYER.hp>0:
            q=PLAYER.gun.fire(frames, PLAYER.x, PLAYER.y, screen, PLAYER.facing)
            if q!=0:
                BULLETS.append(q)
                for npc in npcs:
                    if math.sqrt((npc.x-PLAYER.x)**2+(npc.y-PLAYER.y)**2)<WIDTH:
                        npc.seesplayer=1
        screen.fill((0,0,0))
        if started:
            screen.fill((255,255,255))
            """for tile in tiles:
                tile.render(screen, cmrx, cmry)"""
        if started:
            if frames%inversespawnrate==0:
                if random.randrange(10)==-1:npcs.append(NPC(2*WIDTH, random.randrange(HEIGHT),WIDTH, HEIGHT, [copygun(ppd40e)]))
                else:npcs.append(NPC(2*WIDTH, random.randrange(HEIGHT),WIDTH, HEIGHT, [copygun(tt33e)]))
        cmrx,cmry=PLAYER.update(dir,[x,y,z,a],cmrx,cmry)
        for npc in npcs:
            if SUPERTARGET:
                bul=npc.update(PLAYER,WIDTH,HEIGHT,frames,supertarget=SUPERTARGET)
            else:
                bul=npc.update(PLAYER,WIDTH,HEIGHT,frames)
            if bul:BULLETS.append(bul)
        if not started:
            nadpis.render(screen, HEIGHT//20)
            nadpis2.render(screen, HEIGHT//10)
            cont.render(screen, HEIGHT//20+int(0.5*contsize))
            info.render(screen, HEIGHT//20)
            info2.render(screen, HEIGHT//20)
            info3.render(screen, HEIGHT//20)
            if contphase=="RETROGRADE":
                contsize-=0.2
                if contsize<=0:contphase="PROGRADE"
            else:
                contsize+=0.2
                if contsize>=10:contphase="RETROGRADE"
        for bullet in BULLETS:
            if bullet.vx**2+bullet.vy**2<(HEIGHT/1080)**2:bltsrmv.append(bullet);continue
            bullet.update()
            bullet.render(screen,cmrx,cmry)
            if bullet.pe==1:
                if PLAYER.got_hit(bullet.x, bullet.y, frames) and PLAYER.hp>-100:
                    PLAYER.hp-=int(math.sqrt(bullet.vx**2+bullet.vy**2)/(HEIGHT/1080))
                    bltsrmv.append(bullet)
                if SUPERTARGET.got_hit(bullet):
                    SUPERTARGET.hp-=int(math.sqrt(bullet.vx**2+bullet.vy**2)/(HEIGHT/1080))
                    bltsrmv.append(bullet)
            else:
                if SUPERTARGET.got_hit(bullet):
                    SUPERTARGET.hp-=int(math.sqrt(bullet.vx**2+bullet.vy**2)/(HEIGHT/1080))
                    bltsrmv.append(bullet)
                for npc in npcs:
                    if npc.got_hit(bullet.x,bullet.y,frames,cmrx,cmry):
                        npc.hp-=int(math.sqrt(bullet.vx**2+bullet.vy**2)/(HEIGHT/1080))
                        bltsrmv.append(bullet)
            #if (bullet.x-PLAYER.x)**2+(bullet.y-PLAYER.y)**2>5*WIDTH:bltsrmv.append(bullet)
        blts2=[]
        for bullet in BULLETS:
            if bullet not in bltsrmv:blts2.append(bullet)
        BULLETS=blts2
        if started:
            for npc in npcs:
                npc.render(screen, WIDTH, HEIGHT, frames,cmrx,cmry)
                if npc.hp>0:
                    npc.gun.render(screen,npc.x, npc.y, npc.facing,cmrx,cmry)
            if PLAYER.hp>0:
                hptext=Text(WIDTH//28,14*HEIGHT//15,str(PLAYER.hp),(255,0,0))
            else:
                hptext=Text(WIDTH//28,14*HEIGHT//15,"0",(255,0,0))
            
            if SUPERTARGET:
                SUPERTARGET.render(screen,cmrx,cmry)
                if SUPERTARGET.hp<0:SUPERTARGET.hp=0
                sptext=Text(WIDTH//28,12*HEIGHT//15,str(SUPERTARGET.hp),(252,219,0))
                
            PLAYER.render(screen, WIDTH, HEIGHT, frames, cmrx,cmry)
            if PLAYER.hp>0:
                PLAYER.gun.render(screen,PLAYER.x,PLAYER.y,PLAYER.facing,cmrx,cmry)
            bltsrmv=[]
            mltsrmv=[]
            mlts2=[]
            frmv=[]
            frs2=[]
            for molotov in molotovs:
                if molotov.update():mltsrmv.append(molotov);fires.append(Fire(molotov.x,molotov.y))
                molotov.render(screen,frames,cmrx,cmry)
            for mltv in molotovs:
                if mltv not in mltsrmv:mlts2.append(mltv)
            molotovs=list(mlts2)
            for fire in fires:
                if fire.render(screen,frames,cmrx,cmry):frmv.append(fire)
                for npc in npcs:
                    if fire.hurts(npc):npc.hp-=1
                if fire.hurts(PLAYER):PLAYER.hp-=1
                if SUPERTARGET:
                    if fire.hurts(SUPERTARGET):SUPERTARGET.hp-=1
            for fr in fires:
                if fr not in frmv:frs2.append(fr)
            fires=list(frs2)
            bltext=Text(31*WIDTH//32,14*HEIGHT//15,str(PLAYER.gun.bullets),(0,0,0))
            cmrytext=Text(WIDTH//2,14*HEIGHT//15,str(int(PLAYER.x))+", "+str(int(PLAYER.y)),(255,0,0))
            if TARGETTIME:
                time=TARGETTIME-frames
                mins=time//60//60
                secs=time//60%60
                secstr=str(secs)
                if len(secstr)<2:secstr="0"+secstr
                tartext=Text(30*WIDTH//32,HEIGHT//23,str(mins)+":"+secstr,(255,216,60))
                tartext.render(screen,HEIGHT//10)
            cmrytext.render(screen, HEIGHT//20)
            bltext.render(screen,HEIGHT//10)
            hptext.render(screen, HEIGHT//10)
            sptext.render(screen,HEIGHT//10)
            infotext.render(screen, HEIGHT//20)
        iter=0
        if random.randrange(5)==0:
            VLOCKY.append(vlocka(WIDTH,HEIGHT))
        while 1:
            try:
                VLOCKY[iter].y+=HEIGHT/1080
                VLOCKY[iter].render(screen)
                if VLOCKY[iter].y<HEIGHT:
                    iter+=1
                else:
                    del(VLOCKY[iter])
            except IndexError:
                break
        pygame.display.update()
        if started:frames+=1
        clock.tick(60)
def level3():
    global screen, WIDTH, HEIGHT, MWIDTH, MHEIGHT,fullscreen,VOLUME
    text1=TemporaryText(WIDTH//2,HEIGHT//2,"Sovětský ministr zahraničí a symbol Sovětské agrese Vjačeslav Molotov tvrdil,",(255,255,255), 30, 270)
    text4=TemporaryText(WIDTH//2,HEIGHT//2,"že bombardéry nad Finskem neshazují bomby, ale potravinové balíčky.",(255,255,255), 270,510)
    text2=TemporaryText(WIDTH//2,HEIGHT//2,"Finové jim začali sarkasticky říkat \"Molotovovy chlebíčky\".",(255,255,255), 510,750)
    text3=TemporaryText(WIDTH//2,HEIGHT//2,"Jako odpověď pojmenovali improvizovaný zápalný granát \"Molotovův koktejl\".",(255,255,255), 750,990)
    frames=0
    VLOCKY=[]
    for i in range(WIDTH//4):
        VLOCKY.append(vlocka(WIDTH, HEIGHT, 1))
    while 1:
        if frames==990:
            with open("databtest.json") as db:
                mydb=json.load(db)
            mydb["3"]["finished"]="3"
            with open("databtest.json","w") as db:
                json.dump(mydb,db)
            return
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key==pygame.K_ESCAPE:
                    return "MENU"
                elif event.key==pygame.K_q:
                    pygame.mixer.music.set_volume([0,100][VOLUME==0])
                    VOLUME=[0,100][VOLUME==0]
        screen.fill((0,0,0))
        text1.render(screen, HEIGHT//20)
        text2.render(screen, HEIGHT//20)
        text3.render(screen, HEIGHT//20)
        text4.render(screen, HEIGHT//20)
        iter=0
        if random.randrange(5)==0:
            VLOCKY.append(vlocka(WIDTH,HEIGHT))
        while 1:
            try:
                VLOCKY[iter].y+=HEIGHT/1080
                VLOCKY[iter].render(screen)
                if VLOCKY[iter].y<HEIGHT:
                    iter+=1
                else:
                    del(VLOCKY[iter])
            except IndexError:
                break
        pygame.display.update()
        frames+=1
        clock.tick(60)
def level4():
    global screen, WIDTH, HEIGHT, MWIDTH, MHEIGHT,fullscreen,VOLUME
    cmrx,cmry=0,0#topleftcorner
    TARGETTIME=180*60
    BULLETS=[]
    inversespawnrate=600
    SUPERTARGET=Supertarget(WIDTH//25,HEIGHT//2,pygame.image.load("resources/chajda.png"),hp=999)
    kp_increments=[-int(23*(HEIGHT/1080)),int(9*(HEIGHT/1080)), int(22*(HEIGHT/1080)),int(9*(HEIGHT/1080))]
    l_increments=[-int(21*(HEIGHT/1080)),int(9*(HEIGHT/1080)), int(22*(HEIGHT/1080)),int(9*(HEIGHT/1080))]
    kp31=Gun(4, 3, "suomi_kp31", int(16*(HEIGHT/1080)),90,WIDTH,HEIGHT, int(15*WIDTH/1920), int(67*HEIGHT/1080), kp_increments,71,"resources/kp.mp3","resources/ppl40rld.mp3",0)
    l35=Gun(30, 2, "l35", int(32*(HEIGHT/1080)),90,WIDTH,HEIGHT, int(21*WIDTH/1920), int(57*HEIGHT/1080),l_increments,8,"resources/l35.mp3","resources/tt33_rld.mp3",0)
    m28=Gun(200, 0, "m28", int(70*(HEIGHT/1080)),90,WIDTH,HEIGHT, int(12*WIDTH/1920), int(75*HEIGHT/1080),l_increments,5,"resources/m28.mp3","resources/m28_rld.mp3",300)
    m28e=Gun(400, 5, "m28", int(49*(HEIGHT/1080)),270,WIDTH,HEIGHT, int(12*WIDTH/1920), int(75*HEIGHT/1080),l_increments,5,"resources/m28.mp3","resources/m28_rld.mp3",300)
    ppd40e=Gun(7, 3, "suomi_kp31", int(16*(HEIGHT/1080)),270,WIDTH,HEIGHT, int(15*WIDTH/1920), int(67*HEIGHT/1080), kp_increments,71,"resources/kp.mp3","resources/ppl40rld.mp3",0)
    tt33e=Gun(60, 5, "tt33", int(19*(HEIGHT/1080)),90,WIDTH,HEIGHT, int(18*WIDTH/1920), int(36*HEIGHT/1080),l_increments,8,"resources/l35.mp3","resources/tt33_rld.mp3",0)
    #machine gun kp31
    #firerate cca 750-900 rounds/min--> cca 12.5-15 rps  --> delay 4 framy
    #firespeed cca 396 m/s --> panacek vysokej 180 cm je 128(HEIGHT/1080) takže cca pro x =HEIGHT/1080 je 1.8m 128x tudíž 1m=71*x px tudíž 396m je 28116*x px děleno 60 fps je 468.8x px/f což je mga rychlý
    #proto firespeed bude 64x
    pygame.mixer.music.load("resources/music1.mp3")
    pygame.mixer.music.play(-1,0.0)
    PLAYER=Player(WIDTH//2,HEIGHT//2, WIDTH,HEIGHT,[l35,kp31],molotovcount=3)
    started=0
    nadpis=Text(WIDTH//2, HEIGHT//10, "Level 2", (189, 255,255))
    nadpis2=Text(WIDTH//2, HEIGHT//5, "KOKTEJL", (189, 255,255))
    info=Text(WIDTH//2, HEIGHT//2, "Stisknutím M použiješ molotov. Máš pouze tři na level.", (189, 255,255))
    cont=Text(WIDTH//2, 8*HEIGHT//10, "Mezerník pro spuštění", (189, 255,255))
    contsize=10
    contphase="RETROGRADE"
    gameover=0
    frames=0
    fires=[]
    VLOCKY=[]
    npcs=[]
    tiles=[]
    """tilesize=64*(WIDTH/1920)
    for i in range(-math.ceil(WIDTH/tilesize),2*math.ceil(WIDTH/tilesize)):
        for j in range(-math.ceil(HEIGHT/tilesize),2*math.ceil(HEIGHT/tilesize)):
            if random.randrange(10)==1:
                tiles.append(Tile(i*tilesize, j*tilesize, pygame.transform.scale(pygame.image.load("resources/tile"+str(random.randrange(10))+".png"),(tilesize, tilesize))))"""
    for i in range(WIDTH//4):
        VLOCKY.append(vlocka(WIDTH, HEIGHT, 1))
    molotovs=[]
    while 1:
        if frames>=TARGETTIME:gameover=1
        if gameover:
            pygame.mixer.stop()
            with open("databtest.json") as db:
                mydb=json.load(db)
            mydb["4"]["finished"]="3"
            with open("databtest.json","w") as db:
                json.dump(mydb,db)
            return
        if SUPERTARGET:
            if SUPERTARGET.hp<=0:pygame.mixer.stop();return
        keys=pygame.key.get_pressed()
        dir=[0,0]
        if keys[pygame.K_w]:dir[1]=-1
        elif keys[pygame.K_s]:dir[1]=1
        if keys[pygame.K_a]:dir[0]=-1
        elif keys[pygame.K_d]:dir[0]=1
        x=keys[pygame.K_k]
        #y=keys[pygame.K_l]
        z=keys[pygame.K_i]
        #a=keys[pygame.K_j]
        y=0
        a=0
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key==pygame.K_ESCAPE:
                    return "MENU"
                elif event.key==pygame.K_q:
                    pygame.mixer.music.set_volume([0,100][VOLUME==0])
                    VOLUME=[0,100][VOLUME==0]
                elif event.key==pygame.K_SPACE:
                    if not started:started=1
                elif event.key==pygame.K_u:
                    PLAYER.chnggun(1)
                elif event.key==pygame.K_z:
                    PLAYER.chnggun(-1)
                elif event.key==pygame.K_o:
                    PLAYER.reload()
                elif event.key==pygame.K_m and started and PLAYER.hp>0 and PLAYER.molotovcount>0:
                    pf=PLAYER.gun.firespeed
                    PLAYER.gun.firespeed=7*(HEIGHT/1080)
                    x=PLAYER.gun.fire(frames, PLAYER.x, PLAYER.y, screen, PLAYER.facing, molotov=1)
                    molotovs.append(Molotov(x[0],x[1],x[2],x[3]))
                    PLAYER.gun.firespeed=pf
                    PLAYER.molotovcount-=1
        if keys[pygame.K_SPACE] and frames>60 and PLAYER.hp>0:
            q=PLAYER.gun.fire(frames, PLAYER.x, PLAYER.y, screen, PLAYER.facing)
            if q!=0:
                BULLETS.append(q)
                for npc in npcs:
                    if math.sqrt((npc.x-PLAYER.x)**2+(npc.y-PLAYER.y)**2)<WIDTH:
                        npc.seesplayer=1
        screen.fill((0,0,0))
        if started:
            screen.fill((255,255,255))
            for tile in tiles:
                tile.render(screen, cmrx, cmry)
        if started:
            if frames%inversespawnrate==0:
                if random.randrange(10)==-1:npcs.append(NPC(2*WIDTH, random.randrange(HEIGHT),WIDTH, HEIGHT, [copygun(ppd40e)]))
                else:npcs.append(NPC(2*WIDTH, random.randrange(HEIGHT),WIDTH, HEIGHT, [copygun(tt33e)]))
        cmrx,cmry=PLAYER.update(dir,[x,y,z,a],cmrx,cmry)
        for npc in npcs:
            if SUPERTARGET:
                bul=npc.update(PLAYER,WIDTH,HEIGHT,frames,supertarget=SUPERTARGET)
            else:
                bul=npc.update(PLAYER,WIDTH,HEIGHT,frames)
            if bul:BULLETS.append(bul)
        if not started:
            nadpis.render(screen, HEIGHT//20)
            nadpis2.render(screen, HEIGHT//10)
            info.render(screen, HEIGHT//20)
            cont.render(screen, HEIGHT//20+int(0.5*contsize))
            if contphase=="RETROGRADE":
                contsize-=0.2
                if contsize<=0:contphase="PROGRADE"
            else:
                contsize+=0.2
                if contsize>=10:contphase="RETROGRADE"
        for bullet in BULLETS:
            bullet.update()
            bullet.render(screen,cmrx,cmry)
            if bullet.pe==1:
                if PLAYER.got_hit(bullet.x, bullet.y, frames) and PLAYER.hp>-100:
                    PLAYER.hp-=int(math.sqrt(bullet.vx**2+bullet.vy**2)/(HEIGHT/1080))
                    bltsrmv.append(bullet)
                if SUPERTARGET.got_hit(bullet):
                    SUPERTARGET.hp-=int(math.sqrt(bullet.vx**2+bullet.vy**2)/(HEIGHT/1080))
                    bltsrmv.append(bullet)
            else:
                if SUPERTARGET.got_hit(bullet):
                    SUPERTARGET.hp-=int(math.sqrt(bullet.vx**2+bullet.vy**2)/(HEIGHT/1080))
                    bltsrmv.append(bullet)
                for npc in npcs:
                    if npc.got_hit(bullet.x,bullet.y,frames,cmrx,cmry):
                        npc.hp-=int(math.sqrt(bullet.vx**2+bullet.vy**2)/(HEIGHT/1080))
                        bltsrmv.append(bullet)
            #if (bullet.x-PLAYER.x)**2+(bullet.y-PLAYER.y)**2>5*WIDTH:bltsrmv.append(bullet)
        blts2=[]
        for bullet in BULLETS:
            if bullet not in bltsrmv:blts2.append(bullet)
        BULLETS=blts2
        if started:
            for npc in npcs:
                npc.render(screen, WIDTH, HEIGHT, frames,cmrx,cmry)
                if npc.hp>0:
                    npc.gun.render(screen,npc.x, npc.y, npc.facing,cmrx,cmry)
            if PLAYER.hp>0:
                hptext=Text(WIDTH//28,14*HEIGHT//15,str(PLAYER.hp),(255,0,0))
            else:
                hptext=Text(WIDTH//28,14*HEIGHT//15,"0",(255,0,0))
            moltext=Text(31*WIDTH//32,12*HEIGHT//15,str(PLAYER.molotovcount),(252,0,0))
            if SUPERTARGET:
                SUPERTARGET.render(screen,cmrx,cmry)
                if SUPERTARGET.hp<0:SUPERTARGET.hp=0
                sptext=Text(WIDTH//28,12*HEIGHT//15,str(SUPERTARGET.hp),(252,219,0))
                
            PLAYER.render(screen, WIDTH, HEIGHT, frames, cmrx,cmry)
            if PLAYER.hp>0:
                PLAYER.gun.render(screen,PLAYER.x,PLAYER.y,PLAYER.facing,cmrx,cmry)
            bltsrmv=[]
            mltsrmv=[]
            mlts2=[]
            frmv=[]
            frs2=[]
            for molotov in molotovs:
                if molotov.update():mltsrmv.append(molotov);fires.append(Fire(molotov.x,molotov.y))
                molotov.render(screen,frames,cmrx,cmry)
            for mltv in molotovs:
                if mltv not in mltsrmv:mlts2.append(mltv)
            molotovs=list(mlts2)
            for fire in fires:
                if fire.render(screen,frames,cmrx,cmry):frmv.append(fire)
                for npc in npcs:
                    if fire.hurts(npc):npc.hp-=1
                if fire.hurts(PLAYER):PLAYER.hp-=1
                if SUPERTARGET:
                    if fire.hurts(SUPERTARGET):SUPERTARGET.hp-=1
            for fr in fires:
                if fr not in frmv:frs2.append(fr)
            fires=list(frs2)
            bltext=Text(31*WIDTH//32,14*HEIGHT//15,str(PLAYER.gun.bullets),(0,0,0))
            cmrytext=Text(WIDTH//2,14*HEIGHT//15,str(int(PLAYER.x))+", "+str(int(PLAYER.y)),(255,0,0))
            if TARGETTIME:
                time=TARGETTIME-frames
                mins=time//60//60
                secs=time//60%60
                secstr=str(secs)
                if len(secstr)<2:secstr="0"+secstr
                tartext=Text(30*WIDTH//32,HEIGHT//23,str(mins)+":"+secstr,(255,216,60))
                tartext.render(screen,HEIGHT//10)
            cmrytext.render(screen, HEIGHT//20)
            bltext.render(screen,HEIGHT//10)
            hptext.render(screen, HEIGHT//10)
            sptext.render(screen,HEIGHT//10)
            moltext.render(screen, HEIGHT//10)
        iter=0
        if random.randrange(5)==0:
            VLOCKY.append(vlocka(WIDTH,HEIGHT))
        while 1:
            try:
                VLOCKY[iter].y+=HEIGHT/1080
                VLOCKY[iter].render(screen)
                if VLOCKY[iter].y<HEIGHT:
                    iter+=1
                else:
                    del(VLOCKY[iter])
            except IndexError:
                break
        pygame.display.update()
        if started:frames+=1
        clock.tick(60)
def level5():
    global screen, WIDTH, HEIGHT, MWIDTH, MHEIGHT,fullscreen,VOLUME
    text1=TemporaryText(WIDTH//2,HEIGHT//2,"Finové používali vojenskou taktiku \"Motti\".",(255,255,255), 30, 240)
    text2=TemporaryText(WIDTH//2,HEIGHT//2,"Motti ve finštině znamená hromadu dřeva připravenou na pokácení.",(255,255,255), 240, 450)
    text3=TemporaryText(WIDTH//2,HEIGHT//2,"Finové nechali projít Sověty za svoje linie, mezitím co byli schovaní v lesích.",(255,255,255), 450, 690)
    text4=TemporaryText(WIDTH//2,HEIGHT//2,"Poté odřízli skupinu od zbytku armády.",(255,255,255), 690, 930)
    text5=TemporaryText(WIDTH//2,HEIGHT//2,"Nakonec skupinu ze všech stran \"pokáceli\".",(255,255,255), 930, 1170)
    text6=TemporaryText(WIDTH//2,HEIGHT//2,"Tato taktika fungovala protože Sovětské síly nebyly připravené na boj v hlubokém sněhu a lesích,",(255,255,255), 1170, 1410)
    text7=TemporaryText(WIDTH//2,HEIGHT//2,"a Finové znali terén a byli extrémně pohybliví.",(255,255,255), 1410, 16500)
    frames=0
    VLOCKY=[]
    for i in range(WIDTH//4):
        VLOCKY.append(vlocka(WIDTH, HEIGHT, 1))
    while 1:
        if frames==1650:
            with open("databtest.json") as db:
                mydb=json.load(db)
            mydb["5"]["finished"]="3"
            with open("databtest.json","w") as db:
                json.dump(mydb,db)
            return
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key==pygame.K_ESCAPE:
                    return "MENU"
                elif event.key==pygame.K_q:
                    pygame.mixer.music.set_volume([0,100][VOLUME==0])
                    VOLUME=[0,100][VOLUME==0]
        screen.fill((0,0,0))
        text1.render(screen, HEIGHT//10)
        text2.render(screen, HEIGHT//20)
        text3.render(screen, HEIGHT//20)
        text4.render(screen, HEIGHT//20)
        text5.render(screen, HEIGHT//20)
        text6.render(screen, HEIGHT//20)
        text7.render(screen, HEIGHT//20)
        iter=0
        if random.randrange(5)==0:
            VLOCKY.append(vlocka(WIDTH,HEIGHT))
        while 1:
            try:
                VLOCKY[iter].y+=HEIGHT/1080
                VLOCKY[iter].render(screen)
                if VLOCKY[iter].y<HEIGHT:
                    iter+=1
                else:
                    del(VLOCKY[iter])
            except IndexError:
                break
        pygame.display.update()
        frames+=1
        clock.tick(60)
class Tree:
    def __init__(self,x,y,w, h):
        self.x=x
        self.y=y
        self.w=w
        self.h=h
    def collides(self, obj):
        return obj.x>self.x-self.w//2 and obj.x<self.x+self.w//2 and obj.y>self.y-self.h//2 and obj.y<self.y+self.h//2
    def render(self, screen,cmrx, cmry):
        img=pygame.transform.scale(pygame.image.load("resources/tree.png"),(self.w, self.h))
        rect=img.get_rect()
        rect.center=(self.x-cmrx, self.y-cmry)
        screen.blit(img, rect)
def level6():
    global screen, WIDTH, HEIGHT, MWIDTH, MHEIGHT,fullscreen,VOLUME
    cmrx,cmry=0,0#topleftcorner
    BULLETS=[]
    pygame.mixer.music.load("resources/actmusic2.mp3")
    pygame.mixer.music.play(-1,0.0)
    kp_increments=[-int(23*(HEIGHT/1080)),int(9*(HEIGHT/1080)), int(22*(HEIGHT/1080)),int(9*(HEIGHT/1080))]
    l_increments=[-int(21*(HEIGHT/1080)),int(9*(HEIGHT/1080)), int(22*(HEIGHT/1080)),int(9*(HEIGHT/1080))]
    kp31=Gun(4, 3, "suomi_kp31", int(16*(HEIGHT/1080)),90,WIDTH,HEIGHT, int(15*WIDTH/1920), int(67*HEIGHT/1080), kp_increments,71,"resources/kp.mp3","resources/ppl40rld.mp3",0)
    l35=Gun(30, 2, "l35", int(32*(HEIGHT/1080)),90,WIDTH,HEIGHT, int(21*WIDTH/1920), int(57*HEIGHT/1080),l_increments,8,"resources/l35.mp3","resources/tt33_rld.mp3",0)
    m28=Gun(200, 0, "m28", int(70*(HEIGHT/1080)),90,WIDTH,HEIGHT, int(12*WIDTH/1920), int(75*HEIGHT/1080),l_increments,5,"resources/m28.mp3","resources/m28_rld.mp3",300)
    m28e=Gun(400, 5, "m28", int(49*(HEIGHT/1080)),270,WIDTH,HEIGHT, int(12*WIDTH/1920), int(75*HEIGHT/1080),l_increments,5,"resources/m28.mp3","resources/m28_rld.mp3",300)
    ppd40e=Gun(7, 3, "suomi_kp31", int(16*(HEIGHT/1080)),270,WIDTH,HEIGHT, int(15*WIDTH/1920), int(67*HEIGHT/1080), kp_increments,71,"resources/kp.mp3","resources/ppl40rld.mp3",0)
    tt33e=Gun(60, 5, "tt33", int(19*(HEIGHT/1080)),90,WIDTH,HEIGHT, int(18*WIDTH/1920), int(36*HEIGHT/1080),l_increments,8,"resources/l35.mp3","resources/tt33_rld.mp3",0)
    #machine gun kp31
    #firerate cca 750-900 rounds/min--> cca 12.5-15 rps  --> delay 4 framy
    #firespeed cca 396 m/s --> panacek vysokej 180 cm je 128(HEIGHT/1080) takže cca pro x =HEIGHT/1080 je 1.8m 128x tudíž 1m=71*x px tudíž 396m je 28116*x px děleno 60 fps je 468.8x px/f což je mga rychlý
    #proto firespeed bude 64x
    PLAYER=Player(WIDTH//2,HEIGHT//2, WIDTH,HEIGHT,[l35,kp31,m28],molotovcount=3)
    started=0
    stromx, stromy=WIDTH*2, HEIGHT//2
    strom=Tree(stromx, stromy, 128*(WIDTH/1920), 128*(HEIGHT/1080))
    otherstroms=[]
    for i in range(10):
        otherstroms.append(Tree(random.randrange(2*WIDTH), random.randrange(HEIGHT), 128*(WIDTH/1920), 128*(HEIGHT/1080)))
    nadpis=Text(WIDTH//2, HEIGHT//10, "Level 3", (189, 255,255))
    nadpis2=Text(WIDTH//2, HEIGHT//5, "MOTTI", (189, 255,255))
    info3=Text(WIDTH//2, HEIGHT//3, "Jsi součástí vojenské taktiky Motti.", (189, 255,255))
    info=Text(WIDTH//2, HEIGHT//2, f"Probojuj se ke stromu na pozici {stromx}, {stromy} a schovej se tam. Poté čekej.", (189, 255,255))
    info2=Text(WIDTH//2, 2*HEIGHT//3, "K dispozici máš nově Sovětskou pušku Mosin Nagant, použij jí!", (189, 255,255))
    cont=Text(WIDTH//2, 8*HEIGHT//10, "Mezerník pro spuštění", (189, 255,255))
    infotext=TemporaryText(WIDTH//2,7*HEIGHT//8,"Zůstaň schovaný ve stromu.",(0,0,0), 0, 0)
    contsize=10
    contphase="RETROGRADE"
    gameover=0
    frames=0
    fires=[]
    VLOCKY=[]
    npcs=[]
    for i in range(5):
        x=stromx+random.randrange(WIDTH//4)
        y=stromy+random.randrange(HEIGHT//4)
        if random.randrange(10)==0:npcs.append(NPC(x, y,WIDTH, HEIGHT, [copygun(m28e)]))
        elif random.randrange(10)==1:npcs.append(NPC(x, y,WIDTH, HEIGHT, [copygun(ppd40e)]))
        else:npcs.append(NPC(x, y,WIDTH, HEIGHT, [copygun(tt33e)]))
    tiles=[]
    """tilesize=64*(WIDTH/1920)
    for i in range(-math.ceil(WIDTH/tilesize),2*math.ceil(WIDTH/tilesize)):
        for j in range(-math.ceil(HEIGHT/tilesize),2*math.ceil(HEIGHT/tilesize)):
            if random.randrange(10)==1:
                tiles.append(Tile(i*tilesize, j*tilesize, pygame.transform.scale(pygame.image.load("resources/tile"+str(random.randrange(10))+".png"),(tilesize, tilesize))))"""
    for i in range(WIDTH//4):
        VLOCKY.append(vlocka(WIDTH, HEIGHT, 1))
    molotovs=[]
    sptext=Text(WIDTH//28,12*HEIGHT//15,str(stromx)+", "+str(stromy),(252,219,0))
    sf=0
    hiding=0

    while 1:
        sf+=1
        if strom.collides(PLAYER) and hiding==0:
            for i in range(10):
                x=3*WIDTH
                if random.randrange(10)==0:npcs.append(NPC(x, random.randrange(HEIGHT),WIDTH, HEIGHT, [copygun(m28e)]))
                elif random.randrange(10)==1:npcs.append(NPC(x, random.randrange(HEIGHT),WIDTH, HEIGHT, [copygun(ppd40e)]))
                else:npcs.append(NPC(x, random.randrange(HEIGHT),WIDTH, HEIGHT, [copygun(tt33e)]))
            infotext=TemporaryText(WIDTH//2,7*HEIGHT//8,"Zůstaň schovaný ve stromu.",(0,0,0), 0,300)
            hiding=1
        if gameover:
            pygame.mixer.stop()
            with open("databtest.json") as db:
                mydb=json.load(db)
            mydb["6"]["finished"]="3"
            with open("databtest.json","w") as db:
                json.dump(mydb,db)
            return
        if PLAYER.hp<0:pygame.mixer.stop();return
        keys=pygame.key.get_pressed()
        dir=[0,0]
        if keys[pygame.K_w]:dir[1]=-1
        elif keys[pygame.K_s]:dir[1]=1
        if keys[pygame.K_a]:dir[0]=-1
        elif keys[pygame.K_d]:dir[0]=1
        x=keys[pygame.K_k]
        #y=keys[pygame.K_l]
        z=keys[pygame.K_i]
        #a=keys[pygame.K_j]
        y=0
        a=0
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key==pygame.K_ESCAPE:
                    return "MENU"
                elif event.key==pygame.K_q:
                    pygame.mixer.music.set_volume([0,100][VOLUME==0])
                    VOLUME=[0,100][VOLUME==0]
                elif event.key==pygame.K_SPACE:
                    if not started and sf>30:started=1
                elif event.key==pygame.K_u:
                    PLAYER.chnggun(1)
                elif event.key==pygame.K_z:
                    PLAYER.chnggun(-1)
                elif event.key==pygame.K_o:
                    PLAYER.reload()
                elif event.key==pygame.K_m and started and PLAYER.hp>0 and PLAYER.molotovcount>0:
                    pf=PLAYER.gun.firespeed
                    PLAYER.gun.firespeed=7*(HEIGHT/1080)
                    x=PLAYER.gun.fire(frames, PLAYER.x, PLAYER.y, screen, PLAYER.facing, molotov=1)
                    molotovs.append(Molotov(x[0],x[1],x[2],x[3]))
                    PLAYER.gun.firespeed=pf
                    PLAYER.molotovcount-=1
        if keys[pygame.K_SPACE] and frames>60 and PLAYER.hp>0:
            q=PLAYER.gun.fire(frames, PLAYER.x, PLAYER.y, screen, PLAYER.facing)
            if q!=0:
                BULLETS.append(q)
                for npc in npcs:
                    if math.sqrt((npc.x-PLAYER.x)**2+(npc.y-PLAYER.y)**2)<WIDTH:
                        npc.seesplayer=1
        screen.fill((0,0,0))
        if started:
            screen.fill((255,255,255))
            for tile in tiles:
                tile.render(screen, cmrx, cmry)
        cmrx,cmry=PLAYER.update(dir,[x,y,z,a],cmrx,cmry, r_boundary=WIDTH*2)
        for npc in npcs:
            if strom.collides(PLAYER):
                npc.target=[0,0]
                npc.wandering=0
                if npc.x<WIDTH and npc.hp>0:gameover=1
                bul=npc.update(Player(100000,100000,WIDTH,HEIGHT, [m28e]),WIDTH,HEIGHT,frames)
            else:
                bul=npc.update(PLAYER,WIDTH,HEIGHT,frames)
            if bul:BULLETS.append(bul)
        if not started:
            nadpis.render(screen, HEIGHT//20)
            nadpis2.render(screen, HEIGHT//10)
            info.render(screen, HEIGHT//20)
            info2.render(screen, HEIGHT//20)
            info3.render(screen, HEIGHT//20)
            cont.render(screen, HEIGHT//20+int(0.5*contsize))
            if contphase=="RETROGRADE":
                contsize-=0.2
                if contsize<=0:contphase="PROGRADE"
            else:
                contsize+=0.2
                if contsize>=10:contphase="RETROGRADE"
        for bullet in BULLETS:
            bullet.update()
            bullet.render(screen,cmrx,cmry)
            if bullet.pe==1:
                if PLAYER.got_hit(bullet.x, bullet.y, frames) and PLAYER.hp>-100:
                    PLAYER.hp-=int(math.sqrt(bullet.vx**2+bullet.vy**2)/(HEIGHT/1080))
                    bltsrmv.append(bullet)
            else:
                for npc in npcs:
                    if npc.got_hit(bullet.x,bullet.y,frames,cmrx,cmry):
                        dmg=int(math.sqrt(bullet.vx**2+bullet.vy**2)/(HEIGHT/1080))
                        if dmg>60:dmg=100
                        npc.hp-=dmg
                        bltsrmv.append(bullet)
            #if (bullet.x-PLAYER.x)**2+(bullet.y-PLAYER.y)**2>5*WIDTH:bltsrmv.append(bullet)
        blts2=[]
        for bullet in BULLETS:
            if bullet not in bltsrmv:blts2.append(bullet)
        BULLETS=blts2
        if started:
            for npc in npcs:
                npc.render(screen, WIDTH, HEIGHT, frames,cmrx,cmry)
                if npc.hp>0:
                    npc.gun.render(screen,npc.x, npc.y, npc.facing,cmrx,cmry)
            if PLAYER.hp>0:
                hptext=Text(WIDTH//28,14*HEIGHT//15,str(PLAYER.hp),(255,0,0))
            else:
                hptext=Text(WIDTH//28,14*HEIGHT//15,"0",(255,0,0))
            moltext=Text(31*WIDTH//32,12*HEIGHT//15,str(PLAYER.molotovcount),(252,0,0))
                
            PLAYER.render(screen, WIDTH, HEIGHT, frames, cmrx,cmry)
            if PLAYER.hp>0:
                PLAYER.gun.render(screen,PLAYER.x,PLAYER.y,PLAYER.facing,cmrx,cmry)
            bltsrmv=[]
            mltsrmv=[]
            mlts2=[]
            frmv=[]
            frs2=[]
            for molotov in molotovs:
                if molotov.update():mltsrmv.append(molotov);fires.append(Fire(molotov.x,molotov.y))
                molotov.render(screen,frames,cmrx,cmry)
            for mltv in molotovs:
                if mltv not in mltsrmv:mlts2.append(mltv)
            molotovs=list(mlts2)
            for fire in fires:
                if fire.render(screen,frames,cmrx,cmry):frmv.append(fire)
                for npc in npcs:
                    if fire.hurts(npc):npc.hp-=1
                if fire.hurts(PLAYER):PLAYER.hp-=1
            for fr in fires:
                if fr not in frmv:frs2.append(fr)
            fires=list(frs2)
            bltext=Text(31*WIDTH//32,14*HEIGHT//15,str(PLAYER.gun.bullets),(0,0,0))
            cmrytext=Text(WIDTH//2,14*HEIGHT//15,str(int(PLAYER.x))+", "+str(int(PLAYER.y)),(255,0,0))
            strom.render(screen, cmrx, cmry)
            for stro in otherstroms:stro.render(screen, cmrx, cmry)
            cmrytext.render(screen, HEIGHT//20)
            bltext.render(screen,HEIGHT//10)
            hptext.render(screen, HEIGHT//10)
            moltext.render(screen, HEIGHT//10)
            sptext.render(screen, HEIGHT//30)
            infotext.render(screen, HEIGHT//20)
        iter=0
        if random.randrange(5)==0:
            VLOCKY.append(vlocka(WIDTH,HEIGHT))
        while 1:
            try:
                VLOCKY[iter].y+=HEIGHT/1080
                VLOCKY[iter].render(screen)
                if VLOCKY[iter].y<HEIGHT:
                    iter+=1
                else:
                    del(VLOCKY[iter])
            except IndexError:
                break
        pygame.display.update()
        if started:frames+=1
        clock.tick(60)
def level7():
    global screen, WIDTH, HEIGHT, MWIDTH, MHEIGHT,fullscreen,VOLUME
    cmrx,cmry=1.5*WIDTH,0#topleftcorner
    BULLETS=[]
    pygame.mixer.music.load("resources/actmusic2.mp3")
    pygame.mixer.music.play(-1,0.0)
    kp_increments=[-int(23*(HEIGHT/1080)),int(9*(HEIGHT/1080)), int(22*(HEIGHT/1080)),int(9*(HEIGHT/1080))]
    l_increments=[-int(21*(HEIGHT/1080)),int(9*(HEIGHT/1080)), int(22*(HEIGHT/1080)),int(9*(HEIGHT/1080))]
    kp31=Gun(4, 3, "suomi_kp31", int(16*(HEIGHT/1080)),90,WIDTH,HEIGHT, int(15*WIDTH/1920), int(67*HEIGHT/1080), kp_increments,71,"resources/kp.mp3","resources/ppl40rld.mp3",0)
    l35=Gun(30, 2, "l35", int(32*(HEIGHT/1080)),90,WIDTH,HEIGHT, int(21*WIDTH/1920), int(57*HEIGHT/1080),l_increments,8,"resources/l35.mp3","resources/tt33_rld.mp3",0)
    m28=Gun(200, 0, "m28", int(70*(HEIGHT/1080)),90,WIDTH,HEIGHT, int(12*WIDTH/1920), int(75*HEIGHT/1080),l_increments,5,"resources/m28.mp3","resources/m28_rld.mp3",300)
    m28e=Gun(400, 5, "m28", int(49*(HEIGHT/1080)),270,WIDTH,HEIGHT, int(12*WIDTH/1920), int(75*HEIGHT/1080),l_increments,5,"resources/m28.mp3","resources/m28_rld.mp3",300)
    ppd40e=Gun(7, 3, "suomi_kp31", int(16*(HEIGHT/1080)),270,WIDTH,HEIGHT, int(15*WIDTH/1920), int(67*HEIGHT/1080), kp_increments,71,"resources/kp.mp3","resources/ppl40rld.mp3",0)
    tt33e=Gun(60, 5, "tt33", int(19*(HEIGHT/1080)),90,WIDTH,HEIGHT, int(18*WIDTH/1920), int(36*HEIGHT/1080),l_increments,8,"resources/l35.mp3","resources/tt33_rld.mp3",0)
    #machine gun kp31
    #firerate cca 750-900 rounds/min--> cca 12.5-15 rps  --> delay 4 framy
    #firespeed cca 396 m/s --> panacek vysokej 180 cm je 128(HEIGHT/1080) takže cca pro x =HEIGHT/1080 je 1.8m 128x tudíž 1m=71*x px tudíž 396m je 28116*x px děleno 60 fps je 468.8x px/f což je mga rychlý
    #proto firespeed bude 64x
    PLAYER=Player(2*WIDTH,HEIGHT//2, WIDTH,HEIGHT,[l35,kp31,m28],molotovcount=3)
    started=0
    stromx, stromy=WIDTH*2, HEIGHT//2
    strom=Tree(stromx, stromy, 128*(WIDTH/1920), 128*(HEIGHT/1080))
    otherstroms=[]
    for i in range(10):
        otherstroms.append(Tree(random.randrange(2*WIDTH), random.randrange(HEIGHT), 128*(WIDTH/1920), 128*(HEIGHT/1080)))
    nadpis=Text(WIDTH//2, HEIGHT//10, "Level 4", (189, 255,255))
    nadpis2=Text(WIDTH//2, HEIGHT//5, "SEKÁNÍ DŘEVA", (189, 255,255))
    info=Text(WIDTH//2, HEIGHT//2, "Dokonči Motti - \"posekej\" vojáky na 0, 0.", (189, 255,255))
    cont=Text(WIDTH//2, 8*HEIGHT//10, "Mezerník pro spuštění", (189, 255,255))
    infotext=TemporaryText(WIDTH//2,7*HEIGHT//8,"Zůstaň schovaný ve stromu.",(0,0,0), 0, 0)
    contsize=10
    contphase="RETROGRADE"
    gameover=0
    frames=0
    fires=[]
    VLOCKY=[]
    npcs=[]
    for i in range(10):
        x=random.randrange(-WIDTH//4,WIDTH//4)
        y=random.randrange(-HEIGHT//4,HEIGHT//4)
        if random.randrange(10)==0:npcs.append(NPC(x, y,WIDTH, HEIGHT, [copygun(m28e)]))
        elif random.randrange(10)==1:npcs.append(NPC(x, y,WIDTH, HEIGHT, [copygun(ppd40e)]))
        else:npcs.append(NPC(x, y,WIDTH, HEIGHT, [copygun(tt33e)]))
    for i in range(WIDTH//4):
        VLOCKY.append(vlocka(WIDTH, HEIGHT, 1))
    molotovs=[]
    sptext=Text(WIDTH//28,12*HEIGHT//15,"0, 0",(252,219,0))
    sf=0
    anim=0
    animcounter=0
    alivenum=100
    while 1:
        if alivenum<2 and not anim:
            x=random.randrange(-WIDTH//4,WIDTH//4)
            y=random.randrange(-HEIGHT//4,HEIGHT//4)
            npcs.append(NPC(x, y,WIDTH, HEIGHT, [copygun(ppd40e)]))
        sf+=1
        col=0
        for stro in otherstroms:
            if stro.collides(PLAYER):col=1;break
        alivenum=sum(npc.hp>0 for npc in npcs)
        if anim:
            animcounter+=1
            if animcounter>=8*60:gameover=1
        if gameover:
            pygame.mixer.stop()
            with open("databtest.json") as db:
                mydb=json.load(db)
            mydb["7"]["finished"]="3"
            with open("databtest.json","w") as db:
                json.dump(mydb,db)
            return
        keys=pygame.key.get_pressed()
        dir=[0,0]
        if keys[pygame.K_w]:dir[1]=-1
        elif keys[pygame.K_s]:dir[1]=1
        if keys[pygame.K_a]:dir[0]=-1
        elif keys[pygame.K_d]:dir[0]=1
        x=keys[pygame.K_k]
        #y=keys[pygame.K_l]
        z=keys[pygame.K_i]
        #a=keys[pygame.K_j]
        y=0
        a=0
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key==pygame.K_ESCAPE:
                    return "MENU"
                elif event.key==pygame.K_q:
                    pygame.mixer.music.set_volume([0,100][VOLUME==0])
                    VOLUME=[0,100][VOLUME==0]
                elif event.key==pygame.K_SPACE:
                    if not started and sf>30:started=1
                elif event.key==pygame.K_u:
                    PLAYER.chnggun(1)
                elif event.key==pygame.K_z:
                    PLAYER.chnggun(-1)
                elif event.key==pygame.K_o:
                    PLAYER.reload()
                elif event.key==pygame.K_m and started and PLAYER.hp>0 and PLAYER.molotovcount>0:
                    pf=PLAYER.gun.firespeed
                    PLAYER.gun.firespeed=7*(HEIGHT/1080)
                    x=PLAYER.gun.fire(frames, PLAYER.x, PLAYER.y, screen, PLAYER.facing, molotov=1)
                    molotovs.append(Molotov(x[0],x[1],x[2],x[3]))
                    PLAYER.gun.firespeed=pf
                    PLAYER.molotovcount-=1
        if keys[pygame.K_SPACE] and frames>60 and PLAYER.hp>0:
            q=PLAYER.gun.fire(frames, PLAYER.x, PLAYER.y, screen, PLAYER.facing)
            if q!=0:
                BULLETS.append(q)
                for npc in npcs:
                    if math.sqrt((npc.x-PLAYER.x)**2+(npc.y-PLAYER.y)**2)<WIDTH:
                        npc.seesplayer=1
        screen.fill((0,0,0))
        if started:
            screen.fill((255,255,255))
        cmrx,cmry=PLAYER.update(dir,[x,y,z,a],cmrx,cmry, r_boundary=WIDTH*2)
        for npc in npcs:
            if strom.collides(PLAYER) or col:
                bul=npc.update(Player(100000,100000,WIDTH,HEIGHT, [m28e]),WIDTH,HEIGHT,frames)
            else:
                bul=npc.update(PLAYER,WIDTH,HEIGHT,frames)
            if bul:BULLETS.append(bul)
        if not started:
            nadpis.render(screen, HEIGHT//20)
            nadpis2.render(screen, HEIGHT//10)
            info.render(screen, HEIGHT//20)
            cont.render(screen, HEIGHT//20+int(0.5*contsize))
            if contphase=="RETROGRADE":
                contsize-=0.2
                if contsize<=0:contphase="PROGRADE"
            else:
                contsize+=0.2
                if contsize>=10:contphase="RETROGRADE"
        for bullet in BULLETS:
            bullet.update()
            bullet.render(screen,cmrx,cmry)
            if bullet.pe==1:
                if PLAYER.got_hit(bullet.x, bullet.y, frames) and PLAYER.hp>-100:
                    PLAYER.hp-=int(math.sqrt(bullet.vx**2+bullet.vy**2)/(HEIGHT/1080))
                    bltsrmv.append(bullet)
                    if alivenum<3:
                        anim=1
                        sound=pygame.mixer.Sound("resources/postrelen.mp3")
                        sound.play()
            else:
                for npc in npcs:
                    if npc.got_hit(bullet.x,bullet.y,frames,cmrx,cmry):
                        dmg=int(math.sqrt(bullet.vx**2+bullet.vy**2)/(HEIGHT/1080))
                        if dmg>60:dmg=100
                        npc.hp-=dmg
                        bltsrmv.append(bullet)
            #if (bullet.x-PLAYER.x)**2+(bullet.y-PLAYER.y)**2>5*WIDTH:bltsrmv.append(bullet)
        blts2=[]
        for bullet in BULLETS:
            if bullet not in bltsrmv:blts2.append(bullet)
        BULLETS=blts2
        if started:
            for npc in npcs:
                npc.render(screen, WIDTH, HEIGHT, frames,cmrx,cmry)
                if npc.hp>0:
                    npc.gun.render(screen,npc.x, npc.y, npc.facing,cmrx,cmry)
            if PLAYER.hp>0:
                hptext=Text(WIDTH//28,14*HEIGHT//15,str(PLAYER.hp),(255,0,0))
            else:
                hptext=Text(WIDTH//28,14*HEIGHT//15,"0",(255,0,0))
            moltext=Text(31*WIDTH//32,12*HEIGHT//15,str(PLAYER.molotovcount),(252,0,0))
                
            PLAYER.render(screen, WIDTH, HEIGHT, frames, cmrx,cmry)
            if PLAYER.hp>0:
                PLAYER.gun.render(screen,PLAYER.x,PLAYER.y,PLAYER.facing,cmrx,cmry)
            bltsrmv=[]
            mltsrmv=[]
            mlts2=[]
            frmv=[]
            frs2=[]
            for molotov in molotovs:
                if molotov.update():mltsrmv.append(molotov);fires.append(Fire(molotov.x,molotov.y))
                molotov.render(screen,frames,cmrx,cmry)
            for mltv in molotovs:
                if mltv not in mltsrmv:mlts2.append(mltv)
            molotovs=list(mlts2)
            for fire in fires:
                if fire.render(screen,frames,cmrx,cmry):frmv.append(fire)
                for npc in npcs:
                    if fire.hurts(npc):npc.hp-=1
                if fire.hurts(PLAYER):PLAYER.hp-=1
            for fr in fires:
                if fr not in frmv:frs2.append(fr)
            fires=list(frs2)
            bltext=Text(31*WIDTH//32,14*HEIGHT//15,str(PLAYER.gun.bullets),(0,0,0))
            cmrytext=Text(WIDTH//2,14*HEIGHT//15,str(int(PLAYER.x))+", "+str(int(PLAYER.y)),(255,0,0))
            strom.render(screen, cmrx, cmry)
            for stro in otherstroms:stro.render(screen, cmrx, cmry)
            cmrytext.render(screen, HEIGHT//20)
            bltext.render(screen,HEIGHT//10)
            hptext.render(screen, HEIGHT//10)
            moltext.render(screen, HEIGHT//10)
            sptext.render(screen, HEIGHT//30)
            infotext.render(screen, HEIGHT//20)
        iter=0
        if random.randrange(5)==0:
            VLOCKY.append(vlocka(WIDTH,HEIGHT))
        while 1:
            try:
                VLOCKY[iter].y+=HEIGHT/1080
                VLOCKY[iter].render(screen)
                if VLOCKY[iter].y<HEIGHT:
                    iter+=1
                else:
                    del(VLOCKY[iter])
            except IndexError:
                break
        if anim:
            screen.fill((255,255,255))
        pygame.display.update()
        if started:frames+=1
        clock.tick(60)
def level8():
    global screen, WIDTH, HEIGHT, MWIDTH, MHEIGHT,fullscreen,VOLUME
    text1=TemporaryText(WIDTH//2,HEIGHT//2,"Byl jsi postřelen.",(255,255,255), 30, 240)
    text2=TemporaryText(WIDTH//2,HEIGHT//2,"Ve Finsku okolo 1940 mohly teploty klesnou až na -40°C.",(255,255,255), 240, 450)
    text3=TemporaryText(WIDTH//2,HEIGHT//2,"V takovéto teplotě bez zásob a s prokrváceným oblečením umrzneš přibližně za 7 minut.",(255,255,255), 450, 690)
    text4=TemporaryText(WIDTH//2,HEIGHT//2,"Jediný způsob jak nepadnout do zajetí a přežít je dostat se k základně.",(255,255,255), 690, 930)
    text5=TemporaryText(WIDTH//2,HEIGHT//2,"Bohužel jsi zůstal za nepřátelskou linií.",(255,255,255), 930, 1170)
    text6=TemporaryText(WIDTH//2,HEIGHT//2,"Musíš se tedy prosekat do bezpečí než ti vyprší limit.",(255,255,255), 1170, 1410)
    frames=0
    VLOCKY=[]
    for i in range(WIDTH//4):
        VLOCKY.append(vlocka(WIDTH, HEIGHT, 1))
    while 1:
        if frames==1410:
            with open("databtest.json") as db:
                mydb=json.load(db)
            mydb["8"]["finished"]="3"
            with open("databtest.json","w") as db:
                json.dump(mydb,db)
            return
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key==pygame.K_ESCAPE:
                    return "MENU"
                elif event.key==pygame.K_q:
                    pygame.mixer.music.set_volume([0,100][VOLUME==0])
                    VOLUME=[0,100][VOLUME==0]
        screen.fill((0,0,0))
        text1.render(screen, HEIGHT//10)
        text2.render(screen, HEIGHT//20)
        text3.render(screen, HEIGHT//20)
        text4.render(screen, HEIGHT//20)
        text5.render(screen, HEIGHT//20)
        text6.render(screen, HEIGHT//20)
        iter=0
        if random.randrange(5)==0:
            VLOCKY.append(vlocka(WIDTH,HEIGHT))
        while 1:
            try:
                VLOCKY[iter].y+=HEIGHT/1080
                VLOCKY[iter].render(screen)
                if VLOCKY[iter].y<HEIGHT:
                    iter+=1
                else:
                    del(VLOCKY[iter])
            except IndexError:
                break
        pygame.display.update()
        frames+=1
        clock.tick(60)
def level9():
    global screen, WIDTH, HEIGHT, MWIDTH, MHEIGHT,fullscreen,VOLUME
    cmrx,cmry=6.5*WIDTH,0#topleftcorner
    BULLETS=[]
    pygame.mixer.music.load("resources/actmusic.mp3")
    pygame.mixer.music.play(-1,0.0)
    TARGETTIME=60*60*7
    kp_increments=[-int(23*(HEIGHT/1080)),int(9*(HEIGHT/1080)), int(22*(HEIGHT/1080)),int(9*(HEIGHT/1080))]
    l_increments=[-int(21*(HEIGHT/1080)),int(9*(HEIGHT/1080)), int(22*(HEIGHT/1080)),int(9*(HEIGHT/1080))]
    kp31=Gun(4, 3, "suomi_kp31", int(16*(HEIGHT/1080)),90,WIDTH,HEIGHT, int(15*WIDTH/1920), int(67*HEIGHT/1080), kp_increments,71,"resources/kp.mp3","resources/ppl40rld.mp3",0)
    l35=Gun(30, 2, "l35", int(32*(HEIGHT/1080)),90,WIDTH,HEIGHT, int(21*WIDTH/1920), int(57*HEIGHT/1080),l_increments,8,"resources/l35.mp3","resources/tt33_rld.mp3",0)
    m28=Gun(200, 0, "m28", int(70*(HEIGHT/1080)),90,WIDTH,HEIGHT, int(12*WIDTH/1920), int(75*HEIGHT/1080),l_increments,5,"resources/m28.mp3","resources/m28_rld.mp3",300)
    m28e=Gun(400, 5, "m28", int(49*(HEIGHT/1080)),270,WIDTH,HEIGHT, int(12*WIDTH/1920), int(75*HEIGHT/1080),l_increments,5,"resources/m28.mp3","resources/m28_rld.mp3",300)
    ppd40e=Gun(7, 3, "suomi_kp31", int(16*(HEIGHT/1080)),270,WIDTH,HEIGHT, int(15*WIDTH/1920), int(67*HEIGHT/1080), kp_increments,71,"resources/kp.mp3","resources/ppl40rld.mp3",0)
    tt33e=Gun(60, 5, "tt33", int(19*(HEIGHT/1080)),90,WIDTH,HEIGHT, int(18*WIDTH/1920), int(36*HEIGHT/1080),l_increments,8,"resources/l35.mp3","resources/tt33_rld.mp3",0)
    #machine gun kp31
    #firerate cca 750-900 rounds/min--> cca 12.5-15 rps  --> delay 4 framy
    #firespeed cca 396 m/s --> panacek vysokej 180 cm je 128(HEIGHT/1080) takže cca pro x =HEIGHT/1080 je 1.8m 128x tudíž 1m=71*x px tudíž 396m je 28116*x px děleno 60 fps je 468.8x px/f což je mga rychlý
    #proto firespeed bude 64x
    PLAYER=Player(7*WIDTH,HEIGHT//2, WIDTH,HEIGHT,[l35,kp31,m28],molotovcount=3)
    started=0
    otherstroms=[]
    for i in range(30):
        otherstroms.append(Tree(random.randrange(7*WIDTH), random.randrange(HEIGHT), 128*(WIDTH/1920), 128*(HEIGHT/1080)))
    nadpis=Text(WIDTH//2, HEIGHT//10, "Level 5", (189, 255,255))
    nadpis2=Text(WIDTH//2, HEIGHT//5, "PROSEKEJ SE K VÍTĚZSTVÍ", (189, 255,255))
    info=Text(WIDTH//2, HEIGHT//2, "Dostaň se do bezpečí na souřadnice 0, 0.", (189, 255,255))
    cont=Text(WIDTH//2, 8*HEIGHT//10, "Mezerník pro spuštění", (189, 255,255))
    contsize=10
    contphase="RETROGRADE"
    gameover=0
    frames=0
    fires=[]
    VLOCKY=[]
    npcs=[]
    for i in range(10):
        x=random.randrange(-WIDTH,WIDTH*6)
        y=random.randrange(HEIGHT)
        if random.randrange(10)==0:npcs.append(NPC(x, y,WIDTH, HEIGHT, [copygun(m28e)]))
        elif random.randrange(10)==1:npcs.append(NPC(x, y,WIDTH, HEIGHT, [copygun(ppd40e)]))
        else:npcs.append(NPC(x, y,WIDTH, HEIGHT, [copygun(tt33e)]))
    for i in range(WIDTH//4):
        VLOCKY.append(vlocka(WIDTH, HEIGHT, 1))
    molotovs=[]
    sf=0
    while 1:
        if PLAYER.x>-64 and PLAYER.x<64 and PLAYER.y>-64 and PLAYER.y<64:gameover=1
        sf+=1
        if frames==TARGETTIME or PLAYER.hp<=0:pygame.mixer.stop();return
        if gameover:
            pygame.mixer.stop()
            with open("databtest.json") as db:
                mydb=json.load(db)
            mydb["7"]["finished"]="3"
            with open("databtest.json","w") as db:
                json.dump(mydb,db)
            return
        keys=pygame.key.get_pressed()
        dir=[0,0]
        if keys[pygame.K_w]:dir[1]=-1
        elif keys[pygame.K_s]:dir[1]=1
        if keys[pygame.K_a]:dir[0]=-1
        elif keys[pygame.K_d]:dir[0]=1
        x=keys[pygame.K_k]
        #y=keys[pygame.K_l]
        z=keys[pygame.K_i]
        #a=keys[pygame.K_j]
        y=0
        a=0
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key==pygame.K_ESCAPE:
                    return "MENU"
                elif event.key==pygame.K_q:
                    pygame.mixer.music.set_volume([0,100][VOLUME==0])
                    VOLUME=[0,100][VOLUME==0]
                elif event.key==pygame.K_SPACE:
                    if not started and sf>30:started=1
                elif event.key==pygame.K_u:
                    PLAYER.chnggun(1)
                elif event.key==pygame.K_z:
                    PLAYER.chnggun(-1)
                elif event.key==pygame.K_o:
                    PLAYER.reload()
                elif event.key==pygame.K_m and started and PLAYER.hp>0 and PLAYER.molotovcount>0:
                    pf=PLAYER.gun.firespeed
                    PLAYER.gun.firespeed=7*(HEIGHT/1080)
                    x=PLAYER.gun.fire(frames, PLAYER.x, PLAYER.y, screen, PLAYER.facing, molotov=1)
                    molotovs.append(Molotov(x[0],x[1],x[2],x[3]))
                    PLAYER.gun.firespeed=pf
                    PLAYER.molotovcount-=1
        if keys[pygame.K_SPACE] and frames>60 and PLAYER.hp>0:
            q=PLAYER.gun.fire(frames, PLAYER.x, PLAYER.y, screen, PLAYER.facing)
            if q!=0:
                BULLETS.append(q)
                for npc in npcs:
                    if math.sqrt((npc.x-PLAYER.x)**2+(npc.y-PLAYER.y)**2)<WIDTH:
                        npc.seesplayer=1
        screen.fill((0,0,0))
        if started:
            screen.fill((255,255,255))
        cmrx,cmry=PLAYER.update(dir,[x,y,z,a],cmrx,cmry, r_boundary=WIDTH*7)
        for npc in npcs:
            bul=npc.update(PLAYER,WIDTH,HEIGHT,frames)
            print(npc.target,npc.wandering)
            if bul:BULLETS.append(bul)
        if not started:
            nadpis.render(screen, HEIGHT//20)
            nadpis2.render(screen, HEIGHT//10)
            info.render(screen, HEIGHT//20)
            cont.render(screen, HEIGHT//20+int(0.5*contsize))
            if contphase=="RETROGRADE":
                contsize-=0.2
                if contsize<=0:contphase="PROGRADE"
            else:
                contsize+=0.2
                if contsize>=10:contphase="RETROGRADE"
        for bullet in BULLETS:
            bullet.update()
            bullet.render(screen,cmrx,cmry)
            if bullet.pe==1:
                if PLAYER.got_hit(bullet.x, bullet.y, frames) and PLAYER.hp>-100:
                    PLAYER.hp-=int(math.sqrt(bullet.vx**2+bullet.vy**2)/(HEIGHT/1080))
                    bltsrmv.append(bullet)
            else:
                for npc in npcs:
                    if npc.got_hit(bullet.x,bullet.y,frames,cmrx,cmry):
                        dmg=int(math.sqrt(bullet.vx**2+bullet.vy**2)/(HEIGHT/1080))
                        if dmg>60:dmg=100
                        npc.hp-=dmg
                        bltsrmv.append(bullet)
            #if (bullet.x-PLAYER.x)**2+(bullet.y-PLAYER.y)**2>5*WIDTH:bltsrmv.append(bullet)
        blts2=[]
        for bullet in BULLETS:
            if bullet not in bltsrmv:blts2.append(bullet)
        BULLETS=blts2
        if started:
            for npc in npcs:
                if npc.x>PLAYER.x-WIDTH and npc.x<PLAYER.x+WIDTH:
                    npc.render(screen, WIDTH, HEIGHT, frames,cmrx,cmry)
                    if npc.hp>0:
                        npc.gun.render(screen,npc.x, npc.y, npc.facing,cmrx,cmry)
            if PLAYER.hp>0:
                hptext=Text(WIDTH//28,14*HEIGHT//15,str(PLAYER.hp),(255,0,0))
            else:
                hptext=Text(WIDTH//28,14*HEIGHT//15,"0",(255,0,0))
            moltext=Text(31*WIDTH//32,12*HEIGHT//15,str(PLAYER.molotovcount),(252,0,0))
                
            PLAYER.render(screen, WIDTH, HEIGHT, frames, cmrx,cmry)
            if PLAYER.hp>0:
                PLAYER.gun.render(screen,PLAYER.x,PLAYER.y,PLAYER.facing,cmrx,cmry)
            bltsrmv=[]
            mltsrmv=[]
            mlts2=[]
            frmv=[]
            frs2=[]
            for molotov in molotovs:
                if molotov.update():mltsrmv.append(molotov);fires.append(Fire(molotov.x,molotov.y))
                molotov.render(screen,frames,cmrx,cmry)
            for mltv in molotovs:
                if mltv not in mltsrmv:mlts2.append(mltv)
            molotovs=list(mlts2)
            for fire in fires:
                if fire.render(screen,frames,cmrx,cmry):frmv.append(fire)
                for npc in npcs:
                    if fire.hurts(npc):npc.hp-=1
                if fire.hurts(PLAYER):PLAYER.hp-=1
            for fr in fires:
                if fr not in frmv:frs2.append(fr)
            fires=list(frs2)
            bltext=Text(31*WIDTH//32,14*HEIGHT//15,str(PLAYER.gun.bullets),(0,0,0))
            cmrytext=Text(WIDTH//2,14*HEIGHT//15,str(int(PLAYER.x))+", "+str(int(PLAYER.y)),(255,0,0))
            for stro in otherstroms:
                if stro.x>PLAYER.x-WIDTH and stro.x<PLAYER.x+WIDTH:stro.render(screen, cmrx, cmry)
            cmrytext.render(screen, HEIGHT//20)
            bltext.render(screen,HEIGHT//10)
            hptext.render(screen, HEIGHT//10)
            moltext.render(screen, HEIGHT//10)
        if TARGETTIME:
                time=TARGETTIME-frames
                mins=time//60//60
                secs=time//60%60
                secstr=str(secs)
                if len(secstr)<2:secstr="0"+secstr
                tartext=Text(30*WIDTH//32,HEIGHT//23,str(mins)+":"+secstr,(255,216,60))
                tartext.render(screen,HEIGHT//10)
        iter=0
        if not started:
            if random.randrange(5)==0:
                VLOCKY.append(vlocka(WIDTH,HEIGHT))
            while 1:
                try:
                    VLOCKY[iter].y+=HEIGHT/1080
                    VLOCKY[iter].render(screen)
                    if VLOCKY[iter].y<HEIGHT:
                        iter+=1
                    else:
                        del(VLOCKY[iter])
                except IndexError:
                    break
        pygame.display.update()
        if started:frames+=1
        clock.tick(60)
def level10():
    global screen, WIDTH, HEIGHT, MWIDTH, MHEIGHT,fullscreen,VOLUME
    text1=TemporaryText(WIDTH//2,HEIGHT//2,"Dostal jsi se do bezpečí.",(255,255,255), 30, 240)
    text2=TemporaryText(WIDTH//2,HEIGHT//2,"13.3.1940 válka skončila podpisem Moskevské mírové smlouvy.",(255,255,255), 240, 450)
    text3=TemporaryText(WIDTH//2,HEIGHT//2,"Finsko muselo dát Sovětům asi 11% svého území.",(255,255,255), 450, 690)
    text4=TemporaryText(WIDTH//2,HEIGHT//2,"Na druhou stranu si zachovalo nezávislost a to bylo jeho hlavním cílem.",(255,255,255), 690, 930)
    text5=TemporaryText(WIDTH//2,HEIGHT//2,"Sovětský svaz byl kritizován a vyloučen ze Společnosti národů.",(255,255,255), 930, 1170)
    text6=TemporaryText(WIDTH//2,HEIGHT//2,"KONEC HRY",(255,255,255), 1170, 1410)
    text7=TemporaryText(WIDTH//2, 5*HEIGHT//7,"Zdroje a anotace: github.com/mikulaspater/Winter-war/",(255,255,255),30, 1410)
    frames=0
    VLOCKY=[]
    for i in range(WIDTH//4):
        VLOCKY.append(vlocka(WIDTH, HEIGHT, 1))
    while 1:
        if frames==1410:
            with open("databtest.json") as db:
                mydb=json.load(db)
            mydb["8"]["finished"]="3"
            with open("databtest.json","w") as db:
                json.dump(mydb,db)
            return
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key==pygame.K_ESCAPE:
                    return "MENU"
                elif event.key==pygame.K_q:
                    pygame.mixer.music.set_volume([0,100][VOLUME==0])
                    VOLUME=[0,100][VOLUME==0]
        screen.fill((0,0,0))
        text1.render(screen, HEIGHT//10)
        text2.render(screen, HEIGHT//20)
        text3.render(screen, HEIGHT//20)
        text4.render(screen, HEIGHT//20)
        text5.render(screen, HEIGHT//20)
        text6.render(screen, HEIGHT//10)
        text7.render(screen, HEIGHT//25)
        iter=0
        if random.randrange(5)==0:
            VLOCKY.append(vlocka(WIDTH,HEIGHT))
        while 1:
            try:
                VLOCKY[iter].y+=HEIGHT/1080
                VLOCKY[iter].render(screen)
                if VLOCKY[iter].y<HEIGHT:
                    iter+=1
                else:
                    del(VLOCKY[iter])
            except IndexError:
                break
        pygame.display.update()
        frames+=1
        clock.tick(60)
mainmenu()