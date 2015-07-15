# -*- coding: utf-8 -*-
import pygame
import sys
from pygame.locals import *

GRAV = 0.005 #0.005
FPS  = 60
CURRENT_TIME = 0

class Camera():
  
  #implements PID controller
  Kp = [0.013, 0.0113]
  Ki = [0.0000001, 0.0000001]
  Kd = [0.000001, 0.0001]
  
  #0.00013, 0.0000001, 0.0001
  
  Kp_delta = [0.00113, 0]
  Ki_delta = [0.000000001, 0]
  Kd_delta = [0.0001, 0]
  
  def __init__(self,pos,vel):
    self.pos = list(pos)
    self.old_pos = list(pos)
    self.vel = list(vel)
    self.integrand = [0,0]
    self.integrand_delta = [0,0]
    self.delta = [0,0]
    self.delta_vel = [0,0]
    self.old_delta = [0,0]
    self.old_target = list(pos)
    self.old_target_delta = [0,0]
   
  def  update(self,dt,socke):

    # abstand zum rand je nach blickrichtung
    target_pos = [socke.pos[0] + self.delta[0], socke.pos[1] + self.delta[1]]
    target_delta = [100,0] if socke.Right else [-100,0]
  
    #print("######", self.pos, target_pos)
    self.integrand[0] = self.integrand[0] + dt*(target_pos[0] - self.pos[0])
    self.integrand[1] = self.integrand[1] + dt*(target_pos[1] - self.pos[1])
    
    #folge der kamera
    self.integrand_delta[0] = self.integrand_delta[0] + dt*(target_delta[0] - self.delta[0])
    self.integrand_delta[1] = self.integrand_delta[1] + dt*(target_delta[1] - self.delta[1])
  
    self.vel[0] = dt*( self.Kp[0] * (target_pos[0] - self.pos[0]) + self.Ki[0] * (self.integrand[0]) + self.Kd[0] * ((target_pos[0] - self.pos[0]) - (self.old_target[0] - self.old_pos[0]))/dt)
    self.vel[1] = dt*( self.Kp[1] * (target_pos[1] - self.pos[1]) + self.Ki[1] * (self.integrand[1]) + self.Kd[1] * ((target_pos[1] - self.pos[1]) - (self.old_target[1] - self.old_pos[1]))/dt)
    
    self.delta_vel[0] = dt*( self.Kp_delta[0] * (target_delta[0] - self.delta[0]) + self.Ki_delta[0] * (self.integrand_delta[0]) + self.Kd_delta[0] * ((target_delta[0] - self.delta[0]) - (self.old_target_delta[0] - self.old_delta[0]))/dt)
    self.delta_vel[1] = dt*( self.Kp_delta[1] * (target_delta[1] - self.delta[1]) + self.Ki_delta[1] * (self.integrand_delta[1]) + self.Kd_delta[1] * ((target_delta[1] - self.delta[1]) - (self.old_target_delta[1] - self.old_delta[1]))/dt)
   
    if abs(self.pos[1] - target_pos[1]) < 100 and not (abs(socke.vel[1]) < 0.01):  # and socke.vel[1] < 0:
      self.vel[1] = 0
    
    self.old_pos   = list(self.pos)
    self.old_delta = list(self.delta)
    self.old_target = list(target_pos)
    self.old_target_delta = list(target_delta)
    
    self.pos[0] = self.pos[0] + self.vel[0] * dt
    self.pos[1] = self.pos[1] + self.vel[1] * dt
    
    self.delta[0] = self.delta[0] + self.delta_vel[0] * dt
    self.delta[1] = self.delta[1] + self.delta_vel[1] * dt
   
    
class World():
  
  def __init__(self, stars, enemies, platforms):
    self.stars = stars 
    self.enemies = enemies 
    self.platforms = platforms
  
  def set_init(self):
    for s in self.stars:
      s.visible = True
    for e in self.enemies:
      e.visible = True
    
  def draw_world(self):
    for s in self.stars:
      s.draw()
    for e in self.enemies:
      e.draw()
    for p in self.platforms:
      p.draw()
   
  def update_world(self,dt, number_of_nano_steps): 
    for p in self.platforms:
      p.update(dt/number_of_nano_steps)
    for e in self.enemies:
      e.update(dt/number_of_nano_steps)
      
      
      
class Enemy():
   visible = True
   enemysize = 40
   
   def __init__(self,pos,state):
     self.pos = list(pos)
     self.initialpos = pos[0]
     self.state = state
     
   def draw(self):
     if(self.visible):
       pygame.draw.rect(DISPLAYSURF, GREEN, (int(round(self.pos[0]+shift[0])), int(round(self.pos[1]+shift[1])), self.enemysize,self.enemysize))

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
   diameter = 8
   def __init__(self,pos): 
     self.pos = pos
     
   def draw(self):
     if(self.visible):
       pygame.draw.circle(DISPLAYSURF, BLUE, (int(round(self.pos[0] + shift[0])), int(round(self.pos[1] + shift[1]))), 8, 0)

       
