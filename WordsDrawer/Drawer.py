import sys

from PIL import Image
from FractalDrawer import FractalDrawer


def pixel_processing(img_x, img_y, iterations, vector):
    # Вызываем рисователь для пикселя
    red, green, blue = fd.get_fractal_color(img_x, img_y, iterations, vector)
    return red, green, blue


def get_vector(word):
    with open("vectors_real.vec") as file:
        file.readline()
        word = word.lower()

        # Ищем в файле нужное слово и возвращаем его вектор
        for line in file:
            if line.split("_")[0] == word:
                word_vec = line.split(" ")[1:]
                return [float(word) * 10 for word in word_vec]
    return [i for i in range(1, 300)]


# Создаем картинку для рисования
img = Image.new('RGB', (600, 600), (255, 255, 255))

# Задаем границы картинки и графика
width, height = img.size
start_x = -1.5
end_x = 1.5
start_y = -1.5
end_y = 1.5

# Задаем количество итераций для фракталов
iterations = 50

# Создаем объект- рисовальщик фрактала
fd = FractalDrawer(start_x, start_y, end_x, end_y, width, height)

# Получаем вектор из словаря
word = sys.argv[1]
vec = get_vector(word)

# Обрабатываем каждый пиксель картинки по очереди
x = 0
while x < width:
    y = 0
    while y < height:
        img.putpixel((x, y), pixel_processing(x, y, iterations, vec))
        y += 1
    x += 1
img.show()
