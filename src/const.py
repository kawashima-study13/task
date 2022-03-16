from .tool.dataclass import Dictm


BUTTONS = Dictm({
    'ABORT': ['escape', 'q'],
    'SKIP' : ['c'],
    'LEFT' : ['g', 'a', 'left'], # Green
    'MAIN' : ['r', 'w', 'up'], # Red
    'RIGHT': ['b', 'd', 'right'], # Blue
    'SUB'  : ['y', 's', 'down'], # Yellow
    'PULSE': ['t']
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