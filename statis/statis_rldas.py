# RLDAS 要素统计程序
import numpy as np
from osgeo import gdal
from rasterstats import zonal_stats
import rasterio as rio
import pandas as pd
from .src.base_alg import Convert_Coor_with_SHP, Convert_Coor

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


def stat_func_pre_24(data):
    '''
    降水统计函数
    :param data: 输入的文件
    :return: 返回 每个值所占的比例
     level0:无降水的像元数量,level1 小雨的像元数量,level2 中雨的像元数量,level3 大雨的像元数量,level4 暴雨的像元数量,level5 大暴雨的像元数量,level6 特大暴雨的像元数量
    '''
    pre_24_level0 = (data < 0.1) | (np.isnan(data))  # 无降水
    pre_24_level1 = (data >= 0.1) & (data < 10.0)  # 小雨
    pre_24_level2 = (data >= 10.0) & (data < 25.0)  # 中雨
    pre_24_level3 = (data >= 25.0) & (data < 50.0)  # 大雨
    pre_24_level4 = (data >= 50.0) & (data < 100.0)  # 暴雨
    pre_24_level5 = (data >= 100.0) & (data < 250.0)  # 大暴雨
    pre_24_level6 = (data >= 250.0)  # 特大暴雨

    return np.sum(pre_24_level0), np.sum(pre_24_level1), np.sum(pre_24_level2), np.sum(pre_24_level3), np.sum(
        pre_24_level4), np.sum(pre_24_level5), np.sum(pre_24_level6)

def stat_func_pre_3(data):
    '''
    降水统计函数
    :param data: 输入的文件
    :return: 返回 每个值所占的比例
     level0:无降水的像元数量,level1 小雨的像元数量,level2 中雨的像元数量,level3 大雨的像元数量,level4 暴雨的像元数量,level5 大暴雨的像元数量,level6 特大暴雨的像元数量
    '''
    pre_24_level0 = (data < 0.1) | (np.isnan(data))  # 无降水
    pre_24_level1 = (data >= 0.1) & (data < 1.0)  # 小雨
    pre_24_level2 = (data >= 1.0) & (data < 3.0)  # 中雨
    pre_24_level3 = (data >= 3.0) & (data < 10.0)  # 大雨
    pre_24_level4 = (data >= 10.0) & (data < 20.0)  # 暴雨
    pre_24_level5 = (data >= 20.0) & (data < 50.0)  # 大暴雨
    pre_24_level6 = (data >= 50.0)  # 特大暴雨

    return np.sum(pre_24_level0), np.sum(pre_24_level1), np.sum(pre_24_level2), np.sum(pre_24_level3), np.sum(
        pre_24_level4), np.sum(pre_24_level5), np.sum(pre_24_level6)


def stat_func_cape(data):
    '''
    位能统计函数
    :param data:
    :return:
    '''
    cape_low_risk = (data < 800) | (np.isnan(data))  # 低雷电风险
    cape_high_risk = (data >= 800)  # 高雷电风险
    return np.sum(cape_low_risk), np.sum(cape_high_risk)


def stat_func_wins(data):
    wins_level_0 = (data < 0.3) | (np.isnan(data))  # 无风
    wins_level_1 = (data >= 0.3) & (data < 1.6)  # 1级风
    wins_level_2 = (data >= 1.6) & (data < 3.4)  # 2级风
    wins_level_3 = (data >= 3.4) & (data < 5.5)  # 3级风
    wins_level_4 = (data >= 5.5) & (data < 8.0)  # 4级风
    wins_level_5 = (data >= 8.0) & (data < 10.8)  # 5级风
    wins_level_6 = (data >= 10.8) & (data < 13.9)  # 6级风
    wins_level_7 = (data >= 13.9) & (data < 17.2)  # 7级风
    wins_level_8 = (data >= 17.2) & (data < 20.8)  # 8级风
    wins_level_9 = (data >= 20.8)  # 9级风

    return np.sum(wins_level_0), np.sum(wins_level_1), np.sum(wins_level_2), np.sum(wins_level_3), np.sum(
        wins_level_4), np.sum(wins_level_5), np.sum(wins_level_6), np.sum(wins_level_7), np.sum(wins_level_8), np.sum(
        wins_level_9)


