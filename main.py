from src.tool.io import load_config, load_csv
from src.ppwrapper.interface import Display, Button
from src.mrt.mrt import MRT


cfg = load_config('config/task.ini')

display = Display(full=False, bgcolor=cfg.color.back, txtcolor=cfg.color.main)
button = Button()

display.build()

stimset = load_csv(cfg.mrt.path_stim)
mrt = MRT(display, button, stimset, cfg.mrt, o_path='test.csv')
mrt.run()