#current.py

"""
TO DO:

linear map changes: portals going down, transition key? gem quota? final map?
less awkwardness in enemy movements
automatic enemy movement and tracking...
SKELETON, MEDKIT, GEM!
might have to do special movement function set for skeleton
dream: vertical scroll if time...
"""

from pygame import *
from math import *
from random import *
from datetime import datetime

screen=display.set_mode((1000,600))

#---PICTURES---
back = image.load("level2.png")
backPic=transform.smoothscale(back,(3000,600))
mask = image.load("masklev2.png")
maskPic=transform.smoothscale(mask,(3000,600))
GREEN = (0,255,0)
sprites=[transform.smoothscale(image.load("me.png"),(40,40)),transform.smoothscale(image.load("me2.png"),(40,40))]
enePic=transform.smoothscale(image.load("enemy.png"),(60,60))
medPic=transform.smoothscale(image.load("object/medkit.png"),(20,20))
gem1Pic=transform.smoothscale(image.load("object/gem1.png"),(30,30))
torchPic=transform.smoothscale(image.load("object/torch.png"),(20,60))

#--------------
    
init()
text=font.SysFont("Courier",20)
torchRects=[]
for i in range(10):
    torchRects.append((i*30,50))

#--SPRITES!--#
def makeMove(name,start,end,typ): 
    #returns list of pics in folder "name" and starting with name, of the range start-end, and type ".typ"
    move = []
    for i in range(start,end+1):
        move.append(image.load("%s/%s%03d.%s" % (name,name,i,typ)))
    return move
"""
def drawScene(screen,self):
    offset= 250 - self.X
    screen.blit(backPic,(offset,0))
    pic = pics[move][int(frame)]
    screen.blit(pic,(250,self.rect[1]))

    display.flip()
"""
    
def getPixel(mask,x,y):
    if 0<= x < mask.get_width() and 0 <= y < mask.get_height():
        return mask.get_at((int(x),int(y)))[:3]
    else:
        return (-1,-1,-1)

def moveUp(self,vy):
    for i in range(vy):
        if getPixel(maskPic,self.X+15,self.rect[1]+2) != GREEN:
            self.rect[1] -= 1
        else:
            self.vy = 0

def moveDown(self,vy):
    
    for i in range(vy):
        if getPixel(maskPic,self.X+15,self.rect[1]+45) != GREEN:
            self.rect[1] += 1
        else:
            self.vy = 0
            self.step = True
            
def moveRight(self,vx):
    for i in range(vx):
        if getPixel(maskPic,self.X+28,self.rect[1]+15) != GREEN:
            self.X += 1
            self.X=min(self.X,3000)

def moveLeft(self,vx):
    for i in range(vx):
        if getPixel(maskPic,self.X+2,self.rect[1]+15) != GREEN:
            self.X -= 1
def climb(self):
    y = self.rect[1] + 27
    while y > self.rect[1]+17 and getPixel(maskPic,self.X,y) == GREEN:
        y-=1
    if y > self.rect[1]+17:
        self.rect[1] = y - 27

#--ENEMY SPECIFIC MOVEMENT--
def moveDownSkel(self,y):    
    for i in range(y):
        if getPixel(maskPic,self.X+15,self.rect[1]+45) != GREEN:
            self.rect[1] += 1
        #else:
            #self.vy = 0
            #self.step = True

RIGHT = 0 #indices of Player moves
LEFT = 1

