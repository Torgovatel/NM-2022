"""Множественное тестирование методом Холецкого"""

from BaseFunctions import *
import BaseParams as BP
from TapeMatrix import *


def HAT():
    x_errors, f_errors = [], []
    p = 1
    for i in range(BP.cnt):
        # Генерируем данные
        m = TapeMatrix(BP.N, BP.L)
        m.fill_rand(BP.a, BP.b, k=BP.k, good=BP.good, by_float=BP.by_float)
        xt = []
        if BP.by_float:
            xt = [random.uniform(float(BP.a), float(BP.b)) for _ in range(BP.N)]
        else:
            xt = [random.randint(int(BP.a), int(BP.b)) for _ in range(BP.N)]
        # Решаем систему и находим ошибки
        ft = m * xt
        try:
            x = m.sbh(ft)
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
