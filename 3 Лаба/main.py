from MenuOptions import *
from BaseFunctions import time_in_min_sec


# Функция с интерфейсом для проведения тестов
# Выполняет соответсвующие действия из MenuOptions
def test():
    command = str()         # текущая строка с командами пользователя
    while command != "stop":
        command = input().lower().strip(" \n\t\r")
        cmd_list = command.split()      # получаем список флагов
        if command == "help":
            help()
        elif command == "stop":
            return
        elif command == "status":
            status()
        else:
            found_cmd = False
            if "-n" in cmd_list:
                set_N(cmd_list)
                found_cmd = True

            if "-l" in cmd_list:
                set_L(cmd_list)
                found_cmd = True

            if "-k" in cmd_list:
                set_k(cmd_list)
                found_cmd = True

            if "-cnt" in cmd_list:
                set_cnt(cmd_list)
                found_cmd = True

            if "-ab" in cmd_list:
                set_ab(cmd_list)
                found_cmd = True

            if "-good" in cmd_list:
                set_good(cmd_list)
                found_cmd = True

            if "-by_float" in cmd_list:
                set_by_float(cmd_list)
                found_cmd = True

            if "-type" in cmd_list:
                set_type(cmd_list)
                found_cmd = True

            if "-gauss_tape" in cmd_list:
                set_gauss_tape(cmd_list)
                found_cmd = True

            if "-debug" in cmd_list:
                set_debug(cmd_list)
                found_cmd = True

            if "auto_test" in cmd_list:
                auto_test(cmd_list)
                found_cmd = True

            if "read" in cmd_list:
                found_cmd = read(cmd_list)

            if "print" in cmd_list:
                found_cmd = mprint(cmd_list)

            if "gen" in cmd_list:
                found_cmd = gen(cmd_list)

            if "solve" in cmd_list:
                solve()
                found_cmd = True

            if "analyze" in cmd_list:
                analyze(cmd_list)
                found_cmd = True

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
