import socket

from tqdm import tqdm


LARGENUM = 1024

class Server:
    def __init__(self, host: str='127.0.0.1', port: int=50000):
        self.total: int = 1
        self.i: int = 0

        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(None)
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind((host, port))
        s.listen()
        print('Waiting for connection...')
        self.client, _ = s.accept()
        self.client.settimeout(None)
        print('... connected!')

        while True:
            code = self.client.recv(LARGENUM)
            code = code.decode('utf-8')
            self.proc_code(code)
            self.send('ok')

    def send(self, message):
        self.client.send(message.encode('utf-8'))
    
    def proc_code(self, code: str):
        code = code.split(':')
        if code[0] == 'total':
            self.total = int(code[1])
        if code[0] == 'initial':
            self.initial = int(code[1])
        if code[0] == 'start':
            self.start()
        if code[0] == 'update':
            self.bar.update(int(code[1]))

    def start(self):
        self.bar = tqdm(initial=self.initial, total=self.total)


class ProgressBar:
    def __init__(self, initial: int, total: int,
                 host: str='127.0.0.1', port: int=50000, off: bool=False):
        if off:
            self.off = True
            return
        self.off = False
        while True:
            try:
                self.server = socket.create_connection((host, port), timeout=2)
            except:
                input('Connection failed, press ENTER to continue')
                self.off = True
                return
            break
        self._send(f'initial:{initial}')
        self._send(f'total:{total}')

    def _send(self, code):
        if self.off: return
        self.server.send(code.encode('utf-8'))
        self.server.recv(LARGENUM)

    def start(self):
        self._send('start')

    def update(self, i):
        self._send(f'update:{i}')


if __name__ == '__main__':
    from time import sleep
    from threading import Thread

    def send(s, code):
        s.send(code.encode('utf-8'))
        s.recv(1024)

    TOTAL = 10

    thread = Thread(target=lambda: Server())
    thread.start()

    sleep(1.)

    pbar = ProgressBar(0, TOTAL)
    pbar.start()
    for i in range(TOTAL):
        sleep(1.)
        pbar.update(1)
