import pygame
import sys
from pygame.locals import *


class Platform():
   def __init__(self,anchor,length,width):
     self.anchor = anchor
     self.length = length
     self.width  = width

   def draw(self):
      pygame.draw.rect(DISPLAYSURF, RED, (self.anchor[0], self.anchor[1], self.length, self.width))

class Sock():
  
  def __init__(self,pos,state):
      self.pos = list(pos)
      self.state = state  
   
  def draw(self): 
    pygame.draw.circle(DISPLAYSURF, BLUE, (self.pos[0], self.pos[1]), 20, 0)
   
  def update(self):
    if self.state == 'right':
      self.pos[0] = self.pos[0] + 2
    elif self.state == 'left':
      self.pos[0] = self.pos[0] - 2
    
  def start_move(self,direction):
    self.state = direction
   
  def stop(self):
    self.state = 'still'

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
p1 = Platform((10,20), 50, 10)
floor = Platform((0,250),600,50)
socke = Sock((10,240),'still')
clock = pygame.time.Clock()


spamRect = pygame.Rect(10, 20, 200, 300)
while True: # main game loop
     clock.tick(60)
     DISPLAYSURF.fill(WHITE)
     p1.draw()
     floor.draw()
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
         elif event.type == pygame.KEYUP:
	   socke.stop()
	   
     socke.update()
     pygame.display.update()	