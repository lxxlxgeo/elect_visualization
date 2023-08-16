# -*- coding: utf-8 -*-
"""
Created on 2023/8/14 5:44

@author: lxce
"""
#%%
from RLDAS_self.cldas_plot import Plotter
from RLDAS_self.RLdas_Read import RlDas_Reader
import datetime
from un_config.rldas_configl import generate_plot_config,map_extent,output_prefix
import os
import cmaps

def exec_mid_run(start_time:datetime.datetime,end_time:datetime.datetime,step:int):
    """

    :param start_time: 预报开始的时间
    :param end_time: 预报结束的时间
    :param step: 预报步长
    :return:
    """
    # 初始化数据读取库
    RLDAS_Data_Reader = RlDas_Reader(start_time,end_time,step)

    # 获取降水量变量
    pre_data_list = RLDAS_Data_Reader.get_data('pre')

    # 获取位能变量
    cape_data_list = RLDAS_Data_Reader.get_data('')

    # 获取风速变量
    wins_data_list = RLDAS_Data_Reader.get_data('')

    lon,lat,proj = RLDAS_Data_Reader.__get__init_field_info__() #获取初始场信息,如投影,经纬度等

    color_conf = generate_plot_config(step)    # 根据步长获取颜色表等参数
    if step==3:
        forecast_type = "imm"
    elif step==24:
        forecast_type = 'mid'
    else:
        forecast_type = "others"

    """
    降水量预报
    """
    for pre_item in pre_data_list:
        # 数据产品
        pre_data=pre_item['data']
        forecast_start_time=pre_item['forecast_start_time']
        forecast_end_time=pre_item['forecast_end_time']
        forecast_start_time_str=forecast_start_time.strftime('%m月%d日%H时')
        forecast_end_time_str=forecast_end_time.strftime('%m月%d日%H时')
        # 绘制降水量预报
        pre_ploter = Plotter(
            variable_name='pre',
            variables=['pre', 'wins','cape'],
            ticks=color_conf['pre_ticks'],
            forecast_path_str=start_time_str,
            data_extent=data_extent,
            map_extent=map_extent,
            proj=proj,
            forecast_type=forecast_type
        )

        #降水量颜色表
        color = ("#FFFFFF", "#A6F28F", "#3DBA3D", "#61BBFF", "#0000FF", "#FA00FA", "#800040")

        # 标题
        titles = f"{forecast_start_time_str}-{forecast_end_time_str}黑龙江省降水量预报"

        # 文件名
        filename = f"{forecast_start_time.strftime('%Y%m%d%H')}_{forecast_end_time.strftime('%Y%m%d%H')}_heilongjiang_pre_" + '.png'
        out_file = pre_ploter.get_output_file_path('pre', 1, output_prefix, filename)
        subdirectories = pre_ploter.create_subdirectories(output_prefix)
        for subdirectory in subdirectories.values():
            os.makedirs(subdirectory, exist_ok=True)
        pre_ploter.plot_contour_map(
            lat,
            lon,
            pre_data,
            "降水量/$mm$",
            levels=mid_term['pre_level'],
            colormap=color,
            title=titles,
            output_file=out_file,
            tips="colors",
            draw_river=True
        )
        del titles, out_file



    """
    风速预报出图
    """
    for wins_item in wins_data_list:
        # 数据产品
        wins_data=wins_item['data']

        forecast_start_time=wins_item['forecast_start_time']
        forecast_end_time=wins_item['forecast_end_time']

        forecast_start_time_str=forecast_start_time.strftime('%m月%d日%H时')
        forecast_end_time_str=forecast_end_time.strftime('%m月%d日%H时')
        # 降水变量绘图
        pre_ploter = Plotter(
            variable_name='wins',
            variables=['pre','wins','cape'],
            ticks=color_conf['pre_ticks'],
            forecast_path_str=start_time_str,
            data_extent=data_extent,
            map_extent=map_extent,
            proj=proj,
            forecast_type=forecast_type
        )

        #降水量颜色表
        color = ("#FFFFFF", "#A6F28F", "#3DBA3D", "#61BBFF", "#0000FF", "#FA00FA", "#800040")

        # 标题
        titles = f"{forecast_start_time_str}-{forecast_end_time_str}黑龙江省对流预报"

        # 文件名
        filename = f"{forecast_start_time.strftime('%Y%m%d%H')}_{forecast_end_time.strftime('%Y%m%d%H')}_heilongjiang_pre_" + '.png'
        out_file = pre_ploter.get_output_file_path('cape', 1, output_prefix, filename)
        subdirectories = pre_ploter.create_subdirectories(output_prefix)
        for subdirectory in subdirectories.values():
            os.makedirs(subdirectory, exist_ok=True)
        pre_ploter.plot_contour_map(
            lat,
            lon,
            wins_data,
            "风速/$m/s$",
            levels=mid_term['wins_level'],
            colormap=cmaps.wind_17lev,
            title=titles,
            output_file=out_file,
            tips="colors",
            draw_river=True
        )
        del titles, out_file


    """
    位能预报出图
    """
    for cape_item in cape_data_list:

        # 数据产品
        data=cape_item['data']
        forecast_start_time=cape_item['forecast_start_time']
        forecast_end_time=cape_item['forecast_end_time']

        forecast_start_time_str=forecast_start_time.strftime('%m月%d日%H时')
        forecast_end_time_str=forecast_end_time.strftime('%m月%d日%H时')
        # 降水变量绘图
        pre_ploter = Plotter(
            variable_name='wins',
            variables=['pre','wins','cape'],
            ticks=None,
            forecast_path_str=start_time_str,
            data_extent=data_extent,
            map_extent=map_extent,
            proj=proj,
            forecast_type=forecast_type
        )


        # 标题
        titles = f"{forecast_start_time_str}-{forecast_end_time_str}黑龙江省降水量预报"

        # 文件名
        filename = f"{forecast_start_time.strftime('%Y%m%d%H')}_{forecast_end_time.strftime('%Y%m%d%H')}_heilongjiang_pre_" + '.png'
        out_file = pre_ploter.get_output_file_path('pre', 1, output_prefix, filename)
        subdirectories = pre_ploter.create_subdirectories(output_prefix)
        for subdirectory in subdirectories.values():
            os.makedirs(subdirectory, exist_ok=True)
        pre_ploter.plot_contour_map(
            lat,
            lon,
            data,
            "降水量/$mm$",
            levels=mid_term['pre_level'],
            colormap=color,
            title=titles,
            output_file=out_file,
            tips="colors",
            draw_river=True
        )
        del titles, out_file





















