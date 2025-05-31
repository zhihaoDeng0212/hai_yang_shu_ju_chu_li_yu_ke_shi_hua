import numpy as np
import pandas as pd

if __name__ == '__main__':
    """
    1. 查阅文献，确定识别阿蒙森海的地层年代范围大致为 0 到 2.9 Ma，
        罗斯海的地层年代范围大致为 0 到 2.4 Ma。根据时间范围筛选出 la2004 中的天文数据
    2. 计算岁差
    """
    # la2004 数据
    data_path = r'.\海洋数据处理与可视化\data\Laskar2004\INSOL.LA2004.csv'
    data = pd.read_csv(data_path)

    # 保存路径，参数 sea
    result_path = r'海洋数据处理与可视化\output\预处理后的La2004\{sea}_La2004.csv'

    start_times = {
        'amundsen': -2.9 * 1000,  # kyr
        'ross': -2.4 * 1000  # kyr
    }
    end_time = 0  # kyr
    
    for sea, start_time in start_times.items():

        # 根据时间筛选
        filtered_data = data[(data['t (kyr from J2000)'] >= start_time) & (data['t (kyr from J2000)'] <= end_time)]

        ecc = filtered_data['ecc']
        obliq = filtered_data['obliq (rad)']
        varpi = filtered_data['varpi (rad)']

        # 计算岁差
        precession = ecc * np.sin(varpi)

        # 保存数据
        df = pd.DataFrame({
            'time (kyr from J2000)': filtered_data['t (kyr from J2000)'].values,
            'ecc': ecc,
            'obliq (rad)': obliq,
            'precession (rad)': precession,
        })

        df = df.reset_index(drop=True)
        df.to_csv(result_path.format(sea=sea))
