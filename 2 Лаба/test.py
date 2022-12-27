import matplotlib.pyplot as plt

fig = plt.figure("Анализ роста ошибки при увеличении N")
xx = fig.add_subplot(3, 1, 1)
fx = fig.add_subplot(3, 1, 3)
xx.set_xlabel("размерность системы N")
xx.set_ylabel("ошибка")
xx.set_title(label="График роста ошибки вектора X")
fx.set_xlabel("размерность системы N")
fx.set_ylabel("ошибка")
fx.set_title(label="График роста ошибки вектора F")
plt.show()