# %%
if __name__=='__main__':
    #%%
    mid_term,imm_term=generate_plot_config(3)
    start_time=datetime.datetime(2023,8,14,8)
    end_time=datetime.datetime(2023,8,17,8)
    step=24
    #读取降水变量
    CLDAS_Data_Reader=RlDas_Reader(start_time,end_time,step)
    pre_data_list=CLDAS_Data_Reader.get_data('pre')
    lon,lat,proj=CLDAS_Data_Reader.__get__init_field_info__()
    data_extent=CLDAS_Data_Reader.data_extent
    #wind_data_list=CLDAS_Data_Reader.get_data('WIN','WIND','max')

    start_time_str=start_time.strftime('%Y%m%d%H')
    # 降水变量绘图
    pre_ploter = Plotter(
        variable_name='pre',
        variables=['pre', 'wins'],
        ticks=mid_term['pre_ticks'],
        forecast_path_str=start_time_str,
        data_extent=data_extent,
        map_extent=map_extent,
        proj=proj,
        forecast_type='fourdayd2'
    )
    color = ("#FFFFFF", "#A6F28F", "#3DBA3D", "#61BBFF", "#0000FF", "#FA00FA", "#800040")
    titles = f"{forecast_start_time_str}-{forecast_end_time_str}黑龙江省降水量预报"
    filename = f"{forecast_start_time.strftime('%Y%m%d%H')}_{forecast_end_time.strftime('%Y%m%d%H')}_heilongjiang_pre_scene" + '.png'
    out_file = pre_ploter.get_output_file_path('pre', 1, output_prefix, filename)
    subdirectories = pre_ploter.create_subdirectories(output_prefix)
    for subdirectory in subdirectories.values():
        os.makedirs(subdirectory, exist_ok=True)
    pre_ploter.plot_contour_map(
        lat,
        lon,
        data,
        "降水量/$mm$",
        levels=mid_term['pre_level'],
        colormap=color,
        title=titles,
        output_file=out_file,
        tips="colors",
        draw_river=True
    )
    del titles, out_file




    #%%

    #绘制降水
    for item in pre_data_list:
        data=item['data']
        forecast_start_time=item['forecast_start_time']
        forecast_end_time=item['forecast_end_time']
        forecast_start_time_str=forecast_start_time.strftime('%m月%d日%H时')
        forecast_end_time_str=forecast_end_time.strftime('%m月%d日%H时')

        #降水变量绘图
        pre_ploter=Plotter(
            variable_name='pre',
            variables=['pre','wins'],
            ticks=mid_term['pre_ticks'],
            forecast_path_str=start_time_str,
            data_extent=data_extent,
            map_extent=map_extent,
            proj=proj,
            forecast_type='fourdayd2'
        )
        color=("#FFFFFF", "#A6F28F", "#3DBA3D", "#61BBFF", "#0000FF", "#FA00FA", "#800040")
        titles=f"{forecast_start_time_str}-{forecast_end_time_str}黑龙江省降水量预报"
        filename = f"{forecast_start_time.strftime('%Y%m%d%H')}_{forecast_end_time.strftime('%Y%m%d%H')}_heilongjiang_pre_scene" + '.png'
        out_file=pre_ploter.get_output_file_path('pre',1,output_prefix,filename)
        subdirectories = pre_ploter.create_subdirectories(output_prefix)
        for subdirectory in subdirectories.values():
            os.makedirs(subdirectory, exist_ok=True)
        pre_ploter.plot_contour_map(
            lat,
            lon,
            data,
            "降水量/$mm$",
            levels=mid_term['pre_level'],
            colormap=color,
            title=titles,
            output_file=out_file,
            tips="colors",
            draw_river=True
        )
        del titles,out_file