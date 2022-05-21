import numpy as np
from core_algorithm import Solution
import matplotlib.pyplot as plt

# 城市数量
city_num = 20
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


# 城市坐标
city_pos_list = np.random.rand(city_num, pos_dimension)
# 城市距离矩阵
city_dist_mat = build_dist_mat(city_pos_list)
print("city locations: \n", city_pos_list)


def drawPicture(result_pos_list, fitness_list):
    # 绘制结果图
    fig = plt.figure()
    plt.plot(result_pos_list[:, 0], result_pos_list[:, 1], 'o-r')
    plt.title("solution")
    fig.show()
    # 绘制适应性曲线
    fig = plt.figure()
    plt.plot(fitness_list)
    plt.title("fitness")
    fig.show()


def main():
    # 遗传算法运行
    solution = Solution(city_dist_mat)
    result_list, fitness_list = solution.train()
    result = result_list[-1]
    result_pos_list = city_pos_list[result, :]
    drawPicture(result_pos_list, fitness_list)


if __name__ == '__main__':
    main()