def pre_static(tiffsrc, shpsrc,pre_func):
    pre_tif = '/vsimem/pre_tiff.tif'
    pre_shp = '/vsimem/statis_shp.shp'
    # pre_shp=r'G:\data\CLDAS\sh.shp'
    Convert_Coor(tiffsrc, pre_tif)
    Convert_Coor_with_SHP(shpsrc, pre_shp)
    print("start statis")
    try:
        dataset: gdal.Dataset = gdal.Open(pre_tif)
        geotrans = dataset.GetGeoTransform()
        res_x = abs(geotrans[1])
        res_y = abs(geotrans[5])
        pixel_area = res_x * res_y / (1000 * 1000)
        result_statis = zonal_stats(pre_shp, pre_tif, add_stats={
            'pre_count': pre_func}, geojson_out=True)
        statis_list = []
        for st in result_statis:
            item_stats = dict()

            propert = st['properties']
            pre_count = propert['pre_count']
            sum_count = propert['count']

            pre_mean = propert['mean']
            pre_max = propert['max']

            region = propert['名称']
            print(sum_count)
            print(pre_count)

            level0_count = pre_count[0]
            level1_count = pre_count[1]
            level2_count = pre_count[2]
            level3_count = pre_count[3]
            level4_count = pre_count[4]
            level5_count = pre_count[5]
            level6_count = pre_count[6]

            sum_area = sum_count * pixel_area
            level0_prop = level0_count / sum_count  # level0 占比
            level1_prop = level1_count / sum_count  # level1 占比
            level2_prop = level2_count / sum_count  # level2 占比
            level3_prop = level3_count / sum_count  # level3 占比
            level4_prop = level4_count / sum_count  # level4 占比
            level5_prop = level5_count / sum_count  # level5 占比
            level6_prop = level6_count / sum_count  # level6 占比

            # 收集全部信息
            item_stats['region'] = region
            item_stats['pre_mean'] = pre_mean
            item_stats['pre_max'] = pre_max
            item_stats['area'] = sum_area
            item_stats['pre_level_0'] = level0_prop
            item_stats['pre_level_1'] = level1_prop
            item_stats['pre_level_2'] = level2_prop
            item_stats['pre_level_3'] = level3_prop
            item_stats['pre_level_4'] = level4_prop
            item_stats['pre_level_5'] = level5_prop
            item_stats['pre_level_6'] = level6_prop
            statis_list.append(item_stats)
        return statis_list

    except Exception as e:

        print('error is {}'.format(e))
        return 0
    finally:
        del dataset


def cape_static(tiffsrc, shpsrc):
    pre_tif = '/vsimem/cape_tiff.tif'
    pre_shp = '/vsimem/statis_shp.shp'
    # pre_shp=r'G:\data\CLDAS\sh.shp'
    Convert_Coor(tiffsrc, pre_tif)
    Convert_Coor_with_SHP(shpsrc, pre_shp)
    print("start statis")
    try:
        dataset: gdal.Dataset = gdal.Open(pre_tif)
        geotrans = dataset.GetGeoTransform()
        res_x = abs(geotrans[1])
        res_y = abs(geotrans[5])
        pixel_area = res_x * res_y / (1000 * 1000)
        result_statis = zonal_stats(pre_shp, pre_tif, add_stats={
            'cape_count': stat_func_cape}, geojson_out=True)
        statis_list = []
        for st in result_statis:
            item_stats = dict()

            propert = st['properties']
            cape_count = propert['cape_count']
            sum_count = propert['count']

            cape_mean = propert['mean']
            cape_max = propert['max']

            region = propert['名称']
            cape_low_risk = cape_count[0]
            cape_high_risk = cape_count[1]
            cape_low_risk_prop = cape_low_risk / sum_count
            cape_high_risk_prop = cape_high_risk / sum_count

            # 写入
            item_stats['region'] = region
            item_stats['cape_mean'] = cape_mean
            item_stats['cape_max'] = cape_max
            item_stats['cape_low_risk_prop'] = cape_low_risk_prop
            item_stats['cape_high_risk_prop'] = cape_high_risk_prop
            print(sum_count)
            print(cape_count)
            statis_list.append(item_stats)
        return statis_list
    except Exception as e:
        print("error is {}".format(e))

    finally:
        del dataset

