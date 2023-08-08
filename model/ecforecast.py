# -*- coding: utf-8 -*-
"""
Created on 2023/7/13 17:54

@author: lixiang
"""
from .Base import Base
from sqlalchemy import Column,VARCHAR,BIGINT,DATETIME,FLOAT,INT,PrimaryKeyConstraint

class Forecast_Product_Info(Base):
    '''
    预报结果集成自动化
    '''

    __tablename__='forecast_product_info'

    #自增id
    id=Column(BIGINT,unique=True,autoincrement=True)

    #预报类型:分短临,短期,中期
    #这里有三个 imminent,short-term,medium-term
    #pk
    forecast_type=Column(VARCHAR(50),doc="预报类型",comment="预报的类型,是短临还是短期，中期")

    #统计区域的级别,分省级和市级，省级包括 黑龙江中部，黑龙江南部 等，市级包括 哈尔滨中部，哈尔滨南部等
    #pk
    region_level=Column(VARCHAR(50),doc="出图的区域级别,省级和市级",comment="出图的区域级别")

    #区域
    #包括 省级的包括黑龙江中部，南部等， 市级的包括 各个地级市的东西南北
    #pk
    region=Column(VARCHAR(50),doc="出图的区域,省级和市级",comment="出图的区域")

    #预报步长包括 3小时,24小时,1小时，其中短临的有两种情况:
    #pk
    forecast_step=Column(VARCHAR(50),doc="预报的步长",comment="预报步长")

    #短临小时气象要素标识，这里如果不是短临小时气象要素，则标记为0，如果是，则标记为1
    #报告类型 短临 1，短期 2 ，中期 3
    #pk
    forecast_imminent_tag=Column(INT,doc="短临小时气象标注",comment="短临小时气象要素标注")
    #初始场时间
    forecast_cycle_utc=Column(DATETIME,doc="EC预报文件夹,或者初始场的时间",comment="EC预报文件夹,或者初始场")
    #发报时间 第一报时间
    #pk
    forecast_report_time=Column(DATETIME,doc="发报时间",comment="发报时间")

    #发报时间
    forecast_timestr=Column(VARCHAR(100),doc="预报的时段,比如 2023080420_2023080520",comment="预报的时段")

    #预报时段
    forecast_figure_timestr=Column(VARCHAR(100),doc="图的时段 ",comment="预报时段,每一张图")

    #统计要素

    #统计区域的面积
    area=Column(FLOAT,doc="统计区域面积",comment="统计区域面积")

    #统计区域的最大值
    pre_max=Column(FLOAT,doc="降水最大值",comment="降水最大值")

    #统计区域的平均值
    pre_avg=Column(FLOAT,doc="降水平均值",comment="降水平均值")

    #风速
    #风速最大值
    wind_max=Column(FLOAT,doc="风速最大值",comment="风速最大值")

    #风速平均值
    wind_avg=Column(FLOAT,doc="风速平均值",comment="风速平均值")

    #风速最小值
    wind_min=Column(FLOAT,doc="风速最小值",comment="风速最小值")

    #雷电,位能最大值
    cape_max=Column(FLOAT,doc="位能最大值",comment='位能最大值')
    #位能平均值
    cape_avg=Column(FLOAT,doc="位能平均值",comment="位能平均值")

    #降水量
    #
    forecast_exec_time=Column(DATETIME,doc="执行时间",comment="执行时间")

    #定义主键
    __table_args__=(
        PrimaryKeyConstraint('forecast_type','region_level','region','forecast_step','forecast_imminent_tag','forecast_cycle_utc','forecast_report_time','forecast_figure_timestr'),
    )




