import pandas as pd
import matplotlib.pyplot as plt
from eofs.standard import Eof
import sys


PATHS = {
    '预处理后的数据': r'.\海洋数据处理与可视化\output\经验正交函数分解\预处理后的数据\第2次\result.csv',
    '保存文件夹': r'.\海洋数据处理与可视化\output\经验正交函数分解\图片',
}

if __name__ == '__main__':
    # 使 matplotlib 支持中文和显示负号
    plt.rcParams['font.sans-serif'] = ['Microsoft YaHei']  # 支持中文，不要用 SimHei，因为它不支持负号
    plt.rcParams['axes.unicode_minus'] = False  # 强制显示负号

    # 读取预处理后的数据
    data = pd.read_csv(PATHS['预处理后的数据'])

    # EOF 分解
    # 提取磁化率数据并转为二维数组（维度：深度 × 钻孔）

    # 拼接列名
    tmp = []
    holes=['U1533A', 'U1522A', 'U1523E', 'U1524A', 'U1525A']
    for hole in holes:
        tmp.append(hole + ' mag sus (SI x 10^-5)')

    # 提取数据
    raw_data = pd.read_csv(PATHS['预处理后的数据'])  # 列名应为 depth, U1533A mag sus, U1522A mag sus, U1523E mag sus, U1524A mag sus, U1525A mag sus
    data = raw_data[tmp].values  # shape = (n_depth, n)

    # 数据预处理（去均值）
    data_mean = data.mean(axis=0)
    data_centered = data - data_mean

    # 调试用，检查 data 数据
    # print(data)
    # sys.exit(0)

    # 创建EOF求解器（空间维度为n个钻孔）
    n = len(data_centered)
    solver = Eof(data_centered)
    eofs = solver.eofs(neofs=n)   # 空间模态（n 个钻孔的分布）
    pcs = solver.pcs(npcs=n)      # 时间系数（沿深度的变化）
    variance = solver.varianceFraction()  # 各模态解释方差

    # 调试用，检查 eofs 数据
    # print(eofs)
    # print(variance)
    # print(pcs)
    # print(pcs.shape)  # 应该是 (n_depth, n)
    # sys.exit(0)

    # 时间系数图（沿深度的变化）
    plt.figure(figsize=(8, 4))
    depth = raw_data["Depth (m)"].values
    for i in range(5):
        plt.plot(
            depth, pcs[:, i], 
            label=f"主成分 {i+1} ({variance[i]*100:.1f}%)", 
            marker='^',          # 正三角标记
            markersize=6,       # 标记大小
            markerfacecolor='none',  # 空心关键设置
            markeredgewidth=1.5,     # 边框粗细
        )
    plt.xlabel("深度（米）")
    plt.ylabel("主成分系数")

    # 调整图例
    plt.legend(
        handlelength=1.5,    # 缩短图例线长度
        handleheight=1.0,    # 调整图例线高度
        handletextpad=0.5,   # 减小文本与标记间距
        borderpad=0.3,       # 减小图例边框内边距
        labelspacing=0.15     # 减小图例项间垂直间距
    )

    # 设置网格
    plt.grid(alpha=0.3)

    title = "磁化率沿深度的主成分变化"
    plt.title(title)
    plt.savefig(PATHS['保存文件夹'] + f'\{title}.png', dpi=720, bbox_inches='tight')