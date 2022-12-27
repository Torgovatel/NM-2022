"""множественное тестирование методом Гаусса с выбором по столбцу"""

from BaseFunctions import *
import BaseParams as BP
from Matrix import *

def GAT():
    x_errors, f_errors = [], []
    p = 1
    for i in range(BP.cnt):
        # Генерируем данные
        m = Matrix(BP.N)
        m.fill_rand(BP.a, BP.b, by_float=BP.by_float)
        xt = []
        if BP.by_float:
            xt = [random.uniform(float(BP.a), float(BP.b)) for _ in range(BP.N)]
        else:
            xt = [random.randint(int(BP.a), int(BP.b)) for _ in range(BP.N)]
        # Решаем систему и находим ошибки
        ft = m * xt
        try:
            x = m.sbg(ft)
            f = m * x
            x_err = rate(x, xt)
            f_err = rate(f, ft)
            # Записываем их в список
            x_errors.append(x_err)
            f_errors.append(f_err)
        except ZeroDivisionError:
            pass
        if BP.debug and i >= p * (BP.cnt / 100):
            print("\r" * (p % 10 + 1), end='')
            print(f"{p}%", end='')
            p += 1
    if BP.debug:
        print("100%", end='')
        print("\r\r\r\r", end='')
    return x_errors, f_errors

