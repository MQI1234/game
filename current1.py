#current.py

"""
TO DO:

linear map changes: portals going down, transition key? gem quota? final map?
less awkwardness in enemy movements
automatic enemy movement and tracking...
torchtime fixing
photoshop torcheffect man
might have to do special movement function set for skeleton
dream: vertical scroll if time...
"""

from pygame import *
from math import *
from random import *
from datetime import datetime

screen=display.set_mode((1000,600))

#---PICTURES---
shadow=image.load("black.png")
falling=image.load("falling.png")
fallPic=transform.smoothscale(falling,(1000,2484))
back = image.load("level2.png")
backPic=transform.smoothscale(back,(3000,600))
mask = image.load("masklev2.png")
maskPic=transform.smoothscale(mask,(3000,600))
back2 = image.load("level3.jpg")
backPic2=transform.smoothscale(back2,(3000,600))
mask2 = image.load("masklev3.png")
maskPic2=transform.smoothscale(mask2,(3000,600))
GREEN = (0,255,0)
#sprites=[transform.smoothscale(image.load("me.png"),(40,40)),transform.smoothscale(image.load("me2.png"),(40,40))]
enePic=transform.smoothscale(image.load("enemy.png"),(60,60))
medPic=transform.smoothscale(image.load("object/medkit.png"),(20,20))
gem1Pic=transform.smoothscale(image.load("object/gem1.png"),(50,30))
torchPic=transform.smoothscale(image.load("object/ticon.png"),(50,50))
iciclePic=image.load("object/icicle.png")

#--------------
    
init()
text=font.SysFont("Courier",20)
torchPos=[]
torchPics=[]
for i in range(10):
    torchPos.append((i*50,50))
    torchPics.append(shadow)

#--SPRITES!--#
def makeMove(name,start,end,typ): 
    #returns list of pics in folder "name" and starting with name, of the range start-end, and type ".typ"
    move = []
    for i in range(start,end+1):
        move.append(image.load("%s/%s%03d.%s" % (name,name,i,typ)))
    return move
    
def getPixel(mask,x,y):
    if 0<= x < mask.get_width() and 0 <= y < mask.get_height():
        return mask.get_at((int(x),int(y)))[:3]
    else:
        return (-1,-1,-1)
MAP=0 #so program doesn't crash
def moveUp(self,mask,vy):
    for i in range(vy):
        if getPixel(mask,self.rect[0]+15,self.rect[1]+2) != GREEN:
            self.rect[1] -= 1
        else:
            self.vy = 0

def moveDown(self,mask,vy):
    for i in range(vy):
        if getPixel(mask,self.rect[0]+15,self.rect[1]+45) != GREEN:
            self.rect[1] += 1
        else:
            self.vy = 0
            self.step = True
            
def moveRight(self,mask,vx):
    for i in range(vx):
        if getPixel(mask,self.rect[0]+28,self.rect[1]+15) != GREEN:
            self.rect[0] += 1
            #self.rect[0]=min(self.rect[0],3000)

def moveLeft(self,mask,vx):
    for i in range(vx):
        if getPixel(mask,self.rect[0]+2,self.rect[1]+15) != GREEN:
            self.rect[0] -= 1
def climb(self,mask):
    y = self.rect[1] + 27
    while y > self.rect[1]+17 and getPixel(mask,self.rect[0],y) == GREEN:
        y-=1
    if y > self.rect[1]+17:
        self.rect[1] = y - 27

#--ENEMY SPECIFIC MOVEMENT--
def moveDownSkel(self,mask,y):
    for i in range(y):
        if getPixel(mask,self.rect[0]+15,self.rect[1]+45) != GREEN:
            self.rect[1] += 1
            
