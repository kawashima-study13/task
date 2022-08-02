from typing import List
import random
import csv

from src.tool.io import load_config
from src.tool.dataclass import Dictm


random.seed(2022)
cfg = load_config('config/stim_generation.ini').mrt
O_PATH = 'src/mrt/stim/stim.csv'
CODE_ODD = 1
CODE_NML = 0


def make_random_order_odd_normal(cfg: Dictm) -> List[int]:
    stims_odd = [CODE_ODD] * int(cfg.total_trial * cfg.rate_odd)
    stims_nml = [CODE_NML] * int(cfg.total_trial * (1 - cfg.rate_odd))
    stims = stims_odd + stims_nml
    assert len(stims) == cfg.total_trial
    random.shuffle(stims)
    return stims


def divide_stims_into_blocks(stims: List[int], cfg: Dictm) -> List[List[int]]:
    while True:
        ns_trial_inblocks = random.sample(
            range(cfg.min_interval, cfg.max_interval + 1), cfg.n_block - 1)
        len_lastblock = cfg.total_trial - sum(ns_trial_inblocks)
        if cfg.min_interval <= len_lastblock <= cfg.max_interval:
            break
    
    stimset: List[List[int]] = []
    for n_trial_inblock in ns_trial_inblocks:
        stimset.append(stims[:n_trial_inblock])
        stims = stims[n_trial_inblock:]
    stimset.append(stims)  # <- last block
    return stimset


def validate_stims(stimset: List[List[int]], cfg: Dictm) -> bool:
    """test code"""
    assert len(stimset) == cfg.n_block
    assert sum([len(stims) for stims in stimset]) == cfg.total_trial
    n_odd_shouldbe= cfg.total_trial * cfg.rate_odd
    assert sum([sum(stims) for stims in stimset]) == n_odd_shouldbe
    for stims in stimset:
        assert cfg.min_interval <= len(stims) <= cfg.max_interval
    return True


stims = make_random_order_odd_normal(cfg)
stimset = divide_stims_into_blocks(stims, cfg)
validate_stims(stimset, cfg)

with open(O_PATH, 'w') as f:
    writer = csv.writer(f)
    writer.writerows(stimset)
