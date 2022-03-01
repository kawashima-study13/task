from pathlib import Path
from psychopy import visual

from ..const import BUTTONS
from src.ppwrapper.interface import Display


class Probe:
    def __init__(self, window):
        self.window = window

        path = Path(__file__).parent / 'intro.png'
        self.intro = visual.ImageStim(window, image=path)

        N_TICKS = 5
        START_TICK = 2
        self.scale = visual.RatingScale(
            win=window,
            low=0, high=N_TICKS - 1,
            labels=('', ''),
            scale=None,
            marker='glow',
            markerStart=START_TICK,
            showValue=False,
            showAccept=False,
            acceptKeys=BUTTONS.SUB,
            leftKeys=BUTTONS.LEFT,
            rightKeys=BUTTONS.RIGHT,
            skipKeys=None,
            noMouse=True,
            )
        ...

    def present(self):
        while self.scale.noResponse:
            self.intro.draw()
            self.scale.draw()
            self.window.flip()
        rate = self.scale.getRating()
        self.scale.reset()
        return rate


if __name__ == '__main__':
    display = Display()
    display.build()
    probe = Probe(display.window)
    print(probe.present())