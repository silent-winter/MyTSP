import random
from individual import Individual
import numpy as np


# 城市数量(基因序列长度)
city_num = 20
# 个体数量
individual_num = 60
# 迭代轮数
gen_num = 400
# 变异概率
mutate_prob = 0.25
# 城市维度
pos_dimension = 2


def build_dist_mat(input_list):
    # 城市数量20
    global city_num
    dist_mat = np.zeros([city_num, city_num])
    for i in range(city_num):
        for j in range(i + 1, city_num):
            d = input_list[i, :] - input_list[j, :]
            # 计算点积
            dist_mat[i, j] = np.dot(d, d)
            dist_mat[j, i] = dist_mat[i, j]
    return dist_mat


# 城市坐标矩阵
city_pos_list = np.random.rand(city_num, pos_dimension)
# 城市距离矩阵
city_dist_mat = build_dist_mat(city_pos_list)


def copy_list(old_arr: [int]):
    new_arr = []
    for element in old_arr:
        new_arr.append(element)
    return new_arr


def rank(group):
    for i in range(1, len(group)):
        for j in range(0, len(group) - i):
            if group[j].fitness > group[j + 1].fitness:
                group[j], group[j + 1] = group[j + 1], group[j]
    return group


class Solution:
    def __init__(self, input_):
        global city_dist_mat
        city_dist_mat = input_
        self.best = None  # 每一代的最佳个体
        self.individual_list = []  # 每一代的个体列表
        self.result_list = []  # 每一代对应的解
        self.fitness_list = []  # 每一代对应的适应度

    def cross(self):
        new_gen = []
        random.shuffle(self.individual_list)
        for i in range(0, individual_num - 1, 2):
            # 父代基因
            genes1 = copy_list(self.individual_list[i].genes)
            genes2 = copy_list(self.individual_list[i + 1].genes)
            # 随机交换指定两个位置之间的基因序列
            index1 = random.randint(0, city_num - 2)
            index2 = random.randint(index1, city_num - 1)
            pos1_recorder = {value: idx for idx, value in enumerate(genes1)}
            pos2_recorder = {value: idx for idx, value in enumerate(genes2)}
            # 交叉
            for j in range(index1, index2):
                # 拿到对应位置的index和value
                value1, value2 = genes1[j], genes2[j]
                pos1, pos2 = pos1_recorder[value2], pos2_recorder[value1]
                genes1[j], genes1[pos1] = genes1[pos1], genes1[j]
                genes2[j], genes2[pos2] = genes2[pos2], genes2[j]
                pos1_recorder[value1], pos1_recorder[value2] = pos1, j
                pos2_recorder[value1], pos2_recorder[value2] = j, pos2
            new_gen.append(Individual(genes=genes1, city_num=city_num, city_dist_mat=city_dist_mat))
            new_gen.append(Individual(genes=genes2, city_num=city_num, city_dist_mat=city_dist_mat))
        return new_gen

    # 变异策略：
    def mutate(self, new_gen):
        for individual in new_gen:
            if random.random() < mutate_prob:
                # 翻转切片
                old_genes = copy_list(individual.genes)
                index1 = random.randint(0, city_num - 2)
                index2 = random.randint(index1, city_num - 1)
                genes_mutate = old_genes[index1:index2]
                genes_mutate.reverse()
                individual.genes = old_genes[:index1] + genes_mutate + old_genes[index2:]
        # 两代合并
        self.individual_list += new_gen

    def select(self):
        # 锦标赛
        group_num = 10  # 小组数
        group_size = 10  # 每小组人数
        group_winner = individual_num // group_num  # 每小组获胜人数
        winners = []  # 锦标赛结果
        for i in range(group_num):
            group = []
            for j in range(group_size):
                # 随机组成小组
                player = random.choice(self.individual_list)
                player = Individual(genes=player.genes, city_num=city_num, city_dist_mat=city_dist_mat)
                group.append(player)
            group = rank(group)
            # 取出获胜者
            winners += group[:group_winner]
        self.individual_list = winners

    def next_gen(self):
        # 交叉
        new_gen = self.cross()
        # 变异
        self.mutate(new_gen)
        # 选择
        self.select()
        # 获得这一代的结果
        for individual in self.individual_list:
            if individual.fitness < self.best.fitness:
                self.best = individual

    def train(self):
        # 初代种群
        self.individual_list = [Individual(city_num=city_num, city_dist_mat=city_dist_mat) for _ in range(individual_num)]
        self.best = self.individual_list[0]
        # 迭代
        for i in range(gen_num):
            self.next_gen()
            # 连接首尾
            result = copy_list(self.best.genes)
            result.append(result[0])
            self.result_list.append(result)
            self.fitness_list.append(self.best.fitness)
        return self.result_list, self.fitness_list
