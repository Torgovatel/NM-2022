"""Определение класса симметричной ленточной матрицы"""

import random


class Matrix:
    # Инициализатор:
    # N - размерность матрицы
    # value - значение по умолчанию
    def __init__(self, N, L=None, value=0):
        self.N = N
        if L is None:
            self.L = N
        else:
            self.L = L
        # A - матрица ленты
        self.A = [[value for j in range(N)] for i in range(N)]

    # Конвертация строки в матрицу
    # Используется для последующего ввода
    def from_str(self, str):
        elems = str.strip().split()
        if len(elems) != self.N ** 2:
            raise ValueError(f"Для записи матрицы было необходимо {self.N**2} значений")
        elem_ind = 0
        for i in range(self.N):
            for j in range(self.N):
                self.A[i][j] = float(elems[elem_ind])
                elem_ind += 1

    # Преобразование матрицы в строку для вывода по заданному буферу
    def __to_str__(self, arr):
        res = ""
        # Находим максимальную длину строкового представления числа (для форматирования вывода)
        max_length = max([len(str(arr[i][j])) for i in range(self.N) for j in range(self.N)]) + 1
        for i in range(self.N):
            for j in range(self.N):
                elem = arr[i][j]
                s_elem = str(elem)
                if elem >= 0:
                    s_elem = ' ' + s_elem
                res += s_elem.ljust(max_length) + ' '
            res += '\n'
        return res

    # Переопределение строкового представления
    def __str__(self):
        return self.__to_str__(self.A)

    # Переопределение вывода отладочной информации
    def __repr__(self):
        return self.A.__repr__()

    # Переопределение умножения
    def __mul__(self, x):
        if type(x) == Matrix:
            C = Matrix(self.N, self.L)
            for i in range(self.N):
                for j in range(self.N):
                    for k in range(self.N):
                        C.A[i][j] += self.A[i][k] * x.A[k][j]
            return C
        # Проверяем условия когда перемножать нельзя
        if type(x) != list and type(x) != tuple():
            raise TypeError("Умножение возможно только в случае Matrix * tuple/list")
        if len(x) != self.N:
            raise ValueError(f"Размерность вектора должна быть = {self.N}")
        # Перемножаем
        f = [0 for _ in range(self.N)]
        for num in range(self.N):
            f[num] = 0
            for j in range(self.N):
                f[num] += self.A[num][j] * x[j]
        return f

    # Нахождение индекса максимума в столбце i по строке
    # с заданными в dict взятыми строками
    # и с заданным буфером arr
    def col_max_ind(self, j, dict, arr):
        if not(0 <= j < self.N):
            raise ValueError
        i_res = None
        val = None
        for i in range(self.N):
            if not dict[i] and (val is None or abs(arr[i][j]) > val):
                i_res = i
                val = abs(arr[i_res][j])
        return i_res

    # Вычитание строк
    def sub_row(self, a, b):
        c = [x for x in range(self.N)]
        for i in range(self.N):
            c[i] = a[i] - b[i]
        return c

    # Перемножение строки на число
    def mul_row(self, row, num):
        c = [x for x in range(self.N)]
        for i in range(self.N):
            c[i] = row[i] * num
        return c

    # Решение системы методом Гаусса с частичной стратегией выбора ведущего элемента по столбцу
    def sbg(self, f):
        f = f[:]
        A = [self.A[i][:] for i in range(self.N)]
        # шаг 1 - приведение матрицы
        dict = {num: False for num in range(0, self.N)}     # словарь взятых строк
        list = [x for x in range(self.N)]                   # список порядковых номеров строк (строк с n-ind элементов)
        # Обходим все столбцы
        for j in range(self.N):
            max_ind = self.col_max_ind(j, dict, A)
            k = A[max_ind][j]
            # Преобразовываем строку и вектор правой части
            A[max_ind] = self.mul_row(A[max_ind], 1/k)
            A[max_ind][j] = 1
            f[max_ind] /= k
            # Помечаем строку обработанной и записываем порядковый номер
            dict[max_ind] = True
            list[j] = max_ind
            # Вычитаем текущую строку из необработанных если это имеет смысл
            for i in range(self.N):
                if not dict[i] and A[i][j] != 0:
                    f[i] -= f[max_ind] * A[i][j]
                    A[i] = self.sub_row(A[i], self.mul_row(A[max_ind], A[i][j]))
        # Восстановление решения по готовой матрице
        x = [0 for _ in range(self.N)]
        for i in range(self.N - 1, -1, -1):
            str_num = list[i]
            val = f[str_num]
            for j in range(self.N - i - 1):
                val -= A[str_num][self.N - j - 1] * x[self.N - j - 1]
            x[i] = val / A[str_num][i]
        return x

    # Заполнение матрицы случайными числами по заданным параметрам
    def fill_rand(self, a, b, by_float=False):
        if by_float:
            for i in range(self.N):
                for j in range(self.N):
                    self.A[i][j] = random.uniform(float(a), float(b))
        else:
            for i in range(self.N):
                for j in range(self.N):
                    self.A[i][j] = random.randint(int(a), int(b) + 1)

    # Заполнение ленточной матрицы случайными числами
    def tape_fill_rand(self, a, b, k=2, good=False, by_float=False):
        L, U = Matrix(self.N), Matrix(self.N)
        if by_float:
            for i in range(self.N):
                U.A[i][i] = 1
                for j in range(i + 1, min(i + self.L, self.N)):
                    while U.A[i][j] == 0:
                        U.A[i][j] = random.uniform(float(a), float(b))
            for i in range(self.N):
                for j in range(max(0, i - self.L + 1), i + 1):
                    while L.A[i][j] == 0:
                        L.A[i][j] = random.uniform(float(a), float(b))
        else:
            for i in range(self.N):
                U.A[i][i] = 1
                for j in range(i + 1, min(i + self.L, self.N)):
                    while U.A[i][j] == 0:
                        U.A[i][j] = random.randint(int(a), int(b) + 1)
            for i in range(self.N):
                for j in range(max(0, i - self.L + 1), i + 1):
                    while L.A[i][j] == 0:
                        L.A[i][j] = random.randint(int(a), int(b) + 1)
        self.A = (L * U).A
        k = 10**k
        for i in range(self.N):
            self.A[i][i] /= k
