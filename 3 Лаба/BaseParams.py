"""Набор глобальных пременных - флагов"""

# Набор констант для типа решения
UNDEF = 0
GAUSS = 1
HOL = 2

# Параметры задающие решение
cnt = 1000              # кол-во тестов
N = 6                   # размерность матрицы
L = 2                   # половина ширины ленты для матрицы Холецкого (ленточная симметричная)
a, b = -10, 10          # границы генерации элементов матрицы
by_float = False        # флаг генерации вещественных элементов
good = True             # флаг генерации обусловленной матрицы
debug = True            # флаг для вывода прогресса отладки
k = 2                   # коэффициент приведения для генерации необусловленной матрицы Холецкого
vector = None           # вектор для решения конкретной задачи пользователя
matrix = None           # матрица для решения конкретной задачи пользователя
type = GAUSS            # тип алгоритма применяемого для решения задачи
gauss_tape = True       # генерация ленточной матрицы для гаусса