#maybe change to independent lists 
pics = []
pics.append(makeMove("hunts",10,18,"png"))      #pictures of Player sprite moving right
pics.append(makeMove("hunts",142,150,"png"))    #pictures of Player sprite moving left
pics.append(makeMove("hunts",34,43,"png"))      #pictures of Player sprite falling
frame=0     #current frame within the move
move=0      #current move being performed


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
        self.X=0
        self.state=["RIGHT","WALK"]
        
    def move(self): #changes player position according to keyboard input
        global frame, move, RIGHT, LEFT
        keys=key.get_pressed()
        self.step=False
        newMove = -1
        self.vy+= 1         #add gravity to VY
        if self.vy < 0:
            moveUp(self,-self.vy)
        elif self.vy > 0:
            moveDown(self,self.vy)
        
        if keys[K_SPACE] and self.step:
            self.vy = -14    
        elif keys[K_RIGHT] and self.X < 3000:
            newMove = RIGHT
            moveRight(self,10)
            climb(self)
            
        elif keys[K_LEFT] and self.X > 0:
            newMove = LEFT
            moveLeft(self,10)
            climb(self)       

        else:
            frame = 0

        if move == newMove:     #0 is standing pose, so skips it when Player moves
            frame = frame +0.4 #speeds up switching through frames
            if frame >= len(pics[move]):
                frame = 1
        elif newMove != -1:     # a move was selected
            move = newMove      # make that our current move
            frame = 1
        """
        if keys[K_RIGHT]:
            self.X+=2
            self.X=min(self.X,screen.get_width())
            self.state[0]="RIGHT"

        if keys[K_LEFT]:
            self.X-=2
            self.X=max(0,self.X)
            self.state[0]="LEFT"

        if keys[K_UP] and self.step==True:
            self.vy=-15
            self.step=False

            
        if self.step==False:
            self.state[1]="JUMP"
        self.rect[1]+=self.vy
        #replace with scroll mask thingy later
        if self.rect[1]>500-self.rect[3]: 
            self.rect[1]=500-self.rect[3]
            self.step=True #on ground
            self.state[1]="WALK"
        self.vy+=1
        """
    def hit(self): #decreases player health
        self.health-=5
        self.health=min(100,self.health)
            
    def draw(self): #draws player on screen
        global frame, move
        pic = self.pics[move][int(frame)]
        if 500<=self.X<=2500:
            screen.blit(pic,(500,self.rect[1]))
        elif self.X<500:
            screen.blit(pic,(self.X,self.rect[1]))
        elif self.X>2500:
            screen.blit(pic,(self.X-2000,self.rect[1]))
       

#--ENEMIES--
class Skeleton: #enemy object
    "tracks start pos, current pos, speed"
    #do sprite for walking???
    def __init__(self,pic,x,y,targ,scroll): #takes in picture and position
        self.startX=x
        self.startY=y-pic.get_height()
        self.rect=Rect(self.startX,self.startY,pic.get_width(),pic.get_height()) #rect position
        self.speed=-2
        self.pic=pic
        self.state=["LEFT","WALK"]
        self.targ=targ
        self.scroll=scroll
        self.X=self.rect[0]
    def move(self,targ): #takes in target and moves towards it if target inside certain range, else moves within automated range
        """
        currentX=self.rect[0]
        if self.scroll==True:
            if 500<=targ.X<=2500:
                self.start=self.startX-targ.X
            else:
                self.start=self.startX
        else:
            self.start=self.startX

        #cannot move outside range of 100 left and right
        #automated movement->smoother, even as side scrolls
 
        if targ.X<self.start-100 or targ.X>self.start+100: #target not within moving range
            #automated movement within range
            if self.rect[0]<self.start-100: 
                self.speed*=-1
                self.state[0]="RIGHT"
            if self.rect[0]>self.start+100:
                self.speed*=-1
                self.state[0]="LEFT"
            self.rect[0]=int(self.rect[0]+self.speed)
        """
        #self.X=self.rect[0]
        if self.rect[0]<targ.X:
            moveRight(self,6)
            climb(self)
        elif self.rect[0]>targ.X:
            moveLeft(self,6)
            climb(self)
        self.X=self.rect[0]
        self.rect[0]=self.X
        moveDownSkel(self,10)
    def reset(self): #resets position to starting points
        self.rect[0]=self.startX
        
    def draw(self):
        if 500<=self.targ.X<=2500:
            screen.blit(self.pic,(self.rect[0]-(self.targ.X-500),self.rect[1]))
        elif self.targ.X<500:
            screen.blit(self.pic,(self.rect[0],self.rect[1]))
        elif self.targ.X>2500:
            screen.blit(self.pic,(self.rect[0]-2000,self.rect[1]))

