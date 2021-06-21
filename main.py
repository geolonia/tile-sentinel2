import os
from sentinelsat import SentinelAPI, read_geojson, geojson_to_wkt 
import matplotlib.pyplot as plt
from shapely.geometry import MultiPolygon, Polygon
import rasterio as rio
from rasterio.plot import show
import re
from xml.etree import ElementTree as ET

# 衛星画像取得する範囲を指定
AREA =  [
  [
    139.0240751,
    36.1879383
  ],
  [
    139.0570341,
    34.7880413
  ],
  [
    140.8093534,
    34.8060848
  ],
  [
    140.8642851,
    36.1591156
  ],
  [
    139.0240751,
    36.1879383
  ]
]

from geojson import Polygon
m=Polygon([AREA]) 

# GeoJSON ファイルを出力
object_name = 'Tokyo_Bay'
import json
with open(str(object_name) +'.geojson', 'w') as f:
    json.dump(m, f)
footprint_geojson = geojson_to_wkt(read_geojson(str(object_name) +'.geojson'))

# Copernicus Open Access Hub のユーザー情報を入力
user = 'naogify' 
password = '%8GUmDt9Bqt#oF0&8y@' 
api = SentinelAPI(user, password, 'https://scihub.copernicus.eu/dhus')

# 衛星画像を取得する条件を指定
products = api.query(footprint_geojson,
                     date = ('20200608', '20210608'), #取得希望期間の入力
                     platformname = 'Sentinel-2',
                     processinglevel = 'Level-2A',
                     cloudcoverpercentage = (0,10)) #被雲率（0％〜100％）

# 雲が少ない順にソート
products_gdf = api.to_geodataframe(products)
products_gdf_sorted = products_gdf.sort_values(['cloudcoverpercentage'], ascending=[True])

# NODATA_PIXEL_PERCENTAGE を取得する関数を用意
def get_odata_file_url(uuid, path):
    odata_path = api.api_url + "odata/v1/Products('{}')".format(uuid)
    for p in path.split('/'):
        odata_path += "/Nodes('{}')".format(p)
    odata_path += '/$value'
    return odata_path

def fetch_s2_qi_info(uuid, product_name):
    path = '{}.SAFE/MTD_MSIL2A.xml'.format(product_name)
    url = get_odata_file_url(uuid, path)
    response = api.session.get(url)
    xml = ET.XML(response.content)

    qi_info = {}

    image_quality_indicator = xml.find('.//Image_Content_QI')

    if image_quality_indicator:
      for elem in image_quality_indicator:
          qi_info[elem.tag] = float(elem.text)
    else:
      qi_info = False

    return qi_info

# 1番雲が少ない画像をダウンロード
for i in range(len(products_gdf_sorted)):

  metadata = products_gdf_sorted.iloc[i]
  qi_info = fetch_s2_qi_info(metadata["uuid"], metadata['title'])

  #データがオンラインかつ、NODATA_PIXEL_PERCENTAGE が 0
  if api.is_online(metadata["uuid"]) and qi_info and qi_info['NODATA_PIXEL_PERCENTAGE'] == 0:

    uuid = metadata["uuid"]
    product_title = metadata["title"]
    break
  
api.download(uuid, checksum=True)

# ダウンロードした ZIP ファイルを展開
file_name = str(product_title) +'.zip'
import zipfile
with zipfile.ZipFile(file_name) as zf:
 zf.extractall()

path = str(product_title) + '.SAFE/GRANULE'
files = os.listdir(path)

pathA = str(product_title) + '.SAFE/GRANULE/' + str(files[0])
files2 = os.listdir(pathA)

pathB = str(product_title) + '.SAFE/GRANULE/' + str(files[0]) +'/' + str(files2[1]) +'/R10m'
files3 = os.listdir(pathB)

path_b4 = str(product_title) + '.SAFE/GRANULE/' + str(files[0]) +'/' + str(files2[1]) +'/R10m/' +str(files3[0][0:23] +'TCI_10m.jp2')

b4 = rio.open(path_b4)

fig, ax = plt.subplots(1, figsize=(20, 20))
show(b4, ax=ax)
plt.show()