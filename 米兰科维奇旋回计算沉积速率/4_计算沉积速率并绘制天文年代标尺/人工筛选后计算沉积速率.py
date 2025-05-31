import numpy as np
import pandas as pd

data = pd.read_csv(r'.\海洋数据处理与可视化\output\处理NGR的结果\NGR频谱分析与显著天文周期比对结果\result.csv', index_col=0)
data['sed_rate'] = (data['rotation_thickness'] / data['significant_ecc']).round(3)
data.to_csv(r'.\海洋数据处理与可视化\output\处理NGR的结果\NGR频谱分析与显著天文周期比对结果\旋回厚度、显著短偏心率周期、和沉积速率.csv')
