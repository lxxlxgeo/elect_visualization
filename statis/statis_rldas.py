# RLDAS 要素统计程序
import numpy as np
from osgeo import gdal
from rasterstats import zonal_stats
import rasterio as rio
import pandas as pd
from .src.base_alg import Convert_Coor_with_SHP,Convert_Coor

'''


栅格统计功能,包括 风速统计,降水统计,最大位能统计
其中,

包含的基本信息有：
预报的类型,是短临还是短期,中期
出图区域的级别,1级:省级,2级：省级区域(东西南北中),3级:地级市,4级:地级市区域:东西南北中,5级:县或者区
出图的区域:黑龙江省,黑龙江区域,黑龙江地级市,黑龙江地级市区域,黑龙江县区


风速要素的统计包括
级别的统计：
1,2,3,4,5,6,7,8,9 9个级别的风速占比统计
风速的值的统计：
风速最小值,风速平均值,风速最大值的统计

降水的统计:
降水级别统计
无降水所占比例,小雨所占比例,中雨所占比例,大雨所占比例,暴雨所占比例,特大暴雨所占比例
降水值的统计
降水最大值,降水最小值,降水平均值

位能级别的统计：
位能高风险所占比例,位能无风险或者低风险所占的比例

位能值的统计:
位能最大值,位能最小值,位能平均值

关键技术:解决面积统计有问题:使用UTM 分带投影,由于黑龙江比较靠北,如果使用等经纬投影,则导致黑龙江的面积统计误差过大
黑龙江投影的建议分带为:UTM 52

方法:分别统计:降水,风速,位能,三种要素统计完成后合并为一个pd
'''
def pre_statis(tifffile,shpfile):
    ras_driver=rio.open(tifffile)
    allfine=ras_driver.transform
    array=ras_driver.read(1)
    result=zonal_stats(shpfile,array,affine=allfine)