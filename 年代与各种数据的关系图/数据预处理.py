import pandas as pd
import numpy as np

if __name__ == '__main__':
    """
    1. 去除 NaN 的数据
    2. 去除明显偏离正常范围的数据：
        (1) TOC 的正常范围：0 - 1.5 %
        (2) TN 的正常范围：0 - 0.15 %
    """
    
    # 数据的文件地址，一个参数需要 format，为 hole，例如 U1533A
    amundsen_data_path = r'.\海洋数据处理与可视化\data\阿蒙森海\Chemistry and Microbiology\Carbonate\data_by_hole\379-{hole}-CARB.csv'
    ross_data_path = r'.\海洋数据处理与可视化\data\罗斯海\Chemistry and Microbiology\Carbonate\data_by_hole\374-{hole}-CARB.csv'

    # 读取人工处理的数据地址
    other_data_path = r'.\海洋数据处理与可视化\output\处理NGR的结果\NGR频谱分析与显著天文周期比对结果\旋回厚度、显著短偏心率周期、和沉积速率.csv'
    other_data = pd.read_csv(other_data_path)

    # 保存路径
    save_folder = r'.\海洋数据处理与可视化\output\年代与各种数据的关系图\预处理后的数据（以钻井编号划分）'

    # 列举所有的钻井
    hole_list = {
        'ross': {
            # 'U1521': ['A'],
            'U1522': ['A'],
            'U1523': ['A', 'B', 'E'],
            'U1524': ['A', 'C'],
            'U1525': ['A'],
        },
        'amundsen': {
            'U1533': ['A', 'B', 'C', 'D'],
        }
    }

    # 处理所有钻井数据，预处理数据为需要的格式
    for sea, sites in hole_list.items():

        for site, holes in sites.items():

            for hole in holes:

                # 拼接钻井的全名
                full_name = site + hole

                # 根据不同的海域读取数据
                path = ''
                if sea == 'amundsen':
                    path = amundsen_data_path.format(hole=full_name)
                elif sea == 'ross':
                    path = ross_data_path.format(hole=full_name)
                else:
                    raise ValueError
                data = pd.read_csv(path)

                # 有一些行的数据里，TOC 和 TN 含量为 'b.d'. 将其替换为 NaN，后面统一删除整行
                data['Total carbon (wt%)'] = pd.to_numeric(data['Total carbon (wt%)'], errors='coerce')
                data['Nitrogen (wt%)'] = pd.to_numeric(data['Nitrogen (wt%)'], errors='coerce')

                # 如果行内指定列有 NaN 去除整行
                mask_not_na = (data['Total carbon (wt%)'].notna()) & data['Nitrogen (wt%)'].notna()
                data = data.loc[mask_not_na]

                # 转换一些列表的类型
                data['Total carbon (wt%)'] = data['Total carbon (wt%)'].astype('float64')
                data['Nitrogen (wt%)'] = data['Nitrogen (wt%)'].astype('float64')

                # 去除明显异常的数据
                # TOC 的范围为 [0, 1.5]，此处取最高值为 2
                # TN 的范围为 [0, 0.15]，此处取最高值为 0.2
                mask_toc = (data['Total carbon (wt%)'] >= 0.0) & (data['Total carbon (wt%)'] <= 2)
                mask_tn = (data['Nitrogen (wt%)'] >= 0.0) & (data['Nitrogen (wt%)'] <= 0.2)
                data = data.loc[mask_toc & mask_tn]

                # 重置索引
                data = data.reset_index(drop=True)

                # 准备化学数据，用来计算碳氮比
                depth = data['Top depth CSF-A (m)']
                toc = data['Total carbon (wt%)']
                tn = data['Nitrogen (wt%)']

                # 准备沉积速率，用来计算地层年代
                filtered_row = other_data[other_data['hole'] == full_name]
                sediment_rate = np.float64(filtered_row['sed_rate'].values[0])

                # 计算碳氮比
                cn = toc / tn

                # 计算地层年代
                time = - (depth / sediment_rate)

                # 新建一个 DataFrame 
                new = pd.DataFrame({
                    'Depth (m)': depth,
                    'Time (kyr from J2000)': time,
                    'TOC (wt%)': toc,
                    'TN (wt%)': tn,
                    'C/N': cn
                })
                
                # 根据地层年代排序
                new = new.sort_values(by='Time (kyr from J2000)', ascending=False).reset_index(drop=True)

                # 保存数据
                new.to_csv(save_folder + '/' + full_name + '.csv')

    
