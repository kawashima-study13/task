from threading import Thread
import warnings
import platform
from os import system

from psychopy import prefs
from psychopy.sound import Sound

if platform.system() == 'Windows':
    import winsound


class Beep:
    def __init__(self, hz: float, dursec: float):
        prefs.hardware['audioLib'] = ['PTB']
        try:
            self.player = Sound(hz, secs=dursec)
        except:
            warnings.warn('\n'.join([
                "Coud not use Psychopy's Sound.",
                "Time lag is suspected"]))
            if platform.system() == 'Windows':
                self.player = _WindowsBeep(hz, dursec)
            else:
                self.player = _MacBeep(hz, dursec)

    def play(self):
        self.player.play()


class BeepBase:
    def __init__(self, hz: float, dursec: float):
        self.hz = hz
        self.dursec = dursec

    def play(self):
        subthread = Thread(target=self._play)
        subthread.start()

    def _play(self):
        ...


class _WindowsBeep(BeepBase):
    def __init__(self, hz: float, dursec: float):
        super().__init__(hz, dursec)

    def _play(self):
        winsound.Beep(self.hz, self.dursec)


class _MacBeep(BeepBase):
    def __init__(self, hz: float, dursec: float):
        super().__init__(hz, dursec)

    def _play(self):
        # Need SoX library. brew install sox
        system('play -n synth %s sin %s' % (self.dursec, self.hz))


if __name__ == '__main__':
    from time import sleep
    beep_a = Beep(500., 1.)
    beep_b = Beep(1000., .5)
    beep_a.play()
    sleep(1.)
    beep_b.play()
    sleep(1.)
    beep_a.play()
