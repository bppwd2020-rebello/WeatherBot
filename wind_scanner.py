import filecmp
from datetime import datetime
from datetime import date
import time
from time import sleep
from urllib.request import *
import sys
from weather_code import Weather
import random
from bs4 import BeautifulSoup
from urllib.error import HTTPError
from urllib.error import URLError

weather = Weather()
user_agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36'
today = date.today()
URL = 'https://www.wunderground.com/dashboard/pws/KMAOXFOR33'


class WindScanner():
    def error(self):
        pass

    def __init__(self):
        super().__init__()

    def run(self):
        print("Wind Scanner is online!")
        while(True):
            #print(datetime.now().strftime("%S"))
            sleep(1)
            if datetime.now().strftime("%S") == "00":
                wind_data = []
                highest_wind = 0.0
                highest_gust = 0.0
                print("Scan has commenced at "+datetime.now().strftime("%H:%M:%S")+"!")
                wind_data.append(self.get_wind())
                for x in range(19):
                    sleep(12)
                    wind_data.append(self.get_wind())
                #print(wind_data)
                for x in range(len(wind_data)):
                    try:
                        if wind_data[x][0]>highest_wind:
                            highest_wind=wind_data[x][0]
                    except (TypeError,ValueError):
                        highest_wind=highest_wind
                    try:
                        if wind_data[x][1]>highest_gust:
                            highest_gust=wind_data[x][1]
                    except (TypeError,ValueError):
                        highest_gust=highest_gust
                if highest_wind>2.0 or highest_gust>4.0:
                    print("Highest Wind Speed: "+str(highest_wind)+" mph. Highest Wind Gust: "+str(highest_gust)+" mph")
                else:
                    print("Wind is calm or negligible.")
                    #print("Highest Wind Speed: "+str(highest_wind))
                if highest_wind > 10 or highest_gust > 15:
                    print("The wind reached "+str(highest_wind)+" mph with gusts at "+str(highest_gust)+" on "+today.strftime("%B %d, %Y")+" at "+datetime.now().strftime("%H:%M")+"\n")
                    f = open("wind.txt","a")
                    f.write("The wind reached "+str(highest_wind)+" mph with gusts at "+str(highest_gust)+" on "+today.strftime("%B %d, %Y")+" at "+datetime.now().strftime("%H:%M")+"\n")
                    f.close()




    def get_wind(self):
        winds = [0.0,0.0]

        #print(URL+" at "+datetime.now().strftime("%H:%M:%S"))
        request = Request(URL,headers={'User-Agent': user_agent})
        try:
            site = urlopen(request)
            sleep(2.0)
            html = site.read()
            soup = BeautifulSoup(html,'html.parser')
            wind_speed = soup.find("div", attrs = {'class':'weather__data weather__wind-gust'}).find("div", attrs = {'class':'weather__text'}).find("span", attrs = {'class':'test-false wu-unit ng-star-inserted'}).find("span", attrs = {'class':'wu-value wu-value-to'}).text
            wind_gust = soup.find("div", attrs = {'class':'weather__data weather__wind-gust'}).find("div", attrs = {'class':'weather__text'}).find("span", attrs = {'class':'test-false wu-unit wu-unit-speed ng-star-inserted'}).find("span", attrs = {'class':'wu-value wu-value-to'}).text
        except ( HTTPError, URLError, ValueError, IncompleteRead):
            return(winds)
        if wind_speed != None and wind_gust != None:
            winds[0] = float(wind_speed)
            winds[1] = float(wind_gust)
            return(winds)
        else:
            return(winds)




wind = WindScanner()
wind.run()
