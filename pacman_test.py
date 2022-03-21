import pygame
import random
import time

window_width = 600
window_height = 798
window = pygame.display.set_mode((window_width, window_height))
clock = pygame.time.Clock()
bg = pygame.image.load('images\\map.png')
pacman = pygame.image.load('images\\pacman_left1.png')


def define_direction(dict, way):
    for key in dict.keys():
        if key == way:
            dict[key] = True
        else:
            dict[key] = False


class Pacman:
    def __init__(self):
        self.x = 281
        self.y = 534
        self.width = 44
        self.height = 44
        self.ways = {'left': False, 'right': False,
                     'up': False, 'down': False}
        self.last_move = ''

    def draw(self):
        window.blit(pacman, (self.x, self.y))

    def direction(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_LEFT]:
            define_direction(self.ways, 'left')
        if keys[pygame.K_RIGHT]:
            define_direction(self.ways, 'right')
        if keys[pygame.K_UP]:
            define_direction(self.ways, 'up')
        if keys[pygame.K_DOWN]:
            define_direction(self.ways, 'down')

    def vision(self):
        walls = False
        if self.ways['left']:
            if self.x in [0, 1, 2] and self.y in [344, 345, 346]:
                self.x = 557
                self.y = 344
            else:
                for y in range(self.y, self.y + self.height):
                    if window.get_at((self.x - 1, y)) != (0, 0, 0):
                        walls = True
                        break
        if self.ways['right']:
            if self.x in [555, 556, 557] and self.y in [344, 345]:
                self.x = 0
                self.y = 344
            else:
                for y in range(self.y, self.y + self.height):
                    if window.get_at((self.x + self.width, y)) != (0, 0, 0):
                        walls = True
                        break
        if self.ways['up']:
            for x in range(self.x, self.x + self.width):
                if window.get_at((x, self.y - 1)) != (0, 0, 0):
                    walls = True
                    break
        if self.ways['down']:
            for x in range(self.x, self.x + self.width):
                if window.get_at((x, self.y + self.height)) != (0, 0, 0):
                    walls = True
                    break

        return not walls

    def moving(self):
        self.direction()

        # for left
        if self.ways['left'] and self.vision():

            self.x -= 1
            self.last_move = 'left'
        else:
            if self.ways['left'] and self.last_move == 'up' and\
                    window.get_at((self.x + self.width//2, self.y - 1))\
                    == (0, 0, 0):
                self.y -= 1
            elif self.ways['left'] and self.last_move == 'down' and\
                    window.get_at((self.x + self.width//2,
                                   self.y + self.height)) == (0, 0, 0):
                self.y += 1

        # for right
        if self.ways['right'] and self.vision():
            self.x += 1
            self.last_move = 'right'
        else:
            if self.ways['right'] and self.last_move == 'up' and\
                    window.get_at((self.x + self.width//2, self.y - 1))\
                    == (0, 0, 0):
                self.y -= 1
            elif self.ways['right'] and self.last_move == 'down' and\
                    window.get_at((self.x + self.width//2,
                                   self.y + self.height)) == (0, 0, 0):
                self.y += 1

        # for up
        if self.ways['up'] and self.vision():
            self.y -= 1
            self.last_move = 'up'
        else:
            if self.ways['up'] and self.last_move == 'left' and\
                    window.get_at((self.x - 1, self.y))\
                    == (0, 0, 0):
                self.x -= 1
            elif self.ways['up'] and self.last_move == 'right' and\
                    window.get_at((self.x + self.width,
                                   self.y + self.height//2))\
                    == (0, 0, 0):
                self.x += 1

        # for down
        if self.ways['down'] and self.vision():
            self.y += 1
            self.last_move = 'down'
        else:
            if self.ways['down'] and self.last_move == 'left' and\
                    window.get_at((self.x - 1, self.y + self.height//2))\
                    == (0, 0, 0):
                self.x -= 1
            elif self.ways['down'] and self.last_move == 'right' and\
                    window.get_at((self.x + self.width,
                                   self.y + self.height//2))\
                    == (0, 0, 0):
                self.x += 1


class Ghost:
    def __init__(self):
        self.x = 281
        self.y = 281
        self.height = 44
        self.width = 44
        self.speed = 1
        self.ways = {}
        self.last_move = 'left'

    def g_draw(self):
        pygame.draw.rect(window, (255, 255, 0), (self.x, self.y,
                                                 self.width, self.height))

    def g_vision(self):
        self.ways = dict.fromkeys(['left', 'right', 'up', 'down'], True)

        for y in range(self.y, self.y + self.height):
            if window.get_at((self.x - 1, y)) in [(33, 33, 255), (1, 4, 29)]:
                self.ways['left'] = False
                break

        for y in range(self.y, self.y + self.height):
            if window.get_at((self.x + self.width, y)) in [(33, 33, 255), (1, 4, 29)]:
                self.ways['right'] = False

        for x in range(self.x, self.x + self.width):
            if window.get_at((x, self.y - 1)) in [(33, 33, 255), (1, 4, 29)]:
                self.ways['up'] = False

        for x in range(self.x, self.x + self.width):
            if window.get_at((x, self.y + self.height)) in [(33, 33, 255), (1, 4, 29)]:
                self.ways['down'] = False

    def select_direction(self):
        self.g_vision()

        possible_direction = [x[0] for x in self.ways.items() if x[1]]

        if self.last_move == 'left':
            possible_direction.remove('right')
        if self.last_move == 'right':
            possible_direction.remove('left')
        if self.last_move == 'up':
            possible_direction.remove('down')
        if self.last_move == 'down':
            possible_direction.remove('up')

        length = len(possible_direction) - 1
        self.ways = dict.fromkeys(list(self.ways.keys()), False)
        self.ways[possible_direction[random.randint(0, length)]] = True

    def g_move(self):
        self.select_direction()
        if self.ways['left'] and self.x == 1 and self.y == 344:
            self.x = 555
            self.y = 344
        elif self.ways['left']:
            self.x -= self.speed
            self.last_move = 'left'

        if self.ways['right'] and self.x == 555 and self.y == 344:
            self.x = 1
            self.y = 344
        if self.ways['right']:
            self.x += self.speed
            self.last_move = 'right'

        if self.ways['up']:
            self.y -= self.speed
            self.last_move = 'up'

        if self.ways['down']:
            self.y += self.speed
            self.last_move = 'down'


if __name__ == '__main__':
    pac = Pacman()
    ghost_1 = Ghost()
    run = True
    while run:
        clock.tick(50)
        for even in pygame.event.get():
            if even.type == pygame.QUIT:
                run = False

        window.blit(bg, (0, 0))
        pac.draw()
        ghost_1.g_draw()
        pac.moving()
        ghost_1.g_move()
        pygame.display.update()

    pygame.quit()
