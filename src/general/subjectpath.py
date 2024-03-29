import re
from pathlib import Path

from ..tool.dataclass import Pathlike


def SubDir(*args):
    return _SubDir(*args)


class _SubDir:
    def __init__(self, dir_home: Pathlike):
        if dir_home == 'desktop':
            dir_home = Path().home() / 'desktop'
        self.is_empty_sub = False
        self.dir_home = Path(dir_home)

    def ask_id(self, message: str, pattern: str):
        while True:
            sub_id = input(message)
            if sub_id == '':
                if input('WONT SAVE! n to reinput ID: ') != 'n':
                    self.is_empty_sub = True
                    self.sub_id = None
                    return self
                continue
            elif re.match(pattern, sub_id) is None:
                print(f'ID is invalid (pattern: {pattern})')
                continue
            elif (self.dir_home / sub_id).exists():
                if input('Already exists. n to reinput ID: ') != 'n':
                    break
                continue
            break

        self.sub_id = sub_id
        self.dir = self.dir_home / sub_id
        return self

    def make_dir(self):
        if self.is_empty_sub:
            return self
        self.dir.mkdir(exist_ok=True)
        return self

    def get_dir(self):
        if self.is_empty_sub:
            return
        return self.dir