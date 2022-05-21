import random

class Individual:
    def __init__(self, genes=None, city_num=20, city_dist_mat=None):
        # 随机生成序列
        if genes is None:
            genes = [i for i in range(city_num)]
            random.shuffle(genes)
        self.genes = genes
        self.city_num = city_num
        self.city_dist_mat = city_dist_mat
        self.fitness = self.evaluate_fitness()

    # 适应度函数：走完所有城市的开销求和
    def evaluate_fitness(self):
        # 计算个体适应度
        fitness = 0.0
        for i in range(self.city_num - 1):
            # 起始城市和目标城市
            from_idx = self.genes[i]
            to_idx = self.genes[i + 1]
            fitness += self.city_dist_mat[from_idx, to_idx]
        # 连接首尾
        fitness += self.city_dist_mat[self.genes[-1], self.genes[0]]
        return fitness
