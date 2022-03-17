from psychopy import core

from ..const import BUTTONS
from ..general.lightbox import LightBox 


def inst_test(display, button):
    def disp(display, lightbox, message):
        lightbox.box.draw()
        display.disp_text(message)

    button.clear()
    display.build()
    lightbox = LightBox(display.window)
    display.disp_text(f'TEST: Press {BUTTONS.ABORT} and quit.')
    while True:
        key = button.get_keyname()
        if key in BUTTONS.ABORT:
            break
        elif key in BUTTONS.LEFT:
            disp(display, lightbox, "LEFT button")
        elif key in BUTTONS.RIGHT:
            disp(display, lightbox, "RIGHT button")
        elif key in BUTTONS.MAIN:
            disp(display, lightbox, "MAIN button")
        elif key in BUTTONS.SUB:
            disp(display, lightbox, "SUB button")
        elif key in BUTTONS.PULSE:
            disp(display, lightbox, "MRI Pulse")
        else: 
            disp(display, lightbox, key)
    display.close()


if __name__ == '__main__':
    from ..tool.io import load_config
    from ..ppwrapper.interface import Display, Button


    cfg = load_config('config/task.ini')
    display = Display(cfg.display.size, cfg.display.screen_id,
                      cfg.color.back, cfg.color.main)
    button = Button()
    display.build()
    inst_test(display, button)