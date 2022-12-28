"""Набор вспомогательных функций, используемых в решении"""


# отображение (время в секундах) -> (строка для бользователького представления)
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


# функция подсчета накопленной вычислительной погрешности
def rate(x, xt):
    size = len(x)
    d = []
    for i in range(size):
        d.append(abs(x[i] - xt[i]))
        # if x[i] > q:
        #     d.append(abs((x[i] - xt[i]) / abs(xt[i])))
        # else:
        #     d.append(abs(x[i] - xt[i]))
    return max(map(lambda x: abs(x), d))
