import os
import pandas as pd
import matplotlib as mpl
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
from eofs.standard import Eof
import ssl
import cartopy.crs as ccrs
import cartopy.feature as cfeature
import sys


PATHS = {
    '预处理后的数据': r'.\海洋数据处理与可视化\output\经验正交函数分解\预处理后的数据\第2次\result.csv',
    '保存文件夹': r'.\海洋数据处理与可视化\output\经验正交函数分解\图片',
}


def dms2dec(d, m, s, hemisphere):
    """
    六十进制转换为十进制坐标
    :param d: 度
    :param m: 分
    :param s: 秒
    :param hemisphere: 半球，'N', 'S', 'E', 'W'
    :return: 十进制坐标
    """
    decimal = d + m / 60 + s / 3600
    return -decimal if hemisphere in ['S', 'W'] else decimal


def number_to_color(numbers, colormap='coolwarm'):
    """
    将-1到1范围内的数字映射为颜色
    
    参数:
    numbers: 数字列表/数组 (范围[-1, 1])
    colormap: 使用的色彩映射 (默认为'coolwarm')
    
    返回:
    颜色列表 (RGB元组)
    """
    # 创建归一化对象
    norm = mcolors.Normalize(vmin=-1, vmax=1)
    # 获取colormap
    cmap = plt.get_cmap(colormap)
    # 将数字归一化并映射到颜色
    return [cmap(norm(x)) for x in numbers], norm, cmap


if __name__ == '__main__':
    # 使 matplotlib 支持中文和显示负号
    plt.rcParams['font.sans-serif'] = ['Microsoft YaHei']  # 支持中文，不要用 SimHei，因为它不支持负号
    plt.rcParams['axes.unicode_minus'] = False  # 强制显示负号

    # 解决绘制南极洲地图时的 SSL 证书问题
    ssl._create_default_https_context = ssl._create_unverified_context

    # 读取预处理后的数据
    data = pd.read_csv(PATHS['预处理后的数据'])

    # 准备经纬度数据，longitude 是经度（西经、东经），latitude 是纬度（北纬、南纬）
    coord_data = [{
            'name': 'U1522A', # 罗斯海
            'color': '',
            'lon': dms2dec(174, 45, 4652, 'W'),
            'lat': dms2dec(76, 33, 2262, 'S')
        }, {
            'name': 'U1523E',
            'color': '',
            'lon': dms2dec(176, 47, 6660, 'W'),
            'lat': dms2dec(74, 9, 179, 'S')
        }, {
            'name': 'U1524A',
            'color': '',
            'lon': dms2dec(173, 38, 185, 'W'),
            'lat': dms2dec(74, 13, 427, 'S')
        }, {
            'name': 'U1525A',
            'color': '',
            'lon': dms2dec(173, 55, 2028, 'W'),
            'lat': dms2dec(75, 0, 603, 'S')
        }, {
            'name': 'U1533A', # 阿蒙森海
            'color': '',
            'lon': dms2dec(109, 3.0010, 0, 'W'),
            'lat': dms2dec(68, 44.0168, 0, 'S')
        },
    ]

    # 1. 先绘制南极洲地图

    # 创建地图画布和子图，使用南极立体投影
    # 创建主图和 colorbar 的布局
    fig = plt.figure(figsize=(8, 4))
    # colorbar 区域
    cax = fig.add_axes([0.235, 0.005, 0.55, 0.05])
    ax = plt.subplot(projection=ccrs.SouthPolarStereo())

    # 设置地图范围（南极洲及周边地区）
    ax.set_extent([-200, -100, -70, -60], ccrs.PlateCarree())

    # 添加地理特征
    ax.add_feature(cfeature.LAND, facecolor='white')        # 陆地（白色表示冰雪）
    ax.add_feature(cfeature.OCEAN, facecolor='white')       # 海洋颜色（此处用白色，因为要绘制类似于热力图的效果，避免其他颜色干扰）
    ax.add_feature(cfeature.COASTLINE)                      # 海岸线
    ax.add_feature(cfeature.BORDERS, linestyle=':')         # 国界线（虚线）

    # 添加南极冰架数据（需要cartopy的高分辨率数据）
    ax.add_feature(cfeature.NaturalEarthFeature(
        'physical', 'antarctic_ice_shelves_polys', '50m',
        edgecolor='gray',
        facecolor='white'
    ))

    # 添加经纬度网格线
    gl = ax.gridlines(draw_labels=True, color='gray', linestyle='--', linewidth=2,
                  x_inline=False, y_inline=False, rotate_labels=False)
    gl.top_labels = True
    gl.right_labels = True
    gl.xlabel_style = {'size': 10}
    gl.ylabel_style = {'size': 10}

    # 2. EOF 分解
    # 提取磁化率数据并转为二维数组（维度：深度 × 钻孔）

    # 拼接列名
    tmp = []
    holes=['U1533A', 'U1522A', 'U1523E', 'U1524A', 'U1525A']
    for hole in holes:
        tmp.append(hole + ' mag sus (SI x 10^-5)')

    # 提取数据
    raw_data = pd.read_csv(PATHS['预处理后的数据'])  # 列名应为 depth, U1533A mag sus, U1522A mag sus, U1523E mag sus, U1524A mag sus, U1525A mag sus
    data = raw_data[tmp].values  # shape = (n_depth, n)

    # 数据预处理（去均值）
    data_mean = data.mean(axis=0)
    data_centered = data - data_mean

    # 调试用，检查 data 数据
    # print(data)
    # sys.exit(0)

    # 创建EOF求解器（空间维度为n个钻孔）
    n = len(data_centered)
    solver = Eof(data_centered)
    eofs = solver.eofs(neofs=n)   # 空间模态（n 个钻孔的分布）
    pcs = solver.pcs(npcs=n)      # 时间系数（沿深度的变化）
    variance = solver.varianceFraction()  # 各模态解释方差

    # 调试用，检查 eofs 数据
    # print(eofs)
    # print(variance)
    # sys.exit(0)

    numbers = eofs[0, :]  # 取第一个 EOF 模态（空间分布）
    colors, norm, cmap = number_to_color(numbers, 'plasma')  # 将数字映射为颜色

    # 3. 添加数据点
    for index, coord in enumerate(coord_data):
        # 提取经纬度
        lon = coord['lon']
        lat = coord['lat']
        color = colors[index]  # 获取对应的颜色
        
        # 绘制点
        ax.plot(lon, lat, marker='o', color=color, markersize=7, transform=ccrs.PlateCarree())

    # 添加水平colorbar
    cb = mpl.colorbar.ColorbarBase(cax, cmap=cmap, norm=norm, orientation='horizontal')

    # 添加标题
    plt.title(f'EOF Mode 1 ({variance[0]*100:.1f}%)', fontsize='larger', fontweight='bold')

    # 保存地图
    plt.savefig(os.path.join(PATHS['保存文件夹'], '阿蒙森海、罗斯海 EOF 空间模态图.png'), dpi=720, bbox_inches='tight')