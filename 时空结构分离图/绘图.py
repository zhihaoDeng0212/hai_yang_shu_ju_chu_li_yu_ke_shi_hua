import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import griddata
import cartopy.crs as ccrs
from matplotlib.ticker import FuncFormatter

# 所有数据的文件路径
PATHS = {
    '预处理后的数据': r'.\海洋数据处理与可视化\output\时空结构分离图\预处理后的数据.csv',
    # 参数 hole 可修改
    '保存路径': r'.\海洋数据处理与可视化\output\时空结构分离图\绘图\{hole}.png'
}


def decimal_to_dms(decimal, is_lon=False):
    """将十进制度转换为度分秒字符串"""
    direction = ''
    if is_lon:
        direction = 'E' if decimal >= 0 else 'W'
    else:
        direction = 'N' if decimal >= 0 else 'S'
    
    decimal = abs(decimal)
    degrees = int(decimal)
    minutes = int((decimal - degrees) * 60)
    seconds = (decimal - degrees - minutes/60) * 3600
    return f"{degrees}°{minutes:02d}'{seconds:05.2f}\"{direction}"


if __name__ == '__main__':

    # 使 matplotlib 支持中文和显示负号
    plt.rcParams['font.sans-serif'] = ['Microsoft YaHei']  # 支持中文，不要用 SimHei，因为它不支持负号
    plt.rcParams['axes.unicode_minus'] = False  # 强制显示负号

    data = pd.read_csv(PATHS['预处理后的数据'])

    # 生成空间网格（经纬度范围根据实际钻孔位置调整）
    grid_x, grid_y = np.mgrid[
        data.lon.min():data.lon.max():100j,
        data.lat.min():data.lat.max():100j
    ]

    # 插值物性参数（以磁化率为例）
    grid_susceptibility = griddata(
        points=data[['lon', 'lat']].values,
        values=data['susceptibility (SI)'],
        xi=(grid_x, grid_y),
        method='linear'
    )

    fig, axes = plt.subplots(1, 2, figsize=(12, 6))

    # 空间分布图（某一时间切片）
    contour = plt.contourf(grid_x, grid_y, grid_susceptibility, cmap='viridis')
    fig.colorbar(contour, label='磁化率 (SI)')
    axes[0].scatter(data['lon'], data['lat'], c=data['age (kyr from J2000)'], s=10, label='钻井点位')
    axes[0].set_xlabel('经度')
    axes[0].set_ylabel('纬度')
    axes[0].set_title('磁化率空间分布图 (年代（距今）1 ka)')
    axes[0].xaxis.set_major_formatter(FuncFormatter(lambda x, pos: decimal_to_dms(x, is_lon=True)))
    axes[0].yaxis.set_major_formatter(FuncFormatter(lambda y, pos: decimal_to_dms(y, is_lon=False)))
  
    # 时间-物性演化图（某一钻孔）
    hole_example = data[data['hole'] == 'U1533B']
    axes[1].plot(- hole_example['age (kyr from J2000)'], hole_example['susceptibility (SI)'], 'b-o')
    axes[1].set_xlabel('地层年代 (ka)')
    axes[1].set_ylabel('磁化率 (SI)')
    axes[1].set_title('年代-磁化率演化图 (U1533B)')

    plt.tight_layout()
    plt.savefig(PATHS['保存路径'].format(hole='U1533B'))