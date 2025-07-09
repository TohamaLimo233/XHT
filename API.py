import requests
import json
import os
import sys
sys.dont_write_bytecode = True



class WeatherAPI():
    # 提取常量
    HEADERS = {
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/136.0.0.0 Safari/537.36 Edg/136.0.0.0"
    }
    SIGN = "zUFJoAR2ZVrDy1vF3D07"
    WEATHER_URL_TEMPLATE = (
        "https://weatherapi.market.xiaomi.com/wtr-v3/weather/all?"
        "latitude=110&longitude=112&isLocated=true&locationKey=weathercn%3A{cityid}"
        "&days=1&appKey=weather20151024&sign={sign}&romVersion=7.2.16&appVersion=87"
        "&alpha=false&isGlobal=false&device=cancro&modDevice=&locale=zh_cn"
    )

    def __init__(self, using_cache=True):
        self.citymap = self.GetCityMap()

    def GetCity(self):
        try:
            ctb = requests.get(f"https://mesh.if.iqiyi.com/aid/ip/info?version=1.1.1", headers=self.HEADERS, timeout=5).json()
            return {
                "city":ctb['data']['cityCN'],
                "county":ctb['data']["countyCN"].replace("区", "").replace("县", "").replace("市", "").replace("旗", "").replace("特区", "").replace("林区", ""),
                "latitude": ctb['data']['latitude'],
                "longitude": ctb['data']['longitude']}
        except requests.exceptions.RequestException as e:
            return "获取城市信息失败"

    def GetCityMap(self):
        try:           
            with open(file=os.path.join(os.path.dirname(__file__), "res", "weather", "weatherlib.data"), mode="r", encoding="utf-8") as f:
                content = f.read()
                import base64
                decoded_content = base64.b64decode(content).decode("utf-8")
                try:
                    city_data = json.loads(decoded_content)
                    self.city_map = {item["name"]: int(item["city_num"]) for item in city_data}
                except (json.JSONDecodeError, KeyError) as e:
                    self.city_map = {}
                return self.city_map
        except FileNotFoundError as e:
            return {}

    def LookupCity(self, cityname: str):
        city_id = self.citymap.get(cityname)
        if city_id is None:
            return None
        return city_id

    def FetchWeatherData(self, cityid):
        if cityid is None:
            return "城市ID无效"
        try:
            url = self.WEATHER_URL_TEMPLATE.format(cityid=cityid, sign=self.SIGN)
            response = requests.get(url, headers=self.HEADERS, timeout=5)
            response.raise_for_status()
            data = response.json()
            if "current" in data:
                weather_code = int(data["current"]["weather"])
                try:
                    with open(file=os.path.join(os.path.dirname(__file__), "res", "weather", "weather_status.data"), mode="r", encoding="utf-8") as f:
                        weather_status = json.load(f)
                        weather_desc = next((item["wea"] for item in weather_status["weatherinfo"] if item["code"] == weather_code), "未知")
                except (FileNotFoundError, json.JSONDecodeError) as e:
                    weather_desc = "未知"
                temp = data["current"]["temperature"]["value"]
                return {"weather_desc": weather_desc, "temp": temp, "unit": "℃"}
            else:
                return "Failed"
        except requests.exceptions.RequestException as e:
            return str(e)