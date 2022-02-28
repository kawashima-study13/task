from numpy import datetime64
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

from ...const import CODES


def seconds_to_float(ser: pd.Series):
    return ser.dt.seconds + (ser.dt.microseconds / 1000000)


i_path = 'src/mrt/debug/debug.csv.log'
o_path = 'src/mrt/debug/timedeltas.png'


with open(i_path, 'r') as f:
    lines = f.readlines()
data = pd.DataFrame([line.replace('[', '').replace(']', '').split(' ')
                    for line in lines]).iloc[:, [1, 3]]
data.columns = ['code', 'time']
data = data.astype({'code': str, 'time': datetime64})

trial_start = data.query('code == @CODES.TRIAL_START')
trial_start = trial_start.reset_index(drop=True).time
present_beep = data.query('code == @CODES.MRT_BEEP')
present_beep = present_beep.reset_index(drop=True).time
button_press = data.query('code == @CODES.MRT_PRESSED')
button_press = button_press.reset_index(drop=True).time

# Trial start -> present beep
deltas_present_beep = seconds_to_float(present_beep - trial_start)

# Present_beep -> next trial start
deltas_next_trial = seconds_to_float(
    trial_start.iloc[1:].reset_index(drop=True) - present_beep.iloc[:-1])

# Present_beep -> nearest button press
NS_TO_SEC = 1000000000.
deltas_buttons = (
    button_press.values - present_beep.values.reshape(-1, 1)).astype(float)
idx_deltas_nearest_button = abs(deltas_buttons).argmin(axis=1)
nearest_button = button_press[idx_deltas_nearest_button].reset_index(drop=True) 
deltas_nearest_button = seconds_to_float(nearest_button - present_beep)

# Plot
fig, axes = plt.subplots(1, 3)
deltaset = (deltas_present_beep, deltas_next_trial, deltas_nearest_button)
labels = ('trial start -> beep', 'beep -> next trial', 'beep -> button')
for ax, data, ylabel in zip(axes, deltaset, labels):
    sns.stripplot(y=data, ax=ax)
    sns.boxplot(y=data, ax=ax, color='gray')
    ax.set_ylabel(ylabel)
    plt.tight_layout()
fig.savefig(o_path)