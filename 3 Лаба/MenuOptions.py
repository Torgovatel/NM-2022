from Matrix import *
import random
import matplotlib.pyplot as plt
import time
import math
from BaseFunctions import *
import BaseParams as BP


# в случае command = help
# выводим пользователю доступные пункты меню
def help():
    print("Список команд:\n",
          "stop - завершить работу",
          "status - вывести статус системных переменных",
          "read <флаг типа> - считываем локальный объект",
          "print <флаг типа> - записывает локальный объект",
          "gen <флаг типа> - генерирует объект нужного типа по заданным общим флагам",
          "analyze -n start end cnt - анализ ошибки при росте N от start до end по cnt вычислений",
          "\tобщие флаги:",
          "\t\t-n val - устанавливает размерность матрицы = val (int)",
          "\t\t-cnt val - устанавливает количество опытов = val (int)",
          "\t\t-ab val1 val2 - устанавливает границы интервалов генерации матрицы [val1, val2] (int, int)",
          "\t\t-debug val - устанавливает флаг отладочной информации для обработки = val : (bool as int)",
          "\t\t\t* True - выводить % выполнения обработки",
          "\t\t\t* False - не выводить % выполнения обработки",
          "\tфлаги типа:",
          "\t\t-m - объект : матрица",
          "\t\t-h - объект : список собственных значений",
          "\t\t-x - объект : список собственных векторов",
          sep='\n')


# в случае command = status
# выводим пользователю текущие состояния переменных-настроек
def status():
    print("Статус системных переменных:",
          f"\tКоличество auto опытов: cnt = {BP.cnt}",
          f"\tРазмерность системы: N = {BP.N}",
          f"\tИнтервал генерации: ab = [{BP.a}, {BP.b}]",
          f"\tМатрица = {('fill', 'empty')[BP.matrix is None]}",
          f"\tСобственные значения h = {('fill', 'empty')[BP.h is None]}",
          f"\tСобственные вектора x = {('fill', 'empty')[BP.X is None]}",
          sep='\n')

# в случае command = read
# считываем заданный объект
def read(cmd_list):
    ind = cmd_list.index("read") + 1

    # матрицу считываем из введенных и скленных вместе n строк
    if cmd_list[ind] == "-m":
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

    if cmd_list[ind] == "-m":
        if not (BP.matrix is None):
            print(BP.matrix)
        return True

    if cmd_list[ind] == "-h":
        if not (BP.h is None):
            print(f"h: {BP.h}")
        return True

    if cmd_list[ind] == "-x":
        if not (BP.X is None):
            for i in range(len(BP.X)):
                print(f"x{i+1}: {BP.X[i]}")
        return True
    return False


# в случае command = gen
# генерируем пользователю текущиий объект
def gen(cmd_list):
    ind = cmd_list.index("gen") + 1
    BP.matrix = Matrix(BP.N)
    BP.h, BP.X = BP.matrix.generate(a=BP.a, b=BP.b)
    return False


# Далее идут функции с установкой значения одноименного параметра
def set_N(cmd_list):
    BP.N = int(cmd_list[cmd_list.index("-n") + 1])
    if BP.N <= 0:
        BP.N = 1

def set_cnt(cmd_list):
    BP.cnt = int(cmd_list[cmd_list.index("-cnt") + 1])
    if BP.cnt <= 0:
        BP.cnt = 1

def set_ab(cmd_list):
    BP.a, BP.b = int(cmd_list[cmd_list.index("-ab") + 1]), int(cmd_list[cmd_list.index("-ab") + 2])
