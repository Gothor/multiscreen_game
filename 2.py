import sys, pygame
import asyncio;
import websockets
from threading import Thread
from pygame import Rect
import operator

def constrain(val, min_val, max_val):
  return min(max_val, max(min_val, val))

class Vector2:

  def __init__(self, x, y):
    self._data = [x, y]

  def __getitem__(self, item):
    return self._data[item]

  def __setitem__(self, item, value):
    self._data[item] = value

  def add(self, other):
    self.x = self.x + other[0]
    self.y = self.y + other[1]

  def mul(self, v):
    self.x *= v
    self.y *= v

  def set_x(self, v):
    self._data[0] = v

  def set_y(self, v):
    self._data[1] = v

  def get_x(self):
    return self._data[0]

  def get_y(self):
    return self._data[1]

  x = property(get_x, set_x)
  y = property(get_y, set_y)

class GameObject:
  
  def __init__(self, image, x, y, w, h):
    self.image = image
    self.w = w
    self.h = h
    self.position = Vector2(x, y)
    self.velocity = Vector2(0, 0)
    self.acceleration = Vector2(0, 0)

  def applyForce(self, v):
    self.acceleration.add(v)
    self.acceleration.mul(0.01)

  def update(self):
    self.velocity.mul(0.99)
    self.velocity.add(self.acceleration)
    self.position.add(self.velocity)
    self.acceleration.mul(0)

    self.position.x = constrain(self.position.x, 0, width - self.w)
    self.position.y = constrain(self.position.y, 0, height - self.h)

  def show(self, screen):
    screen.blit(self.image, self.get_rect())

  def get_rect(self):
    return Rect(self.position[0], self.position[1], self.w, self.h)

# Get data
async def get_coords(websocket, path):
  global speed
  while 1:
    coord = await websocket.recv()
    speed = tuple(map(float, coord.split(",")))

def background_loop(loop):
  asyncio.set_event_loop(loop)
  start_server = websockets.serve(get_coords, "0.0.0.0", 8765)
  loop.run_until_complete(start_server)
  loop.run_forever()

loop = asyncio.new_event_loop()
t = Thread(target=background_loop, args=(loop,), daemon=True)
t.start()

# Manage game
pygame.init()

size = width, height = pygame.display.list_modes()[0] # 640, 480
speed = (0, 0)
black = 0, 0, 0

screen = pygame.display.set_mode(size, pygame.FULLSCREEN)

ballImage = pygame.image.load("intro_ball.gif")
ballRect = ballImage.get_rect()
ball = GameObject(ballImage, 0, 0, ballRect.width, ballRect.height)

while 1:
  for event in pygame.event.get():
    if event.type == pygame.QUIT: sys.exit()

  screen.fill(black)
  ball.applyForce(speed)
  ball.update()
  ball.show(screen)
  pygame.display.flip()
