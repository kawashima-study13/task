from typing import Literal

from src.tool.io import load_config, load_csv
from src.tool.dataclass import Dictm
from src.brainvision.brainvision import BrainVisionRec
from src.ppwrapper.interface import Display, Button
from src.mrt.mrt import MRT, MRTColor
from src.general.subjectpath import SubDir
from src.general.inst_test import inst_test
from src.probe.probe import Probe


def make_probe(display: Display, cfg_task: Dictm, color_name: Dictm,
               probe_filename: str) -> Probe:
    if not display.is_built:
        display.build() # For Probe()
    probe = Probe(display.window, probe_filename, color_name,
                  cfg_task.rate_y_probetext, cfg_task.size_probetext,
                  cfg_task.probe_wait_sec)
    return probe


def start_mrt(mode: Literal['thought', 'breath', 'color'], cfg_task: Dictm):
    probe = make_probe(display, cfg_task, cfg.color_name, f'intro_{mode}.jpg')

    o_path = None
    if sub_dir.get_dir():
        o_path = str(sub_dir.get_dir() / f'mrt_{mode}')

    stimset = load_csv(cfg_task.path_stim)

    mrtclass = MRTColor if mode == 'color' else MRT
    mrt = mrtclass(
        display, button, stimset, probe, cfg_task, o_path=o_path + '.csv')
    recorder.init_monitor().init_record(o_path + '.eeg')
    mrt.run()
    print('debug1')
    recorder.stop_record()
    print('debug1')
    mrt.pbar.close()


cfg = load_config('config/task.ini')
display = Display(cfg.display.size, cfg.display.screen_id,
                  cfg.color.back, cfg.color.main)
button = Button()
recorder = BrainVisionRec(cfg.recorder.path_recapp, maximize_window=True,
                          locfile=cfg.recorder.path_recloc)
recorder.open_workspace(cfg.recorder.name_workspace)
recorder.init_monitor()

sub_dir = SubDir(cfg.misc.dir_save)
sub_dir.ask_id('Enter sub. ID (s3001~): ', cfg.misc.reg_subid).make_dir()

while True:
    phase = input('\n'.join((
        '',
        'i. Instrument test',
        'p. Practice MRT with thought probe',
        't. Run MRT with thought probe',
        'b. Run MRT with breath probe',
        'c. Run MRT with color probe',
        'e. End',
        'Input phase char and enter: ',
        )))

    if phase == 'i':
        inst_test(display, button,
                  Dictm(cfg.mrt_base | cfg.mrt_eegonly), cfg.display)

    if phase == 'p':
        cfg_task = Dictm(cfg.mrt_base | cfg.mrt_practice)
        probe = make_probe(
            display, cfg_task, cfg.color_name, 'intro_thought.jpg')
        stimset_practice = load_csv(cfg.mrt_practice.path_stim)
        practice_mrt = MRT(display, button, stimset_practice, probe,
                           cfg_task, o_path=None)
        practice_mrt.run()

    if phase == 't':
        cfg_task = Dictm(cfg.mrt_base | cfg.mrt_eegonly | cfg.mrt_thought)
        start_mrt('thought', cfg_task)

    if phase == 'b':
        cfg_task = Dictm(cfg.mrt_base | cfg.mrt_eegonly | cfg.mrt_breath)
        start_mrt('breath', cfg_task)

    if phase == 'c':
        cfg_task = Dictm(cfg.mrt_base | cfg.mrt_eegonly | cfg.mrt_color)
        start_mrt('color', cfg_task)

    if phase == 'e':
        recorder.stop_all()
        break
    
    button.abort = False
    display.close()
