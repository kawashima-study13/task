from __future__ import annotations
from typing import Literal, Optional
from logging import config, getLogger
from pathlib import Path

from psychopy.clock import Clock

from ..tool.io import load_json
from ..tool.dataclass import Dictm
from ..const import CODES, BUTTONS


class Task:
    def __init__(self, display, button,
                 stimset: tuple[tuple], cfg: dict, o_path: str | Path | None):
        if o_path:
            o_path = Path(o_path)
            while o_path.exists():
                input(f'Save path exists. resolve and press Enter: {o_path}')
            self.logger = self._set_logger(str(o_path) + '.log')
        else:
            self.logger = self._set_logger()

        self.display = display
        self.button = button
        self.stimset = stimset
        self.cfg = cfg
        self.o_path = o_path

        self.timer = Dictm(task=Clock(), block=Clock(), trial=Clock())
        self.progress: dict[int, int] = Dictm(block=0, trial=0)

    def log(self, message: str | tuple, code: str):
        if isinstance(message, tuple):
            message = ''.join(message)
        self.logger.info(message, extra={'code': code})

    def _set_logger(self, log_path: Optional[Path]=None):
        logger_config = load_json('config/logger.json')
        if log_path:
            logger_config['handlers']['logfile']['filename'] = log_path
        else:
            logger_config['loggers']['commonlogger']['handlers'] = ['console']
        config.dictConfig(logger_config)
        return getLogger('commonlogger')

    def run(self):
        self.run_task_head()
        for i, stims in enumerate(self.stimset):
            if self.button.abort: return
            self.progress.block = i
            self.run_block(stims)
        self.run_task_tail()

    def run_task_head(self):
        """Called from self.run(), override and use"""
        if self.button.abort: return
        if not self.display.is_built:
            self.display.build()
        self.display.disp_text(('そのままお待ちください。',
                                '(Waiting pulse)'))
        self.button.wait_keys(keys=BUTTONS.PULSE)

        self.timer.task.reset()
        self.log('Task started.', CODES.TASK)
    
    def run_task_tail(self):
        """Called from self.run(), override and use"""
        if self.button.abort: return
        self.log('Task finished.', CODES.FIN_ALL)

    def run_block(self, stims):
        self.stims = stims

        self.run_block_head()
        for i, stim in enumerate(stims):
            if self.button.abort: return
            self.progress.trial = i
            self.run_trial(stim)
        self.run_block_tail()

    def run_block_head(self):
        """Called from self._run_block(), override and use"""
        if self.button.abort: return
        self.timer.block.reset()
        self.log(('- Block started. ',
                  f'({self.progress.block + 1}/{len(self.stimset)})'),
                 CODES.BLOCK)

    def run_block_tail(self):
        """Called from self._run_block(), override and use"""

    def run_trial(self, stim=None):
        """Called from self._run_block(), override and use"""
        self.timer.trial.reset()
        len_trial = len(self.stimset[self.progress.block])
        self.log(('-- Trial started. ',
                  f'({self.progress.trial + 1}/{len_trial})'),
                 CODES.TRIAL)

    def _run_baseline(self, sec: float, timing: Literal['pre', 'post']):
        code = CODES.BASE_PRE if timing == 'pre' else CODES.BASE_POST
        self.log(f'-- Baseline ({timing}) start', code)
        self.display.disp_text('+')
        self.button.wait(sec)


if __name__ == '__main__':
    from .interface import Display, Button

    display = Display()
    button = Button()
    task = Task(Display(), Button(), ((0,1), (2,3)), dict(), 'test.csv')
    task.run()