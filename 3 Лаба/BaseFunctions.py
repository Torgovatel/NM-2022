"""Набор вспомогательных функций, используемых в решении"""

import random
import BaseParams as BP
from typing import List, Tuple
import MenuOptions

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


def exhaustion() -> Tuple[Tuple[int, float], List[float], float, int]:
    """
    Функция метода исчерпывания.
    Находит 2 максимальное по модулю собственное значение матрицы, и соответсвующий ему собственный вектор.

    Returns:
    ( (индекс с.з., с.з), собственный вектор, оценку точности решения, количество выполненных итераций).
    """
    A1 = BP.matrix.copy()
    tmp = get_list_without_cnt_of_abs_max(BP.h, 0)
    ind = get_max_abs_index(tmp)
    hn = BP.h[ind]
    xn = BP.X[ind]
    for i in range(BP.N):
        for j in range(BP.N):
            A1.a[i][j] -= hn * xn[i] * xn[j]
    tmp = get_list_without_cnt_of_abs_max(tmp, 1)
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
    x_cur = [A1.a[i][ind] for i in range(A1.n)]
    i_cur = 0
    x_prev = 0
    b_prev = 0
    b_cur = 0
    while (BP.by_iter and i_cur < BP.iter) or \
            (not BP.by_iter and (i_cur < 1 or abs(b_prev - b_cur) > BP.h_eps and corner(x_cur, x_prev) > BP.x_eps)):
        v_cur = normalize(x_cur)
        x_prev = x_cur
        x_cur = A1 * v_cur
        b_prev = b_cur
        b_cur = sum([v_cur[i] * x_cur[i] for i in range(BP.N)])
        i_cur += 1
    tmp = get_list_without_cnt_of_abs_max(tmp, 1)
    ind = get_max_abs_index(tmp)
    x_cur = normalize(x_cur)
    r = 0
    tmp = A1 * x_cur
    for i in range(len(tmp)):
        tmp[i] -= b_cur * x_cur[i]
    r = max(list(map(lambda x: abs(x), tmp)))
    return (ind, b_cur), x_cur, r, i_cur


def rate(x: List[float], xt: List[float]) -> float:
    """
    Метод подсчета ошибки нахождения вектора-решения.

    Args:
        x: подсчитанный вектор.
        xt: точный вектор.

    Returns:
        первую норму разности векторов.
    """
    size = len(x)
    d = []
    for i in range(size):
        d.append(abs(x[i] - xt[i]))
    return max(map(lambda x: abs(x), d))


def average_by_test():
    """
    Метод тестирования по вычислению средних значений.
    Запускается в случае ввода команды test.
    Выводит на экран таблицу, содержащую все основные данные о работе тестирующей системы.
    """
    list_h, list_x, list_r, list_iter_cnt = [], [], [], []
    list_h_t, list_x_t = [], []
    for i in range(BP.cnt):
        try:
            MenuOptions.gen()
            (h_ind, h), x, r, iter_cnt = exhaustion()
            list_h.append(h)                                # h подсчитанное
            list_h_t.append(BP.h[h_ind])                    # ht точное
            list_x.append(x[:])                             # x подсчитанный
            list_x_t.append(BP.X[h_ind][:])                 # xt точный
            list_r.append(r)                                # r подсчитанный
            list_iter_cnt.append(iter_cnt)                  # cnt_iter подсчитанный
        except Exception as e:
            e.with_traceback()

    h_aver = sum([abs(list_h[i] - list_h_t[i]) for i in range(len(list_h))]) / len(list_h)
    x_aver = sum([rate(list_x[i], list_x_t[i]) for i in range(len(list_x))]) / len(list_x)
    r_aver = sum(list_r) / len(list_r)
    iter_cnt_aver = sum(list_iter_cnt) / len(list_iter_cnt)
    string = "|      " + str(BP.N).ljust(6) + " |" + \
             "  " + f"  [{BP.ah} ; {BP.bh}]".ljust(12) + "  |" + \
             "      " + f"{BP.h_eps}".ljust(10) + "   |" + \
             "  " + f"{h_aver}"[:14].ljust(14) + "  |" + \
             "  " + f"{x_aver}"[:14].ljust(14) + "  |" + \
             "  " + f"{r_aver}"[:14].ljust(14) + "  |" + \
             "     " + f"{iter_cnt_aver}".ljust(8) + " |"
    # символы:       11              12            11                  18                 17                 17                14
    print("+-------------+----------------+-------------------+------------------+------------------+------------------+--------------+",
         f"| Размерность |   Диапазон h   |   h_esp = x_eps   |   Ср. оценка h   |   Ср. оценка x   |   Ср. оценка r   | Cр. cnt_iter |",
          "+-------------+----------------+-------------------+------------------+------------------+------------------+--------------+",
          string,
          "+-------------+----------------+-------------------+------------------+------------------+------------------+--------------+",
          sep='\n')


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
