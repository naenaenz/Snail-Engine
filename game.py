import math
import copy
import pygame
from pygame.locals import (
    K_UP,
    K_DOWN,
    K_LEFT,
    K_RIGHT,
    K_ESCAPE,
    K_q,
    K_e,
    KEYDOWN,
    QUIT
)

#Initialise objects list
objects = []

#Returns the list index of an object given its id
def getObject(id):
    for objectid in range(len(objects)):
        if objects[objectid].id == id:
            return objectid
    return -1

#Basic object class
class gameObject():
    def __init__(self,id,rotation,scale,offset,parent="world"):
        self.id = id
        self.rotation = rotation
        self.scale = scale
        self.parent = parent
        self.offset = offset
    def getPos(self):
        if(self.parent == "world"):
            return [*self.offset]
        else:
            parentid = getObject(self.parent)
            if parentid == -1:
                self.parent = "world"
                return [*self.offset]
            else:
                parentPos=objects[parentid].getPos()
                return [self.offset[0]+parentPos[0],self.offset[1]+parentPos[1]]
    def getScale(self):
        if(self.parent == "world"):
            return [*self.scale]
        else:
            parentid = getObject(self.parent)
            if parentid == -1:
                self.parent = "world"
                return [*self.scale]
            else:
                parentScale=objects[parentid].getScale()
                return [self.scale[0]*parentScale[0],self.scale[1]*parentScale[1]]
    def getRot(self):
        if(self.parent == "world"):
            return self.rotation
        else:
            parentid = getObject(self.parent)
            if parentid == -1:
                self.parent = "world"
                return self.rotation
            else:
                parentRot=objects[parentid].getRot()
                return self.rotation+parentRot

#Sprite object class
class spriteObject(gameObject):
    def __init__(self,id,rotation,scale,offset,sprite,parent="world"):
        super().__init__(id,rotation,scale,offset,parent)
        self.sprite = sprite
    def render(self):
        pos = self.getPos()
        print(pos, self.getPos(), self.offset)
        sprite = self.sprite
        #scale
        scale = self.getScale()
        pos[0]*=scale[0]
        pos[1]*=scale[1]
        sprite = pygame.transform.scale(sprite,(math.floor(self.sprite.get_width()*scale[0]),math.floor(self.sprite.get_height()*scale[1])))
        #rotate
        parentRot = objects[getObject(self.parent)].getRot()
        rotation = self.getRot()
        tempPos = [*pos]
        #tempPos=[100,100]
        print(pos, self.getPos(), self.offset)
        pos[0] = math.cos(parentRot)*tempPos[0]+math.sin(parentRot)*tempPos[1]
        pos[1] = math.cos(parentRot)*tempPos[1]+math.sin(parentRot)*tempPos[0]
        pygame.transform.rotate(sprite,rotation).convert_alpha()
        print(pos, self.getPos(), self.offset)
        screen.blit(sprite,(pos[0]-sprite.get_width()/2,screen.get_height()-pos[1]-sprite.get_height()/2))

#Renders all objects
def render():
    screen.fill((255,0,0))
    for object in objects:
        if isinstance(object,spriteObject):
            object.render()
    pygame.display.flip()

#Iterates through the event keys and returns which ones were pressed
def handleEvents(keys):
    events = [False for i in keys]
    for event in pygame.event.get():
        #Did the user hit a key?
        if event.type == KEYDOWN:
            #Was it the Escape key? If so, quit.
            if event.key == K_ESCAPE:
                pygame.quit()
            for keyID in range(len(keys)):
                if event.key == keys[keyID]:
                    events[keyID] = True
        #Did the user click the window close button? If so, quit.
        elif event.type == QUIT:
            pygame.quit()
    return events

#Returns if a key is pressed
def keyPressed(key):
    return(pygame.key.get_pressed()[key])

screen = ""

#Initialise pygame
def init():
    global screen
    global objects
    pygame.init()
    screen = pygame.display.set_mode((640, 480))
    objects.append(spriteObject("test",0,[1,1],[100,100],pygame.image.load_extended("test.png")))
    objects.append(spriteObject("aeo",-45,[1,1],[0,64],pygame.image.load_extended("test.png"),"test")) 

#Initialise time variable
time = 0

#Main loop function
def engineMain():
    global time
    time = pygame.time.get_ticks()
    render()
    timeTemp = pygame.time.get_ticks()
    #60hz, has some screen tearing
    pygame.time.delay(math.floor(1000/60-(timeTemp-time)))
    time = timeTemp

#Main game function
def main():
    init()
    while True:
        events = handleEvents(())
        engineMain()
        if keyPressed(K_UP):
            objects[getObject("test")].offset[1]+=5
        if keyPressed(K_LEFT):
            objects[getObject("test")].offset[0]-=5
        if keyPressed(K_DOWN): 
            objects[getObject("test")].offset[1]-=5 
        if keyPressed(K_RIGHT):
            objects[getObject("test")].offset[0]+=5
        if keyPressed(K_q):
            objects[getObject("test")].rotation+=5
        if keyPressed(K_e):
            objects[getObject("test")].rotation-=5

main()
