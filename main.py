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
print('\n'.join((
    '',
    'Input phase num and enter:',
    '1. Instrument test',
    '2. Practice MRT',
    '3. Run MRT',
    '4. Fixation',
    )))
start_phase = int(input())

if start_phase <= 1:
    input('Press enter key to start instrument test.')
    inst_test(display, button, cfg.mrt)

if start_phase <= 2:
    practice_mrt = MRT(display, button,
                       stimset_practice, cfg.mrt_practice, o_path=None)
    input('Press enter key to start practice of MRT.')
    practice_mrt.run()

if start_phase <= 3:
    o_path = sub_dir.get_dir() / 'mrt.csv'
    mrt = MRT(display, button,
              stimset, cfg.mrt, o_path=sub_dir.get_dir() / 'mrt.csv')
    input('Press enter key to start MRT.')
    mrt.run()

if start_phase <= 4:
    mrt = fixation(display, button)