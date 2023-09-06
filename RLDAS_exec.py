# -*- coding: utf-8 -*-
"""
Created on 2023/8/14 5:44

@author: lxce
"""
import pandas as pd

#%%
from RLDAS_self.cldas_plot import Plotter
from RLDAS_self.RLdas_Read import RlDas_Reader
import datetime
from un_config.rldas_configl import generate_plot_config,map_extent,output_prefix
import os
import cmaps
import argparse

# 入库部分
from statis.write_tiff import convert_source_totiff
from statis.statis_rldas import statis_merge
from un_config.rldas_configl import statis_level_1,statis_level_3,statis_level_5
from model.Engine import GetSession
from model.ecforecast import Forecast_Product_Info

#执行函数
def exec_draw_run(start_time:datetime.datetime,end_time:datetime.datetime,step:int):
    """

    :param start_time: 预报开始的时间
    :param end_time: 预报结束的时间
    :param step: 预报步长
    :return:
    """

    # 计算时长,间隔

    time_length=end_time-start_time
    day_length=time_length.days




    # 初始化数据读取库
    RLDAS_Data_Reader = RlDas_Reader(start_time,end_time,step)

    # 获取降水量变量
    pre_data_list = RLDAS_Data_Reader.get_data('pre')

    # 获取位能变量
    cape_data_list = RLDAS_Data_Reader.get_data('cape_2d')

    # 获取风速变量
    wins_data_list = RLDAS_Data_Reader.get_data('wspd_wdir10')

    lon,lat,proj = RLDAS_Data_Reader.__get__init_field_info__() #获取初始场信息,如投影,经纬度等

    color_conf = generate_plot_config(step)    # 根据步长获取颜色表等参数


    if step==3:
        forecast_type = "imminent"
    elif (step==24)&(day_length==1):
        forecast_type="imminent"
    elif (step==24)&(day_length==3) :
        forecast_type = 'short-term'
    elif (step==24)&(day_length>3):
        forecast_type='medium-term'
    else:
        forecast_type = "others"

    """
    降水量预报
    """
    pre_prefix_list=[]
    for pre_item in pre_data_list:

        pre_stat_dict=dict()
        # 数据产品
        pre_data=pre_item['data']
        forecast_start_time=pre_item['forecast_start_time']
        forecast_end_time=pre_item['forecast_end_time']
        forecast_start_time_str=forecast_start_time.strftime('%m月%d日%H时')
        forecast_end_time_str=forecast_end_time.strftime('%m月%d日%H时')



        # 绘制降水量预报
        pre_ploter = Plotter(
            variable_name='pre',
            variables=['pre', 'wins','cp'],
            ticks=color_conf['pre_ticks'],
            forecast_path_str=start_time.strftime('%Y%m%d%H'),
            data_extent=map_extent,
            map_extent=map_extent,
            proj=proj,
            forecast_type=forecast_type
        )

        #降水量颜色表
        color = ("#FFFFFF", "#A6F28F", "#3DBA3D", "#61BBFF", "#0000FF", "#FA00FA", "#800040")

        # 标题
        titles = f"{forecast_start_time_str}-{forecast_end_time_str}黑龙江省降水量预报图"

        # 文件名
        filename = f"{forecast_start_time.strftime('%m%d%H')}_{forecast_end_time.strftime('%m%d%H')}_heilongjiang_pre_forecast" + '.png'
        pre_tif= f"{forecast_start_time.strftime('%m%d%H')}_{forecast_end_time.strftime('%m%d%H')}_heilongjiang_pre_forecast" + '.tif'
        convert_source_totiff(lon,lat,pre_data,pre_tif)

        out_file = pre_ploter.get_output_file_path('pre', 1, output_prefix, filename)
        subdirectories = pre_ploter.create_subdirectories(output_prefix)
        for subdirectory in subdirectories.values():
            os.makedirs(subdirectory, exist_ok=True)
        pre_ploter.plot_contour_map(
            lat,
            lon,
            pre_data,
            "降水量/$mm$",
            levels=color_conf['pre_level'],
            colormap=color,
            title=titles,
            output_file=out_file,
            tips="colors",
            draw_river=True
        )
        pre_stat_dict['forecast_start_time']=pre_item['forecast_start_time']
        pre_stat_dict['forecast_end_time']=pre_item['forecast_end_time']
        pre_stat_dict['pre_tif']=pre_tif
        pre_prefix_list.append(pre_stat_dict)
        del titles, out_file



    """
    风速预报出图
    """
    wins_prefix_list=[]


    for wins_item in wins_data_list:

        wins_stat_dict=dict()

        # 数据产品
        wins_data=wins_item['data']

        forecast_start_time=wins_item['forecast_start_time']
        forecast_end_time=wins_item['forecast_end_time']

        forecast_start_time_str=forecast_start_time.strftime('%m月%d日%H时')
        forecast_end_time_str=forecast_end_time.strftime('%m月%d日%H时')
        # 降水变量绘图
        pre_ploter = Plotter(
            variable_name='wins',
            variables=['pre','wins','cp'],
            ticks=None,
            forecast_path_str=start_time.strftime("%Y%m%d%H"),
            data_extent=map_extent,
            map_extent=map_extent,
            proj=proj,
            forecast_type=forecast_type
        )
        # 标题
        titles = f"{forecast_start_time_str}-{forecast_end_time_str}黑龙江省地面最大风速预报图"

        # 文件名
        filename = f"{forecast_start_time.strftime('%m%d%H')}_{forecast_end_time.strftime('%m%d%H')}_heilongjiang_wins_forecast" + '.png'
        wins_tif = f"{forecast_start_time.strftime('%m%d%H')}_{forecast_end_time.strftime('%m%d%H')}_heilongjiang_wins_forecast" + '.tif'

        convert_source_totiff(lon,lat,wins_data,wins_tif)

        out_file = pre_ploter.get_output_file_path('wins', 1, output_prefix, filename)
        subdirectories = pre_ploter.create_subdirectories(output_prefix)
        for subdirectory in subdirectories.values():
            os.makedirs(subdirectory, exist_ok=True)
        pre_ploter.plot_contour_map(
            lat,
            lon,
            wins_data,
            "风速/$m/s$",
            levels=color_conf['wins_level'],
            colormap=cmaps.wind_17lev,
            title=titles,
            output_file=out_file,
            tips="cmaps",
            draw_river=True
        )

        wins_stat_dict['forecast_start_time']=wins_item['forecast_start_time']
        wins_stat_dict['forecast_end_time']=wins_item['forecast_end_time']
        wins_stat_dict['wins_tif']=wins_tif
        wins_prefix_list.append(wins_stat_dict)
        del titles, out_file


    """
    位能预报出图
    """

    cape_prefix_list=[]
    for cape_item in cape_data_list:
        cape_stat_dict=dict()

        # 数据产品
        data=cape_item['data']
        forecast_start_time=cape_item['forecast_start_time']
        forecast_end_time=cape_item['forecast_end_time']

        forecast_start_time_str=forecast_start_time.strftime('%m月%d日%H时')
        forecast_end_time_str=forecast_end_time.strftime('%m月%d日%H时')
        # 降水变量绘图
        pre_ploter = Plotter(
            variable_name='cp',
            variables=['pre','wins','cp'],
            ticks=None,
            forecast_path_str=start_time.strftime('%Y%m%d%H'),
            data_extent=map_extent,
            map_extent=map_extent,
            proj=proj,
            forecast_type=forecast_type
        )


        # 标题
        titles = f"{forecast_start_time_str}-{forecast_end_time_str}黑龙江省对流有效位能预报图"

        # 文件名
        filename = f"{forecast_start_time.strftime('%m%d%H')}_{forecast_end_time.strftime('%m%d%H')}_heilongjiang_cp_forecast" + '.png'
        cape_tif= f"{forecast_start_time.strftime('%m%d%H')}_{forecast_end_time.strftime('%m%d%H')}_heilongjiang_cp_forecast" + '.tif'
        convert_source_totiff(lon,lat,data,cape_tif)

        out_file = pre_ploter.get_output_file_path('cp', 1, output_prefix, filename)
        subdirectories = pre_ploter.create_subdirectories(output_prefix)
        for subdirectory in subdirectories.values():
            os.makedirs(subdirectory, exist_ok=True)
        pre_ploter.plot_contour_map(
            lat,
            lon,
            data,
            "对流有效位能/$J/kg$",
            levels=color_conf['cape_level'],
            colormap=cmaps.WhBlGrYeRe,
            title=titles,
            output_file=out_file,
            tips="cmaps",
            draw_river=True
        )
        cape_stat_dict['forecast_start_time']=cape_item['forecast_start_time']
        cape_stat_dict['forecast_end_time']=cape_item['forecast_end_time']
        cape_stat_dict['wins_tif']=cape_tif
        cape_prefix_list.append(cape_stat_dict)
        del titles, out_file

    for i in range(len(pre_prefix_list)):

        forecast_start_time_stat = pre_prefix_list[i]['forecast_start_time']
        forecast_end_time_stat = pre_prefix_list[i]['forecast_end_time']


        pre_stat_tif=pre_prefix_list[i]['pre_tif']
        wins_stat_tif=wins_prefix_list[i]['wins_tif']
        cape_stat_tif=cape_prefix_list[i]['cape_tif']
        forecast_utc_time=start_time+datetime.timedelta(hours=-8)
        forecast_time_str_report=start_time.strftime('%Y%m%d%H')+end_time.strftime('%Y%m%d%H')
        forecast_figure_str=forecast_start_time_stat.strftime('%Y%m%d%H')+forecast_end_time_stat.strftime('%Y%m%d%H')

        df_level1_out=statis_merge(pre_stat_tif,wins_stat_tif,cape_stat_tif,statis_level_1,forecast_type,1,step,
                                   0,forecast_utc_time,start_time,forecast_time_str_report,
                                   forecast_figure_str)
        df_level3_out=statis_merge(pre_stat_tif,wins_stat_tif,cape_stat_tif,statis_level_3,forecast_type,3,step,
                                   0,forecast_utc_time,start_time,forecast_time_str_report,
                                   forecast_figure_str)
        df_level5_out=statis_merge(pre_stat_tif,wins_stat_tif,cape_stat_tif,statis_level_5,forecast_type,5,step,
                                   0,forecast_utc_time,start_time,forecast_time_str_report,
                                   forecast_figure_str)
        commit_database(df_level1_out)
        commit_database(df_level3_out)
        commit_database(df_level5_out)






