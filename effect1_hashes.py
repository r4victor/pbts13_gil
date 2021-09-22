# Compare the time of executing CPU-bound code that releases the GIL
# using different number of Python threads.
# See how multithreading takes advantage of multiple cores.
# Run: $ python effect1_hashes.py


from threading import Thread
import time
import hashlib


THREADS_NUM_LIST = [1, 2, 4, 8]
MESSAGE_NUM = 8
MESSAGE = b'0' * ((2 ** 30) // MESSAGE_NUM)


def compute(message):
    for m in message:
        hashlib.sha256(m).digest()


def run_in_threads(threads_num, func, *args):
    threads = [Thread(target=func, args=args) for _ in range(threads_num)]
    for t in threads:
        t.start()
    for t in threads:
        t.join()


def measure():
    for threads_num in THREADS_NUM_LIST:
        messages = [MESSAGE for _ in range(MESSAGE_NUM//threads_num)]
        print(f'n_threads={threads_num}')
        for _ in range(3):
            start = time.time()
            run_in_threads(threads_num, compute, messages)
            print(time.time() - start)
        print()


if __name__ == '__main__':
    measure()