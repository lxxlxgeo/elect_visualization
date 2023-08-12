# -*- coding: utf-8 -*-
"""
Created on 2023/8/12 3:08

@author: lxce
"""
import numpy as np
####CLDAS 配置
cldas_path=r'H:\forecast_server\heilongjiang\CLDAS\data\raw'
#CLDAS的经纬度范围
extent=[120.0,135.5,42.0,55.0]

output_prefix=r'H:\forecast_server\heilongjiang\CLDAS\figureout'

def generate_color_conf():
    pre_mid_level=[0, 0.1, 10, 25, 50, 100, 250, 500]  #短期或中期降水量拉伸
    pre_mid_ticks=[0.1,10,25,50,100,250]               #短期或中期降水刻度
    cape_mid_level=np.arange(200, 4001, 200)           #短期或中期位能拉伸
    wins_mid_level=np.arange(0, 35, 2)  #短期或中期风速拉伸

    pre_imminent_level=[0,0.1,1,3,10,20,50,70] #短临降水拉伸
    pre_imminent_ticks=[0.1,1,3,10,20,50]  #短临降水颜色条刻度
    cape_imminent_level=np.arange(200,4001,200) #短临位能拉伸
    wins_imminent_level=np.arange(0,35,2)  #短临风速拉伸


    mid_short_color_conf=dict()
    mid_short_color_conf['pre_level']=pre_mid_level
    mid_short_color_conf['pre_ticks']=pre_mid_ticks
    mid_short_color_conf['cape_level']=cape_mid_level
    mid_short_color_conf['wins_level']=wins_mid_level

    imminent_color_conf=dict()
    imminent_color_conf['pre_level']=pre_imminent_level
    imminent_color_conf['pre_ticks']=pre_imminent_ticks
    imminent_color_conf['cape_level']=cape_imminent_level
    imminent_color_conf['wins_level']=wins_imminent_level
    return mid_short_color_conf,imminent_color_conf