import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import cartopy.feature as cfeature
import pandas as pd

import ssl

# 使 matplotlib 支持中文和显示负号
plt.rcParams['font.sans-serif'] = ['Microsoft YaHei']  # 支持中文，不要用 SimHei，因为它不支持负号
plt.rcParams['axes.unicode_minus'] = False  # 强制显示负号

# 解决ssl问题，否则无法下载地图
ssl._create_default_https_context = ssl._create_unverified_context

# 让 matplotlib 支持中文
plt.rcParams['font.family'] = ['Microsoft YaHei']


# 转换坐标到十进制格式
def dms2dec(d, m, s, hemisphere):
    decimal = d + m / 60 + s / 3600
    return -decimal if hemisphere in ['S', 'W'] else decimal


# 站点数据，longitude 是经度（西经、东经），latitude 是纬度（北纬、南纬）
data = [
    {
        'name': 'U1522A',
        'color': '#FF0000',  # 红色
        'lon': dms2dec(174, 45, 4652, 'W'),
        'lat': dms2dec(76, 33, 2262, 'S')
    }, {
        'name': 'U1523ABE',
        'color': '#FFFF00',  # 黄色
        'lon': dms2dec(176, 47, 6660, 'W'),
        'lat': dms2dec(74, 9, 179, 'S')
    }, {
        'name': 'U1524A',
        'color': '#006400',  # 绿色
        'lon': dms2dec(173, 38, 185, 'W'),
        'lat': dms2dec(74, 13, 427, 'S')
    }, {
        'name': 'U1524BC',
        'color': '#8A2BE2',  # 紫色
        'lon': dms2dec(173, 37, 9338, 'W'),
        'lat': dms2dec(74, 13, 537, 'S')
    }, {
        'name': 'U1525A',
        'color': '#8B4513',  # 棕色
        'lon': dms2dec(173, 55, 2028, 'W'),
        'lat': dms2dec(75, 0, 603, 'S')
    }
]

# 创建地图
plt.figure(figsize=(6, 6))
proj = ccrs.SouthPolarStereo()
ax = plt.subplot(projection=proj)

# 设置罗斯海区域范围
ax.set_extent([-200, -160, -80, -70], ccrs.PlateCarree())

# 添加地理要素
ax.add_feature(cfeature.LAND, facecolor='white', zorder=2)
ax.add_feature(cfeature.OCEAN, facecolor='#4682b4')
ax.add_feature(cfeature.COASTLINE.with_scale('50m'), linewidth=0.8)

# 添加网格和标签
gl = ax.gridlines(draw_labels=True, color='gray', linestyle='--', linewidth=2,
                  x_inline=False, y_inline=False, rotate_labels=False)
gl.top_labels = False
gl.right_labels = False
gl.xlabel_style = {'size': 10}
gl.ylabel_style = {'size': 10}

# 绘制站点位置
for hole in data:

    name = hole['name']
    lon = hole['lon']
    lat = hole['lat']
    color = hole['color']

    ax.plot(lon, lat, color=color,
        marker='o', markersize=8, markeredgecolor='black', markeredgewidth=1,
        transform=ccrs.PlateCarree(), alpha=1, label=f'Site {name}')

ax.legend(loc='lower right', frameon=True, fontsize=10)

# 添加标题
plt.title('罗斯海钻探位置图\n', fontsize='large', fontweight='bold')

# 保存
plt.savefig(r'.\海洋数据处理与可视化\output\地图\站点图\罗斯海站点图.png', dpi=720, bbox_inches='tight')

