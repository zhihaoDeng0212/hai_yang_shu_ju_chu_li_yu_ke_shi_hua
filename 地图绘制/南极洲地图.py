import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import cartopy.feature as cfeature

import ssl
ssl._create_default_https_context = ssl._create_unverified_context

# 使 matplotlib 支持中文和显示负号
plt.rcParams['font.sans-serif'] = ['Microsoft YaHei']  # 支持中文，不要用 SimHei，因为它不支持负号
plt.rcParams['axes.unicode_minus'] = False  # 强制显示负号

# 创建地图画布和子图，使用南极立体投影
plt.figure(figsize=(6, 6))
ax = plt.subplot(projection=ccrs.SouthPolarStereo())

# 设置地图范围（南极洲及周边地区）
ax.set_extent([-180, 180, -90, -60], ccrs.PlateCarree())

# 添加地理特征
ax.add_feature(cfeature.LAND, facecolor='white')        # 陆地（白色表示冰雪）
ax.add_feature(cfeature.OCEAN, facecolor='#4682b4')     # 海洋颜色
ax.add_feature(cfeature.COASTLINE)                      # 海岸线
ax.add_feature(cfeature.BORDERS, linestyle=':')         # 国界线（虚线）

# 添加南极冰架数据（需要cartopy的高分辨率数据）
ax.add_feature(cfeature.NaturalEarthFeature(
    'physical', 'antarctic_ice_shelves_polys', '50m',
    edgecolor='gray',
    facecolor='white'
))

# 添加经纬度网格线
gl = ax.gridlines(draw_labels=True, color='gray', linestyle='--', linewidth=0.5,
                  x_inline=False, y_inline=False, rotate_labels=False)
gl.top_labels = True
gl.right_labels = True
gl.xlabel_style = {'size': 10}
gl.ylabel_style = {'size': 10}

# 添加标题
plt.title('南极洲全貌图', fontsize='larger', fontweight='bold')

# 保存地图
plt.savefig(r'.\海洋数据处理与可视化\output\地图\南极洲地图', dpi=300, bbox_inches='tight')