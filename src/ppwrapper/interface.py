from __future__ import annotations
from typing import Literal, Sequence
from sys import stdout
from typing import Optional

from psychopy import visual  # visual must be imported 1st
from psychopy.hardware import keyboard
from psychopy import core, clock, event

from ..const import BUTTONS


class Display:
    def __init__(self, size: tuple[int, int] | Literal['full']=(1000, 1000),
                 screen_id: int=0,
                 bgcolor: tuple[int, int, int]=(0,) * 3,
                 txtcolor: tuple[int, int, int]=(100,) * 3):
        
        self.full = size == 'full'
        self.size = size if isinstance(size, tuple) else (1., 1.)
        self.screen_id = screen_id
        self.bgcolor = bgcolor
        self.txtcolor = txtcolor
        self.is_built = False

    def build(self):
        self.window = visual.Window(
            color=self.bgcolor,
            screen=self.screen_id,
            colorSpace='rgb255',
            fullscr=self.full,
            size=self.size,
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
        self.is_built = False
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
    def __init__(self, itvl_input: float=.05):
        self.kb = keyboard.Keyboard()
        self.itvl_input = itvl_input
        self.abort = False

    def glob_key_event(self, key: str):
        if key in BUTTONS.ABORT:
            self.abort = True
            return True
        if key in BUTTONS.SKIP:
            return True
        return False

    def clear(self): # Psychopy's keyboard clear doesn't work
        event.clearEvents()
        for buffer in self.kb._buffers.values():
            buffer.flush()
            buffer._evts.clear()
            buffer._keys.clear()
            buffer._keysStillDown.clear()

    def reset_clock(self):
        self.kb.clock.reset()

    def wait_keys(
        self, keys: Optional[Sequence]=None, maxsec: float=float('inf')):

        self.clear()
        if keys:
            keys = list(keys)
            keys += (BUTTONS.ABORT + BUTTONS.SKIP)
        pressed_keys = self.kb.waitKeys(
            maxWait=maxsec, keyList=keys, waitRelease=True)
        self.glob_key_event(pressed_keys[0])

    def wait(self, sec: float):
        t0 = clock.Clock()
        while t0.getTime() <= sec:
            core.wait(self.itvl_input)
            if self.glob_key_event(self.get_keyname()):
                break

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

    def get_keyname(self, keys: Optional[Sequence]=None,
                    at_release: bool=False):
        if keys:
            keys = list(keys)
            keys += (BUTTONS.ABORT + BUTTONS.SKIP)
        pressed_keys = self.kb.getKeys(keyList=keys, waitRelease=at_release)
        return pressed_keys[0].name if pressed_keys else None


if __name__ == '__main__':
    from ..tool.io import load_config


    cfg = load_config('config/task.ini')
    display = Display(cfg.display.size, cfg.display.screen_id,
                      cfg.color.back, cfg.color.main)
    button = Button()

    display.build()

    display.disp_text('STDタイマーで待機テスト (press any key)')
    button.wait_with_stdtimer()

    display.close()
    input('Test close and build, press enter:')
    display.build()

    for num in [1, 2, 3]:
        display.disp_text(str(num))
        button.wait(sec=1.)

    display.disp_text('Test keys, and press abort key to quit')
    while True:
        core.wait(.1)
        key = button.get_keyname()
        if key:
            print(key)
        if key in BUTTONS.ABORT:
            core.quit()