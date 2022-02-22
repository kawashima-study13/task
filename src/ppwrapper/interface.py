from sys import stdout

from psychopy import visual  # visual must be imported 1st
from psychopy.hardware import keyboard
from psychopy import core, clock

from ..const import BUTTONS


class Display:
    def __init__(self, full=False, bgcolor=(0,) * 3, txtcolor=(100,) * 3):
        self.full = full
        self.bgcolor=bgcolor
        self.txtcolor=txtcolor

    def build(self):
        self.window = visual.Window(
            color=self.bgcolor,
            screen=1,
            colorSpace='rgb255',
            fullscr=self.full,
            size=(1200, 1200),
            allowGUI=(not self.full),
            winType='pyglet',
            units='pix',
            gammaErrorPolicy='ignore')

        self.text = visual.TextStim(
            win=self.window,
            pos=(0., 0.),
            height=40,
            color=self.txtcolor,
            colorSpace='rgb255',
            alignText='center',
            units='pix')

    def close(self):
        self.window.close()

    def disp_text(self, text):
        self.text.text = text
        self.text.draw()
        self.window.flip()


class Button:
    def __init__(self):
        self.kb = keyboard.Keyboard()

    def wait_till(self, keys, maxsec=float('inf')):
        if keys:
            keys += BUTTONS.ABORT
        keys = self.kb.waitKeys(maxWait=maxsec, keyList=keys, waitRelease=True)
        if keys[0] in BUTTONS.ABORT:
            core.quit()

    def get_key(self):
        keys = self.kb.getKeys()
        return keys[0].name if keys else None

    def wait(self, sec):
        abortkey = self.kb.waitKeys(maxWait=sec, keyList=BUTTONS.ABORT)
        if abortkey:
            core.quit()

    def wait_with_stdtimer(self):
        t0 = clock.Clock()
        stdout.write('\n')
        stdout.flush()
        while True:
            inputs = self.get_key()
            if inputs:
                break
            stdout.write('\r===== {:.1f} sec. ====='.format(t0.getTime()))
            stdout.flush()


if __name__ == '__main__':
    display = Display()
    button = Button()

    display.build()
    display.disp_text('Wait with stdtimer (press any key)')
    button.wait_with_stdtimer()
    for num in [1, 2, 3]:
        display.disp_text(num)
        button.wait(sec=1.)
    display.disp_text('Press any key and continue.')
    button.wait_till(keys=None)
    display.disp_text('Test keys, and press abort key to quit')
    while True:
        core.wait(.1)
        key = button.get_key()
        if key:
            print(key)
        if key in BUTTONS.ABORT:
            core.quit()
