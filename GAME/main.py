#made by Mikulas Pater 2025
#POkud toto někdo čte, tak vítej, poutníče
import pygame
import json
import random
import math
testmode=1
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
class Bullet:
    def __init__(self,x,y,vx,vy):
        self.x=x
        self.y=y
        self.vx=vx
        self.vy=vy
    def update(self):
        self.x+=self.vx
        self.y+=self.vy
        self.vx=0.995*self.vx
        self.vy=0.995*self.vy
    def render(self, screen):
        screen.set_at((int(self.x), int(self.y)),(0,0,0))
        screen.set_at((int(self.x+1), int(self.y)),(25,25,25))
        screen.set_at((int(self.x-1), int(self.y)),(25,25,25))
        screen.set_at((int(self.x), int(self.y+1)),(25,25,25))
        screen.set_at((int(self.x), int(self.y-1)),(25,25,25))
        screen.set_at((int(self.x+1), int(self.y+1)),(50,50,50))
        screen.set_at((int(self.x-1), int(self.y-1)),(50,50,50))
        screen.set_at((int(self.x-1), int(self.y+1)),(50,50,50))
        screen.set_at((int(self.x+1), int(self.y-1)),(50,50,50))
sound=1
screen=pygame.display.set_mode((0,0),pygame.FULLSCREEN)
class Player:
    def __init__(self, x, y,WIDTH,HEIGHT,posguns):
        self.x=x
        self.y=y
        self.relativex=x
        self.relativey=y
        self.posguns=posguns
        self.gun=self.posguns[0]
        self.gunind=0
        self.sizex=int(128*(WIDTH/1920))
        self.sizey=int(128*(HEIGHT/1080))
        self.facing="r"
        self.imgidl1r=pygame.transform.scale(pygame.image.load("resources/idle1r.png").convert_alpha(),(self.sizex, self.sizey))
        self.imgidl2r=pygame.transform.scale(pygame.image.load("resources/idle2r.png").convert_alpha(),(self.sizex, self.sizey))
        self.imgidl1l=pygame.transform.scale(pygame.image.load("resources/idle1l.png").convert_alpha(),(self.sizex, self.sizey))
        self.imgidl2l=pygame.transform.scale(pygame.image.load("resources/idle2l.png").convert_alpha(),(self.sizex, self.sizey))
        self.runnin=0
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
    def update(self, dir, gundir):
        prf=self.facing
        if dir[0]==1:self.facing="r"
        if dir[0]==-1:self.facing="l"
        if self.gun.reloading and self.facing!=prf:
            self.gun.prevangle=360-self.gun.prevangle
        self.x+=3*dir[0]
        self.y+=3*dir[1]
        self.runnin=abs(dir[0])+abs(dir[1])>0
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
            #print(targangle, self.gun.angle)
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
            self.gun.reloading=2
            self.gun.bullets=self.gun.rounds
        if self.gun.reloading==2 and self.gun.angle==self.gun.prevangle:
            self.gun.reloading=0
    def reload(self):
        if self.gun.reloading!=0 or self.gun.bullets==self.gun.rounds:return
        self.gun.prevangle=self.gun.angle
        self.gun.reloading=1
        channel=pygame.mixer.find_channel()
        if channel:
            self.gun.reload.play()
    def render(self,screen, WIDTH,HEIGHT,frame):
        if self.runnin and 0:
            screen.blit(pygame.transform.scale(pygame.image.load("resources/run"+self.facing+(frame%8)+".png").convert(),(self.sizex, self.sizey)), (self.x-self.sizex//2, self.y-self.sizey//2))
        else:
            if frame%30<15:
                exec("screen.blit(self.imgidl1"+self.facing+", (self.x-self.sizex//2, self.y-self.sizey//2))")
            else:
                exec("screen.blit(self.imgidl2"+self.facing+", (self.x-self.sizex//2, self.y-self.sizey//2))")

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
    def __init__(self, firerate, maxspread, texturename, firespeed,angle,WIDTH, HEIGHT,twidth,theight, increments,rounds,shot,reload):
        self.firerate=firerate
        self.maxspread=maxspread
        self.texturel=pygame.transform.scale(pygame.image.load("resources/"+texturename+"l.png").convert_alpha(),(twidth, theight))
        self.texturer=pygame.transform.scale(pygame.image.load("resources/"+texturename+"r.png").convert_alpha(),(twidth, theight))
        self.firespeed=firespeed
        self.angle=angle
        self.lastfire=-firerate
        self.WIDTH=WIDTH
        self.HEIGHT=HEIGHT
        self.twidth=twidth
        self.theight=theight
        self.cxil, self.cyil, self.cxir, self.cyir=increments
        self.rounds=rounds
        self.bullets=rounds
        self.reloading=0
        self.prevangle=0
        self.shot=pygame.mixer.Sound(shot)
        self.reload=pygame.mixer.Sound(reload)
    def render(self,screen,px,py,facing):
        angle=360-self.angle
        if facing=="r":
            rotimg=pygame.transform.rotate(self.texturer, angle)
            rect=rotimg.get_rect(center=self.texturer.get_rect(center=(px+self.cxir,py+self.cyir)).center)
        elif facing=="l":
            rotimg=pygame.transform.rotate(self.texturel, angle)
            rect=rotimg.get_rect(center=self.texturel.get_rect(center=(px+self.cxil,py+self.cyil)).center)
        screen.blit(rotimg, rect)
    def fire(self,frames,px,py, screen, facing):
        if frames-self.lastfire<self.firerate or self.reloading!=0 or self.bullets==0:return 0
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
        angle=self.angle+random.randrange(2*self.maxspread)-self.maxspread
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
        #print(angle, vx, vy, vx**2+vy**2)
        self.lastfire=frames
        self.bullets-=1
        channel=pygame.mixer.find_channel()
        if channel:
            self.shot.play()
        return Bullet(xtip, ytip, vx, vy)


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
    nadpis=Text(WIDTH//2, HEIGHT//20, "NÁVOD", (255, 208,0))
    while 1:
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key==pygame.K_ESCAPE:
                    return
                elif event.key==pygame.K_p:
                    if fullscreen:
                        HEIGHT,WIDTH=HEIGHT//2, WIDTH//2
                        screen=pygame.display.set_mode((WIDTH,HEIGHT))
                        fullscreen=0
                    else:
                        HEIGHT,WIDTH=HEIGHT*2, WIDTH*2
                        screen=pygame.display.set_mode((WIDTH,HEIGHT))
                        fullscreen=1
                    
        screen.fill((0,0,0))
        nadpis.render(screen, HEIGHT//10)
        pygame.display.update()
        clock.tick(60)
def about():
    global screen, WIDTH, HEIGHT, MWIDTH, MHEIGHT,fullscreen,VOLUME
    nadpis=Text(WIDTH//2, HEIGHT//20, "O HŘE", (255,208,0))
    """Tato hra byla vytvořena pro soutěž eustory.
    Programoval Mikuláš Pater, příběh vytvořen mnou, založen na zdrojích (viz zdroje).
    Většinu grafiky vytvářel ChatGPT, část stažena přes no copyright stránky.
    Rád bych poděkoval paní prof. Kupcové.
    Zdroje: chat.openai.com, claude.ai, en.wikipedia.org/wiki/Football_War,
    www.britannica.com/topic/Soccer-War, adst.org/2014/06/the-1969-soccer-war/,
    www.youtube.com/watch?v=FVshtHUysBc"""
    while 1:
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key==pygame.K_ESCAPE:
                    return
                    
        screen.fill((0,0,0))
        nadpis.render(screen, HEIGHT//10)
        pygame.display.update()
        clock.tick(60)
def mainmenu():
    global screen, WIDTH, HEIGHT, MWIDTH, MHEIGHT,fullscreen,VOLUME
    nadpis=Text(WIDTH//2, HEIGHT//10, "ZIMNÍ VÁLKA", (189, 255,255))
    button1=Button(2.5*WIDTH/5,2*HEIGHT//7+HEIGHT//20,"Pokračovat ve hře", True, resumegame)
    button2=Button(2.5*WIDTH/5,3*HEIGHT//7+HEIGHT//20,"Levely",0,levelmenu)
    button3=Button(2.5*WIDTH/5,4*HEIGHT//7+HEIGHT//20,"Návod",0,navod)
    button4=Button(2.5*WIDTH/5,5*HEIGHT//7+HEIGHT//20,"O hře",0,about)
    button5=Button(2.5*WIDTH/5,6*HEIGHT//7+HEIGHT//20,"Exit",0,quit)
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
                quit()
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
                        print("paused")
                    exec("button"+str(marked)+".press()")
                elif event.key==pygame.K_m:
                    pygame.mixer.music.set_volume([0,100][VOLUME==0])
                    VOLUME=[0,100][VOLUME==0]
                else:
                    print(event.key)
            elif event.type==pygame.MOUSEBUTTONDOWN:
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
    db=readdatabase()
    while 1:
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key==pygame.K_ESCAPE:
                    return
                    
        screen.fill((0,0,0))
        #stuff
        pygame.display.update()
        clock.tick(60)
def level1():
    global screen, WIDTH, HEIGHT, MWIDTH, MHEIGHT,fullscreen,VOLUME
    text1=TemporaryText(WIDTH//2,HEIGHT//2,"Ve Finsku se píše 30.11.1939.",(255,255,255), 30, 240)
    text2=TemporaryText(WIDTH//2,HEIGHT//2,"Ve Finsku se píše rok 30.11.1939.",(255,255,255), 240, 450)
    frames=0
    VLOCKY=[]
    for i in range(WIDTH//4):
        VLOCKY.append(vlocka(WIDTH, HEIGHT, 1))
    while 1:
        if frames==1000:
            with open("databtest.json") as db:
                mydb=json.load(db)
            mydb["1"]["finished"]="3"
            with open("databtest.json","w") as db:
                json.dump(mydb,db)
            return
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key==pygame.K_ESCAPE:
                    return "MENU"
                elif event.key==pygame.K_m:
                    pygame.mixer.music.set_volume([0,100][VOLUME==0])
                    VOLUME=[0,100][VOLUME==0]
        screen.fill((0,0,0))
        text1.render(screen, HEIGHT//10)
        text2.render(screen, HEIGHT//10)
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
    BULLETS=[]
    kp_increments=[-int(17*(HEIGHT/1080)),int(12*(HEIGHT/1080)), int(30*(HEIGHT/1080)),int(12*(HEIGHT/1080))]
    l_increments=[-int(27*(HEIGHT/1080)),int(12*(HEIGHT/1080)), int(30*(HEIGHT/1080)),int(12*(HEIGHT/1080))]
    kp31=Gun(4, 3, "suomi_kp31", int(16*(HEIGHT/1080)),90,WIDTH,HEIGHT, int(20*WIDTH/1920), int(90*HEIGHT/1080), kp_increments,71,"resources/kp.mp3","resources/m28reload.mp3")
    l35=Gun(30, 3, "l35", int(14*(HEIGHT/1080)),90,WIDTH,HEIGHT, int(27*WIDTH/1920), int(75*HEIGHT/1080),l_increments,8,"resources/l35.mp3","resources/m28reload.mp3")
    m28=Gun(200, 3, "m28", int(70*(HEIGHT/1080)),90,WIDTH,HEIGHT, int(15*WIDTH/1920), int(101*HEIGHT/1080),l_increments,5,"resources/m28.mp3","resources/m28reload.mp3")
    #machine gun kp31
    #firerate cca 750-900 rounds/min--> cca 12.5-15 rps  --> delay 4 framy
    #firespeed cca 396 m/s --> panacek vysokej 180 cm je 128(HEIGHT/1080) takže cca pro x =HEIGHT/1080 je 1.8m 128x tudíž 1m=71*x px tudíž 396m je 28116*x px děleno 60 fps je 468.8x px/f což je mga rychlý
    #proto firespeed bude 64x
    PLAYER=Player(100,100, WIDTH,HEIGHT,[kp31,l35,m28])
    started=0
    nadpis=Text(WIDTH//2, HEIGHT//10, "Level 1", (189, 255,255))
    nadpis2=Text(WIDTH//2, HEIGHT//5, "PRVNÍ ÚTOK", (189, 255,255))
    cont=Text(WIDTH//2, 8*HEIGHT//10, "Mezerník pro spuštění", (189, 255,255))
    contsize=10
    contphase="RETROGRADE"
    gameover=0
    frames=0
    VLOCKY=[]
    for i in range(WIDTH//4):
        VLOCKY.append(vlocka(WIDTH, HEIGHT, 1))
    while 1:
        if gameover:
            with open("databtest.json") as db:
                mydb=json.load(db)
            mydb["1"]["finished"]="3"
            with open("databtest.json","w") as db:
                json.dump(mydb,db)
            return
        keys=pygame.key.get_pressed()
        dir=[0,0]
        gundir=2
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
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key==pygame.K_ESCAPE:
                    return "MENU"
                elif event.key==pygame.K_m:
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
        if keys[pygame.K_SPACE]:
            q=PLAYER.gun.fire(frames, PLAYER.x, PLAYER.y, screen, PLAYER.facing)
            if q!=0 and frames>60:
                BULLETS.append(q)
        screen.fill((0,0,0))
        if started:
            screen.fill((255,255,255))
        PLAYER.update(dir,[x,y,z,a])
        if not started:
            nadpis.render(screen, HEIGHT//20)
            nadpis2.render(screen, HEIGHT//10)
            cont.render(screen, HEIGHT//20+int(0.5*contsize))
            if contphase=="RETROGRADE":
                contsize-=0.2
                if contsize<=0:contphase="PROGRADE"
            else:
                contsize+=0.2
                if contsize>=10:contphase="RETROGRADE"
        else:
            PLAYER.render(screen, WIDTH, HEIGHT, frames)
            PLAYER.gun.render(screen,PLAYER.x,PLAYER.y,PLAYER.facing)
        for bullet in BULLETS:
            bullet.update()
            bullet.render(screen)
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