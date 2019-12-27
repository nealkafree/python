import operator
from functools import reduce, wraps, partial

from toolz import curry, compose


def composition(*args):
    def composition_eval(x, *args):
        return args[0](x) if len(args) == 1 else args[0](composition_eval(x, *args[1:]))

    return lambda x: composition_eval(x, *args)


def meanAge(records):
    def ages(a, rec):
        return a if 'age' not in rec else a + rec['age']

    acc = reduce(ages, records, 0)

    def aged(i, rec):
        return i if 'age' not in rec else i + 1

    n = reduce(aged, records, 0)
    if n:
        return acc / n


def quickPower(base, power):
    if power == 0:
        return 1
    elif power == 1:
        return base
    else:
        return quickPower(base * base, power / 2) if not power % 2 else quickPower(base, power - 1) * base


def isPalindrome(str):
    if not len(str) or len(str) == 1:
        return True
    elif str[0] == str[-1]:
        return isPalindrome(str[1:-1])
    else:
        return False


def makeAmount(sum, num_list):
    if not len(num_list):
        return 0
    elif not sum:
        return 1
    elif min(num_list) > sum:
        return 0
    else:
        return makeAmount(sum, num_list[1:]) + makeAmount(sum - num_list[0], num_list)


def deepReverse(l):
    if isinstance(l, list):
        r = list(map(deepReverse, l))
        return r
    else:
        return l


def flatten(conv_dict):
    def tuple_to_dict(acc, t):
        if isinstance(t[1], dict):
            acc.update(dict(map(lambda x: (t[0] + '.' + x[0], x[1]), flatten(t[1]).items())))
            return acc
        else:
            acc.update({t[0]: t[1]})
            return acc

    return reduce(tuple_to_dict, conv_dict.items(), {})


def parameterized(decorator):
    def decoFunction(*decargs, **deckwargs):
        def res_decorator(func):
            return decorator(func, *decargs, **deckwargs)

        return res_decorator

    return decoFunction


@parameterized
def bucket(func, *d_args, **d_kwargs):
    @wraps(func)
    def inner(*args, **kwargs):
        res = func(*args, **kwargs)
        print('(' + str(d_args) + ', ' + str(d_kwargs) + ', ' + str(res) + ')')
        return res

    return inner


def inc(x):
    return x + 1


def flip(func):
    @wraps(func)
    def inner(*args):
        return func(*reversed(list(args)))

    return inner


@flip
def someFunc(a, b, c):
    return a ** b + c


def makeDecorator(func):
    @curry
    def inner(dec_func, *args, **kwargs):
        return func(dec_func, *args, **kwargs)

    return inner


@makeDecorator
def introduce(f, *args, **kwargs):
    print(f.__name__)
    return f(*args, **kwargs)


@introduce
def id(*whatever):
    return whatever


@introduce
def square(x):
    return x ** 2


def double(x):
    return x * 2


def mean(l):
    return reduce(operator.add, l, 0) / len(l)


def var(l):
    return reduce(lambda a, x: a + (x - mean(l)) ** 2, l, 0) / len(l)

def correlation(xl, yl):
    zipWith = lambda tfunc: compose(partial(map, tfunc), zip)
    mean = lambda l: reduce(operator.add, l, 0) / len(l)
    sdv = lambda l: (reduce(lambda a, x: a + (x - mean(l)) ** 2, l, 0) / len(l)) ** 0.5
    fold = lambda t: (t[0] * t[1] - mean(xl) * mean(yl))
    return sum(zipWith(fold)(xl, yl)) / (len(xl) * sdv(xl) * sdv(yl))

# f = inc
# x = 0
# zero = lambda f: lambda x: x
# one = lambda f: lambda x: f(x)
# two = lambda f: lambda x: f(f(x))
# three = lambda f: lambda x: f(f(f(x)))
# succ = lambda n: lambda f: lambda x: f(n(f)(x))
# plus = lambda m: lambda n: lambda f: lambda x: m(f)(n(f)(x))
# times = lambda m: lambda n: lambda f: m(n(f))
# power = lambda m: lambda n: lambda f: n(m)(f)
# true = lambda x: lambda y: x
# false = lambda x: lambda y: y
# und = lambda b1: lambda b2: b1(b2)(b1)
# orr = lambda b1: lambda b2: b2(b2)(b1)
# isZero = lambda numeral: numeral(lambda x: false)(true)

print(correlation([1,2,3],[3,2,1]))
