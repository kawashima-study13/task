from ..ppwrapper.interface import Display, Button
from ..const import BUTTONS


def fixation(display: Display, button: Button):
    button.clear()
    display.build()
    display.disp_text('+')
    while True:
        key = button.get_keyname()
        if key in BUTTONS.ABORT:
            break


if __name__ == '__main__':
    from src.ppwrapper.interface import Display, Button


    display = Display()
    button = Button()
    fixation(display, button)
