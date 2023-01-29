#%%

import json
import requests

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

    # 風速データの出力
    for i in range(len(data["list"])):
        print(data["list"][i]["dt_txt"])
        print("wind speed:", data["list"][i]["wind"]["speed"])
        print("------------------------------")

    wind_speed = data["list"][0]["wind"]["speed"]
    wind_deg   = data["list"][0]["wind"]["deg"]

    return wind_speed, wind_deg

def main():
    return

if __name__ == '__main__':
    main()



# %%