#--LIST/INDICES OF FRAMES FOR SPRITES--
RIGHT=0 
LEFT=1
CLIMB=2
mepics=[]
mepics.append(makeMove("hunts",10,18,"png"))      #pictures of Player sprite moving right
mepics.append(makeMove("hunts",142,150,"png"))    #pictures of Player sprite moving left
mepics.append(makeMove("hunts",68,73,"png"))
meframe=0     #current frame within the move
memove=0      #current move being performed
skelpics=[]
skelpics.append(makeMove("skel",1,6,"png"))
skelpics.append(makeMove("skel",7,12,"png"))
sframe=0
smove=0

#--PLAYER--
class Player: #player object
    "tracks current position, velocity, platform, and health"
    def __init__(self,pics): #takes in picture
        self.pics=pics
        self.vy=0
        self.step=True
        self.health=200
        self.gems=0
        self.rect=Rect(0,400,40,50)
        self.state=["RIGHT","WALK"]
        
    def move(self): #changes player position according to keyboard input
        global meframe, memove, RIGHT, LEFT, CLIMB, MAP
        keys=key.get_pressed()
        self.step=False
        newMove = -1
        self.vy+= 1         #add gravity to VY
        if self.vy < 0:
            if MAP!=0:
                moveUp(self,MAP.mask,-self.vy)
        elif self.vy > 0:
            if MAP!=0:
                moveDown(self,MAP.mask,self.vy)            
        if keys[K_SPACE] and self.step:
            self.vy = -14    
        elif keys[K_RIGHT] and self.rect[0] < 3000:
            newMove = RIGHT
            if MAP!=0:
                moveRight(self,MAP.mask,10)
                climb(self,MAP.mask)                
        elif keys[K_LEFT] and self.rect[0] > 0:
            newMove = LEFT
            if MAP!=0:
                moveLeft(self,MAP.mask,10)
                climb(self,MAP.mask)
        elif keys[K_UP]:
            newMove=CLIMB
            self.rect[0]+=4
        else: #no keyboard input; player is standing still
            meframe = 0

        if memove == newMove:     #0 is standing pose, so skips it when Player moves
            meframe+=0.4 #speeds up switching through frames
            if meframe >= len(self.pics[memove]):
                meframe = 1
        elif newMove != -1:     # a move was selected
            memove = newMove      # make that our current move
            meframe = 1
    
    def hit(self): #decreases player health
        self.health-=5
        self.health=min(100,self.health)
        
    def reset(self):
        self.rect[0]=0
        self.rect[1]=0
        self.gems=0
    def draw(self): #draws player on screen
        global meframe, memove
        pic = self.pics[memove][int(meframe)]
        if 500<=self.rect[0]<=2500:
            screen.blit(pic,(500,self.rect[1]))
        elif self.rect[0]<500:
            screen.blit(pic,(self.rect[0],self.rect[1]))
        elif self.rect[0]>2500:
            screen.blit(pic,(self.rect[0]-2000,self.rect[1]))
       

#--ENEMIES--
class Skeleton: #enemy object
    "tracks start pos, current pos, speed"
    #do sprite for walking???
    def __init__(self,pics,x,y,targ,scroll): #takes in picture and position
        self.rect=Rect(x,y,25,50) #rect position
        self.speed=-2
        self.pics=pics
        self.hit=0
        self.targ=targ
        self.scroll=scroll
        
    def move(self,targ): #takes in target and moves towards it if target inside certain range, else moves within automated range
        global sframe, smove, RIGHT, LEFT, MAP
        newMove=-1
        if self.rect[0]<targ.rect[0]: #player is right of self
            if MAP!=0:
                moveRight(self,MAP.mask,1)
                climb(self,MAP.mask)
                newMove=RIGHT
                
        elif self.rect[0]>targ.rect[0]: #player is left of self
            if MAP!=0:
                moveLeft(self,MAP.mask,1)
                climb(self,MAP.mask)
                newMove=LEFT
        else: #player is above or below self
            sframe=0

        if smove == newMove:     
            sframe=sframe+0.4 #speeds up switching through frames
        if sframe >= len(self.pics[smove]):
            sframe = 1
        if newMove != -1:    
            smove = newMove      
            sframe = 1
 
            
        if MAP!=0:
            moveDownSkel(self,MAP.mask,5)
        
    def draw(self):
        pic = self.pics[smove][int(sframe)]
        if 500<=self.targ.rect[0]<=2500:
            screen.blit(pic,(self.rect[0]-(self.targ.rect[0]-500),self.rect[1]))
        elif self.targ.rect[0]<500:
            screen.blit(pic,(self.rect[0],self.rect[1]))
        elif self.targ.rect[0]>2500:
            screen.blit(pic,(self.rect[0]-2000,self.rect[1]))

