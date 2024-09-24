from multiprocessing import Pool, cpu_count
import time


def find(n):
    return [i for i in range(1, n + 1) if n % i == 0]


def factorize(*numbers):
    with Pool(cpu_count()) as pool:
        return pool.map(find, numbers)


if __name__ == '__main__':
    start_parallel = time.time()
    a, b, c, d = factorize(128, 255, 99999, 10651060)
    time_parallel = time.time() - start_parallel

    assert a == [1, 2, 4, 8, 16, 32, 64, 128]
    assert b == [1, 3, 5, 15, 17, 51, 85, 255]
    assert c == [1, 3, 9, 41, 123, 271, 369, 813, 2439, 11111, 33333, 99999]
    assert d == [1, 2, 4, 5, 7, 10, 14, 20, 28, 35, 70, 140, 76079, 152158, 304316, 380395, 532553, 760790, 1065106, 1521580, 2130212, 2662765, 5325530, 10651060]

    print(f"time: {time_parallel} seconds")
