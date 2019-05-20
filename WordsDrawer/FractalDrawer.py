class FractalDrawer:

    def __init__(self, start_x, start_y, end_x, end_y, width, height):
        # Задаем параметры изображения- границы графика и коэффицмент, для получения числа в координатах
        self.start_x = start_x
        self.start_y = start_y
        self.kx = (end_x - start_x) / width
        self.ky = (end_y - start_y) / height

    def julia(self, img_x, img_y, iterations):
        # Классический Жулиа. Для тестирования, не трогаем
        ax = self.kx * img_x + self.start_x
        ay = self.ky * img_y + self.start_y
        acc = Complex(ax, ay)
        it = 0
        while it < iterations:
            if acc.get_real() * acc.get_real() + acc.get_img() * acc.get_img() <= 4:
                acc = acc * acc
                acc = acc + Complex(0.37, 0.37)
            else:
                return it
            it += 1
        return it

    def mandelbrot(self, img_x, img_y, iterations):
        # Классический Мандельброт. Для тестирования, не трогаем
        ax = self.kx * img_x + self.start_x
        ay = self.ky * img_y + self.start_y
        acc = Complex(0, 0)
        it = 0
        while it < iterations:
            if acc.get_real() * acc.get_real() + acc.get_img() * acc.get_img() <= 4:
                acc = acc * acc
                acc = acc + Complex(ax, ay)
            else:
                return it
            it += 1
        return it

    def get_fractal_color(self, img_x, img_y, iterations, vector):
        # Тестовый Жулиа. Мучаем по полной

        # Получаем координаты точки
        x = self.kx * img_x + self.start_x
        y = self.ky * img_y + self.start_y

        # Создаем итератор для вектора
        vec_iter = iter(vector)

        # Создаем аккумуляторы для фракталов
        red_acc = Complex(x + next(vec_iter), y + next(vec_iter))
        green_acc = Complex(x + next(vec_iter), y + next(vec_iter))
        blue_acc = Complex(x + next(vec_iter), y + next(vec_iter))

        red = 0
        green = 0
        blue = 0

        # Создаем итератор для фрактала(ов)
        it = 0
        while it < iterations:

            # Делаем новую итерацию алгоритма
            if red_acc.get_real() * red_acc.get_real() + red_acc.get_img() * red_acc.get_img() <= 4:
                red_acc = red_acc * red_acc
                red_acc = red_acc + Complex(next(vec_iter), next(vec_iter))
            else:
                if red == 0:
                    red = it

            if green_acc.get_real() * green_acc.get_real() + green_acc.get_img() * green_acc.get_img() <= 4:
                green_acc = green_acc * green_acc * green_acc
                green_acc = green_acc + Complex(next(vec_iter), next(vec_iter))
            else:
                if green == 0:
                    green = it

            if blue_acc.get_real() * blue_acc.get_real() + blue_acc.get_img() * blue_acc.get_img() <= 4:
                blue_acc = blue_acc * blue_acc * blue_acc * blue_acc
                blue_acc = blue_acc + Complex(next(vec_iter), next(vec_iter))
            else:
                if blue == 0:
                    blue = it

            if not (red == 0 or green == 0 or blue == 0):
                break

            it += 1

        return round(red * 255 / iterations), round(green * 255 / iterations), round(blue * 255 / iterations)

    def get_fractal_color_test(self, img_x, img_y, iterations, vector):
        # Тестовый Жулиа. Мучаем по полной

        # Получаем координаты точки
        x = self.kx * img_x + self.start_x
        y = self.ky * img_y + self.start_y

        # Создаем итератор для вектора
        vec_iter = iter(vector)

        # Создаем аккумуляторы для фракталов
        red_acc = Complex(x + next(vec_iter), y + next(vec_iter))
        green_acc = Complex(x + next(vec_iter), y + next(vec_iter))
        blue_acc = Complex(x + next(vec_iter), y + next(vec_iter))
        saturation_acc = Complex(x + next(vec_iter), y + next(vec_iter))

        red = 0
        green = 0
        blue = 0
        saturation = 0

        # Создаем итератор для фрактала(ов)
        it = 0
        while it < iterations:

            # Делаем новую итерацию алгоритма
            if red_acc.get_real() * red_acc.get_real() + red_acc.get_img() * red_acc.get_img() <= 4:
                red_acc = red_acc * red_acc
                red_acc = red_acc + Complex(next(vec_iter), next(vec_iter))
            else:
                if red == 0:
                    red = it

            if green_acc.get_real() * green_acc.get_real() + green_acc.get_img() * green_acc.get_img() <= 4:
                green_acc = green_acc * green_acc * green_acc
                green_acc = green_acc + Complex(next(vec_iter), next(vec_iter))
            else:
                if green == 0:
                    green = it

            if blue_acc.get_real() * blue_acc.get_real() + blue_acc.get_img() * blue_acc.get_img() <= 4:
                blue_acc = blue_acc * blue_acc * blue_acc * blue_acc
                blue_acc = blue_acc + Complex(next(vec_iter), next(vec_iter))
            else:
                if blue == 0:
                    blue = it

            if saturation_acc.get_real() * saturation_acc.get_real() + saturation_acc.get_img() * saturation_acc.get_img() <= 4:
                saturation_acc = saturation_acc * saturation_acc
                saturation_acc = saturation_acc + Complex(next(vec_iter), next(vec_iter))
            else:
                if saturation == 0:
                    saturation = it

            if not (red == 0 or green == 0 or blue == 0 or saturation == 0):
                break

            it += 1

        return round(red * 255 / iterations), round(green * 255 / iterations), round(blue * 255 / iterations), round(saturation * 100 / iterations)


class Complex:

    def __init__(self, real, img):
        self.real = real
        self.img = img

    def __add__(self, other):
        return Complex(self.real + other.real, self.img + other.img)

    def __mul__(self, other):
        temp = self.real * other.real - self.img * other.img
        return Complex(temp, self.real * other.img + self.img * other.real)

    def get_real(self):
        return self.real

    def get_img(self):
        return self.img
