from __future__ import annotations
from typing import Optional, Any, Sequence, Tuple, List
from pathlib import Path
import random

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
                 probe: Probe | Tuple[Probe], cfg_mrt: Dictm,
                 o_path: str | Path | None):
        super().__init__(display, button, stimset, cfg_mrt, o_path)
        params = self.cfg.beep_dursec, self.cfg.use_ppsound
        self.data: List[Any] = []
        self.trigger = Trigger(self.cfg, mode=self.cfg.trigger_mode)
        self.beep = dict(odd=Beep(self.cfg.odd_hz, *params),
                         normal=Beep(self.cfg.normal_hz, *params))
        self.probe = probe

    def log(self, message: str | tuple,
            code: Optional[str]=None, value: Any=None):
        super().log(message, code)
        if code:
            self.trigger.write(code)
        self.data.append([
            self.progress.block, self.progress.trial, code,
            self.timer.task.getTime(), self.timer.block.getTime(),
            self.timer.trial.getTime(), value])

    def run_task_head(self):
        if self.button.abort: return
        self._run_test_volume()
        if self.button.abort: return
        self._run_baseline(self.cfg.sec_baseline_pre, 'pre')
        super().run_task_head()
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
        rate = self._present_probe()
        self.log(f'---- Answer: {rate}', CODES.CHOICE, rate)
        self.display.disp_text('+')
        self.button.wait(self.cfg.itvl_aft_probe)
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

    def _present_probe(self):
        return self.probe.present(
            f'{self.progress.block + 1}/{len(self.stimset)}')

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

    def _metronome(self, keys: Optional[Sequence]=None):
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
                key = self.button.get_keyname(keys)
                if key in BUTTONS.ABORT:
                    self.button.abort = True
                if key:
                    return key

    def _run_test_volume(self):
        self.display.disp_text((
            'ボタンを押して課題を開始してください。',
            f'このフェーズでは、\n{self.cfg.message}について'
            '\n質問されます。'))
        _ = self._metronome()
        if self.button.abort: return


class MRTBreath(MRT):
    def run_task_head(self):
        if self.button.abort: return
        self._breath_sensing()
        super().run_task_head()

    def _breath_sensing(self):
        """
        Dummy breath sensing phase to support the cover story.
        """
        SENSING_SEC = 15.
        SENSING_SEC_SHORT = 10.

        self.display.disp_text(('これから事前測定を始めます。',
                                '浅めの呼吸を続けてください。',
                                'Press any key.'))
        self.button.wait_keys()
        self.display.disp_text('浅めの呼吸を続けてください。')
        self.button.wait(SENSING_SEC)
        self.display.disp_text(('事前測定を続けます。',
                                '次は深めの呼吸を続けてください。',
                                'Press any key.'))
        self.button.wait_keys()
        self.display.disp_text('深めの呼吸を続けてください。')
        self.button.wait(SENSING_SEC)
        self.display.disp_text(('Error.',
                                'Press any key and retry.'))
        self.button.wait_keys()
        self.display.disp_text('深めの呼吸を続けてください。')
        self.button.wait(SENSING_SEC_SHORT)
        self.display.disp_text(('呼吸の事前測定が完了しました。',
                                'Press any key to continue.'))
        self.button.wait_keys()


class MRTColor(MRT):
    def _gen_color(self):
        MAX_BRIGHT = .1
        MIN_BRIGHT = 1.
        random.seed(int(''.join(self.stims)))
        color_h = random.random() * 360.
        color_v = random.uniform(MIN_BRIGHT, MAX_BRIGHT)
        color_s = 1.
        return color_h, color_s, color_v

    def _present_probe(self):
        color = self._gen_color()
        self.probe.additional_text.setColor(color, 'hsv')
        self.log(f'Color {color} will be presented', value=color)
        return self.probe.present(
            f'{self.progress.block + 1}/{len(self.stimset)}\n'
            '⬛')


class MRTPractice(MRTColor):
    def _present_probe(self):
        message = f'{self.progress.block + 1}/{len(self.stimset)}'
        probe = self.probe[self.progress.block]
        if probe.path_intro.stem.endswith('_color'):
            probe.additional_text.setColor(self._gen_color(), 'hsv')
            message += '\n⬛'
        return probe.present(message)


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

    if False:
        probe = Probe(display.window, 'intro.jpg', cfg.color_name,
                      rate_y_text=-.15, textsize=32., wait_sec=5.)
        stimset = load_csv('src/mrt/stim/stim_dbg.csv')
        mrt = MRT(display, button, stimset, probe, cfg.mrt_base,
                o_path=log_path.parent / log_path.stem)
        mrt.run()
    if True:
        # Check color probes
        cfg_task = Dictm(cfg.mrt_base | cfg.mrt_color)
        probe = Probe(display.window, 'intro_color.jpg', cfg.color_name,
                      rate_y_text=cfg_task.rate_y_probetext,
                      textsize=cfg_task.size_probetext, wait_sec=5.)
        stimset = load_csv('src/mrt/stim/stim.csv')
        mrt = MRTColor(display, button, stimset, probe, cfg_task,
                       o_path=log_path.parent / log_path.stem)
        for stims in stimset:
            mrt.stims = stims
            mrt._present_probe()

