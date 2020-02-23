import matplotlib.pyplot as plt
import numpy as np


# 定义画散点图的函数
import pandas as pd


def draw_scatter(n, s,data):
    """
    :param n: 点的数量，整数
    :param s:点的大小，整数
    : praram data  二维数组数据
    :return: None
    """

    # 通过切片获取横坐标x1
    x1 = data[:, 2]
    print('x1')
    print(x1)
    # 通过切片获取纵坐标R
    y1 = data[:, 8]
    y11 = data[:,6]
    print('y1')
    print(y1)
    # 横坐标x2
    x2 = np.random.uniform(0, 5, n)
    # 纵坐标y2
    y2 = np.array([3] * n)
    # 创建画图窗口
    fig = plt.figure()
    # 将画图窗口分成1行1列，选择第一块区域作子图
    ax1 = fig.add_subplot(1, 1, 1)
    # 设置标题
    ax1.set_title('Result Analysis')
    # 设置横坐标名称
    ax1.set_xlabel('gamma-value')
    # 设置纵坐标名称
    ax1.set_ylabel('R-value')
    # 画散点图
    ax1.scatter(x1, y1, s=s, c='red', marker='.')
    # 画散点图
    ax1.scatter(x1, y11, s=s, c='k', marker='.')
    # 画直线图
    ax1.plot(x2, y2, c='b', ls='--')
    # 调整横坐标的上下界
    plt.xlim(xmax='2020/2/21', xmin='2016/1/12')
    # 显示
    plt.show()


# 主模块
if __name__ == "__main__":
    #加载数据
    original = pd.read_csv("D:\gp\priceWithInterest.csv").values
    print(original[2])
    # 运行
    draw_scatter(n=2000, s=2, data=original)
