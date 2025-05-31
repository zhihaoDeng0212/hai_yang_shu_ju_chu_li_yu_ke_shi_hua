import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


if __name__ == '__main__':

    # 读取数据
    data_path = r'.\海洋数据处理与可视化\output\年代与各种数据的关系图\合并后的预处理数据\{hole}.csv'

    # 合并后的点
    holes = {
        'ross': ['U1522A', 'U1523ABE', 'U1524A', 'U1524C', 'U1525A'],
        'amundsen': ['U1533A', 'U1533B', 'U1533C', 'U1533D']
    }

    # 保存路径
    save_path = r'.\海洋数据处理与可视化\output\年代与各种数据的关系图\关系图\{hole}.png'

    for sea, merged_holes_list in holes.items():

        for merged_holes in merged_holes_list:

            # 创建图表，一行三列，打开 share y 轴
            fig, ax = plt.subplots(1, 3, figsize=(12, 8), sharey=True)
            
            fig.suptitle("地层年龄与 TOC含量、TN含量、碳氮比关系图（{merged_holes}）".format(merged_holes=merged_holes), 
                            fontweight='bold',
                            fontsize= 'larger')

            # 调整子图之间的间距
            plt.subplots_adjust(wspace=0)

            # 使 matplotlib 支持中文
            plt.rcParams['font.sans-serif'] = ['SimHei']

            # 设置网格
            ax[0].grid(linestyle='--', alpha=0.7)
            ax[1].grid(linestyle='--', alpha=0.7)
            ax[2].grid(linestyle='--', alpha=0.7)

            # 读取数据
            data = pd.read_csv(data_path.format(hole=merged_holes))
            age = - data['Time (kyr from J2000)']
            toc = data['TOC (wt%)']
            tn = data['TN (wt%)']
            c_n_ratio = data['C/N']

            # 绘制折线图（带标记点）
            ax[0].plot(toc, age, marker='o', markersize=4, linewidth=1.6, color='blue')
            ax[0].set_xlabel("TOC 含量 (%)", labelpad=12, fontsize='larger')
            ax[1].plot(tn, age, marker='o', markersize=4, linewidth=1.6, color='#8B4513')
            ax[1].set_xlabel("TN 含量 (%)", labelpad=12, fontsize='larger')
            ax[2].plot(c_n_ratio, age, marker='o',markersize=4, linewidth=1.6, color='#006400')
            ax[2].set_xlabel("碳氮比", labelpad=12, fontsize='larger')

            # 设置 y 轴刻度
            ax[0].set_ylabel("地层年龄（kyr BP）", fontsize='larger')

            # 设置 x 轴刻度，从零开始
            ax[0].set_xlim(left=0, right=1.5)  # TOC
            ax[1].set_xlim(left=0, right=0.15)  # TN
            ax[2].set_xlim(left=0)  # 碳氮比

            # 反转Y轴（地层年龄向下增加）
            ax[1].invert_yaxis()

            # 将X轴刻度放到坐标轴上方
            ax[0].tick_params(top=True, labeltop=True, bottom=False, labelbottom=False)
            ax[1].tick_params(top=False, labeltop=False, bottom=True, labelbottom=True)
            ax[2].tick_params(top=True, labeltop=True, bottom=False, labelbottom=False)

            # 将X轴标签放到坐标轴上方
            ax[0].xaxis.set_label_position('top')
            ax[1].xaxis.set_label_position('bottom')
            ax[2].xaxis.set_label_position('top')

            # 保存图表
            plt.savefig(save_path.format(hole=merged_holes), dpi=720)
