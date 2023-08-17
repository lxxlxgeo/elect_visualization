from osgeo import gdal,osr

def write_tiff(outfile,data,extents):
    im_height, im_width = data.shape

    res = round((extents[1] - extents[0]) / im_width, 4)
    driver=gdal.GetDriverByName('GTiff')
    #out_tif_name=os.path.join(out_dir,str(year)+str(month).zfill(2)+'_XCO2_average.tif')
    target_tif_name=outfile

    out_tif=driver.Create(target_tif_name,im_width,im_height,1,gdal.GDT_Float32)
    #设置影像显示区域
    LonMin,LatMax=extents[0],extents[3]
    geotransform=(LonMin,res,0,LatMax,0,-res)
    out_tif.SetGeoTransform(geotransform)
    ##设置地理信息，选取所需的坐标系统
    srs=osr.SpatialReference()
    srs.ImportFromEPSG(4326)#定义输出的坐标为WGS84，Authority['EPSG','4326']
    out_tif.SetProjection(srs.ExportToWkt())#新建图层投影
    #数据写出
    out_tif.GetRasterBand(1).WriteArray(data)#数据写入内存，此时未写入硬盘
    out_tif.FlushCache()#数据写入硬盘
    out_tif=None##关闭tif文件bu