class Bat:
    def __init__(self,area,scroll):
        self.area=area        
        self.rect=Rect(area[0],0,40,50)
        self.startX=self.rect[0]+50
        self.speed=-1
        self.frame=0
        self.scroll=scroll
        
    def move(self,targ):
        """
        if self.scroll==True:
            if 500<=targ.X<=2500:
                self.area[0]=self.startX-targ.X
            if not targ.rect.colliderect(self.area):
                self.rect[0]=self.startX-targ.X
        """
        targRect=Rect(targ.X,targ.rect[1],targ.rect[2],targ.rect[3])
        if targRect.colliderect(self.area):
            d=max(1,dist(self.rect[0],self.rect[1],targ.X,targ.rect[1])) #distance between self and target
            moveX=(targ.X-self.rect[0])*self.speed/d       
            self.rect[0]=int(self.rect[0]-moveX)
            self.rect[1]+=2
            
    def draw(self):
        pics=makeMove("batty",1,4,"jpg") #all frames of bat sprite
        self.frame+=0.2 #gradually adds to frame
        screen.blit(pics[int(self.frame)%4],(self.rect[0],self.rect[1])) #constantly rotates through pictures
            
#--FUNCTIONS!--
def dist(x1,x2,y1,y2): 
    return ((x1-x2)**2 + (y1-y2)**2)**0.5

def checkHit(me,enemy): #checks if hit over 1 second: will not lose health rapidly
    now=datetime.now()
       
#--OBJECTS!--    
class Torch:
    "tracks time since start, makes torchlight effect"
    def __init__(self):
        self.start=datetime.now()

    def torchCount(self): #returns count of  second intervals passed since start
        now=datetime.now()
        return (now.hour*3600+now.minute*60+now.second-(self.start.hour*3600+self.start.minute*60+self.start.second))
        #return floor(num)
   
    def torch(self,me): #takes pic with transparent circle, position and blits it so circle origin is at position
        #HAVE SEPARATE BACKGROUND FUNCTION MAN, NEED TO MAKE MAPS!!!
        dark=Surface((screen.get_width(),screen.get_height()))
        dark.set_alpha(100)
        dark.fill((0,0,0))
        if me.X<500:
            x=me.X
        elif 500<=me.X<=2500:
            x=500
        elif me.X>2500:
            x=me.X-2000
        x+=me.rect[2]//2
        y=me.rect[1]+me.rect[3]//2
        draw.circle(dark,(111,111,111),(int(x),int(y)),60)
        draw.circle(dark,(200,200,200),(int(x),int(y)),45)
        screen.blit(dark,(0,0))
        #replace with photoshop and transparent circle pic

class medKit:
    def __init__(self,pic,x,platY,scroll): #takes in pic, x pos, y pos, player
        self.worth=20
        self.startX=x
        self.rect=Rect(x,platY-pic.get_height(),pic.get_width(),pic.get_height())
        self.got=False #False if not collected yet
        self.pic=pic
        self.scroll=scroll
        
    def move(self,me): #moves position across screen if it is scrolling
        if self.scroll==True:
            if 500<=me.X<=2500:
                self.rect[0]=self.startX-(me.X-500)
        
    def gain(self,me):
        if self.got==False: #collides and not collected
            me.health+=self.worth
            me.health=min(200,me.health)
            self.got=True #True means has been collected
            print("HP")
    def draw(self): 
        #self.newx=self.x-char.rect[0]
        if self.got==False: #only draws if not collected
            screen.blit(self.pic,(self.rect[0],self.rect[1]))

