from pathlib import Path


def SubDir():
    return _SubDir()


class _SubDir:
    def __init__(self):
        self.is_empty_sub = False
        self.dir_home = Path().home() / 'desktop'

    def ask_id(self, message: str):
        while True:
            sub_id = input(message)
            if sub_id == '':
                if input('WONT SAVE! n to cancel: ') != 'n':
                    self.is_empty_sub = True
                    return self
                continue
            elif (not sub_id.startswith('s3')) or (len(sub_id) != 5):
                print('ID must be s3xxx')
                continue
            elif (self.dir_home / sub_id).exists():
                if input('Already exists. n to cancel: ') != 'n':
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