#%%

import cv2
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import cm

import OpenStreetMap 
import OpenWeather1


import eel
import json


@eel.expose   # JavaScriptから呼び出したいPython関数の前にこれを記述
def main_simulation():
    # 表示地点の緯度経度 
    # Vue.jsからポストされた任意の地点を設定できるようにすること

    lat = 35.626
    lon = 139.726

    # Map基点(lat,lon)から終点までの距離（緯度経度）
    angle = 0.00001

    # -------- OpenWeatherMapから風データを取得する(OpenWeather.py) --------
    # 自アカウントのAPIKey
    appid = 'f62cd99ae3ad4f54c119ca6464485f46'
    # 明日以降の天気情報を取得するURL
    forecast_url = 'http://api.openweathermap.org/data/2.5/forecast'

    main_temp = OpenWeather1.forecast(lat, lon, appid, forecast_url)

    # -------- 地図画像の取得と建築物地図の作成(OpenStreetMap.py) --------
    fig = plt.figure(figsize=(11, 11), dpi=300)

    ratio = 16  # 16
    nx = int(768/ratio)
    ny = int(768/ratio)
    
    myLat = 35.618
    myLon = 139.727

    # 解像度違いの地図画像
    mapImg, lowImg  = OpenStreetMap.getMapFromOSM(myLat, myLon, nx, ny, angle)  
    # 解像度違いのマスク（建物配置）画像
    lowImg, lowMask = OpenStreetMap.getMaskFromMap(lowImg) 
    # 高解像度の地図画像を使い、流体粒子表示用の画像を生成・保存
    negaMap = 255 - mapImg

    plt.imshow(mapImg)
    #plt.imshow(lowMask)
    cv2.imwrite('mapimg.png', mapImg)
    cv2.imwrite('lowImg.png', lowImg)
    cv2.imwrite('lowMask.png', lowMask)
    cv2.imwrite('negaMap.png', negaMap)
    # -------- 風速ベクトル図を2次元マップ上に可視化する --------
    fig = plt.figure(figsize=(11, 7), dpi=300)
    plt.imshow(mapImg)
    plotX, plotY = np.meshgrid(np.linspace(0, nx*ratio, nx), np.linspace(0, ny*ratio, ny)) 
            # np.linspace：等差数列を生成 np.linspace(最初の値、最後の値、要素数) 
    plt.colorbar()
    
    plt.xlabel('X')
    plt.ylabel('Y')
    #print(plotY)
    #print(np.amax(u),np.amax(v))
    #print(velocity)

    plt.savefig('figure1.png')

    x, y = OpenStreetMap.get_tile_num(myLat, myLon, 19)

    print('中心のタイル地図のタイル座標=',x,y) # 中心のタイル地図のタイル座標は、タイル地図一枚ごとに与えられる）

    # 9枚のタイル地図のうち、中心タイルの左上のタイル地図の、一番左上端の緯度経度を取得する
    left_bottom0a, left_bottom1a, right_top0a, right_top1a = OpenStreetMap.get_tile_bbox(19, x - 1, y - 1)
    newLat_lefttop = right_top1a    # 左上端緯度
    newLon_lefttop = left_bottom0a  # 左上端経度

    # 9枚のタイル地図のうち、中心タイルの右下のタイル地図の、一番右下端の緯度経度を取得する
    left_bottom0b, left_bottom1b, right_top0b, right_top1b = OpenStreetMap.get_tile_bbox(19, x + 1, y + 1)
    newLat_rightbottom = left_bottom1b  # 右下端緯度
    newLon_rightbottom = right_top0b    # 右下端緯度

    print('画像一番左上の緯度経度=',newLat_lefttop, newLon_lefttop)
    print('画像一番右下の緯度経度=',newLat_rightbottom, newLon_rightbottom)

    # メッシュ座標値を緯度経度に変換する  
    plot_lon_x, plot_lat_y = np.meshgrid(np.linspace(newLon_lefttop, newLon_rightbottom, nx), np.linspace(newLat_lefttop, newLat_rightbottom,  ny))
    #numpy配列ndarrayをリストに変換


    return main_temp

print(main_simulation())
    
# html/css/jsの入っているディレクトリを指定
eel.init('view', allowed_extensions=['.js', '.html', '.css'])

web_app_options = {
	'mode': "edge",
	'port': 8080,
    
}

# 最初の画面のhtmlファイルを指定（会社のパソコン使用時：Chromeを使わない）
eel.start('index.html', options=web_app_options, suppress_error=True)

# 最初の画面のhtmlファイルを指定（個人のパソコン使用時：Chromeを使う）
# eel.start('index.html')