class Gem:
    def __init__(self,pic,x,platY,scroll): #takes in pic, coordinates, player, and if scrolling
        self.startX=x
        self.rect=Rect(x,platY-pic.get_height(),pic.get_width(),pic.get_height())
        self.got=False #False if not collected yet
        self.pic=pic
        self.scroll=scroll
        
    def move(self,me): #changes position if scrolling
        if self.scroll==True:
            if 500<=me.X<=2500:
                self.rect[0]=self.startX-me.X
        
    def gain(self,char): #collected by player
        if self.got==False: #collides and not collected
            char.gems+=1
            self.got=True #True means has been collected
            
    def draw(self):
        if self.got==False: #only draws if not collected
            screen.blit(self.pic,(self.rect[0],self.rect[1]))

#--MAP--

def checkMap(curMap,MAPS,me): #which portal and map place to go to (change structure later)
    #one portal per map, cannot go back, keeps going down : much easier man
    bar=key.get_pressed()    
    for p in curMap.ports:
        if me.rect.colliderect(p) and bar[K_SPACE]:
            return (MAPS.index(curMap)+1)%2
    return MAPS.index(curMap)


class Map: #takes in background pic, enemies, other objects, portal, and tracks state of all
    def __init__(self,back,scroll,me,enemies,kits,gems,ports):
        self.pic=back
        self.scroll=scroll
        self.x=0
        self.me=me
        self.enemies=enemies
        self.kits=kits
        self.gems=gems
        self.ports=ports
        
    def backDraw(self): #draws itself back according to offset
        if self.scroll==True:
            if 500<=self.me.X<=2500: #scroll within this range
                self.x=-1*(self.me.X-500) #offset
                if self.x>0: #never blits right to black screen
                    self.x=0
                if self.x<-1*(self.pic.get_width()-screen.get_width()): #never blits left to black screen
                    self.x=-1*(self.pic.get_width()-screen.get_width())
                screen.blit(self.pic,(self.x,0))
            #stationary displays
            elif self.me.X<500: #not scroll while in this range
                screen.blit(self.pic,(0,0))
            elif self.me.X>2500: #not scroll while in this range
                screen.blit(self.pic,(-2000,0))
        else:
            screen.blit(self.pic,(0,0))
            
    def objectMove(self): #moves all objects of Map        
        #if the lists are not empty, moves objects
        if len(self.enemies)>0:
            for e in self.enemies:
                e.move(self.me)
                    
        if len(self.kits)>0:
            for k in self.kits:
                #if self.scroll==True:
                k.move(self.me)
                    
        if len(self.gems)>0:
            for g in self.gems:
                #if self.scroll==True:
                g.move(self.me) #moves kits on screen and in rects

    def objectDraw(self):
        #if lists not empty, draws objects
        if len(self.enemies)>0:
            for e in self.enemies:
                e.draw()
        if len(self.kits)>0:
            for k in self.kits:
                k.draw()
                    
        if len(self.gems)>0:
            for g in self.gems:
                 g.draw()
                 
    def objectCollide(self): #checks collisions between objects
        meRect=Rect(self.me.X,self.me.rect[1],self.me.rect[2],self.me.rect[3]) #actual rect position of Player, not blitted position
        #if lists not empty, checks collide between rects
        if len(self.kits)>0:
            for k in self.kits:
                if meRect.colliderect(k.rect): #checks if rects collide
                    k.gain(self.me)
                    
        if len(self.gems)>0:
            for g in self.gems:
                if meRect.colliderect(g.rect): #checks if rects collide
                    g.gain(self.me)
                    
        if len(self.enemies)>0:
            for e in self.enemies:
                if meRect.colliderect(e.rect): #checks if collide with enemy rect
                    self.me.hit() #decreases player health





#--ENDS GAME!--
def gameEnd(me,torch): #ends game loop if no health, torch runs out, or completed last map
    if me.health==0 or torch.torchCount()/10>10: 
        return True
    return False
   
#--MENU!--

