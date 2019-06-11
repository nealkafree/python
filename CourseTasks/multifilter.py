class multifilter:

    def judge_half(self, pos, neg):
        return True if pos >= neg else False

    def judge_any(self, pos, neg):
        return True if pos >= 1 else False

    def judge_all(self, pos, neg):
        return False if neg > 0 else True

    def __init__(self, iterable, *funcs, judge=judge_any):
        self.iterable = iterable
        self.funcs = funcs
        self.judge = judge

    def __iter__(self):
        for x in self.iterable:
            pos = 0
            neg = 0
            for f in self.funcs:
                if f(x):
                    pos += 1
                else:
                    neg += 1
            if self.judge(self, pos, neg):
                yield x
