from __future__ import annotations
from typing import Optional
from pathlib import Path

from psychopy import visual

from ..tool.io import load_config
from ..tool.dataclass import Dictm
from ..const import BUTTONS
from ..ppwrapper.interface import Display
from ..general.lightbox import LightBox


class Probe:
    def __init__(self, window: visual.Window, filename_intro: str,
                 cfg_colorname: Dictm, rate_y_text: float, textsize: float=24.,
                 wait_sec: float=0., lightbox: Optional[LightBox]=None):
        RATE_INTRO = 1.
        POS_RATE_Y_PROBE = .6 # 1.0 bottom
        N_TICKS = 5
        START_TICK = 2

        pos_y_probe = (window.size[1] / -2.) * POS_RATE_Y_PROBE
        pos_y_text = (window.size[1] / -2.) * rate_y_text

        self.window = window
        self.lightbox = lightbox
        self.additional_text = visual.TextStim(
            window, text='', pos=(0., pos_y_text), color=cfg_colorname.main,
            height=textsize)

        path = Path(__file__).parent / filename_intro
        self.intro = visual.ImageStim(window, image=path, units='norm')
        self.intro.size = self.intro.size / self.intro.size[0] * RATE_INTRO

        self.scale = visual.RatingScale(
            win=window,
            low=0, high=N_TICKS - 1,
            pos=(0., pos_y_probe),
            labels=('', ''),
            scale=None,
            marker='glow',
            markerStart=START_TICK,
            markerColor=cfg_colorname.highlight,
            lineColor=cfg_colorname.main,
            showValue=False,
            showAccept=False,
            acceptKeys=BUTTONS.SUB,
            leftKeys=BUTTONS.LEFT,
            rightKeys=BUTTONS.RIGHT,
            skipKeys=None,
            noMouse=True,
            maxTime=wait_sec,
            )


    def present(self, text: str='') -> int | None:
        self.window.winHandle.activate()
        self.additional_text.setText(text)
        while self.scale.noResponse:
            self.additional_text.draw()
            self.intro.draw()
            self.scale.draw()
            if self.lightbox:
                self.lightbox.box.draw()  # type: ignore # lightbox.draw() duplicates .flip()
            self.window.flip()
        if self.scale.timedOut:
            self.scale.reset()
            return None
        rate = self.scale.getRating()
        self.scale.reset()
        return rate


if __name__ == '__main__':
    cfg = load_config('config/task.ini')
    display = Display((1280, 960), cfg.display.screen_id,
                      cfg.color.back, cfg.color.main)
    display.build()

    print('Probe for simultaneous recording')
    probe = Probe(display.window, 'intro.jpg', cfg.color_name, rate_y_text=-.2,
                  textsize=48., wait_sec=5.,
                  lightbox=LightBox(display.window, cfg.display))
    print(probe.present('12/18'))