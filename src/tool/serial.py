import serial


class Serial:
    def __init__(self, comname: str, rate: float=9600.):
        self.ser = serial.Serial(comname, rate)

    def write(self, code: str):
        self.ser.write(code.encode('utf-8'))

    def write_print(self, code: str):
        self.write(code)
        print(code)

    def close(self):
        self.ser.close()


if __name__ == '__main__':
    from time import sleep

    
    PORT = 'COM3'
    
    ser = Serial(PORT)

    ser.write_print('test1 ')
    sleep(.5)
    ser.write_print('test2 ')
    sleep(.5)
    ser.write_print('test3 ')
    sleep(.5)
    for x in '12345678901234567890':
        ser.write_print(x)
    ser.close()
