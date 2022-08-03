from .tool.dataclass import Dictm


BUTTONS = Dictm({
    'ABORT': ['escape', 'q'],
    'SKIP' : ['c'],
    'LEFT' : ['3', 'g', 'a', 'left'], # Green
    'MAIN' : ['4', 'r', 'w', 'up'], # Red
    'RIGHT': ['1', 'b', 'd', 'right'], # Blue
    'SUB'  : ['2', 'y', 's', 'down'], # Yellow
    'PULSE': ['5', 't']
})

CODES = Dictm({ # Start timings
    # General
    'MISC'       : 'C10',
    'TASK'       : 'C11',  # Task started at this time
    'FINTASK'    : 'C12',  # Task finished
    'BLOCK'      : 'C13',  # A block started
    'TRIAL'      : 'C14',  # A trial started
    'BASE_PRE'   : 'C15',  # Baseline (pre) started
    'BASE_POST'  : 'C16',  # Baseline (post) started

    # MRT
    'ODD_TRIAL'  : 'C20',  # Odd trial started (odd beep would be presented soon)
    'NORM_TRIAL' : 'C21',  # Normal trial started
    'PROBE'      : 'C22',  # Probe was presented
    'CHOICE'     : 'C23',  # Participant answered to probe
    'BEEP'       : 'C24',  # Odd or normal (see C20 or C21) beep was presented
    'PRESSED'    : 'C25',  # Participant responded
    'MWCAUGHT'   : 'C26',  # Participant responded as MW-caught
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
    CODES.MWCAUGHT,
]