def wins_static(tiffsrc, shpsrc):
    wins_tif = '/vsimem/pre_tiff.tif'
    wins_shp = '/vsimem/statis_shp.shp'
    # pre_shp=r'G:\data\CLDAS\sh.shp'
    Convert_Coor(tiffsrc, wins_tif)
    Convert_Coor_with_SHP(shpsrc, wins_shp)
    print("start statis")
    try:
        dataset: gdal.Dataset = gdal.Open(wins_tif)
        geotrans = dataset.GetGeoTransform()
        res_x = abs(geotrans[1])
        res_y = abs(geotrans[5])
        pixel_area = res_x * res_y / (1000 * 1000)
        result_statis = zonal_stats(wins_shp, wins_tif, add_stats={
            'pre_count': stat_func_wins}, geojson_out=True)
        statis_list = []
        for st in result_statis:
            item_stats = dict()

            propert = st['properties']
            wins_count = propert['pre_count']
            sum_count = propert['count']

            wins_mean = propert['mean']
            wins_max = propert['max']

            region = propert['名称']
            print(sum_count)
            print(wins_count)

            level0_count = wins_count[0]
            level1_count = wins_count[1]
            level2_count = wins_count[2]
            level3_count = wins_count[3]
            level4_count = wins_count[4]
            level5_count = wins_count[5]
            level6_count = wins_count[6]
            level7_count = wins_count[7]
            level8_count = wins_count[8]
            level9_count = wins_count[9]

            sum_area = sum_count * pixel_area
            level0_prop = level0_count / sum_count  # level0 占比
            level1_prop = level1_count / sum_count  # level1 占比
            level2_prop = level2_count / sum_count  # level2 占比
            level3_prop = level3_count / sum_count  # level3 占比
            level4_prop = level4_count / sum_count  # level4 占比
            level5_prop = level5_count / sum_count  # level5 占比
            level6_prop = level6_count / sum_count  # level6 占比
            level7_prop = level7_count / sum_count  # level7 占比
            level8_prop = level8_count / sum_count  # level8 占比
            level9_prop = level9_count / sum_count  # level9 占比



            # 收集全部信息
            item_stats['region'] = region
            item_stats['wins_mean'] = wins_mean
            item_stats['wins_max'] = wins_max
            item_stats['wins_level_0'] = level0_prop
            item_stats['wins_level_1'] = level1_prop
            item_stats['wins_level_2'] = level2_prop
            item_stats['wins_level_3'] = level3_prop
            item_stats['wins_level_4'] = level4_prop
            item_stats['wins_level_5'] = level5_prop
            item_stats['wins_level_6'] = level6_prop
            item_stats['wins_level_7']=level7_prop
            item_stats['wins_level_8'] = level8_prop
            item_stats['wins_level_9'] = level9_prop
            statis_list.append(item_stats)
        return statis_list

    except Exception as e:

        print('error is {}'.format(e))
        return 0
    finally:
        del dataset


def statis_merge(pre_tif,wins_tif,cape_tif,shpfile,forecast_type,region_level,forecast_step,
                 forecast_imminent_tag,forecast_cycle_utc,forecast_report_time,forecast_time_str,forecast_figure_timestr):
    '''
    #,forecast_type,region_level,forecast_step,fore_cast_imminent_tag,forecast_cycle_utc,forecast_report_time
    :param pre_tif:
    :param wins_tif:
    :param cape_tif:
    :param shpfile:
    :param forecast_type:
    :param region_level:
    :param forecast_step:
    :param fore_cast_imminent_tag:
    :param forecast_cycle_utc:
    :param forecast_report_time:
    :return:
    '''
    if forecast_step==3:
        pre_func=stat_func_pre_3
    elif forecast_step==24:
        pre_func=stat_func_pre_24
    else:
        pre_func=stat_func_pre_24
    pre_stat=pre_static(pre_tif,shpfile,pre_func)
    cape_stat=cape_static(cape_tif,shpfile)
    wins_stat=wins_static(wins_tif,shpfile)

    pre_df=pd.DataFrame(pre_stat)
    cape_df=pd.DataFrame(cape_stat)
    wins_df=pd.DataFrame(wins_stat)

    merge_df1=pd.merge(pre_df,cape_df,how='inner',on='region')
    merge_df2=pd.merge(merge_df1,wins_df,how='inner',on='region')

    merge_df2['forecast_type']=forecast_type  #预报类型
    merge_df2['region_level']=region_level   #区域level 省级是1,省级部分是2,地级市3,地级市部分4,县区5
    merge_df2['forecast_step'] = forecast_step  #预报步长
    merge_df2['forecast_imminent_tag']=forecast_imminent_tag  #短临标记
    merge_df2['forecast_cycle_utc']=forecast_cycle_utc   #预报周期UTC
    merge_df2['forecast_report_time']=forecast_report_time #预报时间
    merge_df2['forecast_timestr']=forecast_time_str  #预报时段
    merge_df2['forecast_figure_timestr']=forecast_figure_timestr #每一张图的预报时段
    return merge_df2




