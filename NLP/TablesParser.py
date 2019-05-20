import re


def prepare_tables(path):
    with open(path) as file:
        i = 0
        while i < 13:
            file.readline()
            i += 1
        ll_score = {}
        mi_score = {}
        dice_score = {}
        t_score = {}
        ll_tag = False
        mi_tag = False
        dice_tag = False
        t_tag = False
        i = 1
        for line in file.readlines():
            if line == 'LL score\n':
                ll_tag = True
                i = 1
            if line == 'MI score\n':
                ll_tag = False
                mi_tag = True
                i = 1
            if line == 'Dice score\n':
                mi_tag = False
                dice_tag = True
                i = 1
            if line == 'T score\n':
                dice_tag = False
                t_tag = True
                i = 1
            col = read_row(line)
            if ll_tag and col is not None:
                ll_score[col] = i
                i += 1
            if mi_tag and col is not None:
                mi_score[col] = i
                i += 1
            if dice_tag and col is not None:
                dice_score[col] = i
                i += 1
            if t_tag and col is not None:
                t_score[col] = i
                i += 1
        return ll_score, mi_score, dice_score, t_score


def read_rang_dictionary(lines, start, end, word="", splitter=r'\s+', part=0):
    dictionary = {}
    start_tag = False
    i = 1
    for line in lines:
        print(line)
        if line == start:
            start_tag = True
        if line == end:
            break
        if start_tag:
            col = read_row(line, word, splitter, part)
            if col is not None:
                dictionary[col] = i
                i += 1
    return dictionary


def read_row(line, word, splitter, part):
    words = re.split(r'\s+', line)
    if 'видеть' in words:
        return words[0] + words[1]


def spirmen(score1, score2):
    a = 0
    i = iter(range(1, len(score1)))
    score1_red = {k: next(i) for k in sorted(score1, key=score1.get) if k in score2.keys()}
    i = iter(range(1, len(score2)))
    score2_red = {k: next(i) for k in sorted(score2, key=score2.get) if k in score1.keys()}
    for word, rang in score1_red.items():
        if word in score2_red:
            a += (rang - score2_red[word]) * (rang - score2_red[word])
    n = len(score1_red)
    return 1 - 6 * a / (n * (n * n - 1))


# 1 - 6 * (SUM)(r -r')^2/n(n^2-1)


#ll_score, mi_score, dice_score, t_score = prepare_tables('Collocations Tables/Видеть')
with open('Collocations Tables/Видеть') as file:
    i = 0
    while i < 13:
        file.readline()
        i += 1
    ll_score = read_rang_dictionary(file.readlines(), 'LL score\n', 'MI score\n', 'видеть')
result = []
row_result = []
#row_result.append(spirmen(mi_score, ll_score))
result.append(row_result)
row_result = []
#row_result.append(spirmen(t_score, ll_score))
#row_result.append(spirmen(t_score, mi_score))
result.append(row_result)
row_result = []
#row_result.append(spirmen(dice_score, ll_score))
#row_result.append(spirmen(dice_score, mi_score)),
#row_result.append(spirmen(dice_score, t_score))
result.append(row_result)
for row in result:
    print(row)
