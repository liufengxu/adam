import matplotlib.pyplot as plt
import matplotlib as mpl
from matplotlib.patches import Polygon
from matplotlib.colors import rgb2hex
from matplotlib.ticker import FuncFormatter
import matplotlib.font_manager as fm
from matplotlib.colors import LinearSegmentedColormap
import numpy as np
import pandas as pd
import os
os.environ['PROJ_LIB'] = r'/anaconda3/pkgs/proj4-5.2.0-h6de7cb9_1006/share/proj'
from mpl_toolkits.basemap import Basemap
MYFONT = fm.FontProperties(fname='/Users/liufengxu/Public/MSYH.TTC')  # 准备中文字体，默认英文字体可能出现乱码

fig, ax = plt.subplots(figsize=(9, 8)) # 准备画布。注意该语句必须放到m=Basemap()之前。

m = Basemap(llcrnrlon=77, llcrnrlat=14, urcrnrlon=140, urcrnrlat=51, projection='lcc', lat_1=33, lat_2=45, lon_0=100) #中国地图为投影主体
m.readshapefile('CHN_adm_shp/CHN_adm1', 'states', drawbounds=True)  # 绘制省级行政区轮廓
m.readshapefile('CHN_adm_shp/CHN_adm2', 'counties', drawbounds=False)  # 绘制地级市，但不包含轮廓
# m.readshapefile('TWN_adm_shp/TWN_adm0', 'taiwan', drawbounds=True)  # 政治正确，增加台湾

provincenames = []
for province_dict in m.states_info:
    province_name = province_dict['NL_NAME_1']
    p = province_name.split('|')
    if p[0][0] == '黑':
        s = '黑龙江'
    else:
        s = p[-1]
    if s[0][0] == '内':
        s = '内蒙古'
    elif s[0] == '新':
        s = '新疆'
    elif s[0] == '宁':
        s = '宁夏'
    elif s[0:2] == '广西':
        s = '广西'
    elif s[0:2] == '西藏':
        s = '西藏'
    provincenames.append(s)
provincenames_nodup = list(set(provincenames))  # 去除重复
# print(provincenames_nodup)

path = 'test_map.xlsx'
df = pd.read_excel(path, encoding='UTF-8')  # 读取数据文件到pandas
df = df[df['num'] > 0]
pivoted = pd.pivot_table(df, index='province', values='num', aggfunc=sum)
data = pivoted['num']
data = data.reindex(provincenames_nodup)

cmap1 = LinearSegmentedColormap.from_list('mycmap', ['green', 'white'])  # 定义负值colormap,绿白渐变
vmax1 = 0
vmin1 = min(data)
norm1 = mpl.colors.Normalize(vmin=vmin1, vmax=vmax1)  # 正态分布
cmap2 = LinearSegmentedColormap.from_list('mycmap', ['white', 'red'])  # 定义正值colormap,白红渐变
vmax2 = 50  # 高于50都为最深红色，如不设置阈值这里应为max(data)
vmin2 = 0
norm2 = mpl.colors.Normalize(vmin=vmin2, vmax=vmax2)

# 每个值根据正负和正态分布中的位置给定颜色
colors = {}
for index, value in data.iteritems():
    if value < 0:
        colors[index] = cmap1(np.sqrt((value - vmin1) / (vmax1 - vmin1)))[:3]
    else:
        colors[index] = cmap2(np.sqrt((value - vmin2) / (vmax2 - vmin2)))[:3]

for nshape, seg in enumerate(m.states):
    color = rgb2hex(colors[provincenames[nshape]])  # 颜色格式由RGB转为16位HEX
    poly = Polygon(seg, facecolor=color, edgecolor=color)  # 绘制带有颜色的地级市多边形
    ax.add_patch(poly)  # 将绘制多边形添加到画布上
plt.title('Y分布', fontproperties=MYFONT, fontsize=16, y=0.9)

# 生产渐变色legend colorbar
# cax1 = fig.add_axes([0.18, 0.15, 0.36, 0.01])
cax2 = fig.add_axes([0.18, 0.15, 0.36, 0.01])
comma_fmt = FuncFormatter(lambda x, p: format(int(x), ','))
# cb1 = mpl.colorbar.ColorbarBase(cax1, cmap=cmap1, norm=norm1,
#       spacing='proportional', orientation='horizontal', format=comma_fmt)
cb2 = mpl.colorbar.ColorbarBase(cax2, cmap=cmap2, norm=norm2,
                                spacing='proportional', orientation='horizontal', format=comma_fmt)
cb2.set_label('人数', x=1, fontproperties=MYFONT)

# 去除图片边框
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.spines['bottom'].set_visible(False)
ax.spines['left'].set_visible(False)

# 保存图片，去掉边缘白色区域，透明
plt.savefig('O-Z38638.png', format='png', bbox_inches='tight', transparent=True, dpi=600)

