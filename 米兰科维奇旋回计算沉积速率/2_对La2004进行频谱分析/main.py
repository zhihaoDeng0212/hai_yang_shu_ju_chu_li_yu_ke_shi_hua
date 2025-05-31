import numpy as np
import pandas as pd
from matplotlib import pyplot as plt
from scipy.signal import detrend, periodogram

if __name__ == '__main__':
    """
    对预处理后的天文参数做频谱分析，得到其中显著天文周期（偏心率 ecc、斜率 obliq、岁差 precession）
    """
    data_folder = r'.\海洋数据处理与可视化\output\预处理后的La2004'
    save_folder = r'.\海洋数据处理与可视化\output\对La2004频谱分析结果'

    seas = ['amundsen', 'ross']

    for sea in seas:

        # 加载数据
        data_path = data_folder + r'/' + sea + "_La2004.csv"
        data = pd.read_csv(data_path)
        t = data['time (kyr from J2000)']
        e = data['ecc']
        o = data['obliq (rad)']
        p = data['precession (rad)']

        # 采样间隔，一般是 1kyr
        sampling_period = t[1] - t[0]
        fs = 1 / sampling_period  # 求倒数，即为采样频率

        # 偏心率频谱分析，f_e 是显著频率的集合，单位是 kyr^(-1)
        f_e, p_e = periodogram(e, fs, scaling='density')
        period_e = 1 / f_e

        # 斜率频谱分析
        f_o, p_o = periodogram(o, fs, scaling='density')
        period_o = 1 / f_o

        # 岁差频谱分析
        f_p, p_p = periodogram(p, fs, scaling='density')
        period_p = 1 / f_p

        def find_top_peaks(periods, power, n=4):
            """
            提取显著周期（默认前4个峰值）
            """
            peaks = np.argsort(power)[-n:]
            return periods[peaks]  # 转换为 kyr

        # 提取显著周期
        top_e = find_top_peaks(period_e, p_e)
        top_o = find_top_peaks(period_o, p_o)
        top_p = find_top_peaks(period_p, p_p)

        # 新建一个数据集，后续方便保存为 csv 文件
        df = pd.DataFrame({
            'Ecc': top_e,
            'Obliq (rad)': top_o,
            'Precession (rad)': top_p
        })

        for col_name in df.columns:
            # 为每一个数值四舍五入
            df[col_name] = df[col_name].round(0)

            # 去除每一列中的重复值，仅保留一次，替换为NaN
            mask = df.duplicated(subset=[col_name], keep='first')  # 仅标记后续重复项
            df.loc[mask, col_name] = np.nan

            # 将非空值前移
            df[col_name] = df[col_name].dropna().reset_index(drop=True).reindex(df.index).values

        # 修改索引名称并从 1 开始
        df.index = pd.RangeIndex(start=1, stop=len(df)+1, name='Index')

        # 保存
        df.to_csv(save_folder + r'/' + sea + '的La04频谱分析结果.csv')

