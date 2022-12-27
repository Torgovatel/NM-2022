from Matrix import *
from TapeMatrix import *
import random
import matplotlib.pyplot as plt
import time
import math
from BaseFunctions import *
from GaussAutoTesting import *
from HolAutoTesting import *
import BaseParams as BP


# в случае command = help
# выводим пользователю доступные пункты меню
def help():
    print("Список команд:\n",
          "stop - завершить работу",
          "status - вывести статус системных переменных",
          "auto_test [набор общих флагов] - начать работу с заданными флагами",
          "read <флаг типа> - считываем локальный объект",
          "print <флаг типа> - записывает локальный объект",
          "gen <флаг типа> - генерирует объект нужного типа по заданным общим флагам",
          "solve - решить заданную локальную систему",
          "analyze -n start end cnt - анализ ошибки при росте N от start до end по cnt вычислений",
          "\tобщие флаги:",
          "\t\t-type val - устанавливает размерность матрицы = val (H или G)",
          "\t\t-n val - устанавливает размерность матрицы = val (int)",
          "\t\t-cnt val - устанавливает количество опытов = val (int)",
          "\t\t-k val - устанавливает коэффициент приведения = val (int)",
          "\t\t-ab val1 val2 - устанавливает границы интервалов генерации матрицы [val1, val2] (int, int)",
          "\t\t-good val - устанавливает флаг обусловленности матрицы для генерации = val : (bool as int)",
          "\t\t\t* True - генерация обусловленной матрицы",
          "\t\t\t* False - генерация необусловленной матрицы",
          "\t\t-by_float val - устанавливает флаг отладочной информации для обработки = val : (bool as int)",
          "\t\t\t* True - генерация матриц заполненных double числами",
          "\t\t\t* False - генерация матриц заполненных int числами",
          "\t\t-debug val - устанавливает флаг отладочной информации для обработки = val : (bool as int)",
          "\t\t\t* True - выводить % выполнения обработки",
          "\t\t\t* False - не выводить % выполнения обработки",
          "\t\t-gauss_tape val - устанавливает флаг генерации матрицы Гаусса = val : (bool as int)",
          "\t\t\t* True - матрица Гаусса будет ленточной",
          "\t\t\t* False - матрица Гаусса будет обычной",
          "\tфлаги типа:",
          "\t\t-matrix - объект : матрица",
          "\t\t-vector - объект : вектор",
          sep='\n')


# в случае command = status
# выводим пользователю текущие состояния переменных-настроек
def status():
    print("Статус системных переменных:",
          "\tСпособ решения: type = " + ("undefined", "Гаусс", "Холецкий")[BP.type],
          f"\tКоличество auto опытов: cnt = {BP.cnt}",
          f"\tРазмерность системы: N = {BP.N}",
          f"\tПоловина ширины ленты: L = {BP.L}",
          f"\tИнтервал генерации: ab = [{BP.a}, {BP.b}]",
          f"\tОбусловленность: good = {BP.good}",
          f"\tКоэффициент приведения: k = {BP.k}",
          f"\tВещественные числа: by_float = {BP.by_float}",
          f"\tИндикатор состояния выполнения: debug = {BP.debug}",
          f"\tФлаг матрицы Гаусса: gauss_tape = {BP.gauss_tape}",
          f"\tМатрица = {('fill', 'empty')[BP.matrix is None]}",
          f"\tВектор = {('fill', 'empty')[BP.vector is None]}",
          sep='\n')


# в случае command = auto_test
# проводим множественное тестирование по заданным настройкам
def auto_test(cmd_list):
    start_processing = time.time()
    x_err_avr, f_err_avr = 0, 0
    if BP.type == BP.HOL or BP.type == BP.GAUSS and BP.gauss_tape:
        x_err_avr, f_err_avr = average_by_test(HAT)
        processing_time = time.time() - start_processing
        print(f"Произведено {BP.cnt} опытов со следующими параметрами:",
              ("Необусловленная", "Обусловленная")[BP.good] + f" матрица {BP.N}x{BP.N}",
              f"Интервал генерации: [{BP.a}, {BP.b}]",
              f"Коэффициент: L = {BP.L}\n",
              f"Коэффициент: k = {BP.k}\n",
              "Результаты обработки:",
              f"Погрешность Х = {x_err_avr}",
              f"Погрешность F = {f_err_avr}\n",
              f"Время обработки: {time_in_min_sec(processing_time)}",
              sep='\n')
    else:
        x_err_avr, f_err_avr = average_by_test(GAT)
        processing_time = time.time() - start_processing
        print(f"Произведено {BP.cnt} опытов со следующими параметрами:",
              ("Необусловленная", "Обусловленная")[BP.good] + f" матрица {BP.N}x{BP.N}",
              f"Интервал генерации: [{BP.a}, {BP.b}]\n",
              "Результаты обработки:",
              f"Погрешность Х = {x_err_avr}",
              f"Погрешность F = {f_err_avr}\n",
              f"Время обработки: {time_in_min_sec(processing_time)}",
              sep='\n')


# в случае command = read
# считываем заданный объект
def read(cmd_list):
    ind = cmd_list.index("read") + 1

    # вектор считываем из одной строки
    if cmd_list[ind] == "-vector":
        BP.vector = [float(x) for x in input().split()][:BP.N]
        return True

    # матрицу считываем из введенных и скленных вместе n строк
    if cmd_list[ind] == "-matrix":
        if BP.type == BP.HOL:
            BP.matrix = TapeMatrix(BP.N, BP.L)
        else:
            BP.matrix = Matrix(BP.N, BP.L)
        st = ""
        for _ in range(BP.N):
            st += input() + ' '
        BP.matrix.from_str(st)
        return True

    return False


