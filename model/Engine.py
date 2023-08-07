from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import urllib.parse
import pymysql
'''导入模型'''
#
# from Data_Reader.control_framework_orm.models import Weather_station_his,Weather_station_his_check
#%%
'''
连接字符串

'''


sql_info = {'host': '8.130.174.50',
            'port': '3306',
            'schema': 'heilongjiang_cloud_exhibition',
            'user': 'root',
            'pw': urllib.parse.quote_plus("Tsingtaogiser+1s"),
            'table':'ods_qxsj_dky_tbl_dat_weather_station'}
'''
创建数据库引擎
'''
class Create_Engine(object):
    def __init__(self):
        self.conn=self.conn_to_sql()
    def conn_to_sql(self):
        pymysql.install_as_MySQLdb()
        cmd = f"mysql://{sql_info['user']}:{sql_info['pw']}@{sql_info['host']}:{sql_info['port']}/{sql_info['schema']}"
        engine=create_engine(cmd)
        return engine

def GetEngine():
    Instance=Create_Engine()
    return Instance.conn


def GetSession():
    engine=Create_Engine().conn
    sessionmakers=sessionmaker(bind=engine)
    session=sessionmakers()
    return session
