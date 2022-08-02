from __future__ import annotations
from typing import Any
import socket

from tqdm import tqdm


LARGENUM = 1024

class Server:
    def __init__(self, host: str='127.0.0.1', port: int=50000):
        self.total: int = 1
        self.i: int = 0

        while True:
            self._wait_to_connect(host, port)
            while True:
                try:
                    code = self.client.recv(LARGENUM)
                    code = code.decode('utf-8')
                    self.proc_code(code)
                    self.client.send('ok'.encode('utf-8'))
                except (ConnectionResetError, ConnectionAbortedError):
                    print('Connection closed.\n')
                    if hasattr(self, 'bar'):
                        self.bar.close()
                    break
    
    def _wait_to_connect(self, host: str, port: int):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(None)
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind((host, port))
        s.listen()
        print('Waiting for connection...')
        self.client, _ = s.accept()
        self.client.settimeout(None)
        print('... connected!')
    
    def proc_code(self, code: str):
        codes = code.split(':')
        if codes[0] == 'total':
            self.total = int(codes[1])
        if codes[0] == 'initial':
            self.initial = int(codes[1])
        if codes[0] == 'start':
            self.start()
        if codes[0] == 'update':
            self.bar.update(int(codes[1]))

    def start(self):
        self.bar = tqdm(initial=self.initial, total=self.total)


class ProgressBar:
    def __init__(self, initial: int, total: int,
                 host: str='127.0.0.1', port: int=50000, use: bool=True):
        if not use:
            self.off = True
            return
        self.off = False
        while True:
            try:
                self.server = socket.create_connection((host, port), timeout=2)
                break
            except:
                if input('Pbar connection failed, n to retry: ') != 'n':
                    self.off = True
                    return
        self._send(f'initial:{initial}')
        self._send(f'total:{total}')

    def _send(self, code: str):
        if self.off: return
        self.server.send(code.encode('utf-8'))
        self.server.recv(LARGENUM)

    def start(self):
        self._send('start')

    def update(self, i: int | str):
        self._send(f'update:{i}')

    def close(self):
        self.server.close()


if __name__ == '__main__':
    from time import sleep
    from threading import Thread

    def send(s, code):
        s.send(code.encode('utf-8'))
        s.recv(1024)

    def task():
        TOTAL = 5
        pbar = ProgressBar(0, TOTAL)
        pbar.start()
        for _ in range(TOTAL):
            sleep(1.)
            pbar.update(1)
        pbar.close()

    thread = Thread(target=lambda: Server())
    thread.start()

    sleep(1.)
    task()
    sleep(1.)
    task()
