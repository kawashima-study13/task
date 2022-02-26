from psychopy import core

from ..const import BUTTONS
from ..ppwrapper.task import Task


class MRT(Task):
    def _run_task_head(self):
        super()._run_task_head()
        self.display.disp_text('Press any key to start.')
        self.button.wait_key(keys=None)
        self.display.disp_text('+')
        self.button.clear()

    def _run_trial(self, stim: str):
        super()._run_trial()

        while self.timer.trial.getTime() <= self.cfg.itvl_sec_pre:
            core.wait(.1)
            self._get_press()
        self._present_beep(odd=int(stim) > 0, dursec=self.cfg.beep_dursec)
        while self.timer.trial.getTime() <= self.cfg.itvl_sec_post:
            core.wait(.1)
            self._get_press()

    def _get_press(self):
        if key := self.button.get_keyname():
            if key in BUTTONS.ABORT:
                core.quit()
            self.logger.info('---- {} was pressed ({:.6f}; {:.6f})'.format(
                key, self.timer.trial.getTime(), self.timer.task.getTime()))

    def _present_beep(self, odd: bool, dursec: float):
        type = 'odd' if odd else 'normal'
        self.logger.info(f'--- Present {type} stim {dursec} sec.')
