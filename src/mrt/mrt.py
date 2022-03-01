from __future__ import annotations

import pandas as pd
from psychopy import core

from ..const import BUTTONS, CODES
from ..probe.probe import Probe
from ..ppwrapper.task import Task
from .sound import Beep


class MRT(Task):
    def __init__(self, display, button,
                 stimset: tuple[tuple], cfg: dict, o_path: str | Path):
        super().__init__(display, button, stimset, cfg, o_path)
        self.data = []

    def _run_task_head(self):
        params = self.cfg.odd_hz, self.cfg.beep_dursec, self.cfg.use_ppsound
        self.probe = Probe(self.display.window)
        self.beep = dict(odd=Beep(*params), normal=Beep(*params))

        super()._run_task_head()
        self.display.disp_text('Press any key to start.')
        self.button.wait_key(keys=None)
        self.display.disp_text('+')
        self.button.clear()

    def _run_block_tail(self):
        self.log('--- Probe presented', CODES.PROBE)
        rate = self.probe.present()
        self.log(f'---- Answer: {rate}', CODES.CHOICE, rate)
        self.display.disp_text('+')

    def _run_trial(self, stim: str):
        dursec_trial = sum([self.cfg.itvl_sec_pre,
                            self.cfg.beep_dursec,
                            self.cfg.itvl_sec_post])

        super()._run_trial()
        while self.timer.trial.getTime() <= self.cfg.itvl_sec_pre:
            core.wait(self.button.itvl_input)
            self._get_press()
        self._present_beep(odd=int(stim) > 0, dursec=self.cfg.beep_dursec)
        while self.timer.trial.getTime() <= dursec_trial:
            core.wait(self.button.itvl_input)
            self._get_press()

    def _get_press(self):
        if key := self.button.get_keyname():
            if key in BUTTONS.ABORT:
                core.quit()
            self.log('---- {} was pressed ({:.6f}; {:.6f})'.format(
                key, self.timer.trial.getTime(), self.timer.task.getTime()),
                CODES.MRT_PRESSED)

    def _present_beep(self, odd: bool, dursec: float):
        type = 'odd' if odd else 'normal'
        self.log(f'--- Present {type} stim {dursec} sec.', CODES.MRT_BEEP)
        self.beep[type].play()

    def log(self, message: str | tuple, code: str, value=None):
        super().log(message, code)
        self.data.append([
            self.progress.block, self.progress.trial, code,
            self.timer.task.getTime(), self.timer.block.getTime(),
            self.timer.trial.getTime(), value])

    def _run_task_tail(self):
        super()._run_task_tail()
        data = pd.DataFrame(self.data)
        data.columns = ['block', 'trial', 'code',
                        'sec_task', 'sec_block', 'sec_trial', 'value']
        data.to_csv(self.o_path, index=False)


if __name__ == '__main__':
    from os import system
    from pathlib import Path
    from src.tool.io import load_config, load_csv
    from src.ppwrapper.interface import Display, Button


    log_path = Path('src/mrt/debug/debug.csv.log')
    log_path.unlink(missing_ok=True)

    display = Display()
    button = Button()
    display.build()

    cfg = load_config('config/task.ini').mrt
    stimset = load_csv('src/mrt/stim/stim_dbg.csv')
    mrt = MRT(display, button, stimset, cfg,
              o_path=log_path.parent / log_path.stem)
    mrt.run()

    system('python -m src.mrt.debug.debug')
