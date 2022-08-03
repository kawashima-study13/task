import numpy as np
from psychopy import visual

from ..tool.io import load_config


def LightBox(*args, **kwargs):
    return _LightBox(*args, **kwargs)


class _LightBox:
    def __init__(self, window: visual.Window):
        self.window = window

        cfg = load_config('config/task.ini').display
        coef = cfg.coef_lightbox_pos
        boxsize = np.array((cfg.lightbox_size,) * 2)
        self.box = visual.rect.Rect(
            window, size=boxsize, fillColor='White',
            pos=(window.size / [coef, -coef]) + (boxsize / [-2., 2]))

    def draw(self):
        self.box.draw()
        self.window.flip()