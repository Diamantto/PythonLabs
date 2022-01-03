import random
from scipy.optimize import fminbound

k = 5
g = 3
a = (- k * g) - 2
b = k * g + 1

N = 100
E = 0.01


def task_f(x):
    return x ** 2 + 2 * k * g * x + k


def dividing_m(a, b, E):
    L = E * 10
    while L > E:
        Xmin = (a + b) / 2
        L = b - a
        W_xmin = task_f(Xmin)

        x1 = a + L / 4
        x2 = b - L / 4
        W_x1 = task_f(x1)
        W_x2 = task_f(x2)

        if W_x1 < W_xmin:
            b = Xmin
        elif W_x2 < W_xmin:
            a = Xmin
        else:
            a = x1
            b = x2
    return Xmin, task_f(Xmin)


def random_search(a, b):
    x = [random.uniform(a, b) for i in range(101)]
    y_min = task_f(x[0])
    x_min = 0
    for i in x:
        if task_f(i) < y_min:
            x_min = i
            y_min = task_f(i)

    return x_min, y_min


if __name__ == "__main__":
    print("Точний розв'язок: x_min = {}, f_min = {}".format(fminbound(task_f, a, b),
                                                            task_f(fminbound(task_f, a, b))))
    print("Метод зменшення інтервалу: xmin = {}, fmin = {}".format(*dividing_m(a, b, E)))
    print("Метод випадкового пошуку: xmin = {}, fmin = {}".format(*random_search(a, b)))
