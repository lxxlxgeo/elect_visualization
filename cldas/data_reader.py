# -*- coding: utf-8 -*-
"""
Created on 2023/8/12 2:59

@author: lxce
"""
import h5py
import xarray as xr
from un_config.cldas_config import cldas_path
class Cldas_Reader(object):
    def __int__(self):
        self.filepath = cldas_path