class Bat:
    def __init__(self,area,targ,scroll):
        self.area=area        
        self.rect=Rect(area[0],0,40,50)
        self.speed=-1
        self.frame=0
        self.scroll=scroll
        self.targ=targ
        self.hit=0
        
    def move(self,targ):
        targRect=Rect(targ.rect[0],targ.rect[1],targ.rect[2],targ.rect[3])
        if targRect.colliderect(self.area):
            d=max(1,dist(self.rect[0],self.rect[1],targ.rect[0],targ.rect[1])) #distance between self and target
            moveX=(targ.rect[0]-self.rect[0])*self.speed/d       
            self.rect[0]=int(self.rect[0]-moveX)
            self.rect[1]+=2     
           
    def draw(self):
        pics=makeMove("batty",1,4,"jpg") #all frames of bat sprite
        self.frame+=0.2 #gradually adds to frame
        #screen.blit(pics[int(self.frame)%4],(self.rect[0],self.rect[1])) #constantly rotates through pictures
        if 500<=self.targ.rect[0]<=2500:
            screen.blit(pics[int(self.frame)%4],(self.rect[0]-(self.targ.rect[0]-500),self.rect[1]))
        elif self.targ.rect[0]<500:
            screen.blit(pics[int(self.frame)%4],(self.rect[0],self.rect[1]))
        elif self.targ.rect[0]>2500:
            screen.blit(pics[int(self.frame)%4],(self.rect[0]-2000,self.rect[1]))

class Icicle:
    def __init__(self,area,targ,scroll):
        self.area=area        
        self.rect=Rect(area[0],0,40,50)
        self.speed=-1
        self.scroll=scroll
        self.targ=targ
        self.hit=0
        self.count=0
        
    def move(self,targ):
        targRect=Rect(targ.rect[0],targ.rect[1],targ.rect[2],targ.rect[3])
        if targRect.colliderect(self.area):
            self.count+=1
        if self.count>=1:
            self.rect[1]+=4      
           
    def draw(self):
        if 500<=self.targ.rect[0]<=2500:
            screen.blit(iciclePic,(self.rect[0]-(self.targ.rect[0]-500),self.rect[1]))
        elif self.targ.rect[0]<500:
            screen.blit(iciclePic,(self.rect[0],self.rect[1]))
        elif self.targ.rect[0]>2500:
                screen.blit(iciclePic,(self.rect[0]-2000,self.rect[1]))
            
#--FUNCTIONS!--
def dist(x1,x2,y1,y2): 
    return ((x1-x2)**2 + (y1-y2)**2)**0.5
     
#--OBJECTS!--
'have to do torch taking into account time spent when transitioning'
class Torch: 
    "tracks time since start, makes torchlight effect"
    def __init__(self,pic):
        self.start=datetime.now()
        self.pic=pic
    def torchCount(self): #returns count of seconds passed since start
        now=datetime.now()
        return (now.hour*3600+now.minute*60+now.second-(self.start.hour*3600+self.start.minute*60+self.start.second))
   
    def torchLight(self,me): #takes pic with transparent circle, player and blits it so circle origin is at player centre
        if me.rect[0]<500:
            x=me.rect[0]
        elif 500<=me.rect[0]<=2500:
            x=500
        elif me.rect[0]>2500:
            x=me.rect[0]-2000
        x+=me.rect[2]//2
        y=me.rect[1]+me.rect[3]//2
        screen.blit(self.pic,(x-1500,y-1000))
        
