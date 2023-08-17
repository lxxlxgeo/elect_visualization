# %%
import datetime

import numpy as np

# 目的,windows 测试错误
# import locale
# locale.setlocale (locale.LC_CTYPE, 'Chinese')


'''
数据显示范围
'''
latS = 42.0
latN = 55.0
lonL = 120.0
lonR = 135.5

# 读取数据的变量

mid_variable_name = [
    "Convective available potential energy",
    "Total precipitation",
    # "10 metre wind gust in the last 3 hours",
    '10 metre wind gust in the last 6 hours'
]

imminent_variable_name = [
    "Convective available potential energy",
    "Total precipitation",
    "10 metre wind gust in the last 3 hours"
    # '10 metre wind gust in the last 6 hours'
]

# 变量名，用于提取数据
variable_name_Zh = ["对流有效位能", "降水量", "最大风速"]  # 出图时使用
variabale_name_english_sort = ['cp', 'pre', 'wins']  # 创建文件夹时使用

'''
颜色表,颜色表刻度配置
'''


def generate_color_conf():
    pre_mid_level = [0, 0.1, 10, 25, 50, 100, 250, 500]  # 短期或中期降水量拉伸
    pre_mid_ticks = [0.1, 10, 25, 50, 100, 250]  # 短期或中期降水刻度
    cape_mid_level = np.arange(200, 4401, 200)  # 短期或中期位能拉伸
    wins_mid_level = np.arange(0, 35, 2)  # 短期或中期风速拉伸

    pre_imminent_level = [0, 0.1, 1, 3, 10, 20, 50, 70]  # 短临降水拉伸
    pre_imminent_ticks = [0.1, 1, 3, 10, 20, 50]  # 短临降水颜色条刻度
    cape_imminent_level = np.arange(200, 4401, 200)  # 短临位能拉伸
    wins_imminent_level = np.arange(0, 35, 2)  # 短临风速拉伸

    mid_short_color_conf = dict()
    mid_short_color_conf['pre_level'] = pre_mid_level
    mid_short_color_conf['pre_ticks'] = pre_mid_ticks
    mid_short_color_conf['cape_level'] = cape_mid_level
    mid_short_color_conf['wins_level'] = wins_mid_level

    imminent_color_conf = dict()
    imminent_color_conf['pre_level'] = pre_imminent_level
    imminent_color_conf['pre_ticks'] = pre_imminent_ticks
    imminent_color_conf['cape_level'] = cape_imminent_level
    imminent_color_conf['wins_level'] = wins_imminent_level
    return mid_short_color_conf, imminent_color_conf


'''
颜色表,颜色表刻度配置结束
'''

# 数据文件路径
'''
数据源路径
'''

# fpath='G:/js_elect/ECFile/ecode'

# 数据存放路径
fpath = '/share/Datasets/ECMWF/C1D-grib'
# 数据输出路径
output_prefix = '/share/data/pic_heilongjiang/production'

# 将当前时间获,并转换为触发时间
'''
执行时间转换程序，目的是在不改动原有代码的情况下，时间转换为程序启动时间
'''
# 数据转换为北京时间
# 这段时间是出 20-20,08-08 的图
current_time = datetime.datetime.utcnow() + datetime.timedelta(hours=8)


# 修改时间
def convert_BTJ(current_time):
    # current_time=datetime.datetime(2023,7,31,20)
    # current_time=datetime.datetime.utcnow()+datetime.timedelta(hours=8)
    year = current_time.year
    month = current_time.month
    day = current_time.day
    hour = current_time.hour
    if hour >= 4 and hour < 16:
        # utc 12时
        return datetime.datetime(year, month, day, 5) + datetime.timedelta(days=-1)
    elif hour >= 0 and hour < 4:
        return datetime.datetime(year, month, day, 17) + datetime.timedelta(days=-1)
    elif hour >= 16:
        return datetime.datetime(year, month, day, 17)


# 第一次出05是和11 时的数据:
# 第二次出17时和23 时的数据
def convert_BTJ_imminent_05f(current_time):
    # current_time=datetime.datetime(2023,7,31,20)
    # current_time=datetime.datetime.utcnow()+datetime.timedelta(hours=8)
    year = current_time.year
    month = current_time.month
    day = current_time.day
    hour = current_time.hour
    if hour >= 4 and hour < 16:
        return datetime.datetime(year, month, day, 5) + datetime.timedelta(days=-1)
    elif hour >= 0 and hour < 4:
        return datetime.datetime(year, month, day, 17) + datetime.timedelta(days=-1)
    elif hour >= 16:
        return datetime.datetime(year, month, day, 17)