# в случае command = print
# выводим пользователю текущий объект
def mprint(cmd_list):
    ind = cmd_list.index("print") + 1

    if cmd_list[ind] == "-vector":
        if not (BP.vector is None):
            print(BP.vector)
        return True

    if cmd_list[ind] == "-matrix":
        if not (BP.matrix is None):
            print(BP.matrix)
        return True

    return False


# в случае command = gen
# генерируем пользователю текущиий объект
def gen(cmd_list):
    ind = cmd_list.index("gen") + 1

    if cmd_list[ind] == "-vector":
        if BP.by_float:
            BP.vector = [random.uniform(float(BP.a), float(BP.b)) for _ in range(BP.N)]
        else:
            BP.vector = [random.randint(int(BP.a), int(BP.b)) for _ in range(BP.N)]
        return True

    if cmd_list[ind] == "-matrix":
        if BP.type == BP.HOL:
            BP.matrix = TapeMatrix(BP.N, BP.L)
            BP.matrix.fill_rand(BP.a, BP.b, k=BP.k, good=BP.good, by_float=BP.by_float)
        else:
            BP.matrix = Matrix(BP.N, BP.L)
            if BP.gauss_tape:
                BP.matrix.tape_fill_rand(BP.a, BP.b, k=BP.k, good=BP.good, by_float=BP.by_float)
            else:
                BP.matrix.fill_rand(BP.a, BP.b)
        return True

    return False


# в случае command = solve
# решаем систему по заданным настройкам
def solve():
    if BP.matrix is None or BP.vector is None:
        print("dont have input data...")
    else:
        ft = BP.matrix * BP.vector
        print("По заданной матрице и вектору X, точный вектор правой части F:",
              ft,
              sep='\n')
        try:
            x = []
            if BP.type == BP.HOL:
                x = BP.matrix.sbh(ft)
            else:
                x = BP.matrix.sbg(ft)
            x_err = rate(x, BP.vector)
            f = BP.matrix * x
            f_err = rate(f, ft)
            print(f"Результаты обработки:",
                  f"Xt = {BP.vector}",
                  f"X = {x}",
                  f"Ft = {ft}",
                  f"F = {f}",
                  f"Погрешность нахождения X = {x_err}",
                  f"Погрешность нахождения F = {f_err}",
                  sep='\n')
        except ZeroDivisionError:
            print("К данной матрице алгоритм не может быть применён")


# Далее идут функции с установкой значения одноименного параметра
def set_N(cmd_list):
    BP.N = int(cmd_list[cmd_list.index("-n") + 1])
    if BP.N <= 0:
        BP.N = 1


def set_L(cmd_list):
    BP.L = int(cmd_list[cmd_list.index("-l") + 1])
    if BP.L <= 0:
        BP.L = 1


def set_k(cmd_list):
    BP.k = int(cmd_list[cmd_list.index("-k") + 1])
    if BP.k <= 2:
        BP.k = 2


def set_cnt(cmd_list):
    BP.cnt = int(cmd_list[cmd_list.index("-cnt") + 1])
    if BP.cnt <= 0:
        BP.cnt = 1


def set_ab(cmd_list):
    BP.a, BP.b = int(cmd_list[cmd_list.index("-ab") + 1]), int(cmd_list[cmd_list.index("-ab") + 2])


def set_good(cmd_list):
    ind = cmd_list.index("-good") + 1
    BP.good = (False, True)[cmd_list[ind] == "true"]


def set_by_float(cmd_list):
    ind = cmd_list.index("-by_float") + 1
    BP.by_float = (False, True)[cmd_list[ind] == "true"]


def set_type(cmd_list):
    ind = cmd_list.index("-type") + 1
    if cmd_list[ind] == 'h':
        BP.type = BP.HOL
    else:
        BP.type = BP.GAUSS


def set_gauss_tape(cmd_list):
    ind = cmd_list.index("-gauss_tape") + 1
    BP.gauss_tape = (False, True)[cmd_list[ind] == "true"]


def set_debug(cmd_list):
    ind = cmd_list.index("-debug") + 1
    BP.debug = (False, True)[cmd_list[ind] == "true"]


def analyze(cmd_list):
    ind = cmd_list.index("analyze") + 1
    if cmd_list[ind] == "n":
        start, end = int(cmd_list[ind + 1]), int(cmd_list[ind + 2])
        x_err, f_err = [], []
        old_N, old_cnt, old_L = BP.N, BP.cnt, BP.L
        BP.cnt = int(cmd_list[ind + 3])
        start, end = math.ceil(math.log2(start)), math.floor(math.log2(end))
        n_cur = 2**(start-1)
        for n in range(start, end + 1):
            n_cur *= 2
            BP.N = n_cur
            BP.L = int(BP.N * old_L/old_N)
            xe, fe = average_by_test(HAT)
            x_err.append(xe*10**15), f_err.append(fe*10**13)
            print(f"N = {BP.N}, L = {BP.L}:",
                  f"x_err = {xe}",
                  f"f_err = {fe}\n",
                  sep='\n')
        fig = plt.figure("Анализ роста ошибки при увеличении N")
        xx = fig.add_subplot(3, 1, 1)
        fx = fig.add_subplot(3, 1, 3)
        xx.set_xlabel("размерность системы N=2^x")
        xx.set_ylabel("ошибка * 10^15")
        xx.set_title(label="График роста ошибки вектора X")
        fx.set_xlabel("размерность системы N=2^x")
        fx.set_ylabel("ошибка * 10^15")
        fx.set_title(label="График роста ошибки вектора F")
        xx.plot(range(start, end+1), x_err)
        fx.plot(range(start, end+1), f_err)
        plt.show()
        BP.N = old_N
        BP.cnt = old_cnt
        BP.L = old_L
    elif cmd_list[ind] == "-l":
        pass
