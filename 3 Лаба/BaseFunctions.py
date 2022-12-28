"""Набор вспомогательных функций, используемых в решении"""

import random
import BaseParams as BP
from typing import List, Tuple

def norm(w: List[float]) -> float:
    """
    Функция подсчета евклидовой нормы вектора.

    Args:
        w: вектор в вещественных координатах.

    Returns:
        вещественное число - евклидову норму переданного вектора.
    """
    return sum(map(lambda x: x**2, w))**0.5


def normalize(w: List[float]) -> List[float]:
    """
    Функция нормирования переданного вещественного вектора по евклидовой номер.

    Args:
        w: вектор в вещественных координатах.

    Returns:
        новый вектор в вещественных координатах, нормированный по заданному вектору.
    """
    w_norm = norm(w)
    return list(map(lambda x: x / w_norm, w))


def get_max_abs_index(lst: List[float]) -> int:
    """
    Функция поиска максимального по модулю элемента в списке.

    Args:
        lst: список вещественных чисел для поиска.

    Returns:
        целое число - индекс максимального по модулю элемента в переданном списке.
    """
    i_abs_max = 0
    for i in range(1, len(lst)):
        if abs(lst[i_abs_max]) < abs(lst[i]):
            i_abs_max = i
    return i_abs_max


def get_list_without_cnt_of_abs_max(lst: List[float], cnt: int) -> List[float]:
    """
    Функция замещения элементов списка.
    Замещает переданное количество максимальных по модулю элементов списка фиктивными 0.

    Args:
        lst: список вещественных чисел для обработки.
        cnt: количество элементов для замещения.

    Returns:
        преобразованный список с фиктивными 0 элементами.
    """
    lst = lst[:]
    for _ in range(cnt):
        lst[get_max_abs_index(lst)]=0
    return lst


def corner(v1: List[float], v2: List[float]) -> float:
    """
    Функция анализа угла между векторами.
    Находит косинус угла между векторами и абсолютную разность его отклонения от 1 (или угла от 0 угла).

    Args:
        v1: вещественный вектор для анализа.
        v2: вещественний вектор для анализа.

    Returns:
        абсолютную разность отклонения косинуса угла от 1 (или угла от 0 угла).
    """
    res = sum([v1[i]*v2[i] for i in range(BP.N)])
    res /= norm(v1) * norm(v2)
    return abs(1-res)


def exhaustion() -> Tuple[float, List[float]]:
    """
    Функция метода исчерпывания.
    Находит 2 максимальное по модулю собственное значение матрицы, и соответсвующий ему собственный вектор.

    Returns:
    Найденное собственное значение и соответсвующий ему собственный вектор.
    """
    A1 = BP.matrix.copy()
    tmp = get_list_without_cnt_of_abs_max(BP.h, 0)
    ind = get_max_abs_index(tmp)
    hn = BP.h[ind]
    xn = BP.X[ind]
    for i in range(BP.N):
        for j in range(BP.N):
            A1.a[i][j] -= hn * xn[i] * xn[j]
    x_cur = [0 for _ in range(BP.N)]
    for i in range(BP.N):
        while x_cur[i] == 0:
            x_cur[i] = random.randint(BP.a, BP.b + 1)
    i_cur = 0
    x_prev = 0
    b_prev = 0
    b_cur = 0
    while (BP.by_iter and i_cur < BP.iter) or \
            (i_cur < 1 or abs(b_prev - b_cur) > BP.h_eps and corner(x_cur, x_prev) > BP.v_eps):
        v_cur = normalize(x_cur)
        x_prev = x_cur
        x_cur = A1 * v_cur
        b_prev = b_cur
        b_cur = sum([v_cur[i] * x_cur[i] for i in range(BP.N)])
        i_cur += 1
    print(f"{i_cur} итераций:")
    return b_cur, normalize(x_cur)


def time_in_min_sec(t: float) -> str:
    """
    Функция перевода количества прошедших секунд в строковое представление.

    Args:
        t: вещественное число секунд для преобразования.

    Returns:
        строку, формата [x минут y секунд].
    """
    s_min = "минут"
    s_sec = "секунд"
    time_int = int(t)
    if time_int // 60 % 10 == 1:
        s_min = "минута"
    elif time_int // 60 % 10 in [2, 3, 4]:
        s_min = "минуты"
    if time_int % 60 % 10 == 1:
        s_sec = "секунда"
    elif time_int % 60 % 10 in [2, 3, 4]:
        s_sec = "секунды"
    result = f"{int(time_int) // 60} {s_min}, {int(time_int) % 60} {s_sec}"
    return result