class medKit:
    def __init__(self,pic,x,platY,scroll): #takes in pic, x pos, y pos, player
        self.worth=20
        self.startX=x
        self.rect=Rect(x,platY-pic.get_height(),pic.get_width(),pic.get_height())
        self.got=False #False if not collected yet
        self.pic=pic
        self.scroll=scroll
   
    def gain(self,me):
        if self.got==False: #collides and not collected
            me.health+=self.worth
            me.health=min(200,me.health)
            self.got=True #True means has been collected

    def draw(self,me): 
        if self.got==False: #only draws if not collected
            if 500<=me.rect[0]<=2500:
                screen.blit(self.pic,(self.rect[0]-(me.rect[0]-500),self.rect[1]))
            elif me.rect[0]<500:
                screen.blit(self.pic,(self.rect[0],self.rect[1]))
            elif me.rect[0]>2500:
                screen.blit(self.pic,(self.rect[0]-2000,self.rect[1]))



class Gem:
    def __init__(self,pic,x,y,scroll): #takes in pic, coordinates, player, and if scrolling
        self.rect=Rect(x,y-pic.get_height(),pic.get_width(),pic.get_height())
        self.got=False #False if not collected yet
        self.pic=pic
        self.scroll=scroll
   
    def gain(self,me): #collected by player
        if self.got==False: #collides and not collected
            me.gems+=1
            self.got=True #True means has been collected
            
    def draw(self,me):
        if self.got==False: #only draws if not collected
            if 500<=me.rect[0]<=2500:
                screen.blit(self.pic,(self.rect[0]-(me.rect[0]-500),self.rect[1]))
            elif me.rect[0]<500:
                screen.blit(self.pic,(self.rect[0],self.rect[1]))
            elif me.rect[0]>2500:
                screen.blit(self.pic,(self.rect[0]-2000,self.rect[1]))

#--MAP--
totgems=0 #total number of gems collected during game
def changeMap(curMap,MAPS,me): #takes in map, list of maps, and player object
    global totgems
    #checks if player falls in gap in mask, and changes to next map
    if me.rect[1]>600: #player below mask level
        fallDown(me) #plays falling animation
        me.reset() #resets player position and gem count
        if MAPS.index(curMap)==len(MAPS)-1: #map is final map
            endGame(totgems)
        else:
            return MAPS[MAPS.index(curMap)+1] #returns next map
    return curMap


def fallDown(me): #animation of falling down hole
    global totgems
    totgems+=me.gems
    falls=makeMove("hunts",34,44,"png")
    frame=0
    offset=0
    selfdown=0
    running=True
    while running:
        for evnt in event.get():
            if evnt.type==QUIT:
                running=False
        screen.blit(fallPic,(0,offset))
        screen.blit(falls[frame%9],(500,selfdown))
        screen.blit(shadow,(-975,selfdown-980))
        screen.blit(screen.copy(),(0,0))
        frame+=1
        offset-=50
        if offset<-1850:
            offset=-1850
            selfdown+=30
            if selfdown==600:
                running=False
        time.wait(100)
        display.flip()
            

