import random as rnd
from math import sin


def my_function(x):
    return 2 ** x * sin(10 * x)


class Individ:
    """ Класс одного индивида в популяции"""

    def __init__(self, start, end, mutationSteps, function):
        self.start = start
        self.end = end
        self.x = rnd.triangular(self.start, self.end)
        self.score = 0
        self.function = function
        self.mutationSteps = mutationSteps
        self.calculateFunction()

    def calculateFunction(self):
        self.score = self.function(self.x)

    def mutate(self):
        # задаем отклонение по Х
        delta = 0
        for i in range(1, self.mutationSteps + 1):
            if rnd.random() < 1 / self.mutationSteps:
                delta += 1 / (2 ** i)
        if rnd.randint(0, 1):
            delta = self.end * delta
        else:
            delta = self.start * delta
        self.x += delta
        # ограничим наших индивидом по Х
        if self.x < 0:
            self.x = max(self.x, self.start)
        else:
            self.x = min(self.x, self.end)


class Genetic:
    """ Класс, отвечающий за реализацию генетического алгоритма"""

    def __init__(self, numberOfIndividums, crossoverRate, mutationSteps, mutationChance,
                 generations, function, start, end, extremum):
        # размер популяции
        self.numberOfIndividums = numberOfIndividums
        # шанс рекомбинации
        self.crossoverRate = crossoverRate
        # количество шагов мутации
        self.mutationSteps = mutationSteps
        # поколения
        self.generations = generations
        # целевая функция
        self.function = function
        # шанс мутации
        self.mutatiinChance = mutationChance

        # самое минимальное или максимальное значение
        self.bestScore = 0
        # точка Х
        self.x = [0]
        # область поиска
        self.start = start
        self.end = end
        self.extremum = extremum

    def crossover(self, parent1: Individ, parent2: Individ):

        # создаем 2х новых детей
        child1 = Individ(self.start, self.end, self.mutationSteps, self.function)
        child2 = Individ(self.start, self.end, self.mutationSteps, self.function)
        # создаем новые координаты для детей
        alpha = rnd.uniform(0.01, 1)
        child1.x = parent1.x + alpha * (parent2.x - parent1.x)

        alpha = rnd.uniform(0.01, 1)
        child2.x = parent1.x + alpha * (parent1.x - parent2.x)

        return child1, child2

    def calculateMinScore(self, population, _):
        if population[0].score < self.bestScore:
            self.bestScore = population[0].score
            self.x = [population[0].x]
            print("Поколение:", _)
            print("Изменился min:", self.x, self.bestScore)

    def calculateMaxScore(self, population, _):
        if population[0].score > self.bestScore:
            self.bestScore = population[0].score
            self.x = [population[0].x]
            print("Поколение:", _)
            print("Изменился max:", self.x, self.bestScore)

    def startGenetic(self):

        # создаем стартовую популяцию
        pack = [self.start, self.end, self.mutationSteps, self.function]
        population = [Individ(*pack) for _ in range(self.numberOfIndividums)]

        # запускаем алгоритм
        for _ in range(self.generations):
            if self.extremum == "min":
                population = sorted(population, key=lambda item: item.score)
            else:
                population = sorted(population, key=lambda item: item.score, reverse=True)
            bestPopulation = population[:int(self.numberOfIndividums * self.crossoverRate)]

            childs = []
            for individ1 in bestPopulation:
                # находим случайную пару для каждого индивида и скрещиваем
                individ2 = rnd.choice(bestPopulation)
                while individ1 == individ2:
                    individ2 = rnd.choice(bestPopulation)
                child1, child2 = self.crossover(individ1, individ2)
                childs.append(child1)
                childs.append(child2)
            population.extend(childs)

            for individ in population:
                if rnd.random() < self.mutatiinChance:
                    individ.mutate()
                    individ.calculateFunction()

            # отбираем лучших индивидов
            if self.extremum == "min":
                population = sorted(population, key=lambda item: item.score)
                population = population[:self.numberOfIndividums]
                self.calculateMinScore(population, _)
            else:
                population = sorted(population, key=lambda item: item.score, reverse=True)
                population = population[:self.numberOfIndividums]
                self.calculateMaxScore(population, _)


a = Genetic(numberOfIndividums=100, crossoverRate=0.6, mutationSteps=10, mutationChance=0.4,
            generations=30, function=my_function, start=-3, end=3, extremum="max")
a.startGenetic()

print("Лучшее значение:", a.x, a.bestScore)
