from __future__ import annotations
from typing import Literal, Tuple, List
from itertools import permutations

from src.tool.io import load_config, load_csv
from src.tool.dataclass import Dictm
from src.brainvision.brainvision import BrainVisionRec
from src.ppwrapper.interface import Display, Button
from src.mrt.mrt import MRT, MRTPractice, MRTColor, MRTBreath
from src.general.subjectpath import SubDir
from src.general.inst_test import inst_test
from src.probe.probe import Probe


def make_probe(display: Display, cfg_task: Dictm, color_name: Dictm,
               probe_filename: str) -> Probe:
    if not display.is_built:
        display.build() # For Probe()
    probe = Probe(display.window, probe_filename, color_name,
                  cfg_task.rate_y_probetext, cfg_task.size_probetext,
                  cfg_task.probe_wait_sec)
    return probe


def start_mrt(mode: Literal['thought', 'breath', 'color'], cfg_task: Dictm):
    probe = make_probe(display, cfg_task, cfg.color_name, f'intro_{mode}.jpg')

    o_path = None
    if sub_dir.get_dir():
        o_path = str(sub_dir.get_dir() / f'mrt_{mode}')

    stimset = load_csv(cfg_task.path_stim)

    mrtclass = MRT
    mrtclass = MRTColor if mode == 'color' else mrtclass
    mrtclass = MRTBreath if mode == 'breath' else mrtclass

    mrt = mrtclass(
        display, button, stimset, probe, cfg_task,
        o_path=o_path + '.csv' if o_path else None)

    display.disp_text(f'MRT ({mode}) is ready, press any key and start.')
    button.wait_keys()

    if o_path:
        recorder.init_monitor().init_record(o_path + '.eeg')
    finished_successfully = mrt.run()
    recorder.stop_record()
    mrt.pbar.close()
    return finished_successfully


def order_mrt(sub_id: str | None) -> Tuple[List, List]:
    FIXED_ID = 3000
    N_PATTERN = 6
    MRT_TYPES = ('t', 'b', 'c')
    MRT_MESSAGES = (
        't. Run MRT with thought probe',
        'b. Run MRT with breath probe',
        'c. Run MRT with color probe')
    BASE_MENU = (
        '',
        'Input phase char and enter:'
        '',
        'e. End',
        'i. Instrument test',
        'p. Practice MRT with 3-type probes',
    )

    if sub_id is None:
        return MRT_TYPES, BASE_MENU + MRT_MESSAGES

    sub_id = int(sub_id[1:]) - FIXED_ID
    pattern = sub_id % N_PATTERN
    mrt_types = list(permutations(MRT_TYPES))[pattern]
    mrt_menu = list(permutations(MRT_MESSAGES))[pattern]
    phase_menu = BASE_MENU + mrt_menu
    return list(mrt_types), phase_menu


cfg = load_config('config/task.ini')
display = Display(cfg.display.size, cfg.display.screen_id,
                  cfg.color.back, cfg.color.main)
button = Button()
recorder = BrainVisionRec(cfg.recorder.path_recapp, maximize_window=True,
                          locfile=cfg.recorder.path_recloc)

sub_dir = SubDir(cfg.misc.dir_save)
sub_dir.ask_id('Enter sub. ID (s3001~): ', cfg.misc.reg_subid).make_dir()

mrt_types, phase_menu = order_mrt(sub_dir.sub_id)

while True:
    phase = input('\n'.join(phase_menu + ('\n',)))

    if phase == 'i':
        recorder.init_monitor()
        inst_test(display, button, cfg.mrt_base | cfg.mrt_eegonly, cfg.display)

    elif phase == 'p':
        cfg_task = cfg.mrt_base | cfg.mrt_practice
        probes = (
            make_probe(display, cfg_task, cfg.color_name, 'intro_thought.jpg'),
            make_probe(display, cfg_task, cfg.color_name, 'intro_breath.jpg'),
            make_probe(display, cfg_task, cfg.color_name, 'intro_color.jpg'))
        stimset_practice = load_csv(cfg_task.path_stim)
        practice_mrt = MRTPractice(
            display, button, stimset_practice, probes, cfg_task, o_path=None)
        practice_mrt.run()

    elif phase in mrt_types:
        recorder.open_workspace(cfg.recorder.name_workspace)
        recorder.init_monitor()

        mrt_types_ = tuple(mrt_types)
        for mrt_type in mrt_types_:  # tuple because content of mrt_types pops
            if mrt_type == phase:
                break
            mrt_types.pop(0)

        for mrt_type in mrt_types:
            if mrt_type == 't':
                cfg_task = cfg.mrt_base | cfg.mrt_eegonly | cfg.mrt_thought
                finished_successfully = start_mrt('thought', cfg_task)

            if mrt_type == 'b':
                cfg_task = cfg.mrt_base | cfg.mrt_eegonly | cfg.mrt_breath
                finished_successfully = start_mrt('breath', cfg_task)

            if mrt_type == 'c':
                cfg_task = cfg.mrt_base | cfg.mrt_eegonly | cfg.mrt_color
                finished_successfully = start_mrt('color', cfg_task)

            if not finished_successfully:
                break

            if mrt_type == mrt_types[-1]:
                break

            display.disp_text('お疲れさまでした。\nしばらくご休憩ください。')
            button.wait_with_stdtimer()

    elif phase == 'e':
        recorder.stop_all()
        break

    else:
        continue
    
    button.abort = False
    display.close()