def story(pics): #actual game loop
    me=Player(pics)
    #KEEP INFO IN SEPARATE TEXT FILES LATER-LESS CLUTTER
    enemy=[[Skeleton(enePic,randint(400,1000),500,me,True),Bat(Rect(300,0,1000,600),True)],[Skeleton(enePic,1000,500,me,False)]]
    t=Torch()
    kits=[[medKit(medPic,i,500,True) for i in range(400,601,100)],[medKit(medPic,600,500,False)]] #all medkits
    gems=[[Gem(gem1Pic,900,500,True)],[Gem(gem1Pic,800,500,False)]] #all gems
    ports=[[Rect(0,460,40,40)],[Rect(560,460,40,40)]]
    back1=Surface((backPic.get_width(),backPic.get_height()))
    #mask1=Surface((maskPic.get_width(),maskPic.get_height()))
    for i in range(1):
        back1.blit(backPic,(i*backPic.get_width(),0))

    MAPS=[Map(maskPic,True,me,enemy[0],kits[0],gems[0],ports[0],)] #out of file lists pls
    mapNUM=0
    MAP=MAPS[mapNUM]
    hbar=(560,50,me.health,20)
    backh=hbar #full healthbar outline
    myClock=time.Clock()
    running=True    
    while running:
        for e in event.get():
            if e.type==QUIT:
                running=False
                
        if key.get_pressed()[27]: running=False
        
        #---MAP CHANGE--
        #MAP=MAPS[checkMap(MAP,MAPS,me)]
        
        #---MOVES OBJECTS, CHECKS COLLIDE---
        me.move()
        MAP.objectMove()
        MAP.objectCollide()

        #-----------------------------------
            
        hbar=(560,50,me.health,20)                
        
        #---DRAWS ON SCREEN---
        MAP.backDraw()
        me.draw()
        MAP.objectDraw()
        t.torch(me)
        
        for i in range(10-t.torchCount()//10):
            screen.blit(torchPic,torchRects[i])
            
        draw.rect(screen,(255,255,255),backh,6)
        draw.rect(screen,(255,0,0),hbar)
        screen.blit((text.render(str(10-t.torchCount()%10),True,(255,255,255))),(740,80)) #displays count down in seconds to when a torch is used up
        screen.blit((text.render(str(me.gems)+"/10",True,(255,255,255))),(735,100)) #displays number of gems collected
        display.flip()
        
        #---------------------
        
        #---CHECKS FOR ENDING GAME---
        if gameEnd(me,t)==True:
            screen.fill((0,0,0))
            screen.blit((text.render("GAME OVER",True,(255,255,255))),(360,280))
            display.flip()
            time.wait(1000)
            quit()
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

def mfSelect(): #player can select gender for sprite after start on menu, before actual game loop
    global text
    running=True
    buttons=[Rect(screen.get_width()//5*i,200,120,50) for i in range(1,4,2)]
    labels=["FEMALE","MALE"]

    while running:
        for e in event.get():
            if e.type==QUIT:
                break
        screen.fill((0,0,0))
        pos=mouse.get_pos()
        mb=mouse.get_pressed()
        for b,l in zip(buttons,labels):
            draw.rect(screen,(255,255,255),b,2)
            if b.collidepoint(pos):
                draw.rect(screen,(255,0,0),b,2)
                if mb[0]==1:
                    return labels.index(l)
        screen.blit(text.render(labels[0],True,(255,255,255)),(buttons[0][0],buttons[0][1]))
        screen.blit(text.render(labels[1],True,(255,255,255)),(buttons[1][0],buttons[1][1]))
        display.flip()

#--PAGE LOOP!--
running = True
OUTLINE = (150,50,30)
page = "menu"
while page != "exit":
    if page == "menu":
        page = menu()
    if page == "story":
        time.wait(100)
        #me=sprites[mfSelect()]
        page = story(pics)
    if page == "instructions":
        page = instructions()        
    if page == "credits":
        page = credit()    
    
quit()
