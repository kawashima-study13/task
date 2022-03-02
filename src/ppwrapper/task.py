from __future__ import annotations
from logging import config, getLogger
from pathlib import Path

from psychopy.clock import Clock

from ..tool.io import load_json
from ..tool.dataclass import Dictm
from ..const import CODES


class Task:
    def __init__(self, display, button,
                 stimset: tuple[tuple], cfg: dict, o_path: str | Path):
        self.logger = self._set_logger(str(o_path) + '.log')

        self.display = display
        self.button = button
        self.stimset = stimset
        self.cfg = cfg
        self.o_path = o_path

        if not self.display.is_built:
            self.display.build()
        self.timer = Dictm(task=Clock(), block=Clock(), trial=Clock())
        self.progress: dict[int, int] = Dictm(block=0, trial=0)

    def log(self, message: str | tuple, code: str):
        if isinstance(message, tuple):
            message = ''.join(message)
        self.logger.info(message, extra={'code': code})

    def _set_logger(self, log_path):
        logger_config = load_json('config/logger.json')
        logger_config['handlers']['logfile']['filename'] = log_path
        config.dictConfig(logger_config)
        return getLogger('commonlogger')

    def run(self):
        self.run_task_head()
        for i, stims in enumerate(self.stimset):
            self.progress.block = i
            self.run_block(stims)
        self.run_task_tail()

    def run_task_head(self):
        """Called from self.run(), override and use"""
        self.timer.task.reset()
        self.log('Task started.', CODES.TASK_START)
    
    def run_task_tail(self):
        """Called from self.run(), override and use"""
        self.log('Task finished.', CODES.TASK_FINISH)

    def run_block(self, stims):
        self.stims = stims

        self.run_block_head()
        for i, stim in enumerate(stims):
            self.progress.trial = i
            self.run_trial(stim)
        self.run_block_tail()

    def run_block_head(self):
        """Called from self._run_block(), override and use"""
        self.timer.block.reset()
        self.log(('- Block started. ',
                  f'({self.progress.block + 1}/{len(self.stimset)})'),
                 CODES.BLOCK_START)

    def run_block_tail(self):
        """Called from self._run_block(), override and use"""

    def run_trial(self, stim=None):
        """Called from self._run_block(), override and use"""
        self.timer.trial.reset()
        len_trial = len(self.stimset[self.progress.block])
        self.log(('-- Trial started. ',
                  f'({self.progress.trial + 1}/{len_trial})'),
                 CODES.TRIAL_START)


if __name__ == '__main__':
    from .interface import Display, Button

    display = Display()
    button = Button()
    task = Task(Display(), Button(), ((0,1), (2,3)), dict(), 'test.csv')
    task.run()