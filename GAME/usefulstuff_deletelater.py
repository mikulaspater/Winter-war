def generic():
    global screen, WIDTH, HEIGHT, MWIDTH, MHEIGHT,fullscreen,VOLUME
    pygame.mixer.music.load("music.mp3")
    pygame.mixer.music.play(-1,0.0)
    while 1:
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key==pygame.K_p:
                    if fullscreen:
                        pygame.mouse.set_visible(1)
                        HEIGHT,WIDTH=HEIGHT//2, WIDTH//2
                        screen=pygame.display.set_mode((WIDTH,HEIGHT))
                        fullscreen=0
                        #přidat aktualizaci velikostí mačítek a textu
                    else:
                        pygame.mouse.set_visible(0)
                        HEIGHT,WIDTH=HEIGHT*2, WIDTH*2
                        screen=pygame.display.set_mode((0,0),pygame.FULLSCREEN)
                        fullscreen=1
                elif event.key==pygame.K_m:
                    pygame.mixer.music.set_volume([0,100][VOLUME==0])
                    VOLUME=[0,100][VOLUME==0]
                else:
                    print(event.key)
            elif event.type==pygame.MOUSEBUTTONDOWN:
                print(pygame.mouse.get_pos())
        screen.fill((0,0,0))
        #stuff
        pygame.display.update()
def level1():
    global screen, WIDTH, HEIGHT, MWIDTH, MHEIGHT,fullscreen,VOLUME
    nadpis=Text(WIDTH//2, HEIGHT//20, "LEVEL 1 cutscéna 1", (255,208,0))#smazat
    FINISHED=0
    frames=0
    VLOCKY=[]
    for i in range(WIDTH//4):
        VLOCKY.append(vlocka(WIDTH, HEIGHT, 1))
    while 1:
        if FINISHED:
            with open("database.json") as db:
                mydb=json.load(db)
            mydb["1"]["finished"]="3"
            with open("database.json","w") as db:
                json.dump(mydb,db)
            return
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key==pygame.K_ESCAPE:
                    return "MENU"
                elif event.key==pygame.K_p:
                    if fullscreen:
                        pygame.mouse.set_visible(1)
                        HEIGHT,WIDTH=HEIGHT//2, WIDTH//2
                        screen=pygame.display.set_mode((WIDTH,HEIGHT))
                        fullscreen=0
                        for i in range(len(VLOCKY)//2):
                            del(VLOCKY[0])
                    else:
                        pygame.mouse.set_visible(0)
                        HEIGHT,WIDTH=HEIGHT*2, WIDTH*2
                        screen=pygame.display.set_mode((0,0),pygame.FULLSCREEN)
                        fullscreen=1
                        for i in range(len(VLOCKY)):
                            VLOCKY.append(vlocka(WIDTH, HEIGHT, 1))
                elif event.key==pygame.K_m:
                    pygame.mixer.music.set_volume([0,100][VOLUME==0])
                    VOLUME=[0,100][VOLUME==0]
        screen.fill((0,0,0))
        nadpis.render(screen, HEIGHT//10)
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
class Gun:
    def __init__(self, firerate, maxspread, texturename, firespeed,angle,WIDTH, HEIGHT,twidth,theight):
        self.firerate=firerate
        self.maxspread=maxspread
        self.texturel=pygame.transform.scale(pygame.image.load(texturename+"l.png").convert_alpha(),(int(32*(WIDTH/1920)), int(32*(HEIGHT/1080))))
        self.texturer=pygame.transform.scale(pygame.image.load(texturename+"r.png").convert_alpha(),(int(32*(WIDTH/1920)), int(32*(HEIGHT/1080))))
        self.firespeed=firespeed
        self.angle=angle
        self.lastfire=-firerate
    def render(self,screen,px,py,facing):
        if facing:
            rotimg=pygame.transform.rotate(self.texturer, self.angle)
        elif facing=="l":
            rotimg=pygame.transform.rotate(self.texturel, self.angle)
        rect=rotimg.get_rect(center=self.texture.get_rect(center=(px,py)).center)
        screen.blit(rotimg, rect)
    def fire(self,frames,px,py):
        if frames-self.lastfire<self.firerate:return 0
        #krejzy matika wubbalubbadubdub
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
        print(angle, vx, vy, vx**2+vy**2)
        self.lastfire=frames
        return Bullet(px, py, vx, vy)
class Bullet:
    def __init__(self,x,y,vx,vy):
        self.x=x
        self.y=y
        self.vx=vx
        self.vy=vy
    def update(self):
        self.x+=self.vx
        self.y+=self.vy
    def render(self, screen):
        screen.set_at((int(self.x), int(self.y)),(255,0,0))

"""
Salvadorci vypotřebovali veškerou munici za 15min xDDD

"""