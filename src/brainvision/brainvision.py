from typing import Union, Optional
from time import sleep
from pathlib import Path
from os import startfile
import configparser
import pyautogui


Pathlike = Union[str, Path]
WINDOWTITLE = 'BrainVision Recorder for CGX'
SAVEWINDOWTITLE = '名前を付けて保存'
MISCWINDOWTITLE = 'Recorder2'


class _Window:
    def __init__(self, path_app: Pathlike, window_title: str):
        self.no_app_mode = False
        self.window = self._get_window(window_title)
        if self.window is None:
            if not Path(path_app).exists():
                print('Recorder app was not found.')
                self.window = None
                self.no_app_mode = True
                return
            startfile(str(path_app))
            while True:
                self.window = self._get_window(window_title)
                if self.window:
                    break
                sleep(.5)

    def return_if_noapp(func):
        def wrapper(self, *args, **kwargs):
            if self.no_app_mode:
                return None
            return func(self, *args, **kwargs)
        return wrapper

    @return_if_noapp
    def _get_window(self, window_title):
        windows = pyautogui.getWindowsWithTitle(window_title)
        if len(windows) > 0:
            assert len(windows) == 1, (
                f'There are multiple window titled {window_title}')
            return windows[0]
        return None
        
    @return_if_noapp
    def maximize(self):
        self.window.maximize()

    @return_if_noapp
    def activate(self):
        self.window.activate()

    @return_if_noapp
    def shortcut_open(self):
        self.window.activate()
        pyautogui.keyDown('ctrl')
        pyautogui.press('o')
        pyautogui.keyUp('ctrl')

    def write(self, text: str):
        pyautogui.write(text)

    def press(self, key: str):
        pyautogui.press(key)


class _LocButton:
    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y
    
    def click(self):
        pyautogui.click(self.x, self.y)

class _ImageButton:
    def __init__(self, path_ss: Pathlike):
        self.path_ss = str(path_ss)

    def click(self):
        while True:
            self.loc = pyautogui.locateOnScreen(self.path_ss, confidence=.9)
            if self.loc:
                break
            print('Target not found, retry.')
            sleep(1.)
        pyautogui.click(*pyautogui.center(self.loc))


class BrainVisionRec:
    def __init__(self, path_app: Pathlike, maximize_window: bool=True,
                 locfile: Optional[Pathlike]=None):
        self._load_buttons(locfile)
        self._start_app(path_app, maximize_window)
        self.eeg_exists_inapp = False

    def _load_buttons(self, locfile: Optional[Pathlike]):
        if locfile:
            parser = configparser.ConfigParser()
            parser.read(locfile)
            self.buttons = {
                'monitor': _LocButton(*eval(parser.get('loc', 'monitor'))),
                'record': _LocButton(*eval(parser.get('loc', 'record'))),
                'pause': _LocButton(*eval(parser.get('loc', 'pause'))),
                'stop': _LocButton(*eval(parser.get('loc', 'stop'))),
                'stopall': _LocButton(*eval(parser.get('loc', 'stopall')))}
            return

        dire = Path(__file__).resolve().parent
        self.buttons = {
            'monitor': _ImageButton(dire / 'buttons/monitor.png'),
            'record': _ImageButton(dire / 'buttons/record.png'),
            'pause': _ImageButton(dire /'buttons/pause.png'),
            'stop': _ImageButton(dire / 'buttons/stop.png')}

    def _start_app(self, path_app: Pathlike, maximize_window: bool=True):
        self.window = _Window(path_app, WINDOWTITLE)
        if maximize_window:
            self.window.maximize()

    def _activate_window(self):
        self.window.activate()

    def open_workspace(self, path_workspace: Pathlike):
        """
        Note that ":" turns into "*" with Japanese keyboard
        """

        self.window.shortcut_open()
        self.window.write(str(path_workspace))
        self.window.press('enter')
        return self

    def init_monitor(self):
        self.buttons['monitor'].click()
        return self

    def init_record(self, path_savefile: Pathlike):
        if to_overwrite:=Path(path_savefile).exists():
            input(f'{path_savefile} already exists.\n'
                  'Press Enter and continue (data will be overwritten).')
        self.buttons['record'].click()
        if self.eeg_exists_inapp:
            while self.window._get_window(MISCWINDOWTITLE) is None:
                sleep(.1)
            self.window.write('n')  # N to "Append data?"
        while self.window._get_window(SAVEWINDOWTITLE) is None:
            sleep(.1)
        self.window.write(str(path_savefile))
        self.window.press('enter')
        if to_overwrite:
            self.window.write('y')
        self.eeg_exists_inapp = True
        return self

    def pause_record(self):
        self.buttons['pause'].click()
        return self
    
    def stop_record(self):
        self.buttons['stop'].click()
        return self

    def stop_all(self):
        self.buttons['stopall'].click()
        self.eeg_exists_inapp = False
        return self

if __name__== '__main__':
    INTERVALSEC = 5.
    print('Please confirm you have no monitor whose Y position is negative')
    print('Open recorder app')
    path = r'C:\Program Files\Brain Products\Vision\Recorder2\Recorder.exe'
    recorder = BrainVisionRec(path, locfile='config/brainvision.ini')
    sleep(INTERVALSEC)
    
    print('Open workspace')
    recorder.open_workspace('s13.rwksp2')
    sleep(INTERVALSEC)

    print('If app was already opend, no problem')

    print('Start monitoring')
    recorder.init_monitor()
    sleep(INTERVALSEC)

    print('Start recording with given filename')
    recorder.init_record(r'C:\Users\issakuss\Desktop\test.eeg')
    sleep(INTERVALSEC)

    print('Pause recording')
    recorder.pause_record()
    sleep(INTERVALSEC)

    print('Stop recording')
    recorder.stop_record()
    sleep(INTERVALSEC)

    print('Prompt when start recording with name already exists')
    recorder.init_record(r'C:\Users\issakuss\Desktop\test.eeg')
    sleep(INTERVALSEC)
    recorder.stop_record()
    sleep(INTERVALSEC)

    print('Stop all')
    recorder.stop_all()
    sleep(INTERVALSEC)