def convert_BTJ_imminent_11f(current_time):
    # current_time=datetime.datetime(2023,7,31,20)
    # current_time=datetime.datetime.utcnow()+datetime.timedelta(hours=8)
    year = current_time.year
    month = current_time.month
    day = current_time.day
    hour = current_time.hour
    print("小时 " + str(hour))
    if hour >= 4 and hour < 16:
        print("ok dasy")
        return datetime.datetime(year, month, day, 11) + datetime.timedelta(days=-1)
    elif hour >= 0 and hour < 4:
        # prin
        return datetime.datetime(year, month, day, 23) + datetime.timedelta(days=-1)
    elif hour >= 16:
        # print("okis")
        return datetime.datetime(year, month, day, 23)


def convert_BTJ_imminent_22f(current_time):
    # current_time=datetime.datetime(2023,7,31,20)
    # current_time=datetime.datetime.utcnow()+datetime.timedelta(hours=8)
    year = current_time.year
    month = current_time.month
    day = current_time.day
    hour = current_time.hour
    print("小时 " + str(hour))

    return datetime.datetime(year, month, day, 22)


def convert_BTJ_imminent_16f(current_time):
    # current_time=datetime.datetime(2023,7,31,20)
    # current_time=datetime.datetime.utcnow()+datetime.timedelta(hours=8)
    year = current_time.year
    month = current_time.month
    day = current_time.day
    hour = current_time.hour
    print("小时 " + str(hour))

    return datetime.datetime(year, month, day, 15) + datetime.timedelta(days=-1)


# 20时的短临图片
# 这个时间段出20 和凌晨 2点的数据
# 第一次出 20点和02点的数据 下午 下午16:40 运行
# 第二次出 08 点和14 点的数据 早上 4：50 运行

# 第一次运行
def convert_BTJ_imminent_20f(current_time):
    # current_time=datetime.datetime(2023,8,3,8)
    # current_time=datetime.datetime(2023,7,31,20)
    # current_time=datetime.datetime.utcnow()+datetime.timedelta(hours=8)
    year = current_time.year
    month = current_time.month
    day = current_time.day
    hour = current_time.hour
    if hour >= 4 and hour < 16:
        # utc 12时
        return datetime.datetime(year, month, day, 2) + datetime.timedelta(days=-1)
    elif hour >= 0 and hour < 4:
        return datetime.datetime(year, month, day, 8) + datetime.timedelta(days=-1)
    elif hour >= 16:
        return datetime.datetime(year, month, day, 8)


def convert_BTJ_imminent_02f(current_time):
    # current_time=datetime.datetime(2023,8,3,8)
    # current_time=datetime.datetime.utcnow()+datetime.timedelta(hours=8)
    year = current_time.year
    month = current_time.month
    day = current_time.day
    hour = current_time.hour
    if hour >= 4 and hour < 16:
        # utc 12时
        return datetime.datetime(year, month, day, 20) + datetime.timedelta(days=-1)
    elif hour >= 0 and hour < 4:
        return datetime.datetime(year, month, day, 14) + datetime.timedelta(days=-1)
    elif hour >= 16:
        return datetime.datetime(year, month, day, 14)


def convert_BTJ_20(current_time):
    # current_time=datetime.datetime.utcnow()+datetime.timedelta(hours=8)
    year = current_time.year
    month = current_time.month
    day = current_time.day
    hour = current_time.hour
    if hour >= 4 and hour < 16:
        # utc 12时
        return datetime.datetime(year, month, day, 20) + datetime.timedelta(days=-1)
    elif hour >= 0 and hour < 4:
        return datetime.datetime(year, month, day, 20) + datetime.timedelta(days=-1)
    elif hour >= 16:
        return datetime.datetime(year, month, day, 20)

    # [16:0]-[0:4]


# def convert_BTJ_imminent11():
#     current_time=datetime.datetime.utcnow()+datetime.timedelta(hours=8)
#     year=current_time.year
#     month=current_time.month
#     day=current_time.day
#     hour=current_time.hour
#     #if hour>=4 and hour<16:
#     return datetime.datetime(year,month,day,11)+datetime.timedelta(days=-1)

# path:
# def convert_BTJ_Test(testtime):
#     current_time=testtime
#     #current_time=datetime.datetime.utcnow()+datetime.timedelta(hours=8)
#     year=current_time.year
#     month=current_time.month
#     day=current_time.day
#     hour=current_time.hour
#     if hour==4:
#         return datetime.datetime(year,month,day,11)+datetime.timedelta(days=-1)
#     elif hour==16:
#         return datetime.datetime(year,month,day,5)+datetime.timedelta(days=-1)

'''
备注:UTC12 运行时段 前一天4:00 
'''

# %%