class Platform():
   vel = [0,0]
   
   def __init__(self,anchor,length,width):
     self.anchor = anchor
     self.length = length
     self.width  = width

   def draw(self):
      pygame.draw.rect(DISPLAYSURF, RED, (int(round(self.anchor[0]+shift[0])), int(round(self.anchor[1]+shift[1])), self.length, self.width))

   def update(self, dt):
      self.anchor = (self.anchor[0] + dt*self.vel[0], self.anchor[1] + dt*self.vel[1])
      

class Bounce(Platform):
  
   def __init__(self,anchor,length,width,jumpvel,standvel):
     self.anchor = anchor
     self.length = length
     self.width  = width 
     self.jumpvel = jumpvel
     self.standvel = standvel
      
class MovePlat(Platform):
   
   time_counter = 0
   
   def __init__(self,anchor,length,width,switchtime):
     self.anchor = anchor
     self.length = length
     self.width  = width 
     self.switchtime = switchtime
   
   
   def update(self, dt):
      self.anchor = (self.anchor[0] + dt*self.vel[0], self.anchor[1] + dt*self.vel[1])   
      self.time_counter = self.time_counter + dt
      if self.time_counter > self.switchtime :
	self.vel[0] = (-1)*self.vel[0]
        self.time_counter = 0    
   
   
class AnimatedSprite():
  def __init__(self, delay, images):
    # delay in ms
    self.images = images
    self.delay  = delay * FPS / 1000 # dieses delay in Anzahl Frames
    print self.delay
    self.ticks  = 0
    
  def draw(self,pos):
    DISPLAYSURF.blit(self.images[(self.ticks / self.delay) % len(self.images)], pos)
    self.ticks = self.ticks + 1
      
      
