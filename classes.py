import pygame


class Colors:
    white = (255, 255, 255)
    red = (255, 0, 0)
    blue = (0, 0, 255)
    green = (0,255,0)
    black = (0, 0, 0)


class Ship:
    _pos_x = 0
    _pos_y = 0
    _size_x = 0
    _size_y = 0
    _type = 1
    _spawn = False

    def __init__(self, pos_x, pos_y, size_x=30, size_y=50, _type=1):
        self._pos_x = pos_x
        self._pos_y = pos_y
        self._size_x = size_x
        self._size_y = size_y
        self._type = _type

    def has_collided(self, bullet):
        if not self._spawn:
            return False
        if ((self._pos_x + 16.4 >= bullet.get_pos_x()) and (self._pos_x - 16.4 <= bullet.get_pos_x())) and (
                (self._pos_y + 25.4  >= bullet.get_pos_y()) and (self._pos_y - 25.4 <= bullet.get_pos_y())):
            return True
        return False

    def has_spawned(self):
        return self._spawn

    def get_pos_x(self):
        return self._pos_x

    def get_pos_y(self):
        return self._pos_y

    def get_width_x(self):
        return self._size_x

    def get_height_y(self):
        return self._size_y

    def set_position(self, pos_x, pos_y):
        self._pos_x = pos_x
        self._pos_y = pos_y

    def change_position(self, pos_x, pos_y):
        self._pos_x += pos_x
        self._pos_y += pos_y


class Pattern:
    _tick = 0
    _index = 0
    _route = [[[0, 0, 0]], [[100, 0, 0], [200, -2, 2], [500, -2, 0], [700, 2, 0], [10000, 0, -2]],
                [[100, 0, 0], []]]  # time moving_X moving_Y
    _num = 0
    _interval = 0

    def __init__(self, interval=0):
        self._interval = interval


class EShip(Ship, Pattern):
    _pattern = 0

    def __init__(self, pos_x, pos_y, interval=0, pattern=0, size_x=30, size_y=50, _type=1):
        Ship.__init__(self, pos_x, pos_y, size_x, size_y, _type)
        Pattern.__init__(self, interval)
        self._pattern = pattern

    def update_pos(self):
        self._tick += 1
        route = self._route[self._pattern]

        if route[0][0] + self._interval < self._tick:
            self._spawn = True

        if self._index < len(route):
            if self._spawn:
                self.change_position(route[self._index][1], route[self._index][2])
                if route[self._index][0] + self._interval < self._tick:
                    self._index += 1
        else:
            self.change_position(route[-1][1], route[-1][2])

    def draw(self, screen):
        left = self._pos_x - self._size_x / 2
        top = self._pos_y - self._size_y / 2
        if self._type == 1:
            img = pygame.image.load("./img/enemy1.png")
        elif self._type == 2:
            img = pygame.image.load("./img/enemy2.png")

        img = pygame.transform.scale(img, (self._size_x, self._size_y))
        # pygame.draw.rect(screen, Colors.blue, (left, top, self._size_x, self._size_y))
        screen.blit(img, (self._pos_x-self._size_x/2, self._pos_y-self._size_y/2))


class MyShip(Ship):
    _id = 0

    def __init__(self, pos_x, pos_y, size_x=30, size_y=50, id_=0):
        super().__init__(pos_x, pos_y, size_x, size_y)
        self._id = id_

    def return_id(self):
        return self._id

    def draw(self, screen):
        left = self._pos_x - self._size_x / 2
        top = self._pos_y - self._size_y / 2
        img = pygame.image.load("./img/me.png")
        img = pygame.transform.scale(img, (self._size_x, self._size_y))
        # pygame.draw.rect(screen, Colors.red, (left, top, self._size_x, self._size_y))
        screen.blit(img, (self._pos_x-self._size_x/2, self._pos_y-self._size_y/2))

    def has_collided(self, eship):
        if not eship.has_spawned():
            return False
        if ((self._pos_x + self._size_x/2 >= eship.get_pos_x() - eship.get_width_x()/2) and (self._pos_x - self._size_x/2 <= eship.get_pos_x()) + eship.get_width_x()/2) and (
                (self._pos_y + self._size_y/2 >= eship.get_pos_y() - eship.get_height_y()/2) and (self._pos_y - self._size_y/2 <= eship.get_pos_y() + eship.get_height_y()/2)):
            return True
        return False


class Bullet:
    _pos_x = 0
    _pos_y = 0
    _size_x = 0
    _size_y = 0
    _velocity = 0

    def __init__(self, pos_x, pos_y, velocity, size_x=3, size_y=5):
        self._pos_x = pos_x
        self._pos_y = pos_y
        self._velocity = velocity
        self._size_x = size_x
        self._size_y = size_y

    def get_pos_x(self):
        return self._pos_x

    def get_pos_y(self):
        return self._pos_y

    def get_velocity(self):
        return self._velocity

    def update_pos(self):
        self._pos_y += self._velocity

    def draw(self, screen):
        left = self._pos_x - self._size_x / 2
        top = self._pos_y - self._size_y / 2
        img = pygame.image.load("./img/bullet.png")
        img = pygame.transform.scale(img, (10, 20))
        screen.blit(img, (left - 4, top))
        pygame.draw.rect(screen, Colors.blue, (left, top, self._size_x, self._size_y))

