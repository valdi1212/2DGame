import pygame


class Player(object):

    def __init__(self):
        self.rect = pygame.Rect(40, 40, 20, 20)
        self.alive = True
        self.has_armour = False
        self.last_touched = None
        self.points = 5

    def move(self, x, y):
        if x != 0:
            self.move_single_axis(x, 0)
        if y != 0:
            self.move_single_axis(0, y)

    def move_single_axis(self, x, y):
        self.rect.x += x
        self.rect.y += y

        for wall in walls:
            if self.rect.colliderect(wall.rect):
                if x > 0:
                    self.rect.right = wall.rect.left
                if x < 0:
                    self.rect.left = wall.rect.right
                if y > 0:
                    self.rect.bottom = wall.rect.top
                if y < 0:
                    self.rect.top = wall.rect.bottom

        for armour in armours:
            if self.rect.colliderect(armour.rect):
                if self.has_armour and self.last_touched != armour:
                    print('You can only wear one armour at a time.')
                    self.last_touched = armour
                elif self.has_armour is False:
                    self.has_armour = True
                    self.points -= 2
                    armours.remove(armour)
                    print('You pick up and wear the armour, costing you 2 points. Total points: %d' % self.points)

        for bomb in bombs:
            if self.rect.colliderect(bomb.rect):
                if self.has_armour:
                    bombs.remove(bomb)
                    self.has_armour = False
                    self.points += 5
                    print('Your armour absorbs the blast, but becomes unusable in the process.')
                    print('You gain 5 points for causing the bomb to go off! Total points: %d' % self.points)
                else:
                    self.alive = False
                    print('GAME OVER\nYou exploded!')
                    break

        if self.rect.colliderect(gate.rect) and gate.is_open:
            global running
            running = False
            print('You win!\nYour points: %d' % self.points)


class Wall(object):
    def __init__(self, pos):
        self.rect = pygame.Rect(pos[0], pos[1], 20, 20)


class Gate(object):
    def __init__(self, pos):
        self.rect = pygame.Rect(pos[0], pos[1], 20, 20)
        self.is_open = False


class Armour(object):
    def __init__(self, pos):
        self.rect = pygame.Rect(pos[0], pos[1], 20, 20)


class Bomb(object):
    def __init__(self, pos):
        self.pos = pos
        self.rect = pygame.Rect(pos[0], pos[1], 20, 20)


# setting up pygame
pygame.init()
window_size = window_width, window_height = 640, 480
window = pygame.display.set_mode(window_size, 0, 32)
pygame.display.set_caption('Maze')

# defining color constants
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
ORANGE = (255, 128, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# creating variables
timer = pygame.time.Clock()
walls = []
armours = []
bombs = []
global gate
player = Player()

# TODO? generate maze rather than predefining it
# -> look up maze generation and emulate?
# -> must remember to account for the bombs and armours
# -> generating armour within reach of the player will be tricky
level = [
    "WWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWW",
    "W         AW   W  AW       W  AW",
    "W    WWWWWWW       WWW WWWWW   W",
    "W      W   WWWWWW       W  W   W",
    "WWWW   W        W WWW  WWW W   W",
    "W      W  W  W  W WAWW     WW  W",
    "WWWWWW    WWWW  B W W       W  W",
    "W    WWWW   W  WWWW WWW     W  W",
    "W           WWWW      WWW   W  W",
    "WWWWW W     B       WWW     B  W",
    "W   W WW    WW   W WW W   WWWWWW",
    "W   W W BWWWW    W  W W      WAW",
    "W   WWW  W AW  W W  W WWW    B W",
    "W   W    W  WWWWWW  W        W W",
    "W  WW  WWW  W   W BWWWW   WW W W",
    "W  W     W  W   W   W      W   W",
    "W  WWWW  W  W  WW W   W    WWWWW",
    "W  W     W  W     W   W        W",
    "WBWW     W  WW  WWWWWWW     WB W",
    "W        W       W AW   WWWWW WW",
    "W    WWWWWWWWWWBWW  W     W    W",
    "W  WWW   WA      W WW          W",
    "W AW             W        W    G",
    "WWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWW",
]

x = y = 0
for row in level:
    for col in row:
        if col == "W":
            walls.append(Wall((x, y)))
        if col == "G":
            gate = Gate((x, y))
        if col == "B":
            bombs.append(Bomb((x, y)))
        if col == "A":
            armours.append(Wall((x, y)))
        x += 20
    y += 20
    x = 0

# main loop
running = True

while running:
    # lock the framerate to 60fps
    timer.tick(60)
    if player.points >= 15:
        gate.is_open = True
        print('The gate has opened!')

    # polling events
    e = pygame.event.poll()
    if e.type == pygame.QUIT:
        running = False
    elif e.type == pygame.KEYDOWN and e.key == pygame.K_ESCAPE:
        running = False

    # Move the player
    key = pygame.key.get_pressed()
    if key[pygame.K_LEFT]:
        player.move(-2, 0)
    if key[pygame.K_RIGHT]:
        player.move(2, 0)
    if key[pygame.K_UP]:
        player.move(0, -2)
    if key[pygame.K_DOWN]:
        player.move(0, 2)

    # check if player is dead
    if player.alive is not True:
        running = False

    # render everything on the screen
    window.fill(BLACK)
    for wall in walls:
        pygame.draw.rect(window, WHITE, wall.rect)
    for bomb in bombs:
        pygame.draw.circle(window, BLUE, (bomb.pos[0] + 10, bomb.pos[1] + 10), 10, 0)
    for armour in armours:
        pygame.draw.rect(window, (100, 100, 100), armour.rect)

    if gate.is_open:
        pygame.draw.rect(window, GREEN, gate.rect)
    else:
        pygame.draw.rect(window, RED, gate.rect)

    if player.has_armour:
        pygame.draw.rect(window, YELLOW, player.rect)
    else:
        pygame.draw.rect(window, ORANGE, player.rect)

    pygame.display.flip()

pygame.quit()
