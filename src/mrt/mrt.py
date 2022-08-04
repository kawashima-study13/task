from __future__ import annotations
from typing import Any, List

import pandas as pd
from psychopy import core, clock

from ..tool.dataclass import Dictm
from ..const import BUTTONS, CODES
from ..general.trigger import Trigger
from ..probe.probe import Probe
from ..ppwrapper.interface import Display, Button
from ..ppwrapper.task import Task
from .sound import Beep


class MRT(Task):
    def __init__(self, display: Display, button: Button, stimset: tuple[tuple],
                 probe: Probe, cfg_mrt: Dictm, o_path: str | Path | None):
        super().__init__(display, button, stimset, cfg_mrt, o_path)
        params = self.cfg.beep_dursec, self.cfg.use_ppsound
        self.data: List[Any] = []
        self.trigger = Trigger(self.cfg, mode=self.cfg.trigger_mode)
        self.beep = dict(odd=Beep(self.cfg.odd_hz, *params),
                         normal=Beep(self.cfg.normal_hz, *params))
        self.probe = probe

    def log(self, message: str | tuple, code: str, value: Any=None):
        super().log(message, code)
        self.trigger.write(code)
        self.data.append([
            self.progress.block, self.progress.trial, code,
            self.timer.task.getTime(), self.timer.block.getTime(),
            self.timer.trial.getTime(), value])

    def run_task_head(self):
        if self.button.abort: return
        self._run_test_volume()
        if self.button.abort: return
        super().run_task_head()
        self._run_baseline(self.cfg.sec_baseline_pre, 'pre')
        self.pbar.start()
        self.display.disp_text('o')

    def run_task_tail(self):
        if self.button.abort: return
        self._run_baseline(self.cfg.sec_baseline_post, 'post')
        if self.button.abort: return
        super().run_task_tail()

        self.display.disp_text(('お疲れさまでした。', 'そのままお待ちください。',
                                '(saving...)'))
        data = pd.DataFrame(self.data)
        data.columns = ['block', 'trial', 'code',
                        'sec_task', 'sec_block', 'sec_trial', 'value']
        if self.o_path is not None:
            data.to_csv(self.o_path, index=False)
        self.display.disp_text(('お疲れさまでした。', 'そのままお待ちください。',
                                '(saving...complete.',
                                'press ENTER to finish.)'))
        self.button.wait_keys(keys=['return'])

    def run_block_tail(self):
        self.log('--- Probe presented', CODES.PROBE)
        rate = self.probe.present()
        self.log(f'---- Answer: {rate}', CODES.CHOICE, rate)
        self.display.disp_text('o')
        self.button.clear()

    def run_trial(self, stim: str):
        super().run_trial()

        if int(stim) > 0:
            trialname = 'ODD'
            code = CODES.ODD_TRIAL
        else:
            trialname = 'NORMAL'
            code = CODES.NORM_TRIAL
        self.log(f'--- It is {trialname} trial.', code)

        dursec_trial = sum([self.cfg.itvl_sec_pre,
                            self.cfg.beep_dursec,
                            self.cfg.itvl_sec_post])
        while self.timer.trial.getTime() <= self.cfg.itvl_sec_pre:
            core.wait(self.button.itvl_input)
            self._get_press(at_release=False)
        self._present_beep(odd=int(stim) > 0, dursec=self.cfg.beep_dursec)
        while self.timer.trial.getTime() <= dursec_trial:
            core.wait(self.button.itvl_input)
            self._get_press(at_release=False)

    def _get_press(self, at_release: bool):
        if key := self.button.get_keyname(at_release=at_release):
            self.button.glob_key_event(key)
            if key in (*BUTTONS.LEFT, *BUTTONS.MAIN, *BUTTONS.SUB):
                self.log('---- {} was pressed ({:.6f}; {:.6f})'.format(
                    key, self.timer.trial.getTime(),
                    self.timer.task.getTime()), CODES.PRESSED)
            if key in BUTTONS.RIGHT:
                self.log('---- MW was caught ({:.6f}; {:.6f})'.format(
                    self.timer.trial.getTime(), self.timer.task.getTime()),
                    CODES.MWCAUGHT)

    def _present_beep(self, odd: bool, dursec: float, log: bool=True):
        type = 'odd' if odd else 'normal'
        if log:
            self.log(f'--- Present {type} stim {dursec} sec.', CODES.BEEP)
        self.beep[type].play()

    def _metronome(self):
        RATE: int = 4
        self.button.clear()
        i = 0
        t0 = clock.Clock()
        itvl = self.cfg.itvl_sec_pre + self.cfg.itvl_sec_post
        while True:
            t0.reset()
            i += 1
            is_odd = not (i % RATE)
            self._present_beep(is_odd, self.cfg.beep_dursec, log=False)
            while t0.getTime() < itvl:
                key = self.button.get_keyname()
                if key in BUTTONS.ABORT:
                    self.button.abort = True
                if key:
                    return key

    def _run_test_volume(self):
        self.display.disp_text('ボタンを押して課題を開始してください。')
        _ = self._metronome()
        if self.button.abort: return


class MRTSimul(MRT):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def _run_test_volume(self):
        self.display.disp_text(('そのままお待ちください。',
                                '(Press ENTER to test vol)'))
        self.button.wait_keys(keys=['return'])

        for n in range(self.cfg.n_mripulse_towait_bfr_voltune, 0, -1):
            self.display.disp_text((f'(Waiting MRI pulses: {n})'))
            key = self.button.wait_keys(keys=BUTTONS.PULSE)

        self.display.disp_text(('２種類の音が聞こえたら',
                                '上ボタンで課題開始',
                                '聞こえなかったら',
                                '下ボタン'))
        self.button.clear()

        key = self._metronome()
        if self.button.abort: return
        if key in BUTTONS.SUB:
            self.display.disp_text(('そのままお待ちください。',
                                    '(Volume is too low!',
                                    'press QUIT key)'))
            self.button.wait(float('inf'))
            return

        self.display.disp_text(('そのままお待ちください。',
                                '(Waiting a pulse)'))
        self.button.wait_keys(keys=BUTTONS.PULSE)


if __name__ == '__main__':
    from pathlib import Path
    from src.tool.io import load_config, load_csv
    from src.ppwrapper.interface import Display, Button
    from src.probe.probe import Probe


    log_path = Path('src/mrt/debug/debug.csv.log')
    log_path.unlink(missing_ok=True)

    cfg = load_config('config/task.ini')

    display = Display()
    button = Button()
    display.build()

    probe = Probe(display.window, 'intro.jpg', cfg.color_name, 5.)

    stimset = load_csv('src/mrt/stim/stim_dbg.csv')
    mrt = MRT(display, button, stimset, probe, cfg.mrt,
              o_path=log_path.parent / log_path.stem)
    mrt.run()
