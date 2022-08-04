import numpy as np
from psychopy import visual

from ..tool.dataclass import Dictm


def LightBox(*args, **kwargs):
    return _LightBox(*args, **kwargs)


class _LightBox:
    def __init__(self, window: visual.Window, cfg_display: Dictm):
        self.window = window

        coef = cfg_display.coef_lightbox_pos
        boxsize = np.array((cfg_display.lightbox_size,) * 2)
        self.box = visual.rect.Rect(
            window, size=boxsize, fillColor='White',
            pos=(window.size / [coef, -coef]) + (boxsize / [-2., 2]))

    def draw(self):
        self.box.draw()
        self.window.flip()


if __name__ == '__main__':
    from ..tool.io import load_config
    from ..ppwrapper.interface import Display


    cfg = load_config('config/task.ini')
    display = Display((1840, 1280), cfg.display.screen_id,
                      cfg.color.back, cfg.color.main)
    display.build()

    lightbox = LightBox(display.window, cfg.display)
    while True:
        lightbox.draw()