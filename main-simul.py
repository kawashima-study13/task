from src.tool.io import load_config, load_csv
from src.tool.dataclass import Dictm
from src.ppwrapper.interface import Display, Button
from src.mrt.mrt import MRT, MRTSimul
from src.general.subjectpath import SubDir
from src.general.inst_test import inst_test
from src.general.fixation import fixation
from src.probe.probe import Probe


def make_probe(display: Display, cfg_task: Dictm, color_name: Dictm,
               probe_filename: str) -> Probe:
    if not display.is_built:
        display.build() # For Probe()
    probe = Probe(display.window, probe_filename, color_name,
                  cfg_task.rate_y_probetext, cfg_task.size_probetext,
                  cfg_task.probe_wait_sec)
    return probe


cfg = load_config('config/task.ini')
display = Display(cfg.display.size, cfg.display.screen_id,
                  cfg.color.back, cfg.color.main)
button = Button()

stimset = load_csv(cfg.mrt_base.path_stim)
stimset_practice = load_csv(cfg.mrt_practice.path_stim)

o_dir = cfg.misc.dir_save
reg_subid = cfg.misc.reg_subid
sub_dir = SubDir(o_dir).ask_id('Enter sub. ID: ', reg_subid).make_dir()

while True:
    phase = input('\n'.join((
        '',
        'i. Instrument test',
        'f. Fixation',
        '1. Practice MRT',
        '2. Run MRT',
        'Input phase num and enter: ',
        )))

    if phase == 'i':
        inst_test(display, button, cfg_display=cfg.display,
                  cfg_task=Dictm(cfg.mrt_base | cfg.mrt_simul))

    if phase == 'f':
        mrt = fixation(display, button)

    if phase == '1':
        cfg_task = Dictm(cfg.mrt_base | cfg.mrt_practice)
        probe = make_probe(display, cfg_task, cfg.color_name, 'intro.jpg')
        practice_mrt = MRT(display, button, stimset_practice, probe,
                           cfg_task, o_path=None)
        practice_mrt.run()

    if phase == '2':
        cfg_task = Dictm(cfg.mrt_base | cfg.mrt_simul)
        probe = make_probe(display, cfg_task, cfg.color_name, 'intro.jpg')
        o_path = sub_dir.get_dir() / 'mrt.csv' if sub_dir.get_dir() else None
        mrt = MRTSimul(display, button, stimset, probe,
                       cfg_task, o_path=o_path)
        mrt.run()
        mrt.pbar.close()
    
    button.abort = False
    display.close()
