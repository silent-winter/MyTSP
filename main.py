import numpy as np
from ga import Ga
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

print(city_dist_mat)

# 遗传算法运行
ga = Ga(city_dist_mat)
result_list, fitness_list = ga.train()
result = result_list[-1]
result_pos_list = city_pos_list[result, :]

# 绘图
# 解决中文显示问题
plt.rcParams['font.sans-serif'] = ['KaiTi']  # 指定默认字体
plt.rcParams['axes.unicode_minus'] = False  # 解决保存图像是负号'-'显示为方块的问题

fig = plt.figure()
plt.plot(result_pos_list[:, 0], result_pos_list[:, 1], 'o-r')
plt.title(u"路线")
plt.legend()
fig.show()

fig = plt.figure()
plt.plot(fitness_list)
plt.title(u"适应度曲线")
plt.legend()
fig.show()
