import time

def timer(func):
    def timer_(*args, **kwargs):
        t0 = time.time()
        func(*args, **kwargs)
        print(f'{func.__name__}: {time.time() - t0} sec')
    return timer_