def commit_database(out_df:pd.DataFrame):
    Session=GetSession()
    for item in out_df:
        entity=Forecast_Product_Info(
            forecast_type=item.forecast_type,region_level=item.region_level,region=item.region,
            forecast_step=item.forecast_step,forecast_imminent_tag=item.forecast_imminent_tag,
            forecast_cycle_utc=item.forecast_cycle_utc,forecast_report_time=item.forecast_report_time,
            forecast_timestr=item.forecast_time_str,forecast_figure_timestr=item.forecast_figure_timestr,
            area=item.area,pre_max=item.pre_max,pre_avg=item.pre_mean,wind_max=item.wins_max,wind_avg=item.wins_mean,
            cape_max=item.cape_max,cape_avg=item.cape_mean,
            pre_level_0=item.pre_level_0,
            pre_level_1=item.pre_level_1,pre_level_2=item.pre_level_2,pre_level_3=item.pre_level_3,
            pre_level_4=item.pre_level_4,pre_level_5=item.pre_level_5,pre_level_6=item.pre_level_6,
            cape_low_risk=item.cape_low_risk,cape_high_risk=item.cape_high_risk,
            wins_level0=item.wins_level_0,wins_level1=item.wins_level_1,wins_level2=item.wins_level_2,
            wins_level3=item.wins_level_3,wins_level4=item.wins_level_4,wins_level5=item.wins_level_5,
            wins_level6=item.wins_level_6,wins_level7=item.wins_level_7,wins_level8=item.wins_level_8,
            wins_level9=item.wins_level_9,
            forecast_exec_time=datetime.datetime.utcnow()+datetime.timedelta(hours=8)
        )
        Session.merge(entity)

    Session.commit()
    print("入库成功")

    Session.close()















