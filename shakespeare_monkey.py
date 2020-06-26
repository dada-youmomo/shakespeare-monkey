import random
import time


# 创造新字母，也即新基因
def rand_char():
    c = random.choice([i for i in range(64, 90)])
    if c == 64:
        return chr(32)  # chr() 用一个范围在range（256）内的（就是0-255）整数作参数，返回一个对应的字符。
    if random.random() > 0.5:
        return chr(c + 32)  # 小写
    return chr(c)


# DNA类
class DNA:
    def __init__(self, length):
        self.genes = []
        self.fitness = 0
        for i in range(length):
            self.genes.append(rand_char())  # 将空列表通过.append()函数拼接了字母（基因），构成了DNA

    # 适应度函数，返回正确字母的百分比
    def fitness_points(self, target):
        score = 0
        for i in range(len(self.genes)):
            if self.genes[i] == target[i]:
                score += 1
        self.fitness = score / len(target)  # 这里得到个体的适应度范围：[0, 1]
        self.fitness = pow(self.fitness, 4)   # 利用抛物线函数替代线性函数，提高算法性能

    # 遗传交叉
    def crossover(self, partner):
        midpointA = len(self.genes) // 2  # “//”是整除的意思
        child = DNA(len(self.genes))  # 创建了一个DNA类的对象
        child.genes.clear()  # 清空child对象的self.genes变量
        # 新DNA的前半部分
        for i in range(int(midpointA)):
            child.genes.append(self.genes[i])
        # 新DNA的后半部分
        for i in range(int(midpointA), len(self.genes)):
            child.genes.append(partner.genes[i])
        return child

    # 基因突变
    def mutate(self, rate):
        for i in range(len(self.genes)):
            if random.random() < rate:
                self.genes[i] = rand_char()


# Population类
class Population:
    def __init__(self, target, mutation_rate, population_size):
        self.population = []  # 种群
        self.mating_pool = []  # 交配池
        self.mutation_rate = mutation_rate  # 突变率
        self.target = target  # 目标句子
        self.average_fitness = 0  # 平均适应度
        self.max_fitness = 0  # 最大适应度

        # 通过调用DNA类，生成大小为max的种群
        for i in range(population_size):
            self.population.append(DNA(len(target)))  # 种群中的每一个体都是DNA类的对象

    # 计算种群中个体的适应度
    def calculate_fitness(self):
        length = len(self.population)
        fit = 0

        for i in range(length):
            self.population[i].fitness_points(self.target)  # 调用.fitness_points方法（函数）
            fit += self.population[i].fitness  # 累加得到总的适应度值

        # 计算平均适应度
        fit /= len(self.population)
        self.average_fitness = fit

    # 算法模拟自然选择
    def natural_selection(self):
        self.mating_pool.clear()  # 清空变量
        self.max_fitness = 0
        index = 0  # 索引

        # 找到种群中适应度最大的个体
        for i in range(len(self.population)):
            if self.population[i].fitness > self.max_fitness:
                self.max_fitness = self.population[i].fitness
                index = i

        print(self.population[index].genes)  # 打印输出，该代种群中适应度最大的个体

        # # 生成交配池，将比率转换成对应的个数，没有排序
        # for i in range(len(self.population)):
        #     probability = (self.population[i].fitness / self.max_fitness) * len(self.target)
        #     for j in range(int(probability)):
        #         self.mating_pool.append(self.population[i])

    # accept/reject strategy（接受/拒绝策略）
    def accept_reject(self):
        be_safe = 0
        while True:
            # print(self.population)
            index = random.randint(0, len(self.population) - 1)  # [a, b]中的任意整数，可以取到边界
            partner = self.population[index]
            r = random.uniform(0, self.max_fitness)
            if r < partner.fitness:
                return partner
            be_safe += 1
            if be_safe > 10000:
                return None

    # 父母交配得到孩子
    def generate(self):
        length = len(self.population)

        new_population = []
        # self.population.clear()  # 清空种群

        for i in range(length):
            # partnerA = random.choice(self.mating_pool)
            # partnerB = random.choice(self.mating_pool)
            partnerA = self.accept_reject()
            partnerB = self.accept_reject()
            child = partnerA.crossover(partnerB)  # 交叉
            child.mutate(self.mutation_rate)  # 突变
            new_population.append(child)  # 得到子代
        self.population = new_population

    # 判断种群中是否有适应度为1的个体
    def evaluate(self):
        for i in range(len(self.population)):
            # print("Fitness : " + str(self.population[i].fitness))
            if self.population[i].fitness == 1:
                return 1
            else:
                continue
        return 0

    # 打印输出
    def display(self):
        for i in range(len(self.population)):
            print(self.population[i].genes)


def procedure():
    check = 0  # 检查，完成与否
    generation = 0  # 代数
    target = "To be or not to be"  # 目标句子
    # target = "Kobe"
    population = Population(target, 0.01, 1000)
    seconds = float(time.time())

    while not check == 1:
        generation += 1
        population.calculate_fitness()
        population.natural_selection()
        check = population.evaluate()
        population.generate()
        # print("Average Fitness : " + str(population.average_fitness))
        # print("Generations : " + str(generation))

        if check:
            print("Matched ! ")
            print("Evolved : " + str(target))
            print("Total Generations : " + str(generation))

    print("Total time : " + str(float(time.time()) - seconds) + "s")


if __name__ == "__main__":
    procedure()
