from .tool.dataclass import Dictm


BUTTONS = Dictm({
    'ABORT': ['escape', 'q'],
    'LEFT' : ['3', 'a', 'left'], # Green
    'MAIN' : ['4', 'w', 'up'], # Red
    'RIGHT': ['1', 'd', 'right'], # Blue
    'SUB'  : ['2', 's', 'down'] # Yellow
})

CODES = Dictm({
    'TASK_START' : 'C11',
    'TASK_FINISH': 'C12',
    'BLOCK_START': 'C13',
    'TRIAL_START': 'C14',
    'BASE_PRE'   : 'C15',
    'BASE_POST'  : 'C16',
    'PROBE'      : 'C20',
    'CHOICE'     : 'C21',
    'MRT_BEEP'   : 'C22',
    'MRT_PRESSED': 'C23',
})

CODES_TO_LOG = None # Set None and all codes will be annotated