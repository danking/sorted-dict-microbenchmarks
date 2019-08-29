import sortedcontainers as sc
import time
import numpy as np


kvs = {str(i): i for i in range(10_000)}
print('kvs = {str(i): i for i in range(10_000)}')
pairs = list(kvs.items())
print('pairs = list(kvs.items())')
mm_kvs = {str(i): i for i in range(1_000_000)}
print('mm_kvs = {str(i): i for i in range(1_000_000)}')
mm_pairs = list(kvs.items())
print('mm_pairs = list(kvs.items())')


def timer(name, f, setup, iterations=15):
    times = []
    for _ in range(iterations):
        x = setup()
        start = time.monotonic()
        f(x)
        times.append(time.monotonic() - start)
    print(f'{name}: {np.mean(times)} +- {np.std(times)}')


timer('d.update(kvs)',
      lambda d: d.update(kvs),
      lambda: sc.SortedDict())
timer('d.update(pairs)',
      lambda d: d.update(pairs),
      lambda: sc.SortedDict())
timer('d.update(mm_kvs)',
      lambda d: d.update(mm_kvs),
      lambda: sc.SortedDict())


def d_with_1m():
    d = sc.SortedDict()
    d.update(mm_kvs)
    return d


timer('(d with 1M).update(kvs)',
      lambda d: d.update(kvs),
      d_with_1m)

timer('sorted(pairs, key=lambda x: x[0])',
      lambda _: sorted(pairs, key=lambda x: x[0]),
      lambda: list(kvs.items()))
timer('pairs.sort(key=lambda x: x[0])',
      lambda _: pairs.sort(key=lambda x: x[0]),
      lambda: list(kvs.items()))
timer('sorted(mm_pairs, key=lambda x: x[0])',
      lambda mm_pairs: sorted(mm_pairs, key=lambda x: x[0]),
      lambda: list(mm_kvs.items()))
timer('mm_pairs.sort(key=lambda x: x[0])',
      lambda mm_pairs: mm_pairs.sort(key=lambda x: x[0]),
      lambda: list(mm_kvs.items()))
