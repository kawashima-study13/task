from numpy import datetime64
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

from ...tool.io import load_config
from ...const import CODES


def extract_time(data: pd.DataFrame, code: str) -> np.array:
    code = CODES[code]
    time = data.query('code == @code')
    return time.time.values


def find_nearest(base, lookfor):
    deltas = base - lookfor.reshape(-1, 1)
    return abs(deltas).argmin(axis=0)


def seconds_to_float(ser: pd.Series):
    return ser.dt.seconds + (ser.dt.microseconds / 1000000)

NS_TO_SEC = 1000000000.
cfg = load_config('config/task.ini').mrt
i_path = 'src/mrt/debug/debug.csv.log'
o_path = 'src/mrt/debug/timedeltas.png'


with open(i_path, 'r') as f:
    lines = f.readlines()
data = pd.DataFrame([line.replace('[', '').replace(']', '').split(' ')
                    for line in lines]).iloc[:, [1, 3]]
data.columns = ['code', 'time']
data = data.astype({'code': str, 'time': datetime64})

trial_start = extract_time(data, 'TRIAL_START')
present_beep = extract_time(data, 'MRT_BEEP')
button_press = extract_time(data, 'MRT_PRESSED')

idx_nearest = find_nearest(base=present_beep, lookfor=button_press)
deltaset = (present_beep - trial_start,
            trial_start[1:] - present_beep[:-1],
            button_press[idx_nearest] - present_beep)

fig, axes = plt.subplots(1, 3)
labels = ('trial start -> beep', 'beep -> next trial', 'beep -> button')
ideals = (
    cfg.itvl_sec_pre, cfg.itvl_sec_post + cfg.beep_dursec, 0.)
for ax, data, ylabel, ideal in zip(axes, deltaset, labels, ideals):
    data = data.astype(float) / NS_TO_SEC
    sns.stripplot(y=data, ax=ax)
    sns.boxplot(y=data, ax=ax, color='gray')
    ax.plot(ax.get_xlim(), (ideal, ideal))
    ax.set_ylabel(ylabel)
    plt.tight_layout()
fig.savefig(o_path)