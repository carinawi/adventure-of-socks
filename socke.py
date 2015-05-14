import pygame
import sys
from pygame.locals import *

GRAV = 0.005 #0.005

class Enemy():
   visible = True
   
   def __init__(self,pos,state):
     self.pos = list(pos)
     self.initialpos = pos[0]
     self.state = state
     
   def draw(self):
     if(self.visible):
       pygame.draw.rect(DISPLAYSURF, GREEN, (int(round(self.pos[0]+shift[0])), int(round(self.pos[1]+shift[1])), 40,40))

   def update(self, dt):
      
     if self.state == 1 :
      self.pos[0] = self.pos[0] + 0.05*dt
     else:
      self.pos[0] = self.pos[0] - 0.05*dt
       
     if self.pos[0] >= self.initialpos +100:
       self.state = 0
     if self.pos[0] <= self.initialpos - 100:
       self.state = 1
      
      
class Star():  
   visible = True  
   def __init__(self,pos): 
     self.pos = pos
     
   def draw(self):
     if(self.visible):
       pygame.draw.circle(DISPLAYSURF, BLUE, (int(round(self.pos[0] + shift[0])), int(round(self.pos[1] + shift[1]))), 8, 0)

       
class Platform():
   def __init__(self,anchor,length,width):
     self.anchor = anchor
     self.length = length
     self.width  = width

   def draw(self):
      pygame.draw.rect(DISPLAYSURF, RED, (int(round(self.anchor[0]+shift[0])), int(round(self.anchor[1]+shift[1])), self.length, self.width))

class Sock():
  img = pygame.image.load('entwurf1-klein.png')


  JUMPING_VELOCITY = 1.1 #1.2
  
  starsnumber = 0
  
  hearts = 3
  
  def __init__(self,pos,state):
      self.pos = list(pos)
      self.state = state 
      self.vel = 0
   
  def draw(self):
    x = int(round(self.pos[0] + shift[0]))
    y = int(round(self.pos[1] + shift[1]))
    #pygame.draw.circle(DISPLAYSURF, BLUE, (x,y), 20, 0)
    DISPLAYSURF.blit(self.img, (x-40,y-40))
   
  def update(self,dt):
    if not self.onboard():#socke.pos[1] <= 250:
      self.vel = self.vel + GRAV*dt
    elif self.onboard() and self.vel < 0:
      self.vel = self.vel + GRAV*dt
    else:  
      self.vel = 0 
    
    p = self.overboard(dt)
    if p :
      self.pos[1] = min(self.pos[1] + self.vel * dt,p.anchor[1])
    else :
      self.pos[1] = self.pos[1] + self.vel * dt
    
    if self.state == 'right' and not self.lefttouch():
      self.pos[0] = self.pos[0] + 0.6*dt
    elif self.state == 'left'and not self.righttouch():
      self.pos[0] = self.pos[0] - 0.6*dt
    
    s = self.startouch()
    if(s):
       if(s.visible):
         self.starsnumber = self.starsnumber + 1
         s.visible = False
    
    e = self.enemybeat()  
    if(e):
        e.visible = False
      
    if(self.enemytouch()):
      self.hearts = self.hearts - 1
      self.pos[0] = self.pos[0] - 90
    
    
  def start_jump(self):
    if(self.onboard()):  
      self.vel = -self.JUMPING_VELOCITY
    
  def start_move(self,direction):
    self.state = direction
   
  def stop(self):
    self.state = 'still'

  def onboard(self):  
    for p in world:
      if self.pos[0] >= p.anchor[0] and self.pos[0] <= (p.anchor[0] + p.length):
	if self.pos[1] <= p.anchor[1]+1 and self.pos[1] >= p.anchor[1]-1:
	  return True
     	  
	  
    return False	

  def lefttouch(self):
    for p in world:
      if self.pos[0] <= p.anchor[0]+1 and self.pos[0] >= p.anchor[0]-1:
	if self.pos[1] >= p.anchor[1] and self.pos[1] <= p.anchor[1]+p.width:
	  return True

    return False	

  def righttouch(self):
    for p in world:
      if self.pos[0] <= p.anchor[0]+p.length+1 and self.pos[0] >= p.anchor[0]+p.length-1:
	if self.pos[1] >= p.anchor[1] and self.pos[1] <= p.anchor[1]+p.width:  
	  return True

    return False    
            
      
  def overboard(self,dt):
    proposedY = self.pos[1] + self.vel * dt
    for p in world:
      if self.pos[0] >= p.anchor[0] and self.pos[0] <= p.anchor[0] + p.length and self.pos[1] - p.anchor[1] <= 3 and proposedY - p.anchor[1] >= -3:
	return p
    
    return None
    
  def startouch(self):
    for s in stars:
      if abs(self.pos[0] -s.pos[0]) <= 20:
	if abs(self.pos[1]-s.pos[1]) <= 20:  
	  return s

    return None
   
  def enemytouch(self):
    for e in enemies:
      if e.visible == True:  
        if self.pos[0] <= e.pos[0]+40+1 and self.pos[0] >= e.pos[0]+40-1:
	  if self.pos[1] >= e.pos[1] and self.pos[1] <= e.pos[1]+40:  
	    return True
        if self.pos[0] <= e.pos[0]+1 and self.pos[0] >= e.pos[0]-1:
	  if self.pos[1] >= e.pos[1] and self.pos[1] <= e.pos[1]+40:
	    return True 
    return False  

  def enemybeat(self):  
    for e in enemies:
      if self.pos[0] >= e.pos[0] and self.pos[0] <= (e.pos[0] + 40):
	if self.pos[1] <= e.pos[1]+1 and self.pos[1] >= e.pos[1]-1:
	  return e
     	  
	  
    return None
    
    
