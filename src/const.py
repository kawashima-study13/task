from .tool.dataclass import Dictm


BUTTONS = Dictm({
    'ABORT': ['escape', 'q'],
    'SKIP' : ['c'],
    'LEFT' : ['3', 'a', 'left'], # Green
    'MAIN' : ['4', 'w', 'up'], # Red
    'RIGHT': ['1', 'd', 'right'], # Blue
    'SUB'  : ['2', 's', 'down'] # Yellow
})

CODES = Dictm({ # Start timings
    # General
    'TASK'       : 'C10',
    'FIN_ALL'    : 'C11',
    'BLOCK'      : 'C12',
    'TRIAL'      : 'C13',
    'BASE_PRE'   : 'C14',
    'BASE_POST'  : 'C15',

    # MRT
    'ODD_TRIAL'  : 'C20',
    'NORM_TRIAL' : 'C21',
    'PROBE'      : 'C22',
    'CHOICE'     : 'C23',
    'BEEP'       : 'C24',
    'PRESSED'    : 'C25',
})

CODES_TO_LOG = [  # Set None and all codes will be annotated
    # General
    CODES.TASK,
    CODES.FIN_ALL,
    CODES.BASE_PRE,
    CODES.BASE_POST,

    # MRT
    CODES.ODD_TRIAL,
    CODES.NORM_TRIAL,
    CODES.PROBE,
    CODES.CHOICE,
    CODES.BEEP,
    CODES.PRESSED,
]