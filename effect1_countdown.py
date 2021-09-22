# Compare the time of performing a CPU-bound task
# using different number of Python threads.
# See how the GIL kills parallelism.
# Run: $ python effect1_countdown.py

from threading import Thread
import time


N = 100_000_000
THREADS_NUM_LIST = [1, 2, 4, 8]


def countdown(n):
    while n > 0:
        n -= 1


def run_in_threads(threads_num, func, *args):
    threads = [Thread(target=func, args=args) for _ in range(threads_num)]
    for t in threads:
        t.start()
    for t in threads:
        t.join()


def measure():
    for threads_num in THREADS_NUM_LIST:
        n = N //threads_num
        print(f'{threads_num=}; {n=}')
        for _ in range(3):
            start = time.time()
            run_in_threads(threads_num, countdown, n)
            print(time.time() - start)
        print()


if __name__ == '__main__':
    measure()