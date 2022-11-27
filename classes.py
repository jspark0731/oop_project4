import pygame

size_x = 30
size_y = 50
bullet_size_x = 3
bullet_size_y = 5


class Colors:
    white = (255, 255, 255)
    red = (255, 0, 0)
    blue = (0, 0, 255)
    green = (0, 255, 0)
    black = (0, 0, 0)


class Load_image:
    enemy1_img = pygame.image.load("./img/enemy1.png")
    enemy1_img = pygame.transform.scale(enemy1_img, (size_x, size_y))

    enemy2_img = pygame.image.load("./img/enemy2.png")
    enemy2_img = pygame.transform.scale(enemy2_img, (size_x, size_y))

    myship_img = pygame.image.load("./img/me.png")
    myship_img = pygame.transform.scale(myship_img, (size_x, size_y))

    bullet_img = pygame.image.load("./img/bullet.png")
    bullet_img = pygame.transform.scale(bullet_img, (10, 20))


class Ship:
    _pos_x = 0
    _pos_y = 0
    _size_x = 0
    _size_y = 0
    _type = 1
    _spawn = False

    def __init__(self, pos_x, pos_y, _type=1):
        self._pos_x = pos_x
        self._pos_y = pos_y
        self._size_x = size_x
        self._size_y = size_y
        self._type = _type

    def has_collided(self, bullet):
        if not self._spawn:
            return False
        if ((self._pos_x + 16.4 >= bullet.get_pos_x()) and (self._pos_x - 16.4 <= bullet.get_pos_x())) and (
                (self._pos_y + 25.4 >= bullet.get_pos_y()) and (self._pos_y - 25.4 <= bullet.get_pos_y())):
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
    _route = [[[0, 0, 0]], [[100, 0, 0], [200, -2, 2], [500, -2, 0], [700, 0, 2], [900, 2, 0], [10000, 0, -2]],
              [[100, 0, 0], [300, 2, 2], [500, 2, 0], [700, 0, 2], [900, -2, 0], [10000, 0, -2]],
              [[100, 0, 0], [300, 2, -2], [400, -2, 0], [600, 2, 3], [10000, 0, -2]]]  # time moving_X moving_Y
    _num = 0
    _interval = 0
    _start_position = [[0, 0], [1000, 100], [-100, 100], [-100, 800]]

    def __init__(self, interval=0):
        self._interval = interval

    def get_pos_x(self, num):
        return self._start_position[num][0]

    def get_pos_y(self, num):
        return self._start_position[num][1]


class EShip(Ship, Pattern):
    _pattern = 0

    def __init__(self, pos_x, pos_y, interval=0, pattern=0, _type=1):
        Ship.__init__(self, pos_x, pos_y, _type)
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
        if self._type == 1:
            screen.blit(Load_image.enemy1_img, (self._pos_x - self._size_x / 2, self._pos_y - self._size_y / 2))
        elif self._type == 2:
            screen.blit(Load_image.enemy2_img, (self._pos_x - self._size_x / 2, self._pos_y - self._size_y / 2))


class MyShip(Ship):
    _id = 0

    def __init__(self, pos_x, pos_y, id_=0):
        super().__init__(pos_x, pos_y)
        self._id = id_

    def return_id(self):
        return self._id

    def draw(self, screen):
        screen.blit(Load_image.myship_img, (self._pos_x - self._size_x / 2, self._pos_y - self._size_y / 2))

    def has_collided(self, eship):
        if not eship.has_spawned():
            return False
        if (((self._pos_x - eship.get_pos_x() <= self._size_x / 2 + eship.get_width_x() / 2) and (
                self._pos_x - eship.get_pos_x() >= - self._size_x / 2 - eship.get_width_x() / 2)) and (
                (self._pos_y - eship.get_pos_y() <= self._size_y / 2 + eship.get_height_y() / 2) and (
                self._pos_y - eship.get_pos_y() >= - self._size_y / 2 - eship.get_height_y() / 2))):
            return True
        return False


class Bullet:
    _pos_x = 0
    _pos_y = 0
    _size_x = 0
    _size_y = 0
    _velocity = 0

    def __init__(self, pos_x, pos_y, velocity):
        self._pos_x = pos_x
        self._pos_y = pos_y
        self._velocity = velocity
        self._size_x = bullet_size_x
        self._size_y = bullet_size_y

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

        screen.blit(Load_image.bullet_img, (left - 4, top))
        # pygame.draw.rect(screen, Colors.blue, (left, top, self._size_x, self._size_y))