pygame.init()
DISPLAYSURF = pygame.display.set_mode((400, 300))
pygame.display.set_caption('Hello World!')
BLACK = (  0,   0,   0)
WHITE = (255, 255, 255)
RED = (255,   0,   0)
GREEN = (  0, 255,   0)
BLUE = (  0,   0, 255)
#DISPLAYSURF.fill(WHITE)
#pygame.draw.polygon(DISPLAYSURF, GREEN, ((146, 0), (291, 106), (236, 277), (56, 277), (0, 106)))
p1 = Platform((10,200), 50, 10)
p2 = Platform((90,150), 50, 10)
p3 = Platform((190,100), 50, 10)
p4 = Platform((230,230),50,50)
floor = Platform((-60,250),900,50)
socke = Sock((10,250),'still')
clock = pygame.time.Clock()
s1 = Star((270,70))
s2 = Star((360,240))
e1 = Enemy((390,220),1)
stars = [s1,s2]
world = [floor,p1,p2,p3,p4]
enemies = [e1]
shift = list((0,0))

font=pygame.font.Font(None,30)

def texts(score, pos, col):
   scoretext=font.render(str(score), 1,col)
   DISPLAYSURF.blit(scoretext, pos)


spamRect = pygame.Rect(10, 20, 200, 300)
while True: # main game loop
     if socke.pos[1] >= 800 or socke.hearts == 0:
       DISPLAYSURF.fill(BLACK)
       texts('Game Over',(150,150),WHITE)
       pygame.display.update()
       for event in pygame.event.get():
           if event.type == QUIT:
              pygame.quit()
              sys.exit()
           if event.type == pygame.KEYUP:
	      socke = Sock((10,250),'still')
	      for s in stars:
		s.visible = True
              for e in enemies:
		e.visible = True
              
     else: 
       clock.tick(60)
       DISPLAYSURF.fill(WHITE)
       texts(socke.starsnumber,(330,5),BLACK)
       texts('Stars:',(270,5),BLACK)
       texts(socke.hearts,(70,5),BLACK)
       texts('Hearts:',(0,5),BLACK)
       shift = list((-socke.pos[0]+200,-socke.pos[1]+250))
       for p in world:
         p.draw()
     
       for s in stars:
	 s.draw()
       
       for e in enemies:
	 e.draw()
      
       socke.draw()
      
       for event in pygame.event.get():
           if event.type == QUIT:
              pygame.quit()
              sys.exit()
           elif event.type == pygame.KEYDOWN:
	     if event.key == K_LEFT:
               socke.start_move('left')
             if event.key == K_RIGHT:
               socke.start_move('right')
             if event.key == K_UP:
	        socke.start_jump()
           elif event.type == pygame.KEYUP:
	     if event.key == K_RIGHT or event.key == K_LEFT:
	       socke.stop()
     
     
       dt = float(clock.get_time())
       number_of_nano_steps = 10
       for i in range(number_of_nano_steps):
	 socke.update(dt/number_of_nano_steps)
	 for e in enemies:
	   e.update(dt/number_of_nano_steps)
       pygame.display.update()
     
     