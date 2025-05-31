import pandas as pd
import numpy as np


PATHS = {
    # 参数 sea 待修改
    '待处理数据': r'.\海洋数据处理与可视化\output\经验正交函数分解\预处理后的数据\第1次\{sea}.csv',
    '保存路径': r'.\海洋数据处理与可视化\output\经验正交函数分解\预处理后的数据\第2次\result.csv',
}

PARAMS = {
    '海域': [
        '阿蒙森海', 
        '罗斯海'
        ],
}


if __name__ == '__main__':
    """
    本程序按照深度 depth 唯一的原则，将各个钻孔的磁化率数据整合到一个 dataframe 中。
    处理后的数据将保存到指定路径。
    """

    # 创建一个空的 DataFrame，作为结果
    result_df = pd.DataFrame({
        'Depth (m)': [],

        # 阿蒙森海
        'U1533A mag sus (SI x 10^-5)': [],
        # 'U1533B mag sus (SI x 10^-5)': [],
        # 'U1533C mag sus (SI x 10^-5)': [],
        # 'U1533D mag sus (SI x 10^-5)': [],

        # 罗斯海
        # 'U1521A mag sus (SI x 10^-5)': [],
        'U1522A mag sus (SI x 10^-5)': [],
        # 'U1523A mag sus (SI x 10^-5)': [],
        # 'U1523B mag sus (SI x 10^-5)': [],
        'U1523E mag sus (SI x 10^-5)': [],
        'U1524A mag sus (SI x 10^-5)': [],
        # 'U1524C mag sus (SI x 10^-5)': [],
        'U1525A mag sus (SI x 10^-5)': [],
    })

    for sea in PARAMS['海域']:
        # 读取数据
        data = pd.read_csv(PATHS['待处理数据'].format(sea=sea))

        # 处理数据，遍历第一次处理好的数据，depth 将唯一，不会有重复
        for row in data.itertuples():
            hole = getattr(row, 'Hole')
            depth = getattr(row, '_3')
            mag_sus = getattr(row, '_5')
            
            # 过滤一些不想要的 hole，一旦出现，就跳转到下一行
            filter = [
                # 阿蒙森海
                'U1533B',
                'U1533C',
                'U1533D',

                # 罗斯海
                'U1521A',
                'U1523A',
                'U1523B',
                'U1524C',
                ]
            if hole in filter:
                continue

            # 首先，判断这个 depth 是否在 result_df 中出现过
            if depth in result_df['Depth (m)'].values:
                # 如果出现过，就只补充磁化率数据
                col_name = hole + ' mag sus (SI x 10^-5)'
                result_df.loc[result_df['Depth (m)'] == depth, col_name] = mag_sus
            else:
                # 如果没出现过，就根据海域创建新行，并添加进去
                new_row = pd.DataFrame({
                    'Depth (m)': [depth],

                    # 阿蒙森海
                    'U1533A mag sus (SI x 10^-5)': [np.nan if hole != 'U1533A' else mag_sus],
                    # 'U1533B mag sus (SI x 10^-5)': [np.nan if hole != 'U1533B' else mag_sus],
                    # 'U1533C mag sus (SI x 10^-5)': [np.nan if hole != 'U1533C' else mag_sus],
                    # 'U1533D mag sus (SI x 10^-5)': [np.nan if hole != 'U1533D' else mag_sus],

                    # 罗斯海
                    # 'U1521A mag sus (SI x 10^-5)': [np.nan if hole != 'U1521A' else mag_sus],
                    'U1522A mag sus (SI x 10^-5)': [np.nan if hole != 'U1522A' else mag_sus],
                    # 'U1523A mag sus (SI x 10^-5)': [np.nan if hole != 'U1523A' else mag_sus],
                    # 'U1523B mag sus (SI x 10^-5)': [np.nan if hole != 'U1523A' else mag_sus],
                    'U1523E mag sus (SI x 10^-5)': [np.nan if hole != 'U1523E' else mag_sus],
                    'U1524A mag sus (SI x 10^-5)': [np.nan if hole != 'U1524A' else mag_sus],
                    # 'U1524C mag sus (SI x 10^-5)': [np.nan if hole != 'U1524C' else mag_sus],
                    'U1525A mag sus (SI x 10^-5)': [np.nan if hole != 'U1525A' else mag_sus],
                })

                # 拼接
                result_df = pd.concat([result_df, new_row], ignore_index=True)

    # 对海域的循环结束，将有 nan 的行去掉
    result_df = result_df.dropna(axis=0)

    # 保存数据
    result_df.to_csv(PATHS['保存路径'])
