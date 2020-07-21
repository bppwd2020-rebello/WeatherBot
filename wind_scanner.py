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
                    sleep(13.75)
                    wind_data.append(self.get_wind())
                #print(wind_data)
                for x in range(len(wind_data)):
                    if wind_data[x][0]>highest_wind:
                        highest_wind=wind_data[x][0]
                    if wind_data[x][1]>highest_gust:
                        highest_gust=wind_data[x][1]
                print("Highest Wind Speed: "+str(highest_wind)+" mph")
                print("Highest Wind Gust: "+str(highest_gust)+" mph")
                if highest_wind > 10 or highest_gust > 15:
                    print("The wind reached "+str(highest_wind)+" mph with gusts at "+str(highest_gust)+" on "+today.strftime("%B %d, %Y")+" at "+datetime.now().strftime("%H:%M")+"\n")
                    f = open("wind.txt","a")
                    f.write("The wind reached "+str(highest_wind)+" mph with gusts at "+str(highest_gust)+" on "+today.strftime("%B %d, %Y")+" at "+datetime.now().strftime("%H:%M")+"\n")
                    f.close()




    def get_wind(self):
        winds = ["N/A","N/A"]

        #print(URL+" at "+datetime.now().strftime("%H:%M:%S"))
        request = Request(URL,headers={'User-Agent': user_agent})
        try:
            html = urlopen(request).read()
            soup = BeautifulSoup(html,'html.parser')
            temp = soup.find_all("span",attrs= {'class':'wu-value wu-value-to'})
        except ( HTTPError, URLError, ValueError):
            return("ERROR")

        if temp != []:
            changed = True
            winds[0] = float(temp[2].text)
            winds[1] = float(temp[3].text)
            return(winds)
        else:
            return(winds)




wind = WindScanner()
wind.run()
