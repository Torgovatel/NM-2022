"""
Модуль настроек меню.
Содержит одноименные командные функции для запуска из основной части программы.
"""

from Matrix import *
import random
import matplotlib.pyplot as plt
import time
import math
from typing import List
from BaseFunctions import *
import BaseParams as BP


def help():
    """
    Функция, вызываемая в случае ввода команды help.
    Выводит на экран список пользовательских команд.
    """
    print("Список команд:\n",
          "stop - завершить работу",
          "status - вывести статус системных переменных",
          "read <флаг типа> - считываем локальный объект",
          "print <флаг типа> - записывает локальный объект",
          "gen <флаг типа> - генерирует объект нужного типа по заданным общим флагам",
          "solve - решить штуку",
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


def status():
    """
    Функция, вызываемая в случае ввода команды help.
    Выводит на экран состояние внутренних переменных.
    """
    print("Статус системных переменных:",
          f"\tКоличество auto опытов: cnt = {BP.cnt}",
          f"\tРазмерность системы: N = {BP.N}",
          f"\tИнтервал генерации: ab = [{BP.a}, {BP.b}]",
          f"\tНаходить по итерациям: by_iter = {BP.by_iter}",
          f"\tКоличество итераций при итерировании: iter = {BP.iter}",
          f"\tМатрица = {('fill', 'empty')[BP.matrix is None]}",
          f"\tСобственные значения h = {('fill', 'empty')[BP.h is None]}",
          f"\tСобственные вектора x = {('fill', 'empty')[BP.X is None]}",
          sep='\n')


def solve():
    """
    Функция, вызываемая в случае ввода команды solve.
    Выводит на экран найденное собственное значение и соответствующий ему собственный вектор.
    """
    if not (BP.matrix is None) and not (BP.X is None) and not (BP.h is None):
        h, x = exhaustion()
        print(f"h{BP.N-1} = {h}, x{BP.N-1} = {x}")


def read(cmd_list: List[str]) -> bool:
    """
    Функция, вызываемая в случае ввода команды read.
    Считывает с консоли объект, заданный дальнейшим флагом.

    Args:
        cmd_list: список введенных команд (для дальнейшего поиска флага подкоманды).

    Returns:
        флаг - была ли команда закончена.
    """
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


def mprint(cmd_list: List[str]) -> bool:
    """
    Функция, вызываемая в случае ввода команды mprint.
    Выводит в консоль объект, заданный дальнейшим флагом.

    Args:
        cmd_list: список введенных команд (для дальнейшего поиска флага подкоманды).

    Returns:
        флаг - была ли команда закончена.
    """
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


def gen():
    """
    Функция, вызываемая в случае ввода команды gen.
    Генерирует матрицу, список ее собственных значений и векторов.
    """
    BP.matrix = Matrix(BP.N)
    BP.h, BP.X = BP.matrix.generate(a=BP.a, b=BP.b)


def set_N(cmd_list: List[str]):
    """
    Функция, вызываемая в случае ввода флага -n <val>.
    Устанавливает переданное значение в системную настройку N - размерность матрицы.

    Args:
        cmd_list: список введенных команд (для дальнейшего поиска значения флага).
    """
    BP.N = int(cmd_list[cmd_list.index("-n") + 1])
    if BP.N <= 0:
        BP.N = 1


def set_iter(cmd_list: List[str]):
    """
    Функция, вызываемая в случае ввода флага -iter <val>.
    Устанавливает переданное значение в системную настройку iter - количество итераций при обязательном итерировании.

    Args:
        cmd_list: список введенных команд (для дальнейшего поиска значения флага).
    """
    BP.iter = int(cmd_list[cmd_list.index("-iter") + 1])
    if BP.iter <= 0:
        BP.iter = 1


def set_by_iter(cmd_list: List[str]):
    """
    Функция, вызываемая в случае ввода флага -by_iter <val>.
    Устанавливает переданное значение в системную настройку by_iter - флаг обязательного итерирования.

    Args:
        cmd_list: список введенных команд (для дальнейшего поиска значения флага).
    """
    ind = cmd_list.index("-by_iter") + 1
    BP.by_iter = (False, True)[cmd_list[ind] == "true"]


def set_cnt(cmd_list: List[str]):
    """
    Функция, вызываемая в случае ввода флага -cnt <val>.
    Устанавливает переданное значение в системную настройку cnt - количество автотестов.

    Args:
        cmd_list: список введенных команд (для дальнейшего поиска значения флага).
    """
    BP.cnt = int(cmd_list[cmd_list.index("-cnt") + 1])
    if BP.cnt <= 0:
        BP.cnt = 1


def set_ab(cmd_list: List[str]):
    """
    Функция, вызываемая в случае ввода флага -ab <val1> <val2>.
    Устанавливает переданные значения в системные настройки [a,b] - интервал генерации w для матрицы Хаусхолдера.

    Args:
        cmd_list: список введенных команд (для дальнейшего поиска значения флага).
    """
    BP.a, BP.b = int(cmd_list[cmd_list.index("-ab") + 1]), int(cmd_list[cmd_list.index("-ab") + 2])
