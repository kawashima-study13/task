from pyxid2 import get_xid_devices


class XID:
    def __init__(self, pulse_dursec: float):
        while True:
            devices = get_xid_devices()
            if len(devices) == 1:
                break
            if len(devices) == 0:
                print('No XID devices found.')
            if len(devices) > 1:
                print('More than one device found.')
            input('Press Enter key to retry.')
        self.xid = devices[0]
        SEC_TO_MSEC = 1000
        self.xid.set_pulse_duration(
            int(pulse_dursec * SEC_TO_MSEC))

    def write(self, code: int):
        self.xid.activate_line(bitmask=code)


if __name__ == '__main__':
    xid = XID(0.01)
    input('Press Enter key and test simultaneous write')
    for x in range(1, 20):
        xid.write(x)
    while True:
        code = input('Input int: ')
        xid.write(int(code))