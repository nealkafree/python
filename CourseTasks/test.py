import itertools


def mul2(x):
    return x % 2 == 0


def mul3(x):
    return x % 3 == 0


def mul5(x):
    return x % 5 == 0


def primes():
    x = 2
    while True:
        f = True
        for i in range(2, x):
            if x % i == 0:
                f = False
        if f:
            yield x
        x += 1


print(list(itertools.takewhile(lambda x: x <= 31, primes())))
