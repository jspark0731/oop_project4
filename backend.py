import socket
from json import loads, dumps

from frontend import MyShip, Bullet, EShip, Pattern


class Server:
    _ip = ''
    _port = 0
    _sock = []
    connected = False
    _temp_myships = []
    _ships, _bullets, _myships, _destroyed, _life, _score, _pause = [], [], [], [], 0, 0, False

    def __init__(self, ip='127.0.0.1', port=1234):  # sets ip address and port
        self._ip = ip
        self._port = port

    def set_stage(self, stage=0):  # restores original game start.
        if stage == 0:
            self._ships, self._bullets, self._destroyed, self._life, self._score, self._pause = [], [], [], 0, 0, False
            self.add_ship([EShip(100, 100), EShip(200, 100), EShip(300, 100)])
            for i in range(12):
                for j in range(5):
                    pattern = Pattern(j * 30)
                    self.add_ship([EShip(pattern.get_pos_x(i % 3 + 1), pattern.get_pos_y(i % 3 + 1), j * 30 + i * 700, i % 3 + 1)])

    def client_connect(self):  # connect with client
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server_socket.bind((self._ip, self._port))
        server_socket.listen()
        sock, addr = server_socket.accept()
        self._sock.append(sock)
        print("connected")
        self.connected = True
        self._myships.append(MyShip(100 * len(self._sock), 400))
        return len(self._sock) - 1

    def close_connection(self):  # disconnect with client
        for sock in self._sock:
            sock.shutdown(1)
            sock.close()
        print("closing connection")

    def download(self):  # get data from client
        self._temp_myships = self._myships
        self._myships = []
        temp_pause = []
        for sock in self._sock:
            try:
                data = sock.recv(2048)
                data = data.decode()
                if data == "":  # disconnection error
                    self.connected = False
                    return
                data = loads(data)
                if data == "-1" or data == "":  # disconnection signal
                    self.connected = False
                    return
                if data == "restart":  # restart signal
                    self._myships = self._temp_myships
                    self.set_stage()
                    return
                self._myships.append(MyShip(data['myship'][0], data['myship'][1]))
                for bullet in data['bullet']:
                    self._bullets.append(Bullet(bullet[0], bullet[1], bullet[2]))
                temp_pause.append(data['pause'])
            except Exception as e:
                print("error", e)
        if True in temp_pause:
            self._pause = True
        else:
            self._pause = False

    def upload(self):  # sends data to server
        data = {}
        data['myship'] = []
        for i in self._myships:  # MyShip x, y positions
            data['myship'].append([i.get_pos_x(), i.get_pos_y()])
        data['bullet'] = []
        for i in self._bullets:  # Bullet x, y positions
            data['bullet'].append([i.get_pos_x(), i.get_pos_y(), i.get_velocity()])
        data['ships'] = []
        for i in self._ships:    # EShip x, y positions
            if i.has_spawned():
                data['ships'].append([i.get_pos_x(), i.get_pos_y()])
        data['destroyed'] = self._destroyed

        data['life'] = self._life
        data['score'] = self._score
        data['pause'] = self._pause
        data = dumps(data)

        for sock in self._sock:
            sock.send(data.encode())

    def send(self, data, num):  # Used to send very simple data to client
        data = dumps(data)
        data = data.encode()
        self._sock[num].send(data)

    def add_ship(self, ship):  # adds EShip to Server
        for i in ship:
            self._ships.append(i)

    def calc(self):  # Calculate next step
        if self._pause:
            return
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
                    self._score += 1
                    remove_ship_bullet.append(ship)
                    remove_bullet.append(bullet)
            for myship in self._myships:
                if myship.has_collided(ship):
                    self._life += 1
                    self._score += 1
                    remove_ship_ship.append(ship)

        destroyed = []
        for ship in remove_ship_bullet:
            destroyed.append([ship.get_pos_x(), ship.get_pos_y()])
        self._destroyed = destroyed

        for ship in remove_ship_bullet + remove_ship_ship:
            try:
                self._ships.remove(ship)
            except:
                pass

        for bullet in remove_bullet:
            self._bullets.remove(bullet)


class Client:
    _sock = None
    _ip = ''
    _port = 0

    def __init__(self, ip='127.0.0.1', port=1234):
        self._ip = ip
        self._port = port

    def init(self, ip='127.0.0.1', port=1234):
        self._ip = ip
        self._port = port

    def connect_server(self):  # connect to server
        self._sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self._sock.connect((self._ip, self._port))

    def upload(self, myships, bullets, pause):  # send data to server
        data = {}
        data['myship'] = [myships.get_pos_x(), myships.get_pos_y()]
        data['bullet'] = []
        data['pause'] = pause
        for bullet in bullets:
            data['bullet'].append([bullet.get_pos_x(), bullet.get_pos_y(), bullet.get_velocity()])
        data = dumps(data)
        self._sock.send(data.encode())

    def send(self, data):  # send simple data to server like restart or etc
        self._sock.send(dumps(data).encode())

    def recieve(self):  # recieves very simple data from server, not used
        data = self._sock.recv(1024)
        data = data.decode()
        data = loads(data)
        return data

    def download(self):  # gets data from server
        myships = []
        data = self._sock.recv(2048)
        data = loads(data.decode())
        for i in data['myship']:
            myships.append(MyShip(i[0], i[1]))
        bullets = []
        for bullet in data['bullet']:
            bullets.append(Bullet(bullet[0], bullet[1], bullet[2]))

        ships = []
        for ship in data['ships']:
            ships.append(EShip(ship[0], ship[1]))

        destroyed = data['destroyed']  # [[1,2], [2,3]]
        life = data['life']
        score = data['score']
        pause = data['pause']
        return myships, bullets, ships, destroyed, life, score, pause

    def close(self):  # disconnects from server
        self._sock.shutdown(socket.SHUT_RDWR)
        self.clear_buffer()

    def clear_buffer(self):
        try:
            while self._sock.recv(1024): pass
        except:
            pass


def start_server(cnt=1, port=1234):  # starts up server
    server = Server(port=port)
    server.set_stage()
    for i in range(cnt):
        num = server.client_connect()
        server.send(num, num)
    server.upload()
    while server.connected:
        server.download()
        server.calc()
        server.upload()
    server.close_connection()
    return


if __name__ == '__main__':
    start_server()
