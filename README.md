<p>从NASA网站上下载了2018的nc数据，由于跨了170小时，数据量较大，<p/>
<p>可以先下载panoply查看数据中的详细信息再写程序，https://www.giss.nasa.gov/tools/panoply/，<p/>
<p>本文件用netCDF4将nc文件转为了shp，然后通过arcpy把得到的feature分等级转为mxd（设置了每个图层的显示的比例尺范围）<p/>
<p>时间的转化看panoply的描述。<p/>
