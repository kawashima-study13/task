from src.tool.io import load_config, load_csv
from src.ppwrapper.interface import Display, Button
from src.mrt.mrt import MRT
from src.general.subjectpath import SubDir
from src.general.inst_test import inst_test
from src.general.fixation import fixation


cfg = load_config('config/task.ini')
display = Display(cfg.display.size, cfg.display.screen_id,
                  cfg.color.back, cfg.color.main)
button = Button()

stimset = load_csv(cfg.mrt.path_stim)
stimset_practice = load_csv(cfg.mrt_practice.path_stim)

sub_dir = SubDir().ask_id('Enter sub. ID (s3001~): ').make_dir()

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
        inst_test(display, button, cfg.mrt)

    if phase == 'f':
        mrt = fixation(display, button)

    if phase == '1':
        practice_mrt = MRT(display, button, stimset_practice, cfg.mrt_practice,
                           o_path=None)
        practice_mrt.run()

    if phase == '2':
        o_path = sub_dir.get_dir() / 'mrt.csv' if sub_dir.get_dir() else None
        mrt = MRT(display, button, stimset, cfg.mrt, o_path=o_path)
        mrt.run()
        mrt.pbar.close()
    
    button.abort = False
    display.close()
