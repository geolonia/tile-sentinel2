import os
from sentinelsat import SentinelAPI, read_geojson, geojson_to_wkt 
import matplotlib.pyplot as plt
from shapely.geometry import MultiPolygon, Polygon

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

# 1番雲が少ない画像をダウンロード
for i in range(len(products)):

  unclassified = products_gdf_sorted.iloc[i]["unclassifiedpercentage"]

  metadata = api.get_product_odata(products_gdf_sorted.iloc[i]["uuid"])
  print(metadata)
  
  #データがオンラインかつ、unclassifiedpercentage が1以上
  if api.is_online(products_gdf_sorted.iloc[i]["uuid"]) and unclassified == 0:

    uuid = products_gdf_sorted.iloc[i]["uuid"]
    product_title = products_gdf_sorted.iloc[i]["title"]
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