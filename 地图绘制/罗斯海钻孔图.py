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
data_path = r'.\海洋数据处理与可视化\data\罗斯海\expedition374.csv'
data = pd.read_csv(data_path)

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
for row in data.itertuples():

    name = row.hole
    lon = dms2dec(row.lon_deg, row.lon_min, row.lon_sec, row.lon_dir)
    lat = dms2dec(row.lat_deg, row.lat_min, row.lat_sec, row.lat_dir)
    color='black'

    ax.plot(lon, lat, color=color,
        marker='o', markersize=6, transform=ccrs.PlateCarree(), alpha=0.8, label=f'Site {name}')

    ax.text(lon + 0.5, lat + 0.3, name,
            transform=ccrs.PlateCarree(), color=color, fontsize=8, va='top', ha='left')

# ax.legend(loc='lower right', frameon=True, fontsize=10)

# 添加标题
plt.title('罗斯海钻孔位置图', fontsize='large', fontweight='bold')

# 保存
plt.savefig(r'.\海洋数据处理与可视化\output\地图\罗斯海钻孔图.png', dpi=720, bbox_inches='tight')

