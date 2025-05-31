import matplotlib.pyplot as plt
import pandas as pd
from mpl_toolkits.mplot3d import Axes3D
 
# 示例数据格式（需替换为实际数据）：
# 假设数据包含经度、纬度、有机碳通量三个维度
data = pd.read_csv('carbon_flux.csv')
x = data['longitude']
y = data['latitude']
z = data['flux']
 
# 创建三维坐标系
fig = plt.figure(figsize=(10, 8))
ax = fig.add_subplot(111, projection='3d')
 
# 绘制散点图
scatter = ax.scatter(x, y, z, 
                    c=z,  # 用颜色表示通量值
                    cmap='viridis',
                    s=20,  # 点的大小
                    alpha=0.7)
 
# 添加颜色条
cbar = plt.colorbar(scatter, pad=0.1)
cbar.set_label('Organic Carbon Flux (gC/m²/yr)')
 
# 坐标轴标签
ax.set_xlabel('Longitude')
ax.set_ylabel('Latitude')
ax.set_zlabel('Carbon Flux')
 
# 调整观察角度（可选）
ax.view_init(elev=25, azim=45)  # 俯仰角25度，方位角45度
 
plt.title('3D Sediment Carbon Flux Distribution')
plt.tight_layout()
plt.show()