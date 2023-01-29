#%%
import smopy
import cv2
import numpy as np
import math

def getMapFromOSM(lat, lon, nx, ny, angle):

    # マップの境界を指定してオブジェクトを定義する・・・Map(lat_min, lon_min, lat_max, lon_max, z=Zoomレベル)
    map = smopy.Map((lat, lon, lat+angle, lon+angle), z=19)
    mapImg = map.to_numpy()
    return mapImg, cv2.resize(mapImg, (nx, ny))


def getMaskFromMap(mapImg):
    lower = np.array([100, 19, 100])
    upper = np.array([150, 20, 250])
    hsv = cv2.cvtColor(mapImg, cv2.COLOR_BGR2HSV)
    mask = cv2.inRange(hsv, lower, upper)   # building = 255, other = 0
    maskedMapImg = cv2.bitwise_and(mapImg, mapImg, mask)
    return maskedMapImg, mask


"""
    smopyは、768×768ピクセルの地図を描画する場合、指定した座標を含むタイル地図(256×256)を中心
    として、その周りに合計9個のタイル地図を配置しているようである。 
    このため、ベクトル図の座標をcesiumに渡すには、9個のタイル地図のうち、一番左上のタイル地図と
    一番右下のタイル地図の緯度経度を取得する必要がある。
    https://sorabatake.jp/7325/
"""
# 緯度経度とズーム率から、その点を含んだ地図タイルの座標を取得する
def get_tile_num(lat, lon, z):
    """
    緯度経度からタイル座標を取得する
    Parameters
    ----------
    lat : number 
        タイル座標を取得したい地点の緯度(deg) 
    lon : number 
        タイル座標を取得したい地点の経度(deg) 
    z   : int 
        タイルのズーム率
    Returns
    -------
    xtile : int
        タイルのX座標
    ytile : int
        タイルのY座標
    """
    # https://wiki.openstreetmap.org/wiki/Slippy_map_tilenames#Python
    lat_rad = math.radians(lat)
    n = 2.0 ** z
    xtile = int((lon + 180.0) / 360.0 * n)
    ytile = int((1.0 - math.log(math.tan(lat_rad) +
                                    (1 / math.cos(lat_rad))) / math.pi) / 2.0 * n)
    return xtile, ytile

# タイル座標からバウンディングボックスを取得する
def get_tile_bbox(z, x, y):
    """
    タイル座標からバウンディングボックスを取得する
    ※タイル座標(z, x, y)を与えると、その画像の左下と右上の緯度経度を取得する
    https://tools.ietf.org/html/rfc7946#section-5
    Parameters
    ----------
    z : int 
        タイルのズーム率 
    x : int 
        タイルのX座標 
    y : int 
        タイルのY座標 
    Returns
    -------
    bbox: tuple of number
        タイルのバウンディングボックス
        (左下経度, 左下緯度, 右上経度, 右上緯度)
    """
    def num2deg(xtile, ytile, zoom):
        # https://wiki.openstreetmap.org/wiki/Slippy_map_tilenames#Python
        n = 2.0 ** zoom
        lon_deg = xtile / n * 360.0 - 180.0
        lat_rad = math.atan(math.sinh(math.pi * (1 - 2 * ytile / n)))
        lat_deg = math.degrees(lat_rad)
        return (lon_deg, lat_deg)

    right_top = num2deg(x + 1, y, z)
    left_bottom = num2deg(x, y + 1, z)
    return (left_bottom[0], left_bottom[1], right_top[0], right_top[1])
        # 左下経度、左下緯度、右上経度、右上緯度を返す

def main():
    return

if __name__ == '__main__':
    main()

# %%
