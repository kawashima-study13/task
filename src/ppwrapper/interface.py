from __future__ import annotations
from sys import stdout
from typing import Optional

from psychopy import visual  # visual must be imported 1st
from psychopy.hardware import keyboard
from psychopy import core, clock, event

from ..const import BUTTONS


class Display:
    def __init__(self, full: bool=False,
                 bgcolor: tuple[int, int, int]=(0,) * 3,
                 txtcolor: tuple[int, int, int]=(100,) * 3):
        self.full = full
        self.bgcolor = bgcolor
        self.txtcolor = txtcolor
        self.is_built = False

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
            font='YuGothic',
            pos=(0., 0.),
            height=40,
            color=self.txtcolor,
            colorSpace='rgb255',
            alignText='center',
            units='pix')

        self.is_built = True

    def close(self):
        self.window.close()

    def disp_text(self, text: str | list[str] | tuple[str]):
        """
        If list or tuple, contents will be concatenated as new line.
        """
        if isinstance(text, (list, tuple)):
            text = '\n'.join(text)
        self.text.text = text
        self.text.draw()
        self.window.flip()


class Button:
    def __init__(self, itvl_input=.05):
        self.kb = keyboard.Keyboard()
        self.itvl_input = itvl_input

    def clear(self): # Psychopy's keyboard clear doesn't work
        event.clearEvents()
        for buffer in self.kb._buffers.values():
            buffer.flush()
            buffer._evts.clear()
            buffer._keys.clear()
            buffer._keysStillDown.clear()

    def reset_clock(self):
        self.kb.clock.reset()

    def wait_key(
        self, keys: Optional[list | tuple]=None, maxsec: float=float('inf')):

        if keys:
            keys = tuple(keys)
            keys + (BUTTONS.ABORT,)
        keys = self.kb.waitKeys(maxWait=maxsec, keyList=keys, waitRelease=True)
        if keys[0] in BUTTONS.ABORT:
            core.quit()

    def wait(self, sec: float):
        t0 = clock.Clock()
        while t0.getTime() <= sec:
            core.wait(self.itvl_input)
            key = self.get_keyname()
            if key in BUTTONS.ABORT:
                core.quit()

    def wait_with_stdtimer(self):
        t0 = clock.Clock()
        stdout.write('\n')
        stdout.flush()
        while True:
            core.wait(self.itvl_input)
            inputs = self.get_keyname()
            if inputs:
                break
            stdout.write('\r===== {:.1f} sec. ====='.format(t0.getTime()))
            stdout.flush()

    def get_keyname(self):
        keys = self.kb.getKeys()
        return keys[0].name if keys else None


if __name__ == '__main__':
    display = Display()
    button = Button()

    display.build()

    display.disp_text('STDタイマーで待機テスト (press any key)')
    button.wait_with_stdtimer()
    for num in [1, 2, 3]:
        display.disp_text(num)
        button.wait(sec=1.)

    display.disp_text('Test keys, and press abort key to quit')
    while True:
        core.wait(.1)
        key = button.get_keyname()
        if key:
            print(key)
        if key in BUTTONS.ABORT:
            core.quit()
