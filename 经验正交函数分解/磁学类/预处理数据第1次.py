import pandas as pd
import numpy as np


PATHS = {
    # 参数 hole 待修改
    '阿蒙森海的待处理数据': r'.\海洋数据处理与可视化\data\阿蒙森海\Magnetism\Magnetic susceptibility (section half)\data_by_hole_compiled_scales\379-{hole}-MSPOINT-ALLSCALES.csv',
    # 参数 hole 待修改
    '罗斯海的待处理数据': r'.\海洋数据处理与可视化\data\罗斯海\Magnetism\Magnetic susceptibility (section half)\data_by_hole\374-{hole}-MSPOINT.csv',
    # 参数 sea 待修改
    '保存路径': r'.\海洋数据处理与可视化\output\经验正交函数分解\预处理后的数据\第1次\{sea}.csv',
    
    '沉积速率': r'.\海洋数据处理与可视化\output\处理NGR的结果\NGR频谱分析与显著天文周期比对结果\旋回厚度、显著短偏心率周期、和沉积速率.csv'
}

PARAMS = {
    '所有的钻井': {
        '罗斯海': {
            # 'U1521': ['A'],
            'U1522': ['A'],
            'U1523': ['A', 'B', 'E'],
            'U1524': ['A', 'C'],
            'U1525': ['A'],
        },
        '阿蒙森海': {
            'U1533': ['A', 'B', 'C', 'D'],
        }
    }
}

if __name__ == '__main__':
    """
    本程序用于将不同钻孔的磁化率数据和年代数据（利用沉积速率计算）合并到一个 dataframe 中，
    并保存到指定路径
    """

    sed_rate_data = pd.read_csv(PATHS['沉积速率'])

    for sea, sites in PARAMS['所有的钻井'].items():

        data_path = ''
        if sea == '阿蒙森海':
            data_path = PATHS['阿蒙森海的待处理数据']
        elif sea == '罗斯海':
            data_path = PATHS['罗斯海的待处理数据']

        # 新建一个 dataframe 一个海域的放在一起，该数据为第一个处理的版本
        new = pd.DataFrame({
            'Hole': [],
            'Depth (m)': [],
            'Time (kyr from J2000)': [],
            'Magnetic susceptibility (SI x 10^-5)': [],
        })

        for site, holes in sites.items():
            for hole in holes:
                
                # 拼接好，用来读取数据
                site_hole = site + hole

                # 磁化率和深度
                data = pd.read_csv(data_path.format(hole=site_hole))
                depth = data['Depth CSF-A (m)']
                mag_sus = data['Magnetic susceptibility (SI x 10^-5)']

                # 沉积速率
                filtered_row = sed_rate_data[sed_rate_data['hole'] == site_hole]
                sediment_rate = np.float64(filtered_row['sed_rate'].values[0])

                # 计算年代（BP kyr from J2000）
                time = - (depth / sediment_rate)

                # 拼接 dataframe
                new = pd.concat([new, pd.DataFrame({
                    'Hole': [site_hole] * len(depth),
                    'Depth (m)': depth,
                    'Time (kyr from J2000)': time,
                    'Magnetic susceptibility (SI x 10^-5)': mag_sus,
                })], ignore_index=True)

                # 对 hole 的循环结束
            # 对 site 的循环结束
        # 对 sea 的循环结束
        new.to_csv(PATHS['保存路径'].format(sea=sea))