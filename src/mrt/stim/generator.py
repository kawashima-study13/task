import doctest
import numpy as np

from ...tool.io import load_config



np.random.seed(2022)
cfg = load_config('config/stim.ini').mrt
PROBE_CODE: int = 10
O_PATH = 'src/mrt/stim/stim.csv'

def validate_ids_itvl(ids, n_trial, min_interval) -> bool:
    """
    >>> ids = np.array([8, 4, 2, 1, 2])
    >>> n_trial = 10
    >>> validate_ids_itvl(ids, n_trial, min_interval=6)
    True
    >>> validate_ids_itvl(ids, n_trial, min_interval=7)
    False
    """

    n_aft_probe = n_trial - ids
    itvls = ids + np.insert(n_aft_probe[:-1], 0, 0)
    return (itvls >= min_interval).all()

doctest.testmod()

stimset = (np.random.rand(cfg.n_block, cfg.n_trial) <= cfg.rate_odd)
stimset = stimset.astype(int)

while True:
    ids_probe = np.random.randint(0, cfg.n_trial - 1, cfg.n_block)
    if validate_ids_itvl(ids_probe, cfg.n_trial, cfg.min_interval):
        break

assert len(stimset) == len(ids_probe) # use strict arg in python 3.10
for stims, idx_probe in zip(stimset, ids_probe):
    stims[idx_probe] += PROBE_CODE

np.savetxt(O_PATH, stimset, fmt='%d', delimiter=',')