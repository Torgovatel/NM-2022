import io
import random

# Класс для работы с векторами основанный на python-list
class Vector:
    # Инициализатор (заполняет default значением = 0)
    def __init__(self, size=0):
        self.__buf = [0 for _ in range(size)]

    # Вставка в конец вектора (через метод python-list)
    def push_back(self, value):
        self.__buf.append(value)

    # Переопределение вызова функции len()
    def __len__(self):
        return len(self.__buf)

    # Переопределение вызова функции abs()
    def __abs__(self):
        v = Vector()
        for x in self.__buf:
            v.__buf.append(abs(x))
        return v

    # Переопределение оператора [] для получения значения
    def __getitem__(self, item):
        return self.__buf[item - (item > 0)]

    # Переопределение оператора [] для присваивания значения
    def __setitem__(self, key, value):
        self.__buf[key - (key > 0)] = value

    # Переопределение оператора +
    def __add__(self, other):
        # Ставим защиту от неподходящих типов
        if type(other) != Vector:
            raise TypeError("Операция + возможна только в случае типов Vector + Vector")
        v = Vector()
        # Суммируем соответствующие значения
        for x, y in zip(self.__buf, other.__buf):
            v.push_back(x + y)
        return v

    # Переопределение оператора -
    def __sub__(self, other):
        # Ставим защиту от неподходящих типов
        if type(other) != Vector:
            raise TypeError("Операция - возможна только в случае типов Vector + Vector")
        v = Vector()
        # Вычитаем соответсвующие значения
        for x, y in zip(self.__buf, other.__buf):
            v.push_back(x - y)
        return v

    # Переопределение оператора * (вектора на число)
    def __mul__(self, other):
        # Ставим защиту от неподходящих типов
        if type(other) != int and type(other) != float:
            raise TypeError("Операция * возможна только в случае типов Vector * int/double")
        v = Vector()
        # Умножаем
        for x in self.__buf:
            v.push_back(x * other)
        return v

    # Переопределение оператора * левостороннего
    def __rmul__(self, other):
        return self * other

    # Переопределение оператора * с самоприсваиванием
    def __imul__(self, other):
        return self * other

    # Переопределение оператора /
    def __truediv__(self, other):
        # Ставим защиту от неподходящих типов
        if type(other) != int and type(other) != float:
            raise TypeError("Операция / возможна только в случае типов Vector * int/float")
        # И защиту от деления на 0
        if other == 0:
            raise ZeroDivisionError("Недопустимо деление на 0")
        return self * (1 / other)

    # Переопределение оператора / левостороннего
    def __rtruediv__(self, other):
        return self / other

    # Переопределение оператора / с самоприсваиванием
    def __itruediv__(self, other):
        return self / other

    # Переопределение отладочной информации
    def __repr__(self):
        return self.__buf.__repr__()

    # Переопределение пользовательского строкового представления
    def __str__(self):
        return self.__buf.__str__()

    # Подсчет нормы как максимума по модулю
    def norm(self):
        return max(abs(self))

    # Считывание с консоли
    def read(self):
        for x in input().split():
            self.__buf.append(float(x))

    # Вывод в консоль
    def print(self):
        print(*self.__buf, sep=' ', end='')

    # Считывание с файла
    def file_read(self, file_descriptor):
        # Ставим защиту от неподходящих типов
        if type(file_descriptor) != io.TextIOWrapper:
            raise TypeError("file_descriptor должен ссылаться на объект полученный функцией open(...)")
        for value in file_descriptor.readline().split():
            self.__buf.append(float(value))

    # Вывод в файл
    def write(self, file_descriptor):
        if type(file_descriptor) != io.TextIOWrapper:
            raise TypeError("file_descriptor должен ссылаться на объект полученный функцией open(...)")
        file_descriptor.write(' '.join([str(x) for x in self.__buf]))

    # Заполнение случайными числами
    def fill_rand(self, a, b, by_float=False, rand_sign=False):
        if a >= b or (b - a) <= 1:
            raise ValueError("Неверно заданный интервал (расширьте и проверьте границы)")
        if by_float:
            for i in range(len(self.__buf)):
                self.__buf[i] = random.uniform(float(a), float(b))
                # В случае нуля оставляем что-то маленькое, если это возможно
                if self.__buf[i] == 0:
                    if b != 0:
                        self.__buf[i] = b
                    else:
                        self.__buf[i] = a
                if rand_sign:
                    self.__buf[i] *= random.choice([1, -1])
        else:
            for i in range(len(self.__buf)):
                self.__buf[i] = random.randint(a, b)
                if self.__buf[i] == 0:
                    if b != 0:
                        self.__buf[i] = b
                    else:
                        self.__buf[i] = a
                if rand_sign:
                    self.__buf[i] *= random.choice([1, -1])
        return self

    # Глубокое копирование
    def copy(self):
        v = Vector()
        v.__buf = self.__buf[:]
        return v

    # Переворот списка
    def reverse(self):
        v = self.copy()
        v.__buf = v.__buf[::-1]
        return v

    # Поиск минимума
    def min(self):
        return min(self.__buf)

    # Поиск максимума
    def max(self):
        return max(self.__buf)
