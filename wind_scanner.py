import filecmp
from datetime import datetime
from datetime import date
import aiohttp
import asyncio
import time
from time import sleep
#from urllib.request import *
import sys
from weather_code import Weather
import random
from bs4 import BeautifulSoup


weather = Weather()
user_agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36'
today = date.today()
URL = 'https://www.wunderground.com/dashboard/pws/KMAOXFOR33'


async def main(loop):
    print("Wind Scanner is online!")
    while(True):
        #print(datetime.now().strftime("%S"))
        sleep(1)
        if datetime.now().strftime("%S") == "00":
            wind_data = []
            highest_wind = 0.0
            highest_gust = 0.0
            print("Scan has commenced at "+datetime.now().strftime("%H:%M:%S")+"!")
            wind_and_gust = await get_wind()
            wind_data.append(wind_and_gust)
            for x in range(19):
                sleep(13)
                wind_and_gust = await get_wind()
                wind_data.append(wind_and_gust)
            for wind in wind_data:
                if wind[0]>highest_wind:
                    highest_wind=wind[0]
                if wind[1]>highest_gust:
                    highest_gust=wind[1]

            if highest_wind>2.0 or highest_gust>4.0:
                    print("Highest Wind Speed: "+str(highest_wind)+" mph. Highest Wind Gust: "+str(highest_gust)+" mph")
            else:
                #print("Wind is calm or negligible.")
                print("Highest Wind Speed: "+str(highest_wind))
            if highest_wind > 10 or highest_gust > 15:
                print("The wind reached "+str(highest_wind)+" mph with gusts at "+str(highest_gust)+" on "+today.strftime("%B %d, %Y")+" at "+datetime.now().strftime("%H:%M")+"\n")
                f = open("wind.txt","a")
                f.write("The wind reached "+str(highest_wind)+" mph with gusts at "+str(highest_gust)+" on "+today.strftime("%B %d, %Y")+" at "+datetime.now().strftime("%H:%M")+"\n")
                f.close()

            print("------------------------------------------------------------")




async def get_wind():
    winds = [0.0,0.0]

    #print(URL+" at "+datetime.now().strftime("%H:%M:%S"))
    try:
        async with aiohttp.ClientSession() as session:
            html = await fetch(session, URL)

        soup = BeautifulSoup(html,'html.parser')

        wind_speed = soup.find("div", attrs = {'class':'weather__data weather__wind-gust'}).find("div", attrs = {'class':'weather__text'}).find("span", attrs = {'class':'test-false wu-unit ng-star-inserted'}).find("span", attrs = {'class':'wu-value wu-value-to'}).text
        wind_gust = soup.find("div", attrs = {'class':'weather__data weather__wind-gust'}).find("div", attrs = {'class':'weather__text'}).find("span", attrs = {'class':'test-false wu-unit wu-unit-speed ng-star-inserted'}).find("span", attrs = {'class':'wu-value wu-value-to'}).text
    except (AttributeError, ValueError) as err:
        print("Hit an error: "+err)
        return(winds)
    if wind_speed != None and wind_gust != None:
        winds[0] = float(wind_speed)
        winds[1] = float(wind_gust)
        return(winds)
    else:
        print("Unknown Issue, wind info not found")
        return(winds)


async def fetch(session, url):
    async with session.get(url) as response:
        return await response.text()

loop = asyncio.get_event_loop()
loop.run_until_complete(main(loop))
