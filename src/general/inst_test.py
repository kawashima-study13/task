from ..tool.dataclass import Dictm
from ..const import BUTTONS, CODES
from ..mrt.sound import Beep
from ..general.lightbox import LightBox 
from ..general.trigger import Trigger
from ..ppwrapper.interface import Display, Button


def inst_test(display: Display, button: Button, cfg_task: Dictm, cfg_display: Dictm):
    def disp(display: Display, lightbox: LightBox, message: str):
        lightbox.box.draw()
        display.disp_text(message)

    beep_norm = Beep(cfg_task.normal_hz, cfg_task.beep_dursec)
    beep_odd = Beep(cfg_task.odd_hz, cfg_task.beep_dursec)
    trigger = Trigger(cfg_task, mode=cfg_task.trigger_mode)
    button.clear()
    display.build()
    lightbox = LightBox(display.window, cfg_display)
    display.disp_text(f'TEST: Press {BUTTONS.ABORT} and quit.')
    while True:
        key = button.get_keyname()
        if key in BUTTONS.ABORT:
            break
        elif key in BUTTONS.LEFT:
            disp(display, lightbox, "LEFT button (and odd beep)")
            beep_odd.play()
        elif key in BUTTONS.RIGHT:
            disp(display, lightbox, "RIGHT button (and normal beep)")
            beep_norm.play()
        elif key in BUTTONS.MAIN:
            disp(display, lightbox, "MAIN button")
            trigger.write(CODES.MISC)
        elif key in BUTTONS.SUB:
            disp(display, lightbox, "SUB button")
            trigger.write(CODES.MISC)
        elif key in BUTTONS.PULSE:
            disp(display, lightbox, "MRI Pulse")
            trigger.write(CODES.MISC)
        else: 
            disp(display, lightbox, key)


if __name__ == '__main__':
    from ..tool.io import load_config
    from ..ppwrapper.interface import Display, Button


    cfg = load_config('config/task.ini')
    display = Display(cfg.display.size, cfg.display.screen_id,
                      cfg.color.back, cfg.color.main)
    button = Button()
    display.build()
    inst_test(display, button, cfg.mrt)