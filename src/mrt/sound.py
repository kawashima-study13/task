from threading import Thread
import warnings
import platform
from os import system

from psychopy import prefs
from psychopy.sound import Sound

if platform.system() == 'Windows':
    import winsound


class Beep:
    def __init__(self, hz: float, dursec: float,
                 use_psychopy: bool=True, multithread: bool=True):
        if use_psychopy:
            prefs.hardware['audioLib'] = ['PTB']
            self.player = Sound(hz, secs=dursec)
        else:
            warnings.warn('Psychopy is not used, time lag suspected.')
            if platform.system() == 'Windows':
                self.player = _WindowsBeep(hz, dursec, multithread)
            else:
                self.player = _MacBeep(hz, dursec, multithread)

    def play(self):
        self.player.play()


class OSBeep:
    def __init__(self, hz: float, dursec: float, multithread: bool):
        self.multithread = multithread
        self.hz = hz
        self.dursec = dursec

    def play(self):
        if self.multithread:
            subthread = Thread(target=self._play)
            subthread.start()
        else:
            self._play()


    def _play(self):
        ...


class _WindowsBeep(OSBeep):
    def __init__(self, hz: float, dursec: float, multithread: bool):
        super().__init__(hz, dursec)

    def _play(self):
        winsound.Beep(self.hz, self.dursec)


class _MacBeep(OSBeep):
    def __init__(self, hz: float, dursec: float, multithread: bool):
        super().__init__(hz, dursec)

    def _play(self):
        # Need SoX library. brew install sox
        system('play -qn synth %s sin %s' % (self.dursec, self.hz))


if __name__ == '__main__':
    from time import sleep

    def test(use_psychopy):
        beep_a = Beep(500., 1., use_psychopy)
        beep_b = Beep(1000., .5, use_psychopy)
        beep_a.play()
        sleep(1.)
        beep_b.play()
        sleep(1.)
        beep_a.play()

    print('Test OS-based')
    test(False)
    print('Test Psychopy-based')
    test(True)