# Sentinel2 衛星画像タイル

## 依存関係のインストール

[`sentinelhub.py`](https://github.com/sentinel-hub/sentinelhub-py)、[`gdal`](https://gdal.org/) 、[`mb-util`](https://github.com/mapbox/mbutil) が必要です。
以下の手順にそってインストールして下さい。

### sentinelhub.py

`pip` をお使いの場合は以下を実行して下さい。

```
$ pip install sentinelhub --upgrade
```

`<your access key>` に AWSアクセスキーを、`<your secret access key>` にシークレットアクセスキーを設定して、以下を実行して下さい。

```
$ sentinelhub.config --aws_access_key_id <your access key> --aws_secret_access_key <your secret access key>
```

### gdal

Mac で `Homebrew` をお使いの場合は以下を実行して下さい。Windowsの場合は適宜調べて下さい。

```
$ brew install gdal
```

### mb-util

`easy_install` をお使いの場合は以下を実行して下さい。

```
$ easy_install mbutil
```

## Sentinel2の画像をS3からダウンロード

```
$ sentinelhub.aws --tile 54SUE 2021-06-01
```

ダウンロード可能なタイルIDと期間を見つけるのには[EO Browser](https://apps.sentinel-hub.com/eo-browser/?zoom=8&lat=35.95578&lng=139.45496&themeId=DEFAULT-THEME) を使用。

https://sentinelhub-py.readthedocs.io/en/latest/aws_cli.html#sentinel-2-tiles

## 複数の衛星画像をマージ

```
$ gdal_merge.py -n 0 L1C_T54SUE_A022122_20210601T012656/IMG_DATA/T54SUE_20210601T012659_TCI.jp2 L1C_T54SVE_A022122_20210601T012656/IMG_DATA/T54SVE_20210601T012659_TCI.jp2
```

## Sentinel2の画像をzxy形式で分割

```
$ gdal2tiles.py --xyz -v -x out.tif tiles/
```

## mbtilesに書き出し

```
$ mb-util --image_format=png tiles sentinel2.mbtiles
```
