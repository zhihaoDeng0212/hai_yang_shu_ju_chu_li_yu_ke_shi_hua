import numpy as np
import pandas as pd
from PIL.JpegImagePlugin import samplings
from matplotlib import pyplot as plt
from scipy.signal import detrend, periodogram, butter, filtfilt


def draw(time, ecc, depth, ngr,rotation_thickness, significant_ecc, hole_name, result_folder):
    """
    rotation_thickness 旋回厚度
    </br>
    significant_ecc 显著短偏心率周期
    """
    # 使 matplotlib 支持中文和显示负号
    plt.rcParams['font.sans-serif'] = ['Microsoft YaHei']  # 支持中文，不要用 SimHei，因为它不支持负号
    plt.rcParams['axes.unicode_minus'] = False  # 强制显示负号

    # 数据预处理
    ngr_detrended = detrend(ngr)  # 去趋势化
    ngr_normalized = (ngr_detrended - np.mean(ngr_detrended)) / np.std(ngr_detrended)
    sampling_period = depth[1] - depth[0]

    # 为数据取整
    tmp = rotation_thickness.round(0)
    significant_ecc = significant_ecc.astype(str)

    # 设计 Butterworth 带通滤波器提取目标周期（例如，短偏心率94ka, 旋回厚度29.8m）
    lowcut = 1 / (tmp + 1)  # 下限频率（对应 ~ 31 米周期）
    highcut = 1 / (tmp - 1)  # 上限频率（对应 ~ 29 米周期）
    nyquist = 0.5 * sampling_period
    low = lowcut / nyquist
    high = highcut / nyquist

    # 设计Butterworth带通滤波器
    b, a = butter(N=4, Wn=[low, high], btype='band')

    # 应用滤波器
    filtered_gr = filtfilt(b, a, ngr_normalized)

    # 绘图
    fig, axes = plt.subplots(1, 2, figsize=(6, 12))
    fig.subplots_adjust(wspace=0.4)

    axes[0].plot(ecc, time, '-', 
                 label='偏心率 '+ significant_ecc + 'ka', 
                 color='blue')
    axes[1].plot(filtered_gr, depth, '-', 
                 label='旋回厚度 ' + rotation_thickness.astype(str) + 'm', 
                 color='green')

    # 设置横轴，理论周期曲线，偏心率 ecc 和斜率 obliq
    axes[0].set_xlabel('理论周期曲线', loc='center')
    axes[1].set_xlabel('周期滤波曲线', loc='center')

    # 设置纵轴，年龄 kyr
    axes[0].set_ylim(0.0, 3 * 1000)
    axes[1].set_ylim(0.0, np.max(depth) * 1.05)
    axes[0].set_ylabel('年龄 (kyr)', loc='center')
    axes[1].set_ylabel('深度 (depth)', loc='center')

    # 绘图
    for ax in axes:
        ax.legend(loc='upper left')
        ax.grid(True, alpha=0.7)
        ax.invert_yaxis()  # 反转纵轴

    # 保存
    plt.savefig(
        result_folder + r'/{hole_name}'.format(hole_name=hole_name), 
        dpi=720)


if __name__ == '__main__':
    """
    1. 人工处理，根据旋回厚度比例，与显著米兰科维奇周期进行校对，得到短偏心率周期
    2. 人工处理，计算沉积速率
    """

    """
    3. 根据短偏心率周期，对 NGR 数据做滤波分析，绘制天文年代标尺图
    """
    # 读取处理过的 laskar 2004 数据文件
    la04_data_path = r'.\海洋数据处理与可视化\output\处理过的La2004.csv'
    la04_data = pd.read_csv(la04_data_path)
    la04_data = la04_data.sort_values(by='time (kyr from J2000)', ascending=True)
    time = - la04_data['time (kyr from J2000)']
    ecc = la04_data['ecc']

    # U1533 数据的文件路径，参数 hole 记得 format，A, B, C, D
    u1533_data_path = r'.\海洋数据处理与可视化\data\阿蒙森海\Physical Properties\Natural gamma radiation\data_by_hole_compiled_scales\379-U1533{id}-NGR-ALLSCALES.csv'
    
    # 读取人工处理的数据，
    other_path = r'.\海洋数据处理与可视化\output\处理NGR的结果\NGR频谱分析与显著天文周期比对结果\result.csv'
    other_data = pd.read_csv(other_path)

    # 处理结果的保存路径
    result_folder = r'.\海洋数据处理与可视化\output\处理NGR的结果\天文年代标尺'

    holes = {
        'U1533': ['A', 'B', 'D'],  # C 的数据太少，不做
    }

    for hole_name, ids in holes.items():
        if hole_name == 'U1533':
            for id in ids:

                # 拼接钻井名，如 U1533 + A
                full_name = hole_name + id

                # 根据钻孔编号读取数据
                hole_data = pd.read_csv(u1533_data_path.format(id=id))
                depth = hole_data['Depth CCSF-379-U1533-ABCD-20191030 (m)']
                ngr = hole_data['NGR total counts (cps)']

                filtered_row = other_data[other_data['hole'] == full_name]
                significant_ecc = filtered_row['significant_ecc'].values[0]
                rotation_thickness = filtered_row['rotation_thickness'].values[0]

                draw(time               =   time, 
                     ecc                =   ecc,
                     depth              =   depth, 
                     ngr                =   ngr,
                     rotation_thickness =   rotation_thickness,
                     significant_ecc    =   significant_ecc,
                     hole_name          =   full_name,
                     result_folder      =   result_folder)