class Sock():
  sprite_walk_right = AnimatedSprite(50, [ pygame.image.load("laufanimation/%02d.png" % i) for i in range(13) ])
  sprite_walk_left  = AnimatedSprite(50, [ pygame.transform.flip(pygame.image.load("laufanimation/%02d.png" % i),True,False) for i in range(13) ])
  sprite_still      = AnimatedSprite(50, [ pygame.image.load("still.png") ])
  sprite_still_left = AnimatedSprite(50, [ pygame.transform.flip(pygame.image.load("still.png"),True,False) ])
  sprite_jump_right = AnimatedSprite(50, [ pygame.image.load("jump.png")  ])
  sprite_jump_left  = AnimatedSprite(50, [ pygame.transform.flip(pygame.image.load("jump.png"),True,False) ])

  JUMPING_VELOCITY = 1.1 #1.2
  RUNNING_VELOCITY = 0.6
  LASTBOUNCE_TOL = 2000
  
  timestamp_lastbounceplatform = 0
  lastbounceplatform           = None
  
  starsnumber = 0
  
  hearts = 3
  length = 45
  height = 45
  standing_factor = 0.8
  enemy_standing_factor = 0.9
  #xvel = 0.6
  Right = True # What was the last position Socke got? Right is default...
  
  def __init__(self,pos,state):
      self.pos = list(pos)
      self.old_pos = list(pos)
      self.state = state 
      self.vel = [0,0]
      
      self.last_standed_platform = None

  def draw(self):
    x = int(round(self.pos[0] + shift[0])) #-  self.length
    y = int(round(self.pos[1] + shift[1])) -  self.height
    #pygame.draw.rect(DISPLAYSURF, BLUE, (x, y, self.length, self.height))
    x = x - float(self.length*0.4)
    y = y - float((self.height)*0.4)
    
    if self.vel[1] != 0:
      if self.Right == False:#self.state == 'left':
	self.sprite_jump_left.draw((x,y))
      else:
	self.sprite_jump_right.draw((x,y))
    else:
      if self.Right == True and not self.is_still():
	self.sprite_walk_right.draw((x,y))
      elif self.Right == False and not self.is_still():
	self.sprite_walk_left.draw((x,y))
      elif self.Right == True:
	self.sprite_still.draw((x,y))
      elif self.Right == False:
	self.sprite_still_left.draw((x,y))

  # Geschwindigkeit, die Socke ohne eigene Bewegung hat (zum Beispiel durch bewegende Plattform)
  def basevel(self):
    p = self.onboard()
    if p:
      return (p.vel[0], 0)   # XXX: sollte auch y-Geschwindigkeit mitnehmen
    else:
      return (0,0)
	
  def is_still(self):
    return self.vel[0] == self.basevel()[0]
	
  def update(self,dt):
    
    self.old_pos = list(self.pos)
    
    if not self.onboard():#socke.pos[1] <= 250:
      self.vel[1] = self.vel[1] + GRAV*dt
    elif self.onboard() and self.vel[1] < 0:
      self.vel[1] = self.vel[1] + GRAV*dt
    else:  
      self.vel[1] = 0 

    p = self.overboard(dt)
    if p:
      self.pos[1] = min(self.pos[1] + self.vel[1] * dt,p.anchor[1])
    else :
      self.pos[1] = self.pos[1] + self.vel[1] * dt

    p = self.onboard()
    if self.last_standed_platform != p:
	self.stop()
    self.last_standed_platform = p
    if isinstance(p,Bounce):
      self.start_jump(False)
    
    #wichtig, dass die basevel nicht nur am anfang auf ner platform gesetzt wird!!!
    if(self.state == 'still'):
      self.vel[0] = self.basevel()[0]
      
    if (self.vel[0] > 0 and not self.lefttouch()) or (self.vel[0] < 0 and not self.righttouch()):
      self.pos[0] = self.pos[0] + self.vel[0]*dt

    s = self.startouch()
    if(s):
       if(s.visible):
         self.starsnumber = self.starsnumber + 1
         s.visible = False
    
    e = self.enemybeat()  
    if(e):
        e.visible = False
      
    #dringend nachbessern!!!!! unverwundbarkeit etc.  
    if(self.enemytouch()):
      self.hearts = self.hearts - 1
      if(self.state == 'right' or self.state == 'still'):
        self.pos[0] = self.pos[0] - 90
      if(self.state == 'left'):
        self.pos[0] = self.pos[0] + 90
        
        
  def start_jump(self,userjump):
    
    if userjump: # this realizes whether I induced a jump actively or not
      
      if self.lastbounceplatform and CURRENT_TIME - self.timestamp_lastbounceplatform < self.LASTBOUNCE_TOL:
	self.vel[1] = -self.JUMPING_VELOCITY - self.lastbounceplatform.jumpvel
        self.lastbounceplatform = None
        
      if self.onboard():      
        p = self.onboard()
        if isinstance(p,Bounce):
          self.vel[1] = -self.JUMPING_VELOCITY - p.jumpvel    
        else:
	  self.vel[1] = -self.JUMPING_VELOCITY 
    
    else:
      p = self.onboard()
      self.timestamp_lastbounceplatform = CURRENT_TIME
      self.lastbounceplatform           = p
      self.vel[1] = - p.standvel

	
  def start_move(self,direction):
    self.state = direction
    if direction == 'left':
      self.vel[0] = self.basevel()[0] - self.RUNNING_VELOCITY
    elif direction == 'right':
      self.vel[0] = self.basevel()[0] + self.RUNNING_VELOCITY
     
  def stop(self):
    self.state = 'still'
    self.vel[0] = self.basevel()[0]
  
  # Steht Socke momentan auf einer Plattform? (Minimales überstehen ist okay.)
  def onboard(self):  
    for p in world:
      if self.pos[0] + self.standing_factor * self.length >= p.anchor[0] and self.pos[0] + self.length - self.standing_factor * self.length <= p.anchor[0] + p.length:
	if self.pos[1] <= p.anchor[1]+1 and self.pos[1] >= p.anchor[1]-1:
	  return p

    return None	

    
  def lefttouch(self):
    for p in world:
      if self.pos[0]+self.length <= p.anchor[0]+1 and self.pos[0]+self.length >= p.anchor[0]-1:
	if self.pos[1]-self.height >= p.anchor[1]-(self.height-5) and self.pos[1]<= p.anchor[1]+p.width+(self.height-5):
	  return True

    return False	

  def righttouch(self):
    for p in world:
      if self.pos[0] <= p.anchor[0]+p.length+1 and self.pos[0] >= p.anchor[0]+p.length-1:
	if self.pos[1]-self.height >= p.anchor[1]-(self.height-5) and self.pos[1]<= p.anchor[1]+p.width+(self.height-5): 
	  return True

    return False    
            
  # Flog Socke während des Zeitschritts durch eine Plattform? 
  def overboard(self,dt):
    proposedY = self.pos[1] + self.vel[1] * dt
    for p in world:
      if (self.pos[0]) + self.standing_factor*self.length >= p.anchor[0] and (self.pos[0]+self.length)-self.standing_factor*self.length <= p.anchor[0] + p.length and self.pos[1] - p.anchor[1] <= 3 and proposedY - p.anchor[1] >= -3:
	return p
    
    return None
  
  
   #something is strange here..
  def startouch(self):
    for s in stars:
      if abs(self.pos[0] -s.pos[0]) <= s.diameter or abs(self.pos[0] + self.length - s.pos[0]) <= s.diameter:
	if self.pos[1] <= s.pos[1]+6+self.height and (self.pos[1]-self.height) >= s.pos[1]-6-self.height:  
	  return s

    return None
   
  def enemytouch(self):
    for e in enemies:
      if e.visible == True:  
        if self.pos[0] <= e.pos[0]+e.enemysize+1 and self.pos[0] >= e.pos[0]+e.enemysize-1:
	  if self.pos[1]-self.height >= e.pos[1]-(self.height-10) and self.pos[1]<= e.pos[1]+e.enemysize+(self.height-10): 
	    return True
        if self.pos[0]+self.length <= e.pos[0]+1 and self.pos[0]+self.length >= e.pos[0]-1:
	  if self.pos[1]-self.height >= e.pos[1]-(self.height-10) and self.pos[1]<= e.pos[1]+e.enemysize+(self.height-10):
	    return True 
    return False  

  def enemybeat(self):  
    for e in enemies:
      if (self.pos[0])+self.enemy_standing_factor*self.length >= e.pos[0] and (self.pos[0]+self.length)-self.enemy_standing_factor*self.length <= (e.pos[0] + e.enemysize):
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
p0 = MovePlat((-50,190),50,10,2000)
p1 = Bounce((10,190), 50, 10,1.5,0.5)
p2 = Platform((90,140), 50, 10)
p3 = Platform((190,90), 50, 10)
p4 = Platform((230,220),50,50)
p4.vel = (0.01, 0)
p0.vel = list((-0.05,0))
floor = Platform((-60,250),900,50)
socke = Sock((-60.0,250.0),'still')
clock = pygame.time.Clock()
s1 = Star((270,70))
s2 = Star((360,240))
e1 = Enemy((390,220),1)
stars = [s1,s2]
world = [floor,p1,p2,p3,p4,p0]
enemies = [e1]
w1 = World(stars, enemies, world)
shift = list((0,0))
camera = Camera(list((socke.pos[0],socke.pos[1])), (0,0))

