from bs4 import BeautifulSoup
from urllib.request import *
from urllib.error import HTTPError
from datetime import datetime

user_agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36'

#Temp, feels like temp, wind direction, wind speed, wind gust, dew point, humidity, precip rate, precip accumulation, pressure, UV, Solar power
information = ["N/A","N/A","N/A","N/A","N/A","N/A","N/A","N/A","N/A","N/A","N/A","N/A","N/A","N/A"]
URL = 'https://www.wunderground.com/dashboard/pws/'
URL2 = 'https://www.wunderground.com/weather/us/'

class Weather():
    def error(self, message):
        pass

    def __init__(self):
        super().__init__()
        self.flag = 0
        self.data = []


    def get_time(self,code):
        local_url = URL2 + "state/town/" + code
        request = Request(local_url,headers={'User-Agent': user_agent})
        try:
            html = urlopen(request).read()
            soup = BeautifulSoup(html,'html.parser')
            time = soup.find("p", attrs={'class':'timestamp'}).text
            time = time.split()[1]+" "+time.split()[2]+" "+time.split()[3]
            location = soup.find("h1").text
            region = location.split(",")[1].split()[0]
            location = location.split(",")[0]+" , "+region
            info = [time,location]
            return(info)
        except HTTPError as err:
            return("Information Unavailible")


    def get_weather(self, code):
        changed = False
        local_url = URL + code
        print(local_url+" at "+datetime.now().strftime("%H:%M:%S"))
        request = Request(local_url,headers={'User-Agent': user_agent})
        try:
            html = urlopen(request).read()
        except HTTPError as err:
            return("THIS STATION DOES NOT EXIST")

        soup = BeautifulSoup(html,'html.parser')

        temp = soup.find_all("span",attrs= {'class':'wu-value wu-value-to'})
        watts = soup.find_all("div",attrs={'class':'weather__text'})

        if temp != []:
            changed = True
            information[0] = temp[0].text+"°F"
            information[1] = temp[1].text+"°F"
            information[2] = soup.find("span", attrs={'class':'text-bold'}).text
            information[3] = temp[2].text+"mph"
            information[4] = temp[3].text+"mph"
            information[5] = temp[4].text+"°F"
            information[6] = temp[5].text+"in/h"
            information[9] = temp[6].text+"inHg"
            information[8] = temp[7].text+"%"
            information[7] = temp[8].text+"in"


            if watts != None and watts[len(watts)-1].text.endswith('watts/m²'):
                information[10] = temp[9].text
                information[11] = watts[len(watts)-1].text
            info = self.get_time(code)
            information[12] = info[0]
            information[13] = info[1]


        """ print("Temperature: "+information[0])
        print("Feels Like Temp: "+information[1])
        print("Wind Direction: "+information[2])
        print("Wind Speed: "+information[3])
        print("Wind Gust: "+information[4])
        print("Dew Point: "+information[5])
        print("Current Rainfall Rate: "+information[6])
        print("Pressure: "+information[9])
        print("Humidity: "+information[7])
        print("Rainfall Today: "+information[8])
        print("UV Radiation Level: "+information[10])
        print("Solar Radiation Level: "+information[11])
        """
        if changed:
            return(information)
        else:
            return("THIS STATION IS OFFLINE")

    def get_forecast(self,code):
        local_url = URL2 + "state/town/" + code
        print(local_url+" at "+datetime.now().strftime("%H:%M:%S"))
        request = Request(local_url,headers={'User-Agent': user_agent})
        #html = urlopen(request).read()
        try:
            html = urlopen(request).read()
            soup = BeautifulSoup(html,'html.parser')


            days = soup.find_all("span",attrs= {'class':'day'})
            dates = soup.find_all("span",attrs= {'class':'date'})
            temps = soup.find_all("span",attrs= {'class':'temp'})
            rain_chances = soup.find_all("a",attrs= {'class':'hook'})
            texts =  soup.find_all("a",attrs= {'class':'module-link'})

            closest = [days[0].text,dates[0].text,temps[1].text,rain_chances[0].text,texts[1].text]
            middle = [days[1].text,dates[1].text,temps[2].text,rain_chances[1].text,texts[3].text]
            furthest = [days[2].text,dates[2].text,temps[3].text,rain_chances[2].text,texts[5].text]

            info = self.get_time(code)
            forecast = [closest,middle,furthest,info[0],info[1]]
            return(forecast)
        except HTTPError as err:
            return("THIS FORECAST DOES NOT EXIST")
