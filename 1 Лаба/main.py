from MyPackage.Matrix import Matrix
from MyPackage.Vector import Vector
import time


# Метод подсчета ошибок по эксперименту
# n - размерность матрицы для генерации
# [a, b] - интервал для заполенения случайными значениями
# cnt - количество проводимых испытаний
# good - флаг обусловленности матрицы
# by_float - флаг заполенения целыми или же вещественными числами
def errors_by_test(n=1, a=10, b=50, cnt=10, good=True, by_float=True, debug=False):
    q = b + 1
    x_errors, f_errors = [], []
    p = 1
    for i in range(cnt):
        # Генерируем данные
        m = Matrix(n)
        m.fill_rand(a, b, good=good, by_float=by_float)
        xt = Vector(n)
        xt.fill_rand(a, a + (b - a) // 2, by_float=by_float)
        # Решаем систему и находим ошибки
        ft = m * xt
        try:
            x = m.solution(ft)
            f = m * x
            x_err = Matrix.error_rate(x, xt, q)
            f_err = Matrix.error_rate(f, ft, q)
            # Записываем их в список
            x_errors.append(x_err)
            f_errors.append(f_err)
        except ZeroDivisionError:
            pass
        if debug and i >= p * (cnt / 100):
            print("\r" * (p % 10 + 1), end='')
            print(f"{p}%", end='')
            p += 1
    if debug:
        print("100%", end='')
        print("\r\r\r\r", end='')
    return x_errors, f_errors


# Метод подсчета среднего по ошибкам для теста
# n - размерность матрицы для генерации
# [a, b] - интервал для заполенения случайными значениями
# cnt - количество проводимых испытаний
# good - флаг обусловленности матрицы
# by_float - флаг заполенения целыми или же вещественными числами
def average_errors_by_test(n=1, a=10, b=50, cnt=10, good=True, by_float=True, debug=False):
    x, f = errors_by_test(n, a, b, cnt, good=good, by_float=by_float, debug=debug)
    # Учитывая машинную точность, считаем среднее по минимуму из 2 возможных формул
    x_rate, f_rate = 0., 0.
    for i in range(len(x)):
        x_rate = (x_rate * i + x[i]) / (i + 1)
        f_rate = (f_rate * i + f[i]) / (i + 1)
    return min((x_rate, sum(x) / len(x))), min((f_rate, sum(f) / len(f)))


# Функция парсящая время в строку "x минут y секунд"
def time_in_min_sec(time):
    s_min = "минут"
    s_sec = "секунд"
    time_int = int(time)
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


# Функция с интерфейсом для проведения тестов
def test():
    n = 8
    a, b = -100, 100
    cnt = 100
    good = True
    debug = True
    by_float = True
    print_step = False
    command = str()
    m = None
    xt = None
    while command != "stop":
        command = input().lower().strip(" \n\t\r")
        cmd_list = command.split()
        if command == "help":
            print("Список команд:\n",
                  "stop - завершить работу",
                  "status - вывести статус системных переменных",
                  "auto_start [набор общих флагов] - начать работу с заданными флагами",
                  "read <флаг типа> <флаг импорта> - считываем локальный объект",
                  "write <флаг типа> <флаг экспорт> - записывает локальный объект",
                  "gen <флаг типа> - генерирует объект нужного типа по заданным общим флагам",
                  "solve - решить заданную локальную систему",
                  "\tобщие флаги:",
                  "\t\t-n val - устанавливает размерность матрицы = val (int)",
                  "\t\t-cnt val - устанавливает количество опытов = val (int)",
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
                  "\t\t-print_step val - устанавливает флаг вывода результатов val (bool)",
                  "\t\t\t* True - выводить пошаговые преобразования вектора правой части",
                  "\t\t\t* False - не выводить пошаговые преобразования вектора правой части",
                  "\tфлаги типа:",
                  "\t\t-matrix - считывание матрицы",
                  "\t\t-vector - считывание вектора",
                  "\tфлаги импорта/экспорта:",
                  "\t\t-console - консольное считывание/запись",
                  "\t\t-file name.txt - файловое считывание/запись для текстового файла name.txt",
                  sep='\n')
        elif command == "stop":
            return
        elif command == "status":
            print("Статус системных переменных:",
                  f"\tКоличество auto опытов: cnt = {cnt}",
                  f"\tРазмерность системы: n = {n}",
                  f"\tИнтервал генерации: ab = [{a}, {b}]",
                  f"\tОбусловленность: good = {good}",
                  f"\tВещественные числа: by_float = {by_float}",
                  f"\tИндикатор состояния выполнения: debug = {debug}",
                  f"\tИндикатор промежуточных состояний: print_step = {print_step}",
                  f"\tМатрица = {('fill', 'empty')[m is None]}",
                  f"\tВектор = {('fill', 'empty')[xt is None]}",
                  sep='\n')
        else:
            found_cmd = False
            if "-n" in cmd_list:
                n = int(cmd_list[cmd_list.index("-n") + 1])
                if n <= 0:
                    n = 1
                found_cmd = True
            if "-cnt" in cmd_list:
                cnt = int(cmd_list[cmd_list.index("-cnt") + 1])
                if cnt <= 0:
                    cnt = 1
                found_cmd = True
            if "-ab" in cmd_list:
                a, b = int(cmd_list[cmd_list.index("-ab") + 1]), int(cmd_list[cmd_list.index("-ab") + 2])
                found_cmd = True
            if "-good" in cmd_list:
                ind = cmd_list.index("-good") + 1
                good = (False, True)[cmd_list[ind] == "true"]
                found_cmd = True
            if "-by_float" in cmd_list:
                ind = cmd_list.index("-by_float") + 1
                by_float = (False, True)[cmd_list[ind] == "true"]
                found_cmd = True
            if "-debug" in cmd_list:
                ind = cmd_list.index("-debug") + 1
                debug = (False, True)[cmd_list[ind] == "true"]
                found_cmd = True
            if "-print_step" in cmd_list:
                ind = cmd_list.index("-print_step") + 1
                print_step = (False, True)[cmd_list[ind] == "true"]
                found_cmd = True
            if "auto_start" in cmd_list:
                start_processing = time.time()
                x_err_avr, f_err_avr = average_errors_by_test(n, a, b, cnt, good=good, by_float=by_float, debug=debug)
                processing_time = time.time() - start_processing
                print(f"Произведено {cnt} опытов со следующими параметрами:",
                      ("Необусловленная", "Обусловленная")[good] + f" матрица {n}x{n}",
                      f"Интервал генерации: [{a}, {b}]\n",
                      "Результаты обработки:",
                      f"Погрешность Х = {x_err_avr}",
                      f"Погрешность F = {f_err_avr}\n",
                      f"Время обработки: {time_in_min_sec(processing_time)}",
                      sep='\n')
                found_cmd = True
            if "read" in cmd_list:
                ind = cmd_list.index("read") + 1
                if cmd_list[ind + 1] == "-console":
                    if cmd_list[ind] == "-vector":
                        xt = Vector()
                        xt.read()
                        found_cmd = True
                    if cmd_list[ind] == "-matrix":
                        m = Matrix()
                        m.read()
                        found_cmd = True
                if cmd_list[ind + 1] == "-file":
                    with open(cmd_list[ind + 2], "r", encoding="utf-8") as inp:
                        if cmd_list[ind] == "-vector":
                            xt = Vector()
                            xt.file_read(inp)
                            found_cmd = True
                        if cmd_list[ind] == "-matrix":
                            m = Matrix()
                            m.file_read(inp)
                            found_cmd = True
            if "write" in cmd_list:
                ind = cmd_list.index("write") + 1
                if cmd_list[ind + 1] == "-console":
                    if cmd_list[ind] == "-vector":
                        if not (xt is None):
                            xt.print()
                            print()
                        found_cmd = True
                    if cmd_list[ind] == "-matrix":
                        if not (m is None):
                            m.print()
                            print()
                        found_cmd = True
                if cmd_list[ind + 1] == "-file":
                    with open(cmd_list[ind + 2], "w", encoding="utf-8") as out:
                        if cmd_list[ind] == "-vector":
                            if not (xt is None):
                                xt.write(out)
                            found_cmd = True
                        if cmd_list[ind] == "-matrix":
                            if not (m is None):
                                m.write(out)
                            found_cmd = True
            if "gen" in cmd_list:
                ind = cmd_list.index("gen") + 1
                if cmd_list[ind] == "-vector":
                    xt = Vector(n)
                    xt.fill_rand(a, a + (b - a) // 2, by_float=by_float)
                    found_cmd = True
                if cmd_list[ind] == "-matrix":
                    m = Matrix(n)
                    m.fill_rand(a, b, good=good, by_float=by_float)
                    found_cmd = True
            if "solve" in cmd_list:
                found_cmd = True
                if m is None or xt is None:
                    print("dont have input data...")
                else:
                    ft = m * xt
                    print("По заданной матрице и вектору X, точный вектор правой части F:",
                          ft,
                          sep='\n')
                    try:
                        x = m.solution(ft, x=xt, print_step=print_step)
                        x_err = m.error_rate(x, xt, b + 1)
                        f = m * x
                        f_err = m.error_rate(f, ft, b + 1)
                        print(f"Результаты обработки:",
                              f"Xt = {xt}",
                              f"X = {x}",
                              f"Ft = {ft}",
                              f"F = {f}",
                              f"Погрешность нахождения X = {x_err}",
                              f"Погрешность нахождения F = {f_err}",
                              sep='\n')
                    except ZeroDivisionError:
                        print("К данной матрице алгоритм не может быть применён")
            if not found_cmd:
                print("Undefined command")


# Основное тело программы
def main():
    print("Программа запущена")
    start_work_time = time.time()
    test()
    work_time = time.time() - start_work_time
    print("Программа завершила работу",
          f"Время работы программы: {time_in_min_sec(work_time)}",
          sep='\n')


if __name__ == "__main__":
    main()
