from __future__ import annotations
from pathlib import Path

from ..tool.dataclass import Dictm


class Task:
    def __init__(self, display, button,
                 stimset: tuple[tuple], cfg: dict, o_path: str | Path):
        self.display = display
        self.button = button
        self.stimset = stimset
        self.cfg = cfg
        self.o_path = o_path

        self.progress: dict[int, int] = Dictm(block=0, trial=0)

    def run(self):
        self._run_task_head()
        for stims in self.stimset:
            self._run_block(stims)
        self._run_task_tail()

    def _run_task_head(self):
        """Called from self.run(), override and use"""
        print('Task head now (test code)')
    
    def _run_task_tail(self):
        """Called from self.run(), override and use"""
        print('Task tail now (test code)')

    def _run_block(self, stims):
        self.stims = stims

        self._run_block_head()
        for stim in stims:
            self._run_trial(stim)
        self._run_block_tail()

    def _run_block_head(self):
        """Called from self._run_block(), override and use"""
        print('Block head now (test code)')

    def _run_block_tail(self):
        """Called from self._run_block(), override and use"""
        print('Block tail now (test code)')

    def _run_trial(self, stim):
        """Called from self._run_block(), override and use"""
        print(stim)


if __name__ == '__main__':
    from .interface import Display, Button

    display = Display()
    button = Button()
    task = Task(Display(), Button(), ((0,1), (2,3)), dict(), 'test')
    task.run()