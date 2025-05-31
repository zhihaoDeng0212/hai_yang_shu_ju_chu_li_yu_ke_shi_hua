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
        'name': 'U1532',
        'color': 'red',  # 改颜色
        'lon': dms2dec(107, 31.5003, 0, 'W'),
        'lat': dms2dec(68, 36.6833, 0, 'S')
    }, {
        'name': 'U1533',
        'color': 'black',  # 改颜色
        'lon': dms2dec(109, 3.0010, 0, 'W'),
        'lat': dms2dec(68, 44.0168, 0, 'S')
    },
]

# 创建地图
plt.figure(figsize=(6, 6))
proj = ccrs.SouthPolarStereo()
ax = plt.subplot(projection=proj)

# 设置阿蒙森海区域范围 (西经105°到110°，南纬67°到68°)
ax.set_extent([-120, -90, -75, -68], ccrs.PlateCarree())

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
        marker='o', markersize=10, transform=ccrs.PlateCarree(), alpha=0.8, label=f'Site {name}')

    ax.text(lon + 0.5, lat - 0.3, name,
            transform=ccrs.PlateCarree(), color=color, fontsize=12, va='top', ha='left')

ax.legend(loc='lower right', frameon=True, fontsize=10)

# 添加标题
plt.title('阿蒙森海钻探位置图\nSite U1532 & U1533', fontsize='large', fontweight='bold')

# 保存
plt.savefig(r'.\海洋数据处理与可视化\output\地图\站点图\阿蒙森海站点图.png', dpi=720, bbox_inches='tight')

