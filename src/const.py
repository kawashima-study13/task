from .tool.dataclass import Dictm


BUTTONS = Dictm({
    'ABORT': ['escape', 'q'],
    'LEFT' : ['3', 'a', 'left'], # Green
    'MAIN' : ['4', 'w', 'up'], # Red
    'RIGHT': ['1', 'd', 'right'], # Blue
    'SUB'  : ['2', 's', 'down'] # Yellow
})

CODES = Dictm({
    'TASK_START': 'C10',
    'TASK_FINISH': 'C11',
    'BLOCK_START': 'C20',
    'TRIAL_START': 'C30',
    'PROBE'      : 'C40',
    'CHOICE'     : 'C41',
    'BASE_PRE'   : 'C50',
    'BASE_POST'  : 'C51',
    'MRT_BEEP'   : 'C60',
    'MRT_PRESSED': 'C61',
})

CODES_TO_LOG = [
    CODES.PROBE,
    CODES.MRT_PRESSED, # Overwrap risk?
]