from __future__ import annotations
from logging import config, getLogger

from ..tool.io import load_json
from ..tool.dataclass import Dictm


class Task:
    def __init__(self, display, button,
                 stimset: tuple[tuple], cfg: dict, o_path: str):
        self.logger = self._set_logger(o_path + '.log')

        self.display = display
        self.button = button
        self.stimset = stimset
        self.cfg = cfg
        self.o_path = o_path

        self.progress: dict[int, int] = Dictm(block=0, trial=0)

    def _set_logger(self, log_path):
        logger_config = load_json('config/logger.json')
        logger_config['handlers']['fileHandler']['filename'] = log_path
        config.dictConfig(logger_config)
        return getLogger(__name__)

    def run(self):
        self._run_task_head()
        for i, stims in enumerate(self.stimset):
            self.progress.block = i
            self._run_block(stims)
        self._run_task_tail()

    def _run_task_head(self):
        """Called from self.run(), override and use"""
        self.logger.info('Task started.')
    
    def _run_task_tail(self):
        """Called from self.run(), override and use"""
        self.logger.info('Task finished.')

    def _run_block(self, stims):
        self.stims = stims

        self._run_block_head()
        for i, stim in enumerate(stims):
            self.progress.trial = i
            self._run_trial(stim)
        self._run_block_tail()

    def _run_block_head(self):
        """Called from self._run_block(), override and use"""
        self.logger.info(''.join([
                '- Block started. ',
                f'({self.progress.block + 1}/{len(self.stimset)})']))

    def _run_block_tail(self):
        """Called from self._run_block(), override and use"""

    def _run_trial(self, stim):
        """Called from self._run_block(), override and use"""
        len_trial = len(self.stimset[self.progress.block])
        self.logger.info(f'{self.progress.trial + 1}/{len_trial}')


if __name__ == '__main__':
    from .interface import Display, Button

    display = Display()
    button = Button()
    task = Task(Display(), Button(), ((0,1), (2,3)), dict(), 'test.csv')
    task.run()