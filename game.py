import pygame
from pygame.locals import (
    K_UP,
    K_DOWN,
    K_LEFT,
    K_RIGHT,
    K_ESCAPE,
    KEYDOWN,
    QUIT,
)


objects = []

def getObject(id):
    for objectid in range(len(objects)):
        if objects[objectid].id == id:
            return objectid
    return -1

class gameObject():
    def __init__(self,id,offset,layer=1,parent="world"):
        self.id = id
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
    def __init__(self,id,offset,sprite,layer=1,parent="world",):
        super().__init__(id,offset,layer,parent)
        self.sprite = sprite
    def render(self):
        screen.blit(self.sprite,(super().getPos()[0]-self.sprite.get_width()/2,screen.get_height()-super().getPos()[1]-self.sprite.get_height()/2))

def render():
    screen.fill((0,0,0))
    for object in objects:
        if isinstance(object,spriteObject):
            object.render()
    pygame.display.update()

def handleEvents():
    events = [False, False, False, False]
    for event in pygame.event.get():
        # Did the user hit a key?
        if event.type == KEYDOWN:
            # Was it the Escape key? If so, quit.
            if event.key == K_ESCAPE:
                pygame.quit()
            elif event.key == K_UP:
                events[0] = True
            elif event.key == K_LEFT:
                events[1] = True
            elif event.key == K_DOWN:
                events[2] = True
            elif event.key == K_RIGHT:
                events[3] = True
        # Did the user click the window close button? If so, quit.
        elif event.type == QUIT:
            pygame.quit()
    return events
screen = ""
def init():
    global screen
    global objects
    pygame.init()
    screen = pygame.display.set_mode((640, 480))
    objects.append(spriteObject("test",[100,100],pygame.image.load("test.jpeg").convert()))

def engineMain():
    render()
    pygame.time.delay(16)

def main():
    init()
    while True:
        events = handleEvents()
        engineMain()
        if events[0]:
            objects[getObject("test")].offset[1]+=5
        if events[1]:
            objects[getObject("test")].offset[0]-=5
        if events[2]:
            objects[getObject("test")].offset[1]-=5 
        if events[3]:
            objects[getObject("test")].offset[0]+=5 
main()
