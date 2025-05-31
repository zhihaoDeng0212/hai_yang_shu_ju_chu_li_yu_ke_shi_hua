import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from eofs.standard import Eof


# 所有数据的文件路径
PATHS = {
    '预处理后的数据（阿蒙森海）': r'.\海洋数据处理与可视化\output\经验正交函数分解\预处理后的数据\第2次\阿蒙森海.csv',
    '预处理后的数据（罗斯海）': r'.\海洋数据处理与可视化\output\经验正交函数分解\预处理后的数据\第2次\罗斯海.csv',

    '保存文件夹（阿蒙森海）': r'.\海洋数据处理与可视化\output\经验正交函数分解\图片\阿蒙森海',
    '保存文件夹（罗斯海）': r'.\海洋数据处理与可视化\output\经验正交函数分解\图片\罗斯海'
}

def draw(data_path, holes, colors, save_path):
    # 1. 读取CSV数据（假设文件名为data.csv）
    df = pd.read_csv(data_path)  # 列名应为 depth, A mag sus, B mag sus, C mag sus

    # 2. 提取磁化率数据并转为二维数组（维度：深度 × 钻孔）
    tmp = []
    for hole in holes:
        tmp.append(hole + ' mag sus (SI x 10^-5)')
    data = df[tmp].values  # shape = (n_depth, 3)

    # 3. 数据预处理（去均值）
    data_mean = data.mean(axis=0)
    data_centered = data - data_mean

    # 4. 创建EOF求解器（空间维度为3个钻孔）
    n = len(holes)
    solver = Eof(data_centered)
    eofs = solver.eofs(neofs=n)   # 空间模态（3个钻孔的分布）
    pcs = solver.pcs(npcs=n)      # 时间系数（沿深度的变化）
    variance = solver.varianceFraction()  # 各模态解释方差

    # 5. 可视化
    # 5.1 空间模态图（显示每个钻孔的EOF权重）
    fig, axs = plt.subplots(1, n, figsize=(12, 4), sharey=True)
    sites = holes
    colors = colors
    for i in range(len(holes)):
        axs[i].bar(sites, eofs[i], color=colors)
        axs[i].set_title(f"EOF{i+1} ({variance[i]*100:.1f}%)")
        axs[i].set_xlabel("钻孔")
        if i == 0:
            axs[i].set_ylabel("EOF权重")
    plt.suptitle("磁化率 空间模态（钻孔间差异）")
    plt.tight_layout()
    plt.savefig(save_path + ' 磁化率 空间模态图.png')

    # 5.2 时间系数图（沿深度的变化）
    plt.figure(figsize=(8, 4))
    depth = df["Depth (m)"].values
    for i in range(n):
        plt.plot(depth, pcs[:, i], label=f"PC{i+1} ({variance[i]*100:.1f}%)")
    plt.xlabel("深度（米）")
    plt.ylabel("主成分系数")
    plt.legend()
    plt.title("磁化率 沿深度的 PC 变化")
    plt.grid(alpha=0.3)
    plt.savefig(save_path + ' 磁化率 时间系数图.png')


if __name__ == '__main__':
    
    # 使 matplotlib 支持中文和显示负号
    plt.rcParams['font.sans-serif'] = ['Microsoft YaHei']  # 支持中文，不要用 SimHei，因为它不支持负号
    plt.rcParams['axes.unicode_minus'] = False  # 强制显示负号

    draw(
        data_path=PATHS['预处理后的数据（阿蒙森海）'], 
        holes=['U1533A', 'U1533C', 'U1533D'], 
        colors=["#1f77b4", "#ff7f0e", "#2ca02c"],
        save_path=PATHS['保存文件夹（阿蒙森海）']
        )