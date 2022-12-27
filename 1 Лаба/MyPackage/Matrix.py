from MyPackage.Vector import Vector
import random

class Matrix:
    # Инициализатор матрицы (создает квадратную матрицу NxN где N-натуральное)
    def __init__(self, size=1):
        # В случае неподходящего типа или размера default размер = 1
        if type(size) != int or size <= 0:
            size = 1
        self.__a, self.__b, self.__c, self.__p, self.__q = (Vector(size) for _ in range(5))

    # Переопределение оператора +
    def __add__(self, other):
        m = Matrix()
        # Ставим защиту от неподходящих типов
        if type(other) != Matrix:
            raise TypeError("Операция + возможна только в случае типов Matrix + Matrix")
        # Копируем данные
        m.__a, m.__b, m.__c, m.__p, m.__q = \
            self.__a.copy(), self.__b.copy(), self.__c.copy(), self.__p.copy(), self.__q.copy()
        # Производим сложение по векторам
        m.__a = self.__a + other.__a
        m.__b = self.__b + other.__b
        m.__c = self.__c + other.__c
        m.__p = self.__p + other.__p
        m.__q = self.__q + other.__q
        return m

    # Переопределение оператора -
    def __sub__(self, other):
        m = Matrix()
        # Ставим защиту от неподходящих типов
        if type(other) != Matrix:
            raise TypeError("Операция - возможна только в случае типов Matrix - Matrix")
        # Копируем данные
        m.__a, m.__b, m.__c, m.__p, m.__q = \
            self.__a.copy(), self.__b.copy(), self.__c.copy(), self.__p.copy(), self.__q.copy
        # Производим вычитание по векторам
        m.__a = self.__a - other.__a
        m.__b = self.__b - other.__b
        m.__c = self.__c - other.__c
        m.__p = self.__p - other.__p
        m.__q = self.__q - other.__q
        return m

    # Переопределение оператора * (только для умножения матрицы на вектор)
    def __mul__(self, other):
        # Ставим защиту от неподходящих типов
        if type(other) != int and type(other) != float and type(other) != Vector:
            raise TypeError("Операция * возможна только в случае типов Matrix * Vector")
        size = len(other)
        # Защита от разных размерностей
        if size != len(self.__a):
            raise ValueError("Несоразмерные вектор и матрица")
        v = Vector(size)
        # Сначала рассмотрим частные случаи
        if size >= 1:
            v[1] = self.__b[1] * other[-1]
        if size >= 2:
            v[1] += self.__a[1] * other[-2]
            v[2] = self.__b[2] * other[-2] + self.__c[2] * other[-1]
        if size >= 3:
            v[2] += self.__a[2] * other[-3]
            v[3] = self.__b[3] * other[-3] + self.__c[3] * other[-2] + self.__q[3] * other[-1]
        # Затем рассмотрим общий случай
        if size >= 4:
            v[3] += self.__a[3] * other[-4]
            for i in range(4, size + 1):
                v[i] = self.__b[i] * other[-i] + self.__c[i] * other[1 - i] + \
                       self.__p[i] * other[-2] + self.__q[i] * other[-1]
                if i != size:
                    v[i] += self.__a[i] * other[-i - 1]
        return v

    # Переопределение оператора * правостороннего
    def __rmul__(self, other):
        return self * other

    # Пользовательское строковое представление
    def __str__(self):
        return self.to_string()

    def max_str_len(self):
        def func(lst):
            return max([len(str(val)) for val in lst])
        return max(map(func, (self.__a, self.__b, self.__c, self.__p, self.__q)))

    # Преобразование матрицы в строковый вид
    # Метод вспомогательный для отсутствия дублирования кода
    def to_string(self):
        string = str()
        size = len(self.__a)
        max_len = self.max_str_len()
        # Рассмотрим частные случаи
        if size == 1:
            string = str(self.__q[1]).ljust(max_len, ' ')
        elif size == 2:
            string = str(self.__p[1]).ljust(max_len, ' ') + ' ' + str(self.__q[1]).ljust(max_len, ' ') + '\n' + \
                     str(self.__p[2]).ljust(max_len, ' ') + ' ' + str(self.__q[2]).ljust(max_len, ' ')
        else:
            # Иначе - рассмотрим общий случай
            zeros = "0"
            for i in range(1, size + 1):
                # Устанавливаем нули до диагонали
                for cnt in range(size - 2 - i + 1):
                    string += ' ' + zeros.ljust(max_len, ' ') + ' '
                # Устанавливаем значения на диагонали
                if i != size:
                    if self.__a[i] >= 0:
                        string += ' '
                    string += str(self.__a[i]).ljust(max_len + (self.__a[i] < 0), ' ') + ' '
                if self.__b[i] >= 0:
                    string += ' '
                string += str(self.__b[i]).ljust(max_len + (self.__b[i] < 0), ' ') + ' '
                if i != 1:
                    if self.__c[i] >= 0:
                        string += ' '
                    string += str(self.__c[i]).ljust(max_len + (self.__c[i] < 0), ' ') + ' '
                # Устанавливаем нули после диагонали
                for cnt in range(max(0, i-4)):
                    string += ' ' + zeros.ljust(max(0, max_len), ' ') + ' '
                # Устанавливаем последние столбцы
                if i >= 4:
                    if self.__p[i] >= 0:
                        string += ' '
                    string += str(self.__p[i]).ljust(max_len + (self.__p[i] < 0), ' ') + ' '
                if i >= 3:
                    if self.__q[i] >= 0:
                        string += ' '
                    string += str(self.__q[i]).ljust(max_len + (self.__q[i] < 0), ' ') + ' '
                if i != size:
                    string += '\n'
        return string

    # Печать в консоль
    def print(self):
        print(self.to_string())

    # Считывание с источника по заданной функции (методу)
    # Метод вспомогательный для отсутствия дублирования кода
    # func обязана возвращать строковое представление
    def read_with_func(self, func):
        lst = [float(x) for x in func().split()]
        size = len(lst)
        self.__a = Vector(size)
        self.__b = Vector(size)
        self.__c = Vector(size)
        self.__p = Vector(size)
        self.__q = Vector(size)
        # Сначала частные случаи
        if size >= 1:
            self.__q[1] = self.__b[1] = lst[-1]
        if size >= 2:
            self.__p[1] = self.__a[1] = lst[-2]
            lst = [float(x) for x in func().split()]
            self.__p[2], self.__q[2] = self.__b[2], self.__c[2] = lst[-2], lst[-1]
        if size >= 3:
            self.__a[2] = lst[-3]
            lst = [float(x) for x in func().split()]
            self.__b[3] = lst[-3]
            self.__c[3] = self.__p[3] = lst[-2]
            self.__q[3] = lst[-1]
        # Затем общий случай
        if size >= 4:
            self.__a[3] = lst[-4]
            cnt = 0
            for i in range(4, size + 1):
                lst = [float(x) for x in func().split()]
                self.__p[i], self.__q[i] = lst[-2], lst[-1]
                self.__b[i], self.__c[i] = lst[-4 - cnt], lst[-3 - cnt]
                # В последней строке нет коэффициента а
                if i != size:
                    self.__a[i] = lst[-5 - cnt]
                cnt += 1

    # Считывание с консоли
    def read(self):
        self.read_with_func(input)

    # Считывание с файла
    def file_read(self, file_descriptor):
        self.read_with_func(file_descriptor.readline)

    # Запись в файл
    def write(self, file_descriptor):
        file_descriptor.write(self.to_string())

    # Метод заполнения побочной диагонали для хорошей обусловленности матрицы
    def __fill_diag_rand_good(self, a, b, by_float=True):
        if a >= 0:
            # В случае [a>0, b>0] меньшие абсолютные значения лежат слева
            begin, end = a, a + (b - a - 1) // 4
        elif b <= 0:
            # В случае [a<0, b<0] меньшие абсолютные значения лежат права
            begin, end = b - (b - a - 1) // 4, b
        else:
            # В случае [a<0, b>0] - меньшие значения лежат в области 0
            d = min((abs(b), abs(a))) // 5
            begin, end = 0, 0
            if a < -d:
                begin = -d
            if b > d:
                end = d
        self.__a.fill_rand(begin, end, by_float=by_float)
        self.__c.fill_rand(begin, end, by_float=by_float)
        n = len(self.__a)
        for i in range(1, n + 1):
            sum = 0
            if i != 1:
                sum += abs(self.__a[i-1])
            if i != n:
                sum += abs(self.__c[i+1])
            if a >= 0:
                # В случае [a>0, b>0] устанавливаем нижнюю грань генерации
                self.__b[i] = [random.randint(int(sum), b),
                               random.uniform(float(sum), float(b))][by_float]
            else:
                # a < 0
                gen_a, gen_b = False, False
                sgn_b = (1, -1)[b < 0]
                if -sum >= a and sum * sgn_b <= b:
                    # Если сумма модулей лежит в области обеих границ, то рандомно выбираем из какой генерировать
                    gen_a = random.choice([True, False])
                    gen_b = not gen_a
                if gen_a or -sum >= a and sum * sgn_b >= b:
                    # Если сумма модулей лежит в области только левой границы
                    self.__b[i] = [random.randint(a, int(-sum)),
                                   random.uniform(float(a), float(-sum))][by_float]
                elif gen_b or -sum <= a and sum * sgn_b <= b:
                    # Если сумма модулей лежит в области только правой границы
                    self.__b[i] = [random.randint(sgn_b * (int(sum) + 1), b),
                                   random.uniform(float(sum * sgn_b), float(b))][by_float]
                else:
                    raise ValueError("Невозможно сгенерировать нужную матрицу по заданному диапазону")
            if self.__b[i] == 0:
                self.__b[i] = (a, b)[max(abs(a), abs(b)) == abs(b)]
                if by_float:
                    self.__b[i] += random.random()
                    if self.__b[i] > b:
                        self.__b[i] = b - 0.001

    # Метод заполнения побочной диагонали для плохой обусловленности матрицы
    def __fill_diag_rand_bad(self, a, b, by_float=True):
        # Для плохой обусловленности
        self.__a.fill_rand(a, b, by_float=by_float)
        self.__c.fill_rand(a, b, by_float=by_float)
        n = len(self.__a)
        for i in range(1, n + 1):
            s = 0
            if i != 1:
                s += abs(self.__a[i - 1])
            if i != n:
                s += abs(self.__c[i + 1])
            s -= 1
            sgn_a, sgn_b = (-1, 1)[a >= 0], (-1, 1)[b >= 0]
            if a >= 0:
                # [a >= 0, b > 0]
                try:
                    self.__b[i] = [random.randint(a, int(min(b, s))),
                                   random.uniform(float(a), float(min(b, s)))][by_float]
                except ValueError:
                    self.__b[i] = a
            else:
                if b <= 0:
                    # [a < 0, b <= 0]
                    try:
                        self.__b[i] = [random.randint(int(max(a, -s)), b),
                                       random.uniform(float(max(a, -s)), float(b))][by_float]
                    except ValueError:
                        self.__b[i] = b
                else:
                    # [a < 0, b > 0]
                    self.__b[i] = [random.randint(int(max(a, -s)), int(min(b, s))),
                                   random.uniform(float(max(a, -s)), float(min(b, s)))][by_float]
            if self.__b[i] == 0:
                self.__b[i] = (sgn_a, sgn_b)[max(abs(a), abs(b)) == abs(b)]
                if by_float:
                    self.__b[i] += random.random()
                    if self.__b[i] > b:
                        self.__b[i] = b - 0.001

    # Заполнение случайными числами
    # good - показатель обусловленности
    def fill_rand(self, a, b, good=True, by_float=True):
        if a >= b:
            raise ValueError("Неверно заданный интервал")
        if good:
            self.__fill_diag_rand_good(a, b, by_float)
        else:
            self.__fill_diag_rand_bad(a, b, by_float)
        # Заполняем столбцы по изначальным интервалам т.к. они ни на что не влияют
        self.__p.fill_rand(a, b, by_float=by_float)
        self.__q.fill_rand(a, b, by_float=by_float)
        size = len(self.__a)
        # Перезапись дублирующихся элементов
        if size >= 1:
            self.__q[1] = self.__b[1]
        if size >= 2:
            self.__p[1] = self.__a[1]
            self.__p[2], self.__q[2] = self.__b[2], self.__c[2]
        if size >= 3:
            self.__p[3] = self.__c[3]

    # Нахождение решение системы уравнений
    def solution(self, v, x=None, print_step=False):
        size = len(v)
        f = v.copy()
        m = Matrix()
        # Заводим копии чтобы не испортить исходную матрицу и работаем в последствии с ними
        m.__a, m.__b, m.__c, m.__p, m.__q = \
            self.__a.copy(), self.__b.copy(), self.__c.copy(), self.__p.copy(), self.__q.copy()
        # 1 шаг - создание нулей на верхней кодиагонали и единиц на диагонали
        for i in range(size, 1, -1):
            tmp = m.__b[i]
            if tmp != 1:
                # Если единица есть изначально, то делить вектор на главный элемент не нужно
                if tmp == 0:
                    mes = "Встречено деление на 0 в операции на " + str(i) + " строке"
                    raise ZeroDivisionError(mes)
                m.__b[i] = 1
                m.__c[i] /= tmp
                m.__p[i] /= tmp
                m.__q[i] /= tmp
                f[i] /= tmp
            tmp = m.__a[i - 1]
            if tmp != 0:
                # Если ноль уже на верхней кодиагонали то ничего делать не надо
                m.__a[i - 1] = 0
                m.__b[i - 1] -= tmp * m.__c[i]
                m.__p[i - 1] -= tmp * m.__p[i]
                m.__q[i - 1] -= tmp * m.__q[i]
                # Защита от дублирующихся элементов
                if i == 4:
                    m.__c[i - 1] = m.__p[i - 1]
                if i == 3:
                    m.__c[i - 1] = m.__q[i - 1]
                f[i - 1] -= tmp * f[i]
        # Устанавливаем финальные единицы в последней правой верхней клетке матрицы
        f[1] /= m.__b[1]
        m.__b[1], m.__q[1] = 1, 1
        if print_step:
            if x is None:
                print(f"После 1 шага:",
                      f"Матрица A:",
                      m,
                      "Вектор F:",
                      f,
                      sep='\n', end='\n\n')
            else:
                print(f"После 1 шага:",
                      f"Матрица A:",
                      m,
                      "Вектор F:",
                      f,
                      "Вектор Ft:",
                      m * x,
                      sep='\n', end='\n\n')
        # 2 шаг - преобразование в 0 столбца q
        for i in range(2, size + 1):
            f[i] -= f[1] * m.__q[i]
            m.__q[i] = 0
            if i == 2:
                m.__c[i] = 0
        # и преобразование в 0 столбца p
        for i in range(3, size + 1):
            f[i] -= f[2] * m.__p[i]
            m.__p[i] = 0
            if i == 3:
                m.__c[i] = 0
        if print_step:
            if x is None:
                print(f"После 2 шага:",
                      f"Матрица A:",
                      m,
                      "Вектор F:",
                      f,
                      sep='\n', end='\n\n')
            else:
                print(f"После 2 шага:",
                      f"Матрица A:",
                      m,
                      "Вектор F:",
                      f,
                      "Вектор Ft:",
                      m * x,
                      sep='\n', end='\n\n')
        # 3 шаг - создание 0 в нижней кодиагонали
        for i in range(4, size + 1):
            f[i] -= m.__c[i] * f[i - 1]
            m.__c[i] = 0
        # поскольку матрица единичная с побочной диагональю, вектор решения будет перевернут
        if print_step:
            if x is None:
                print(f"После 3 шага:",
                      f"Матрица A:",
                      m,
                      "Вектор F:",
                      f,
                      sep='\n', end='\n\n')
            else:
                print(f"После 3 шага:",
                      f"Матрица A:",
                      m,
                      "Вектор F:",
                      f,
                      "Вектор Ft:",
                      m * x,
                      sep='\n', end='\n\n')
        return f.reverse()

    # Метод подсчета ошибки для тестов
    # x - полученный численный вектор
    # xt - точный исходный вектор
    # q - неотрицательное число подбираемое с учетом особенностей решаемой системы уравнений
    @staticmethod
    def error_rate(x, xt, q):
        size = len(x)
        d = Vector()
        for i in range(1, size + 1):
            if x[i] > q:
                d.push_back(abs((x[i] - xt[i]) / abs(xt[i])))
            else:
                d.push_back(abs(x[i] - xt[i]))
        return d.norm()
