# Sentinel2 衛星画像タイル


## 環境構築

### 認証

https://scihub.copernicus.eu/dhus/#/self-registration でユーザー登録をしてください。

ユーザー登録時に入力したユーザーネームとパスワードを `.netrc.sample` の `<your username>` と `<your password>` と置き換えてください。

以下のコマンドを実行して、`.netrc` をホームディレクトリに配置します。

```
mv .netrc.sample ~/.netrc
```

### 依存関係のインストール

Python 

```
$ pip install sentinelsat matplotlib shapely rasterio re xml
```

GDAL

```
$ brew install gdal
```

MBUtil
```
$ easy_install mbutil
```

## 開発手順

### 衛星画像をダウンロード

```
$ python main.py
```

### 複数の衛星画像をマージ

```
$ gdal_merge.py -n 0 L1C_T54SUE_A022122_20210601T012656/IMG_DATA/T54SUE_20210601T012659_TCI.jp2 L1C_T54SVE_A022122_20210601T012656/IMG_DATA/T54SVE_20210601T012659_TCI.jp2
```

### Sentinel2の画像をzxy形式で分割

```
$ gdal2tiles.py --xyz -v -x out.tif tiles/
```

### mbtilesに書き出し

```
$ mb-util --image_format=png tiles sentinel2.mbtiles
```
