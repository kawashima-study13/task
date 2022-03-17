from pathlib import Path

import numpy as np
from psychopy import visual

from ..tool.io import load_config
from ..const import BUTTONS
from ..ppwrapper.interface import Display
from ..general.lightbox import LightBox


class Probe:
    def __init__(self, window):
        RATE_INTRO = 1.
        POS_RATE_Y_PROBE = .6 # 1.0 bottom
        N_TICKS = 5
        START_TICK = 2

        self.window = window

        path = Path(__file__).parent / 'intro.jpg'
        self.intro = visual.ImageStim(window, image=path, units='norm')
        self.intro.size = self.intro.size / self.intro.size[0] * RATE_INTRO

        pos_y = (window.size[1] / -2.) * POS_RATE_Y_PROBE
        cfg = load_config('config/task.ini')
        color = cfg.color_name
        N_TICKS = 5
        START_TICK = 2
        self.scale = visual.RatingScale(
            win=window,
            low=0, high=N_TICKS - 1,
            pos=(0., pos_y),
            labels=('', ''),
            scale=None,
            marker='glow',
            markerStart=START_TICK,
            markerColor=color.highlight,
            lineColor=color.main,
            showValue=False,
            showAccept=False,
            acceptKeys=BUTTONS.SUB,
            leftKeys=BUTTONS.LEFT,
            rightKeys=BUTTONS.RIGHT,
            skipKeys=None,
            noMouse=True,
            )

        self.lightbox = LightBox(window)

    def present(self):
        while self.scale.noResponse:
            self.intro.draw()
            self.scale.draw()
            self.lightbox.box.draw()
            self.window.flip()
        rate = self.scale.getRating()
        self.scale.reset()
        return rate


if __name__ == '__main__':
    cfg = load_config('config/task.ini')
    display = Display(cfg.display.size, cfg.display.screen_id,
                      cfg.color.back, cfg.color.main)
    display.build()
    probe = Probe(display.window)
    print(probe.present())