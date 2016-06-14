#fallingAnim.py
#BEAUTIFUL...
from pygame import *
screen=display.set_mode((1200,600))
falling=image.load("falling.png")
fallPic=transform.smoothscale(falling,(1200,2484))
def makeMove(name,start,end,typ):
    ''' This returns a list of pictures. They must be in the folder "name"
        and start with the name "name".
        start, end - The range of picture numbers 
    '''
    move = []
    for i in range(start,end+1):
        move.append(image.load("%s/%s%03d.%s" % (name,name,i,typ)))
    return move
pics=makeMove("hunts",34,43,"png")
frame=0
offset=0
selfdown=0
running=True
while running:
    for evnt in event.get():
        if evnt.type==QUIT:
            running=False
    screen.blit(fallPic,(0,offset))
    screen.blit(pics[frame%9],(600,selfdown))
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
        
            
quit()
