from pygame import *

PRESSED = {}

def compute_inputs():
  for e in event.get():
    if e.type == QUIT:
      exit()
    if e.type == KEYDOWN:
      PRESSED[e.key] = True
    if e.type == KEYUP:
      PRESSED[e.key] = False

def idle():
  if K_UP in PRESSED and PRESSED[K_UP]:
    pos[1] -= 2
  if K_DOWN in PRESSED and PRESSED[K_DOWN]:
    pos[1] += 2
  if K_LEFT in PRESSED and PRESSED[K_LEFT]:
    pos[0] -= 2
  if K_RIGHT in PRESSED and PRESSED[K_RIGHT]:
    pos[0] += 2

if __name__ == '__main__':
  screen = display.set_mode(flags=FULLSCREEN)
  avatar = image.load('/mnt/d/Rodolphe/Pictures/avatar256x256.png').convert()

  pos = [0, 0]
  mouse.set_visible(False)

  while 1:
    compute_inputs()
    idle()

    screen.fill((0,0,0))
    screen.blit(avatar, avatar.get_rect().move(pos), avatar.get_rect())
    display.update()
    time.delay(int(1000 / 60))

