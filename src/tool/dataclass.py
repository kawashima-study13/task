from typing import Union
from itertools import product

from pathlib import Path


Pathlike = Union[str, Path]

class Dictm(dict):
    # https://blog.bitmeister.jp/?p=4658
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.__dict__ = self

    def product_values(self, verbose=False):
        prod = product(*list(self.values()))
        if not verbose:
            return prod
        for p in prod:
            verb = '-'.join([str(p_) for p_ in p])
            yield p + (verb,)

    def __or__(self, other):
        self.__dict__ = dict(self) | dict(other)
        return self

foo = Dictm({'a': 0, 'b': 1})
bar = Dictm({'c': 2})
baa = Dictm({'d': 3})
print(foo | bar)
