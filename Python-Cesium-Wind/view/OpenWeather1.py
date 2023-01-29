#%%

import json
import requests
lat=35.626
lon=139.726
appid='f62cd99ae3ad4f54c119ca6464485f46'
forecast_url='http://api.openweathermap.org/data/2.5/forecast'

# OpenWeatherMapから任意の緯度経度の天気データを3時間毎に5日間分JSONデータで取得する
def forecast(lat, lon, appid, forecast_url):
    # API呼出し
    response = requests.get("{}?lat={}&lon={}&lang=ja&units=metric&APPID={}".format(
        forecast_url, lat, lon, appid))
    
    # 結果出力
    print("---")
    data = response.json()
    data = json.loads(response.text)
    #jsontext = json.dumps(data, indent=4)
    #print (jsontext)

    # 温度データの出力
    for i in range(len(data["list"])):
        print(data["list"][i]["dt_txt"])
        print("main temp:", data["list"][i]["main"]["temp"])
        print("------------------------------")

    main_temp = data["list"][0]["main"]["temp"]
    

    return main_temp

print(forecast(35.626,139.726,'f62cd99ae3ad4f54c119ca6464485f46','http://api.openweathermap.org/data/2.5/forecast'))

def main():
    return

if __name__ == '__main__':
    main()