def convert_time_imm(hour,d_day,d_date):
    now_time=datetime.datetime.utcnow()+datetime.timedelta(hours=8)+datetime.timedelta(days=d_date)
    year=now_time.year
    month=now_time.month
    day=now_time.day
    hour=hour
    exec_start_time=datetime.datetime(year,month,day,hour)  #确定的执行时间
    exec_end_time=exec_start_time+datetime.timedelta(days=d_day)
    return exec_start_time,exec_end_time







# %%
if __name__=='__main__':
    #%%
    parser = argparse.ArgumentParser(description='RLDAS 渲染主程序')
    parser.add_argument('--runmodel','-m',help=' runmodel 为运行模式,分别为 自动或者手动',default='auto')
    parser.add_argument('--start_time','-s',help="手动运行程序的开始时间,为一字符串的形式",default=None)
    parser.add_argument('--hour','-t',help="自动运行所需要提供的运行小时,比如5时,8时,11时,14时等",default=8)
    parser.add_argument('--d_day','-d',help="自动运行所需要提供的间隔时间,默认为1天",default=1)
    parser.add_argument('--step','-p',help="自动运行所需要提供的步长",default=3)
    parser.add_argument('--d_date','-dt',help="当天的数据运行第二天的数据",default=0)
    args=parser.parse_args()
    run_model=args.runmodel

    #run_mdoel
    if run_model=='auto':
        run_hour=int(args.hour)
        run_d_day=int(args.d_day)
        run_step=int(args.step)
        d_date=int(args.d_date)
        start_time,end_time=convert_time_imm(hour=run_hour,d_day=run_d_day,d_date=d_date)
        time_now=datetime.datetime.utcnow()+datetime.timedelta(hours=8)
        now_hours=time_now.hour
        
        exec_draw_run(start_time,end_time,run_step)

    '''
    运行方式  RLDAS_exec.py -t 8 -d 1 -p 3 为当前时刻 出短临的 8时
    '''

    #start_time = datetime.datetime(2023, 8, 28, 11)
    # start_time=datetime.datetime(2023,8,28,11)
    # end_time=datetime.datetime(2023,8,29,11)
    # step=3
    # #
    # exec_draw_run(start_time,end_time,24)

    
    #exec_draw_run()
    