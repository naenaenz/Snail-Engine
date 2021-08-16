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


objects = []

def getObject(id):
    for objectid in range(len(objects)):
        if objects[objectid].id == id:
            return objectid
    return -1

class gameObject():
    def __init__(self,id,rotation,offset,layer=1,parent="world"):
        self.id = id
        self.rotation = rotation
        self.layer = layer
        self.parent = parent
        self.offset = offset
    def getPos(self):
        if(self.parent == "world"):
            return self.offset
        else:
            parentid = getObject(self.parent)
            if parentid == -1:
                self.parent = "world"
                return self.offset
            else:
                return self.offset+objects[parentid].getPos()
  

class spriteObject(gameObject):
    def __init__(self,id,rotation,offset,sprite,layer=1,parent="world",):
        super().__init__(id,rotation,offset,layer,parent)
        self.sprite = sprite
    def render(self):
        sprite = pygame.transform.rotate(self.sprite,self.rotation)
        screen.blit(sprite,(self.getPos()[0]-sprite.get_width()/2,screen.get_height()-self.getPos()[1]-sprite.get_height()/2))

def render():
    screen.fill((0,0,0))
    for object in objects:
        if isinstance(object,spriteObject):
            object.render()
    pygame.display.update()

def handleEvents(keys):
    events = [False for i in keys]
    for event in pygame.event.get():
        # Did the user hit a key?
        if event.type == KEYDOWN:
            # Was it the Escape key? If so, quit.
            if event.key == K_ESCAPE:
                pygame.quit()
            for keyID in range(len(keys)):
                if event.key == keys[keyID]:
                    events[keyID] = True
        # Did the user click the window close button? If so, quit.
        elif event.type == QUIT:
            pygame.quit()
    return events

def keyPressed(key):
    return(pygame.key.get_pressed()[key])

screen = ""

def init():
    global screen
    global objects
    pygame.init()
    screen = pygame.display.set_mode((640, 480))
    objects.append(spriteObject("test",0,[100,100],pygame.image.load("test.png").convert()))

def engineMain():
    render()
    pygame.time.delay(16)

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
