import time


class timeit:
    """ Context manager for timing - with timeit: run()"""

    def __enter__(self):
        self.t1 = time.time()

    def __exit__(self, *args):
        print('Executed in:\t{}s'.format(time.time()-self.t1))
