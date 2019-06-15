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


mod_checker = lambda x, mod=0: lambda y: True if y % x == mod else False


def check_for_replaces(s, a, b):
    i = 0
    while i < 1000:
        if s.find(a) == -1:
            return i
        else:
            s = s.replace(a, b)
        i += 1
    return "Impossible"


def check_for_insights(s, t):
    i = 0
    a = 0
    while i < len(s):
        if s[i:].find(t) == 0:
            a += 1
        i += 1
    return a


s = input()
t = input()
print(check_for_insights(s, t))
