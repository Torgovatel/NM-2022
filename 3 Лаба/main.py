from MenuOptions import *
from BaseFunctions import time_in_min_sec


def test():
    """
    Функция тестирующего интерфейса.
    Реализует функциональность консольного взаимодействия с пользователем через зарезервированные командные слова.
    При вводе команды, ищет соответствие и вызывает соответсвующую функцию-обработчик из модуля MenuOptions.
    """
    command = str()
    while command != "stop":
        command = input().lower().strip(" \n\t\r")
        cmd_list = command.split()
        if command == "help":
            help()
        elif command == "stop":
            return
        elif command == "status":
            status()
        elif command == "solve":
            solve()
        else:
            found_cmd = False
            if "-n" in cmd_list:
                set_N(cmd_list)
                found_cmd = True

            if "-cnt" in cmd_list:
                set_cnt(cmd_list)
                found_cmd = True

            if "-ab" in cmd_list:
                set_ab(cmd_list)
                found_cmd = True

            if "-iter" in cmd_list:
                set_iter(cmd_list)
                found_cmd = True

            if "-by_iter" in cmd_list:
                set_by_iter(cmd_list)
                found_cmd = True

            if "read" in cmd_list:
                found_cmd = read(cmd_list)

            if "print" in cmd_list:
                found_cmd = mprint(cmd_list)

            if "gen" in cmd_list:
                found_cmd = True
                gen(cmd_list)

            if not found_cmd:
                print("Undefined command")


def main():
    """
    Основное тело программы.
    """
    print("Программа запущена")
    start_work_time = time.time()
    test()
    work_time = time.time() - start_work_time
    print("Программа завершила работу",
          f"Время работы программы: {time_in_min_sec(work_time)}",
          sep='\n')


# Точка входа в программу
if __name__ == "__main__":
    main()
