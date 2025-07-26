import requests
import json




class WeatherAPI():
    def __init__(self, using_cache=True):
        self.status = self.ReadWeatherStatus()
        self.headers = {
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/136.0.0.0 Safari/537.36 Edg/136.0.0.0"
        }

    def GetLocation(self):
        try:
            ctb = requests.get(f"https://mesh.if.iqiyi.com/aid/ip/info?version=1.1.1", headers=self.headers, timeout=5).json()
            return {
            "latitude": ctb['data']["latitude"],
            "longitude": ctb['data']["longitude"],                
            "region": ctb['data']['cityCN']
            }
        except requests.exceptions.RequestException as e:
            return {}
        
    def GetWeather(self):
        try:
            location = self.GetLocation()
            url = f"https://api.open-meteo.com/v1/forecast?latitude={location["latitude"]}&longitude={location["longitude"]}&current=temperature_2m,weather_code&models=cma_grapes_global"
            resp = requests.get(url, headers=self.headers, timeout=8)
            if resp.status_code == 200:
                data = resp.json()
                weather =  {
                    "region": location["region"],
                    "temperature": data['current']['temperature_2m'],
                    "unit":data["current_units"]["temperature_2m"],
                    "weather": self.GetWeatherStatus(code=data['current']['weather_code'])
                }
                return weather
            else:
                return {}
        except Exception as e:
            print(e)
            return {'error':str(e)}
            

    def ReadWeatherStatus(self):
        with open("res/weather/weather_status.json", "r", encoding="utf-8") as file:
            return json.load(file)

    def GetWeatherStatus(self, code):
        for item in self.status["status"]:
            if item["code"] == code:
                return item["wea"]
        return "未知"    