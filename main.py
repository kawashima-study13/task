from src.tool.io import load_config, load_csv
from src.ppwrapper.interface import Display, Button
from src.mrt.mrt import MRT
from src.subjectpath import SubDir


cfg = load_config('config/task.ini')
display = Display(full=False, bgcolor=cfg.color.back, txtcolor=cfg.color.main)
button = Button()

stimset = load_csv(cfg.mrt.path_stim)

sub_dir = SubDir().ask_id('Enter sub. ID (s3001~): ').make_dir()

mrt = MRT(
    display, button, stimset, cfg.mrt, o_path=sub_dir.get_dir() / 'mrt.csv')
input('Press enter key to start MRT.')
mrt.run()