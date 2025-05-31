import pandas as pd
import numpy as np
import matplotlib.pyplot as plt 
from scipy.stats import pearsonr


if __name__ == '__main__':

    # 准备数据路径
    data_path = r'.\海洋数据处理与可视化\output\年代与各种数据的关系图\合并后的预处理数据\{hole}.csv'
    save_path = r'.\海洋数据处理与可视化\output\总碳总氮相关性分析图\{sea}碳氮比散点图（{hole}）.png'

    # 将要绘制的海域及站点
    target_merged_holes = {
        '罗斯海': 'U1523ABE',
        '阿蒙森海': 'U1533B'
    }

    # 让 Matplotlib 支持中文和负号
    plt.rcParams['font.sans-serif'] = ['Microsoft YaHei']
    plt.rcParams['axes.unicode_minus'] = False

    for sea, hole in target_merged_holes.items():

        # 读取数据
        data = pd.read_csv(data_path.format(hole=hole))
        tn = data['TN (wt%)']
        toc = data['TOC (wt%)']

        # 创建图像
        plt.plot(figsize=(8, 8))

        # 确定标题
        plt.title(f'{sea}碳氮比散点图（{hole}）')

        # 绘制网格
        plt.grid(linestyle='--', alpha=0.7)

        plt.scatter(tn, toc, marker='x', color='blue')

        # 设置 x 轴
        plt.xlabel("TN 含量（%）", size=12)
        plt.xlim(left=0.01, right=0.08)
        plt.xticks(np.arange(0.01, 0.09, 0.01))  # TN 含量一般在 0 - 0.15%

        # 设置 y 轴
        plt.ylabel("TOC 含量（%）", size=12)
        plt.ylim(bottom=0, top=0.09)
        plt.yticks(np.arange(0, 1.2, 0.3))  # TOC 含量一般是 0 - 1.5%

        """
        计算 pearson 相关系数
        
        范围：-1 到 +1

        意义：
        -1 是完全负相关
        +1 是完全正相关
        0  是无线性关系

        绝对值大小的意义：
        0.8 <= |r| <= 1.0   ：强相关
        0.5 <= |r| <= 0.8   ：中等相关
        0.3 <= |r| <= 0.5   ：弱相关
        |r| <= 0.3          : 极弱或无明显线性相关
        """
        corr, p_value = pearsonr(tn, toc)

        # 拟合线性回归模型
        coefficients = np.polyfit(tn, toc, 1)
        slope = coefficients[0]
        intercept = coefficients[1]
        r_squared = corr ** 2

        toc_pred = np.polyval(coefficients, tn)  # 直接使用多项式求值

        # 绘制直线
        plt.plot(tn, toc_pred, 'r--')

        # 准备文本，在下面绘制
        equation = f'y = {slope:.4f}x + {intercept:.4f}\nR^2 = {r_squared:.4f}'

        # 根据海域的不同，添加个性化配置
        if sea == '阿蒙森海':

            # 添加文献中的直线
            slope = 6.96
            intercept = 0.11
            toc_pred = slope * tn + intercept
            plt.plot(tn, toc_pred, '--', color='#006400')
            text = '陈东 2023'
            plt.text(0.7, 0.7, text, transform=plt.gca().transAxes, fontsize=12, color='#006400')

            # 添加本程序拟合的公式
            plt.text(0.05, 0.1, equation, transform=plt.gca().transAxes, fontsize=12, color='red')

        elif sea == '罗斯海':

            # 添加本程序拟合的公式
            plt.text(0.45, 0.1, equation, transform=plt.gca().transAxes, fontsize=12, color='red')

        # 保存
        plt.savefig(save_path.format(sea=sea, hole=hole))

        # 重置
        plt.close()
