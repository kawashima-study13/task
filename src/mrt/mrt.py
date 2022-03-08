from __future__ import annotations
from typing import Literal

import pandas as pd
from psychopy import core

from ..tool.serial import Serial
from ..const import BUTTONS, CODES, CODES_TO_LOG
from ..probe.probe import Probe
from ..ppwrapper.task import Task
from .sound import Beep


class MRT(Task):
    def __init__(self, display, button,
                 stimset: tuple[tuple], cfg: dict, o_path: str | Path):
        super().__init__(display, button, stimset, cfg, o_path)
        self.data = []
        self.serial = Serial(cfg.comname) if cfg.comname else None

    def log(self, message: str | tuple, code: str, value=None):
        super().log(message, code)
        self._trigger(code)
        self.data.append([
            self.progress.block, self.progress.trial, code,
            self.timer.task.getTime(), self.timer.block.getTime(),
            self.timer.trial.getTime(), value])

    def _trigger(self, code: str):
        if self.serial and ((CODES_TO_LOG is None) or (code in CODES_TO_LOG)):
            self.serial.write(int(code[1:]))

    def run_task_head(self):
        params = self.cfg.beep_dursec, self.cfg.use_ppsound
        if not self.display.is_built:
            self.display.build() # For Probe()
        self.probe = Probe(self.display.window)
        self.beep = dict(odd=Beep(self.cfg.odd_hz, *params),
                         normal=Beep(self.cfg.normal_hz, *params))

        super().run_task_head()
        self._run_baseline(self.cfg.sec_baseline_pre, 'pre')

    def run_task_tail(self):
        self._run_baseline(self.cfg.sec_baseline_post, 'post')
        super().run_task_tail()

        self.display.disp_text(('お疲れさまでした。', 'そのままお待ちください。',
                                'saving...'))
        data = pd.DataFrame(self.data)
        data.columns = ['block', 'trial', 'code',
                        'sec_task', 'sec_block', 'sec_trial', 'value']
        data.to_csv(self.o_path, index=False)
        self.display.disp_text(('お疲れさまでした。', 'そのままお待ちください。',
                                'saving...complete'))
        self.button.wait_key()

    def _run_baseline(self, sec: float, timing: Literal['pre', 'post']):
        code = CODES.BASE_PRE if timing == 'pre' else CODES.BASE_POST
        self.log(f'-- Baseline ({timing}) start', code)
        self.display.disp_text('+')
        self.button.wait(sec)

    def run_block_tail(self):
        self.log('--- Probe presented', CODES.PROBE)
        rate = self.probe.present()
        self.log(f'---- Answer: {rate}', CODES.CHOICE, rate)
        self.display.disp_text('+')

    def run_trial(self, stim: str):
        dursec_trial = sum([self.cfg.itvl_sec_pre,
                            self.cfg.beep_dursec,
                            self.cfg.itvl_sec_post])

        super().run_trial()
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