font=pygame.font.Font(None,30)

def texts(score, pos, col):
   scoretext=font.render(str(score), 1,col)
   DISPLAYSURF.blit(scoretext, pos)


spamRect = pygame.Rect(10, 20, 200, 300)
while True: # main game loop
     if socke.pos[1] >= 800 or socke.hearts <= 0:
       DISPLAYSURF.fill(BLACK)
       texts('Game Over',(150,150),WHITE)
       pygame.display.update()
       for event in pygame.event.get():
           if event.type == QUIT:
              pygame.quit()
              sys.exit()
           if event.type == pygame.KEYUP:
	      socke = Sock((10.0,250.0),'still')
	      camera = Camera(list((socke.pos[0],socke.pos[1])), (0,0))
	      #for s in stars:
		#s.visible = True
              #for e in enemies:
		#e.visible = True
              w1.set_init()
              clock.tick(FPS)
     else: 
       clock.tick(FPS)
       DISPLAYSURF.fill(WHITE)
       texts(socke.starsnumber,(330,5),BLACK)
       texts('Stars:',(270,5),BLACK)
       texts(socke.hearts,(70,5),BLACK)
       texts('Hearts:',(0,5),BLACK)
       
       #shift = list((-socke.pos[0]+200,-socke.pos[1]+250))
       
       shift = [200 - camera.pos[0], 250 - camera.pos[1]] 
       #for p in world:
        # p.draw()
     
       #for s in stars:
	# s.draw()
       
       #for e in enemies:
	# e.draw()
       
       w1.draw_world()
       socke.draw()

       pressed = pygame.key.get_pressed()
       if pressed[pygame.K_RIGHT]:
             socke.start_move('right')
             socke.Right = True
       elif pressed[pygame.K_LEFT]:
             socke.start_move('left')
             socke.Right = False
 
       for event in pygame.event.get():
           if event.type == QUIT:
              pygame.quit()
              sys.exit()
           if event.type == pygame.KEYDOWN:
              if event.key == K_UP:
	         socke.start_jump(True)
           if event.type == pygame.KEYUP:
	     if (event.key == K_RIGHT and not pressed[K_LEFT]) or (event.key == K_LEFT and not pressed[K_RIGHT]):
	        socke.stop()     

       dt = float(clock.get_time())
       number_of_nano_steps = 10
       for i in range(number_of_nano_steps):
	 socke.update(dt/number_of_nano_steps)
	 #for p in world:
	  # p.update(dt/number_of_nano_steps)
	 #for e in enemies:
	  # e.update(dt/number_of_nano_steps)
	 w1.update_world(dt, number_of_nano_steps)
	 camera.update(dt/number_of_nano_steps,socke)
	 CURRENT_TIME = CURRENT_TIME + dt
       pygame.display.update()
     
     