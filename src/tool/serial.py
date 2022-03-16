from __future__ import annotations
from threading import Thread
from time import sleep
import serial


class Serial:
    def __init__(self, comname: str, rate: float=9600., dursec: float=.01):
        self.OFFCODE = 0
        self.dursec = dursec
        self.ser = serial.Serial(comname, rate)
    
    def write(self, code: str | int):
        subthread = Thread(target=self._write, args=(code,))
        subthread.start()

    def _write(self, code: str | int):
        if isinstance(code, str):
            self.ser.write(code.encode('utf-8'))
        else:
            self.ser.write(code.to_bytes(2, 'big'))
        sleep(self.dursec)
        self.ser.write(self.OFFCODE.to_bytes(2, 'big'))

    def write_print(self, code: str):
        self.write(code)
        print(code)

    def close(self):
        self.ser.close()


if __name__ == '__main__':
    ser = Serial(input('Port: '))

    for x in '12345678901234567890':
        ser.write(x)
    while True:
        code = input('Input (eval): ')
        ser.write(eval(code))
