from scipy.integrate import odeint
from numpy import array
from numpy import linspace
import math

k = 4
g = 0


def dxdt(t, x, y):
    return k * t + x - y + g


def dydt(x, y):
    return -x + k * y


def for_example(t, mas):
    return array([k * t + mas[0] - mas[1] + g, -mas[0] + k * mas[1]])


def euler_metod(a, b, h):
    x, y = 0.0, 0.0  # начальные условия
    res = []
    while a <= b:  # находим х и у по формулам
        x += h * dxdt(a, x, y)
        y += h * dydt(x, y)
        res.append((x, y))
        a += h
    return res


def runge_cutta_metod(a, b, h):
    x, y = 0.0, 0.0  # начальные условия
    res = []
    k1 = k2 = k3 = k4 = 0  # X
    q1 = q2 = q3 = q4 = 0  # Y
    while a <= b:
        k1 = h * dxdt(a, x, y)  # находим все эты и подставляем в формулу
        q1 = h * dydt(x, y)

        k2 = h * dxdt(a + h / 2, x + k1 / 2, y + q1 / 2)
        q2 = h * dydt(x + k1 / 2, y + q1 / 2)

        k3 = h * dxdt(a, x + h / 2, y + k2 / 2)
        q3 = h * dydt(x + h / 2, y + q2 / 2)

        k4 = h * dxdt(a, x + h, y + k3)
        q4 = h * dydt(x + h, y + q3)

        x += 1 / 6 * (k1 + 2 * k2 + 2 * k3 + k4)
        y += 1 / 6 * (q1 + 2 * q2 + 2 * q3 + q4)
        res.append((x, y))
        a += h
    return res


def accuracy(mas1, mas2):
    result = []
    for i in range(len(mas1)):
        result.append(math.pow(mas1[i][0] - mas2[i * 2][0], 2))  # X
        result.append(math.pow(mas1[i][1] - mas2[i * 2][1], 2))  # Y
    return math.sqrt(1 / (len(mas1) - 1)) * (sum(result))


def calculation(metod, a, b, h):
    e = 0.1
    older = metod(a, b, h * 2)
    newer = metod(a, b, h)
    while accuracy(older, newer) > e:
        h /= 2
        older = newer
        newer = metod(a, b, h)
    return h, newer

def calculation(metod, a, b, h):
    return metod(a, b, h)


if __name__ == "__main__":
    print("Точное значение:")
    print(odeint(for_example, array([0, 0]), linspace(0, 1, 10), tfirst=True))

    h_euler = 0.25
    result = calculation(euler_metod, 0, 1, h_euler)
    print("\nМетод Эйлера: h = ", h_euler)
    print("\t t0 \t \t dx \t \t dy \t")
    for i in range(len(result)):
        print("{:^10.5} │ {:^10.5} │ {:^10.5}".format(h_euler * i, result[i][0], result[i][1]))

    h_runge_cutta = 0.001
    result = calculation(runge_cutta_metod, 0, 1, h_runge_cutta)
    print("\nМетод Рунге-Кутта: h = ", h_runge_cutta)
    print("\t t0 \t \t dx \t \t dy \t")
    for i in range(len(result)):
        print("{:^10.5} │ {:^10.5} │ {:^10.5}".format(h_runge_cutta * i, result[i][0], result[i][1]))
