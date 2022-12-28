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

            if "-cnt" in cmd_list:
                set_cnt(cmd_list)
                found_cmd = True

            if "-ab" in cmd_list:
                set_ab(cmd_list)
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
