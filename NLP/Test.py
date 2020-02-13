import math

import numpy as np

line1 = 'красный синий красный зеленый красный фисташковый'
line2 = 'фисташковый алый лазоревый белый красный'
N = 10000
df = {'красный': 100, 'синий': 80, 'зеленый': 75, 'фисташковый': 10, 'алый': 50, 'лазоревый': 25, 'белый': 200}


def return_vec(document):
    tf = {word: 1 + math.log10(document.count(word)) if document.count(word) != 0 else 0 for word in df.keys()}
    print(tf)
    idf = {word: math.log10(N / freq) for word, freq in df.items()}
    print(idf)
    vec = [tf[word] * idf[word] for word in df.keys()]
    print(vec)
    len_vec = math.sqrt(sum([i * i for i in vec]))
    return [i / len_vec for i in vec]


# vec1 = return_vec(line1.split())
# vec2 = return_vec(line2.split())
# res = sum([x * y for x, y in zip(vec1, vec2)])
# print([20])
p = np.array([0.55 for _ in range(50)])
a = 0
for i in range(25):
    a += np.prod(1 - p[:i]) * np.prod(p[i:]) * math.factorial(50) / math.factorial(50 - i) / math.factorial(i)
print(a + 0.5 * np.prod(1 - p[:25]) * np.prod(p[25:]) * math.factorial(50) / math.factorial(25) / math.factorial(25))