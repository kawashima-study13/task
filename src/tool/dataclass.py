from itertools import product


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