class Map: #takes in background pic, enemies, other objects, portal, and tracks state of all
    def __init__(self,back,mask,scroll,me,enemies,kits,gems):
        self.pic=back
        self.scroll=scroll
        self.offset=0
        self.me=me
        self.enemies=enemies
        self.kits=kits
        self.gems=gems
        self.mask=mask
        self.gemCount=len(gems)
    def backDraw(self): #draws itself back according to offset
        if self.scroll==True:
            if 500<=self.me.rect[0]<=2500: #scroll within this range
                self.offset=-1*(self.me.rect[0]-500) #offset
                if self.offset>0: #never blits right to black screen
                    self.offset=0
                if self.offset<-1*(self.pic.get_width()-screen.get_width()): #never blits left to black screen
                    self.offset=-1*(self.pic.get_width()-screen.get_width())
                screen.blit(self.pic,(self.offset,0))
            #stationary displays
            elif self.me.rect[0]<500: #not scroll while in this range
                screen.blit(self.pic,(0,0))
            elif self.me.rect[0]>2500: #not scroll while in this range
                screen.blit(self.pic,(-2000,0))
        else:
            screen.blit(self.pic,(0,0))
            
    def objectMove(self): #moves all objects of Map        
        #if the lists are not empty, moves objects
        if len(self.enemies)>0:
            for e in self.enemies:
                e.move(self.me)
        
    def objectCollide(self): #checks collisions between objects       
        #if lists not empty, checks collide between rects
        if len(self.kits)>0:
            for k in self.kits:
                if self.me.rect.colliderect(k.rect): #checks if rects collide
                    k.gain(self.me)
                    
        if len(self.gems)>0:
            for g in self.gems:
                if self.me.rect.colliderect(g.rect): #checks if rects collide
                    g.gain(self.me)
                    
        if len(self.enemies)>0:
            for e in self.enemies:
                if self.me.rect.colliderect(e.rect): #checks if collide with enemy rect
                    self.me.hit() #decreases player health
                    
    def objectDraw(self):
        #if lists not empty, draws objects
        if len(self.enemies)>0:
            for e in self.enemies:
                e.draw()
        if len(self.kits)>0:
            for k in self.kits:
                k.draw(self.me)                        
        if len(self.gems)>0:
            for g in self.gems:
                g.draw(self.me)


#--ENDS GAME!--
def gameEnd(me,torch): #ends game loop if no health, torch runs out, or completed last map
    if me.health==0 or torch.torchCount()/10>=10: 
        return True
    return False

def endGame(gems): #final screen
    screen.fill((0,0,0))
    screen.blit((text.render("YOU GOT:"+str(gems)+"/7",True,(255,255,255))),(360,280))
    display.flip()
    time.wait(2000)
    quit()
    
#--MENU!--

