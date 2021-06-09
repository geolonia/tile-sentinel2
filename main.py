import os

from sentinelsat import SentinelAPI, read_geojson, geojson_to_wkt 
import matplotlib.pyplot as plt

from shapely.geometry import MultiPolygon, Polygon
import rasterio as rio
from rasterio.plot import show
import rasterio.mask

# 衛星画像取得する範囲を指定
AREA =  [
  [
    -220.291841,
    35.6593884
  ],
  [
    -220.2932143,
    35.4817801
  ],
  [
    -220.1380324,
    35.4817801
  ],
  [
    -220.1421523,
    35.6493456
  ],
  [
    -220.291841,
    35.6593884
  ]
]

# 入力された経度の値が西経なので、360°を足して東経に変換
for i in range(len(AREA)):
    AREA[i][0] = AREA[i][0] +360
from geojson import Polygon
m=Polygon([AREA]) 

# GeoJSON ファイルを出力
object_name = 'Tokyo_Bay'
import json
with open(str(object_name) +'.geojson', 'w') as f:
    json.dump(m, f)
footprint_geojson = geojson_to_wkt(read_geojson(str(object_name) +'.geojson'))

# Copernicus Open Access Hub のユーザー情報を入力
user = '' 
password = '' 
api = SentinelAPI(user, password, 'https://scihub.copernicus.eu/dhus')

# 衛星画像を取得する条件を指定
products = api.query(footprint_geojson,
                     date = ('20201201', '20210608'), #取得希望期間の入力
                     platformname = 'Sentinel-2',
                     processinglevel = 'Level-2A',
                     cloudcoverpercentage = (0,100)) #被雲率（0％〜100％）

# 雲が少ない順にソート
products_gdf = api.to_geodataframe(products)
products_gdf_sorted = products_gdf.sort_values(['cloudcoverpercentage'], ascending=[True])
products_gdf_sorted.head()

# 1番雲が少ない画像をダウンロード
uuid = products_gdf_sorted.iloc[2]["uuid"]
product_title = products_gdf_sorted.iloc[2]["title"]
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