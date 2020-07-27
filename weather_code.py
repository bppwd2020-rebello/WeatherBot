from bs4 import BeautifulSoup
from urllib.request import *
from urllib.error import HTTPError
from datetime import datetime
from time import sleep

user_agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36'

#Temp, feels like temp, wind direction, wind speed, wind gust, dew point, humidity, precip rate, precip accumulation, pressure, UV, Solar power
information = ["N/A","N/A","N/A","N/A","N/A","N/A","N/A","N/A","N/A","N/A","N/A","N/A","N/A","N/A"]
URL = 'https://www.wunderground.com/dashboard/pws/'
URL2 = 'https://www.wunderground.com/weather/'

class Weather():
    def error(self, message):
        pass

    def __init__(self):
        super().__init__()
        self.flag = 0
        self.data = []


    def get_time(self,code):
        local_url = URL2 + "us/state/town/" + code
        request = Request(local_url,headers={'User-Agent': user_agent})
        try:
            html = urlopen(request).read()
            soup = BeautifulSoup(html,'html.parser')
            time = soup.find("p", attrs={'class':'timestamp'}).text
            real_time = time.split()[1].split(":")[0]+datetime.now().strftime(":%M")
            time = real_time+" "+time.split()[2]+" "+time.split()[3]
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
            site =urlopen(request)
            sleep(1.0)
            html = site.read()
        except HTTPError as err:
            return("THIS STATION DOES NOT EXIST")

        soup = BeautifulSoup(html,'html.parser')
        watts = soup.find_all("div",attrs={'class':'weather__text'})
        try:
            main_temp = soup.find("div",attrs={'class':'main-temp'}).find("span",attrs={'class':'wu-value wu-value-to'}).text
        except AttributeError:
            main_temp = "--"
        try:
            feels_like_temp = soup.find("div",attrs={'class':'feels-like-temp'}).find("span",attrs={'class':'wu-value wu-value-to'}).text
        except AttributeError:
            feels_like_temp = "--"
        try:
            wind_direction = soup.find("span", attrs={'class':'text-bold'}).text
            if wind_direction == '':
                wind_direction = "--"
        except AttributeError:
            wind_direction = "--"
        try:
            wind_speed = soup.find("div", attrs = {'class':'weather__data weather__wind-gust'}).find("div", attrs = {'class':'weather__text'}).find("span", attrs = {'class':'test-false wu-unit ng-star-inserted'}).find("span", attrs = {'class':'wu-value wu-value-to'}).text
        except AttributeError:
            wind_speed = "--"
        try:
            wind_gust = soup.find("div", attrs = {'class':'weather__data weather__wind-gust'}).find("div", attrs = {'class':'weather__text'}).find("span", attrs = {'class':'test-false wu-unit wu-unit-speed ng-star-inserted'}).find("span", attrs = {'class':'wu-value wu-value-to'}).text
        except AttributeError:
            wind_gust = "--"

        summary = soup.find("div",attrs={'class':'weather__summary'}).find_all("div",attrs={'class':'weather__text'})

        dewpoint = summary[0]
        rainfall_rate = summary[1]
        pressure = summary[2]
        humidity = summary[3]
        rainfall_today = summary[4]
        uv_radiation = summary[5]


        if summary != []:
            changed = True
            information[0] = main_temp
            information[1] = feels_like_temp
            information[2] = wind_direction
            information[3] = wind_speed
            information[4] = wind_gust
            information[5] = dewpoint.text.split('\xa0F')[0]
            information[6] = rainfall_rate.text.split('\xa0')[0]
            information[9] = pressure.text+"Hg"
            information[8] = humidity.text
            information[7] = rainfall_today.text.split('\xa0')[0]
            information[10] = uv_radiation.text


            if watts != None and watts[len(watts)-1].text.endswith('watts/m²'):
                information[11] = watts[len(watts)-1].text
            try:
                info = self.get_time(code)
                information[12] = info[0]
                information[13] = info[1]
            except AttributeError:
                return("THIS STATION DOES NOT EXIST")

        """
        print("Temperature: "+information[0])
        print("Feels Like Temp: "+information[1])
        print("Wind Direction: "+information[2])
        print("Wind Speed: "+information[3])
        print("Wind Gust: "+information[4])
        print("Dew Point: "+information[5])
        print("Current Rainfall Rate: "+information[6])
        print("Pressure: "+information[9])
        print("Humidity: "+information[8])
        print("Rainfall Today: "+information[7])
        print("UV Radiation Level: "+information[10])
        print("Solar Radiation Level: "+information[11])
        """

        if changed:
            return(information)
        else:
            return("THIS STATION IS OFFLINE")

    def get_temp(self, code):
        temps = ["N/A","N/A","N/A","N/A"]
        local_url = URL + code
        print(local_url+" at "+datetime.now().strftime("%H:%M:%S"))
        request = Request(local_url,headers={'User-Agent': user_agent})
        try:
            html = urlopen(request).read()
        except HTTPError as err:
            return("THIS STATION DOES NOT EXIST")

        soup = BeautifulSoup(html,'html.parser')

        temp = soup.find_all("span",attrs= {'class':'wu-value wu-value-to'})

        if temp != []:
            changed = True
            temps[0] = temp[0].text+"°F"
            temps[1] = temp[1].text+"°F"
            info = self.get_time(code)
            temps[2] = info[0]
            temps[3] = info[1]
            return(temps)
        else:
            return(temps)


    def get_wind(self, code):
        winds = ["N/A","N/A","N/A","N/A"]
        local_url = URL + code
        print(local_url+" at "+datetime.now().strftime("%H:%M:%S"))
        request = Request(local_url,headers={'User-Agent': user_agent})
        try:
            html = urlopen(request).read()
        except HTTPError as err:
            return("THIS STATION DOES NOT EXIST")

        soup = BeautifulSoup(html,'html.parser')

        temp = soup.find_all("span",attrs= {'class':'wu-value wu-value-to'})

        if temp != []:
            changed = True
            winds[0] = temp[2].text+" mph"
            winds[1] = temp[3].text+ "mph"
            info = self.get_time(code)
            winds[2] = info[0]
            winds[3] = info[1]
            return(winds)
        else:
            return(winds)


    def get_forecast(self,town,state,flag):
        if flag:
            local_url = URL2 + state+"/"+town+"/"
        else:
            local_url = URL2 + "us/"+state+"/"+town+"/"
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




            time = soup.find("p", attrs={'class':'timestamp'}).text
            time = time.split()[1]+" "+time.split()[2]+" "+time.split()[3]
            location = soup.find("h1").text
            try:
                region = location.split(",")[1].split()[0]
            except(IndexError):
                region = ""
            location = location.split(",")[0]+" , "+region
            info = [time,location]




            forecast = [closest,middle,furthest,info[0],info[1]]
            return(forecast)
        except (HTTPError,IndexError) as err:
            return("The town and state combination you have entered failed, please make sure this is a valid combination.")
