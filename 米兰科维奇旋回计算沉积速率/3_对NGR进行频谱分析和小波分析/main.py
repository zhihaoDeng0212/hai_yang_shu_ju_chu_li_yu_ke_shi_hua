import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
from scipy.signal import periodogram
import numpy as np
import pywt


if __name__ == '__main__':
    """
    目的：根据 NGR 数据，得到前五个显著的旋回厚度及其比值
    可视化的目的：寻找显著周期，验证周期在深度方向上的分布和显著性
    """

    hole_list = {
        'ross': {
            # 'U1521': ['A'],  # 运行时间太长
            'U1522': ['A'],
            'U1523': ['A', 'B', 'E'],
            'U1524': ['A', 'C'],
            'U1525': ['A'],
        },
        'amundsen': {
            'U1533': ['A', 'B', 'C', 'D'],
        }
    }

    amundsen_data_path = r'.\海洋数据处理与可视化\data\阿蒙森海\Physical Properties\Natural gamma radiation\data_by_hole_compiled_scales\379-{hole_full_name}-NGR-ALLSCALES.csv'
    ross_data_path = r'.\海洋数据处理与可视化\data\罗斯海\Physical Properties\Natural gamma radiation\data_by_hole\374-{hole_full_name}-NGR.csv'
    save_folder = r'.\海洋数据处理与可视化\output\处理NGR的结果'
    
    for sea, sites in hole_list.items():
        for site, holes in sites.items():
            for hole in holes:

                # 读取数据
                data_path = ''
                data = []
                depth = []

                hole_full_name = site + hole
                if sea == 'amundsen':
                    data_path = amundsen_data_path.format(hole_full_name=hole_full_name)
                    data = pd.read_csv(data_path)
                    depth = data['Depth CCSF-379-U1533-ABCD-20191030 (m)']
                elif sea == 'ross':
                    data_path = ross_data_path.format(hole_full_name=hole_full_name)
                    data = pd.read_csv(data_path)
                    depth = data['Depth CSF-A (m)']
                else:
                    raise ValueError
               
                ngr = data['NGR total counts (cps)']

                # 创建图像
                fig = plt.figure(figsize=(6, 6))
                gs = gridspec.GridSpec(nrows=3, ncols=1, height_ratios=[2, 2, 0.2], wspace=0.2, hspace=0.6)

                # 使 matplotlib 支持中文和显示负号
                plt.rcParams['font.sans-serif'] = ['Microsoft YaHei']  # 支持中文，不要用 SimHei，因为它不支持负号
                plt.rcParams['axes.unicode_minus'] = False  # 强制显示负号

                # 修改标题
                fig.suptitle(f'U1533{hole} 频谱分析图、小波分析时频图', fontsize='larger', fontweight='bold')

                # 数据预处理
                # 使用的就是处理过的数据，所以无需预处理

                """
                频谱分析
                """
                sampling_period = depth[1] - depth[0]  # 采样间隔为 0.1m
                freqs, power = periodogram(ngr, fs=1/sampling_period)
                significant_peaks = freqs[power > np.percentile(power, 95)]  # 设置 95% 的置信度

                # 识别显著周期
                dominant_period = 1 / significant_peaks[0]  # 对应旋回厚度，单位为 m

                # 分析结果
                temp = np.array(1 / significant_peaks[0:5])

                # 计算比值
                standard = temp[-1]
                a = []
                for i in range(0, temp.shape[0]):
                    a.append(temp[i] / standard)
                
                # 保存数据
                df = pd.DataFrame({
                    '显著周期（前五个）': significant_peaks[0:5],
                    '旋回厚度（前五个）': temp,
                    '前五个旋回厚度的比值': a
                })

                # 生成红色噪声的理论功率谱（AR(1)模型）
                def red_noise_spectrum(freqs, alpha=0.5, sigma=1):
                    """
                    生成红色噪声的理论功率谱（AR(1)模型）
                    """
                    return sigma**2 / (1 - 2 * alpha * np.cos(2 * np.pi * freqs) + alpha**2)
                
                alpha = 0.8  # 自相关系数（需根据实际数据估计）
                sigma = np.var(ngr)  # 噪声方差
                red_power = red_noise_spectrum(freqs, alpha, sigma)

                # 蒙特卡洛模拟计算置信度线
                n_simulations = 1000  # 模拟次数
                simulated_powers = []
                for _ in range(n_simulations):
                    n_samples = len(depth)
                    # 生成红色噪声数据（AR(1)过程）
                    noise = np.zeros(n_samples)
                    noise[0] = np.random.randn()
                    for i in range(1, n_samples):
                        noise[i] = alpha * noise[i-1] + np.random.randn() * sigma
                    
                    # 计算功率谱
                    _, sim_power = periodogram(noise, fs=1/sampling_period, detrend='linear')
                    simulated_powers.append(sim_power)
                
                simulated_powers = np.array(simulated_powers)
                conf_90 = np.percentile(simulated_powers, 90, axis=0)  # 90%置信度
                conf_95 = np.percentile(simulated_powers, 95, axis=0)  # 95%置信度

                """
                可视化频谱分析图
                """
                ax = fig.add_subplot(gs[0])
                target_freq = significant_peaks[0]
                # 原始谱图
                ax.semilogy(freqs, power, label='谱图', color='blue', linewidth=1)
                # 红色噪声理论曲线
                ax.plot(freqs, red_power, label='红色噪声曲线', color='red', linestyle='--')
                # 置信度线
                ax.plot(freqs, conf_90, label='90% 置信度', color='#FFD700', linestyle=':')   # 金黄色
                ax.plot(freqs, conf_95, label='95% 置信度', color='green', linestyle='-.')
                # 标记显著周期
                ax.axvline(target_freq, color='orange', linestyle='--', label=f'频率：{target_freq:.3f} m^(-1)')
                # 设置坐标轴
                ax.set_xlim(0, np.max(freqs))
                ax.set_xlabel(r'频率 / m^(-1)')
                ax.set_ylabel(r'频谱振幅')
                # 显示图例
                ax.legend(
                    loc="lower right",          # 基准位置为右下角
                    bbox_to_anchor=(1.0, 0.0),  # 微调位置（向右下对齐）
                    prop={"size": 8},           # 缩小字体大小
                    frameon=True,               # 显示图例边框
                    borderaxespad=0.5,          # 图例与坐标轴的间距
                    borderpad=0.5,              # 图例边框内边距
                    handlelength=1.5,           # 图例句柄长度
                    handleheight=1.0,           # 图例句柄高度
                    framealpha=0.9              # 边框透明度
                )

                """
                小波分析：连续小波变换
                """
                # 小波变换参数
                scales = np.arange(1, dominant_period)
                coef, freqs = pywt.cwt(ngr, scales, 'morl', sampling_period)

                """
                可视化时频图
                """
                ax = fig.add_subplot(gs[1])
                im = ax.imshow(np.abs(coef), extent=[depth.min(), depth.max(), 1, dominant_period], 
                        cmap='jet', aspect='auto')
                ax.invert_yaxis()  # 倒置 y 轴
                ax.set_xlabel(r'深度 / m')
                ax.set_ylabel(r'旋回厚度 / m')

                # 更新 colorbar
                cbar = fig.colorbar(im, cax=fig.add_subplot(gs[2]), orientation='horizontal', label='波谱能量')

                # 保存结果
                df.to_csv(save_folder + r'\频谱分析结果及比例关系\{hole_full_name}.csv'.format(hole_full_name=hole_full_name))
                plt.savefig(save_folder + r'\频谱分析、小波分析时频图\{hole_full_name}.png'.format(hole_full_name=hole_full_name), dpi=720)
