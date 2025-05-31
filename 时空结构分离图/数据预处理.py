import pandas as pd
import numpy as np


# 所有数据的文件路径
PATHS = {
    # 钻井的地理数据，包含：钻井编号、经度、纬度
    '阿蒙森海钻井地理数据': r'.\海洋数据处理与可视化\data\阿蒙森海\expedition379.csv',
    '罗斯海钻井地理数据': r'.\海洋数据处理与可视化\data\罗斯海\expedition374.csv',

    # 钻井的磁化率数据，包含：钻井编号、深度、磁化率
    # 有参数 hole，可用例如 U1533A 来替换
    '阿蒙森海钻井磁化率': r'.\海洋数据处理与可视化\data\阿蒙森海\Magnetism\Magnetic susceptibility (KappaBridge)\data_by_hole_compiled_scales\379-{hole}-KAPPA-ALLSCALES.csv',
    '罗斯海钻井磁化率': r'',

    # 沉积速率的数据
    '沉积速率': r'.\海洋数据处理与可视化\output\处理NGR的结果\NGR频谱分析与显著天文周期比对结果\旋回厚度、显著短偏心率周期、和沉积速率.csv',

    # 处理后文件的保存路径
    '保存路径': r'.\海洋数据处理与可视化\output\时空结构分离图\预处理后的数据.csv'
}

# 所有的可调参数
PARAMS = {

    # 这里面的海域名字要和上方路径对应
    '海域': [
        '阿蒙森海', 
        # '罗斯海'
    ],

    # 每个海域支持的钻井
    '支持的钻井': [
        'U1533A',
        'U1533B',
        'U1533C',
        'U1533D'
    ],

}


# 转换坐标到十进制格式
def dms2dec(d, m, s, hemisphere):
    decimal = d + m / 60 + s / 3600
    return -decimal if hemisphere in ['S', 'W'] else decimal


if __name__ == '__main__':

    # 加载沉积速率，用来计算年代
    sediment_rate_list = pd.read_csv(PATHS['沉积速率'])

    # 处理好的数据将会被暂存到这个对象中，最后保存
    tmp = []
    for sea in PARAMS['海域']:

        # 根据不同的海域确定航次
        exp = 0
        if sea == '阿蒙森海':
            exp = 379
        elif sea == '罗斯海':
            exp = 374

        # 加载数据
        holes_data = pd.read_csv(PATHS[sea + '钻井地理数据'])

        # 通用处理数据代码
        hole_name = ''
        for hole_row in holes_data.itertuples():
            
            hole_name = hole_row.hole

            # 如果不在支持的钻井里，就去处理下一个
            if hole_name not in PARAMS['支持的钻井']:
                continue

            lon = dms2dec(hole_row.lon_deg, hole_row.lon_min, hole_row.lon_sec, hole_row.lon_dir)
            lat = dms2dec(hole_row.lat_deg, hole_row.lat_min, hole_row.lat_sec, hole_row.lat_dir)

            # 处理磁化率数据
            susceptibility_data = pd.read_csv(PATHS[sea + '钻井磁化率'].format(hole=hole_name))

            # 获得这个钻井的沉积速率
            filtered_row = sediment_rate_list[sediment_rate_list['hole'] == hole_name]
            sediment_rate = np.float64(filtered_row['sed_rate'].values[0])
            
            for sus_row in susceptibility_data.itertuples():

                depth = getattr(sus_row, '_9')
                age = - depth / sediment_rate

                sus = getattr(sus_row, '_15')

                # 拼接到 tmp
                tmp.append([
                    exp,
                    hole_name,
                    lon,
                    lat,
                    depth,
                    age,
                    sus
                ])

    # 保存到本地
    new_df = pd.DataFrame(tmp, columns=[
        'exp',
        'hole',
        'lon',
        'lat',
        'depth (m)',
        'age (kyr from J2000)',
        'susceptibility (SI)',
    ])
    new_df.to_csv(PATHS['保存路径'])