def story(pics): #actual game loop
    global MAP, gems
    me=Player(mepics)
    #KEEP INFO IN SEPARATE TEXT FILES LATER-LESS CLUTTER
    enemy=[[Skeleton(skelpics,randint(400,1000),400,me,True),Bat(Rect(300,0,1000,600),me,True),Icicle(Rect(400,0,1000,600),me,True)],[Skeleton(skelpics,1000,500,me,True)]]    
    kits=[[medKit(medPic,i,500,True) for i in range(400,601,100)],[medKit(medPic,600,500,True)]] #all medkits
    gems=[[Gem(gem1Pic,900,500,True),Gem(gem1Pic,1200,500,True),Gem(gem1Pic,2000,500,True)],[Gem(gem1Pic,800,500,True),Gem(gem1Pic,1500,500,True),Gem(gem1Pic,2200,500,True)]] #all gems

    MAPS=[Map(backPic,maskPic,True,me,enemy[0],kits[0],gems[0]),Map(backPic2,maskPic2,True,me,enemy[1],kits[1],gems[1])] #out of file lists pls
    MAP=MAPS[0]
    t=Torch(torchPics[0])
    hbar=(560,50,me.health,20)
    backh=hbar #full healthbar outline
    myClock=time.Clock()
    oTime=datetime.now()
    running=True    
    while running:
        for e in event.get():
            if e.type==QUIT:
                running=False
                
        if key.get_pressed()[27]: running=False
        nTime=datetime.now()
        
        #---MAP CHANGE--
        #if MAP!=changeMap(MAP,MAPS,me):
            #t=Torch(torchPics[MAPS.index(MAP)])
        MAP=changeMap(MAP,MAPS,me)

        
        #---MOVES OBJECTS, CHECKS COLLIDE---
        me.move()
        MAP.objectMove()
        if (nTime.hour*3600+nTime.minute*60+nTime.second-(oTime.hour*3600+oTime.minute*60+oTime.second))==1:
            MAP.objectCollide()
            oTime=nTime

        #-----------------------------------
            
        hbar=(560,50,me.health,20)                
        
        #---DRAWS ON SCREEN---
        MAP.backDraw()
        me.draw()
        MAP.objectDraw()
        t.torchLight(me)
        
        for i in range(10-t.torchCount()//10): #number of torches left out of ten
            screen.blit(torchPic,torchPos[i]) 
            
        draw.rect(screen,(255,255,255),backh,6)
        draw.rect(screen,(255,0,0),hbar)
        screen.blit((text.render(str(10-t.torchCount()%10),True,(255,255,255))),(740,80)) #displays count down in seconds to when a torch is used up
        screen.blit((text.render(str(me.gems)+"/"+str(MAP.gemCount),True,(255,255,255))),(735,100)) #displays number of gems collected
        display.flip()
        
        #---------------------
        
        #---CHECKS FOR ENDING GAME---
        if gameEnd(me,t)==True:
            screen.fill((0,0,0))
            screen.blit((text.render("GAME OVER",True,(255,255,255))),(360,280))
            display.flip()
            time.wait(1000)
            endGame(gems)
        #---------------------
        myClock.tick(60)
        
    return "menu"    
    
def instructions(): #instructions page
    running = True
    inst = image.load("instructions.jpg").convert()
    inst = transform.smoothscale(inst, screen.get_size())
    screen.blit(inst,(0,0))
    while running:
        for evnt in event.get():          
            if evnt.type == QUIT:
                running = False
        if key.get_pressed()[27]: running = False

        display.flip()
    return "menu"
        
def credit(): #credit page
    running = True
    cred = image.load("credits.jpg").convert()
    cred = transform.smoothscale(cred, screen.get_size())
    screen.blit(cred,(0,0))
    while running:
        for evnt in event.get():          
            if evnt.type == QUIT:
                running = False
        if key.get_pressed()[27]: running = False

        display.flip()
    return "menu"
       

def menu(): #main menu, holds and leads to screens
    global text
    running = True
    myClock = time.Clock()
    menuimg = image.load("menucave.jpg").convert()
    menuimg= transform.smoothscale(menuimg, screen.get_size())
    buttons = [Rect(200,y*60+200,150,40) for y in range(3)]
    vals = ["story","instructions","credits"]
    nlabel1=text.render("Start", 1, (0, 0, 0,))
    nlabel2=text.render("Instructions", 1, (0, 0, 0,))
    nlabel3=text.render("Credits", 1, (0, 0, 0,))
    while running:
        for evnt in event.get():          
            if evnt.type == QUIT:
                return "exit"

        mpos = mouse.get_pos()
        mb = mouse.get_pressed()
        
        screen.blit(menuimg,(0,0))
        for r,v in zip(buttons,vals):
            draw.rect(screen,(222,55,55),r)
            if r.collidepoint(mpos):
                draw.rect(screen,(0,255,0),r,2)
                if mb[0]==1:
                    return v
            else:
                draw.rect(screen,(255,255,0),r,2)
        screen.blit(nlabel1,(250,210))
        screen.blit(nlabel2,(205,270))
        screen.blit(nlabel3,(235,330))
                
        display.flip()

#--PAGE LOOP!--
running = True
OUTLINE = (150,50,30)
page = "menu"
while page != "exit":
    if page == "menu":
        page = menu()
    if page == "story":
        time.wait(50)
        page = story(mepics)
    if page == "instructions":
        page = instructions()        
    if page == "credits":
        page = credit()    
    
quit()
