from pathlib import Path


def SubDir():
    return _SubDir()


class _SubDir:
    def __init__(self):
        self.dir_home = Path().home() / 'desktop'

    def ask_id(self, message):
        while True:
            sub_id = input(message)
            if (not sub_id.startswith('s3')) or (len(sub_id) != 5):
                print('ID must be s3xxx')
                continue
        
            if (self.dir_home / sub_id).exists():
                ans = input('Already exists. continue? Y/n: ')
                if ans not in ('y', 'Y'):
                    continue

            break

        self.sub_id = sub_id
        self.dir = self.dir_home / sub_id
        return self

    def make_dir(self):
        self.dir.mkdir(exist_ok=True)
        return self

    def get_dir(self):
        return self.dir