from typing import Literal

from ..tool.dataclass import Dictm
from ..tool.serial import Serial
from ..const import CODES_TO_LOG


class Trigger:
    class DammyWriter:
        def write(*args, **kwargs):
            pass

    def __init__(self, cfg: Dictm, mode: Literal['off', 'serial', 'xid']):
        if mode == 'off':
            self.writer = self.DammyWriter()
        try:
            if mode == 'serial':
                self.writer = Serial(cfg.comname, dursec=cfg.pulse_dursec)
            if mode == 'xid':
                from ..tool.xid import XID  # error if driver is not installed
                self.writer = XID(pulse_dursec=cfg.pulse_dursec)
        except:
            input('Trigger connection failed, press ENTER to continue')
            self.writer = self.DammyWriter()

    def write(self, code):
        if (CODES_TO_LOG is None) or (code in CODES_TO_LOG):
            self.writer.write(int(code[1:]))
