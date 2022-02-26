from src.tool.io import load_config, load_csv
from src.ppwrapper.interface import Display, Button
from src.mrt.mrt import MRT


display = Display()
button = Button()

display.build()

cfg = load_config('config/task.ini').mrt
stimset = load_csv(cfg.path_stim)
mrt = MRT(display, button, stimset, cfg, o_path='test.csv')
mrt.run()