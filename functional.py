import socket
from json import loads, dumps
from time import sleep

import classes


class Server:
    _ip = ''
    _port = 0
    _sock = []
    connected = False
    _ships, _bullets, _myships, _destroyed, _life, _score = [], [], [], [], 0, []

    def init(self, ip='127.0.0.1', port=1234):
        self._ip = ip
        self._port = port

    def client_connect(self):
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server_socket.bind((self._ip, self._port))
        server_socket.listen()
        sock, addr = server_socket.accept()
        self._sock.append(sock)
        print("connected")
        self.connected = True
        self._myships.append(classes.MyShip(100 * len(self._sock), 400))
        return len(self._sock) - 1

    def close_connection(self):
        for sock in self._sock:
            sock.close()

    def download(self):
        self._myships = []
        for sock in self._sock:
            try:
                data = sock.recv(2048)
                data = data.decode()
                if data == "":
                    self.connected = False
                    return
                data = loads(data)
                self._myships.append(classes.MyShip(data['myship'][0], data['myship'][1]))
                for bullet in data['bullet']:
                    self._bullets.append(classes.Bullet(bullet[0], bullet[1], bullet[2]))
            except Exception as e:
                print("error", e)

    def upload(self):
        data = {}
        data['myship'] = []
        for i in self._myships:
            data['myship'].append([i.get_pos_x(), i.get_pos_y()])
        data['bullet'] = []
        for i in self._bullets:
            data['bullet'].append([i.get_pos_x(), i.get_pos_y(), i.get_velocity()])
        data['ships'] = []
        for i in self._ships:
            if i.has_spawned():
                data['ships'].append([i.get_pos_x(), i.get_pos_y()])
        data['destroyed'] = self._destroyed

        data['life'] = self._life
        data['score'] = self._score
        data = dumps(data)

        for sock in self._sock:
            sock.send(data.encode())

    def send(self, data, num):
        data = dumps(data)
        data = data.encode()
        self._sock[num].send(data)

    def add_ship(self, ship):
        for i in ship:
            self._ships.append(i)

    def calc(self):
        remove_ship_bullet, remove_ship_ship, remove_bullet = [], [], []
        for bullet in self._bullets:
            bullet.update_pos()
            if bullet.get_pos_y() < 0:
                remove_bullet.append(bullet)
        for bullet in remove_bullet:
            self._bullets.remove(bullet)
        remove_bullet = []
        self._life = 0
        for ship in self._ships:
            ship.update_pos()
            for bullet in self._bullets:
                if ship.has_collided(bullet):
                    self._score.append("")
                    remove_ship_bullet.append(ship)
                    remove_bullet.append(bullet)
            for myship in self._myships:
                if myship.has_collided(ship):
                    self._life += 1
                    remove_ship_ship.append(ship)

        destroyed = []
        for ship in remove_ship_bullet:
            destroyed.append([ship.get_pos_x(), ship.get_pos_y()])
        self._destroyed = destroyed

        for ship in remove_ship_bullet + remove_ship_ship:
            self._ships.remove(ship)

        for bullet in remove_bullet:
            self._bullets.remove(bullet)


class Client:
    _sock = None
    _ip = ''
    _port = 0

    def init(self, ip='127.0.0.1', port=1234):
        self._ip = ip
        self._port = port

    def connect_server(self):
        self._sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._sock.connect((self._ip, self._port))

    def upload(self, myships, bullets):
        data = {}
        data['myship'] = [myships.get_pos_x(), myships.get_pos_y()]
        data['bullet'] = []
        for bullet in bullets:
            data['bullet'].append([bullet.get_pos_x(), bullet.get_pos_y(), bullet.get_velocity()])
        data = dumps(data)
        self._sock.send(data.encode())

    def send(self, data):
        self._sock.send(dumps(data).encode())

    def recieve(self):
        data = self._sock.recv(1024)
        data = data.decode()
        data = loads(data)
        return data

    def download(self):
        myships = []
        data = self._sock.recv(2048)
        data = loads(data.decode())
        for i in data['myship']:
            myships.append(classes.MyShip(i[0], i[1]))
        bullets = []
        for bullet in data['bullet']:
            bullets.append(classes.Bullet(bullet[0], bullet[1], bullet[2]))

        ships = []
        for ship in data['ships']:
            ships.append(classes.EShip(ship[0], ship[1]))

        destroyed = data['destroyed'] # [[1,2], [2,3]]

        life = data['life']

        score = data['score']

        return myships, bullets, ships, destroyed, life, score

    def close(self):
        self._sock.close()


def start_server(cnt=1):
    server = Server()
    server.init()
    server.add_ship([classes.EShip(100, 100), classes.EShip(200, 100), classes.EShip(300, 100)])
    for i in range(5):
        server.add_ship([classes.EShip(1000, 100, i * 60, 1)])
    for i in range(cnt):
        num = server.client_connect()
        server.send(num, num)
    server.upload()
    while server.connected:
        server.download()
        server.calc()
        server.upload()
    server.close_connection()


if __name__ == '__main__':
    start_server()
