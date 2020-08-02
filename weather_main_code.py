import discord
from bs4 import BeautifulSoup
from discord.ext import commands
from discord.ext.commands import Bot
from discord import FFmpegPCMAudio
import asyncio
import aiohttp
import filecmp
from datetime import datetime
from time import time
from urllib.request import *
import sys
from weather_code import Weather
import random

URL = 'https://www.wunderground.com/dashboard/pws/'
weather = Weather()

towns = ["SYC","MICHAEL","MERVE","AUSTIN","IMMI","NORTHRIDGE","SOUTHBOROUGH","HELOTES","BOSTON","NORFOLK","METHUEN","SPRINGFIELD","MOSCOW","BUCHAREST","PASADENA","CHARLTON","SOUTHBRIDGE","LOVELL","AMMAN","WINCHESTER","BOGOTA","WEYMOUTH","LANTANA","MEDIA","PLAINVIEW","MILLIS","SANFERNANDO","NORWELL","ADABA"]
codes = ["KNHASHLA2","KMDSILVE171","KMDSILVE171","KMAOXFOR33","IBANIJAM2","KCANORTH365","KMASOUTH43","KTXHELOT27","KMABOSTO124","KMANORFO14","KMAMETHU40","KMASPRIN28","IMOSCOW299","IBUCHARE87","KCAPASAD140","KMACHARL47","KMAWESTV8","KMEBRIDG15","IVALLE48","KMAWINCH55","IBOGOT76","KMAWEYMO41","KFLLANTA2","KPAMEDIA30","KNYPLAIN9","KMAMILLI11","ISANFERN13","KMANORWE20","ISOUTH677"]


TOKEN = ""

with open("token.txt", 'r') as f:
    TOKEN = f.readline()




class Client(discord.Client):
    def __init__(self):
        super().__init__()

        self.channel = "Weather Channel"

    #Ben helped me fix this method, credit given
    async def weather_run(self, code, message, flag):
        channel = message.channel
        await message.channel.send("Recieved! Station Code: " + code + ".")
        response = await weather.get_weather(code)
        if response == "THIS STATION DOES NOT EXIST":
            await message.channel.send(response)
        elif response == "THIS STATION IS OFFLINE":
            await message.channel.send(response)
        else:
            embed=discord.Embed(title="Current Readings for "+response[13]+":", description="Url: " + URL + code+"\n Units: **Imperial** / Metric", color=0x193ed2)
            embed.add_field(name="Temperature", value=response[0]+"°F", inline=True)
            embed.add_field(name="Feels Like Temperature", value=response[1]+"°F", inline=True)
            embed.add_field(name="Dew Point", value=response[5]+"°F", inline=True)
            embed.add_field(name="Wind Speed", value=response[3]+"mph", inline=True)
            embed.add_field(name="Wind Gust", value=response[4]+"mph", inline=True)
            embed.add_field(name="Wind Direction", value=response[2], inline=True)
            embed.add_field(name="Rainfall Rate", value=response[6]+"in/hr", inline=True)
            embed.add_field(name="Rainfall Today", value=response[7]+"in", inline=True)
            embed.add_field(name="Humidity", value=response[8], inline=True)
            if flag:
                embed.add_field(name="Pressure", value=response[9], inline=True)
                embed.add_field(name="UV Radiation Value", value=response[10], inline=True)
                embed.add_field(name="Solar Radiation", value=response[11], inline=True)
            embed.set_footer(text="Current weather response from station "+code+" at "+response[12])

            embed_message = await message.channel.send(embed=embed)
            reactions_embed = await message.channel.fetch_message(embed_message.id)
            reactions = ['\U0001f1ee','\U0001f1f2']
            for emoji in reactions:
                await reactions_embed.add_reaction(emoji)


    async def forecast_run(self, town, state, flag, broken_flag, message,code):
        await message.channel.send("Recieved! Town Name: "+town+", "+state+".")
        response = await weather.get_forecast(town,state,flag,broken_flag,code)
        #print(response)
        if random.randint(0,100)>2:
            if response == "The town and state combination you have entered failed, please make sure this is a valid combination. Sometimes the website may break, try again if you know this is a correct combonation.":
                await message.channel.send(response)
            else:
                global embed_imperial
                embed_imperial=discord.Embed(title="Forecast", description="Current forecast for "+response[4]+"."+"\n Units: **Imperial** / Metric", color=0x002aff)
                embed_imperial.add_field(name=response[0][0], value=response[0][1], inline=True)
                embed_imperial.add_field(name=response[0][2].split()[0], value=response[0][2].split()[1]+"°F", inline=True)
                embed_imperial.add_field(name="Rain Chance / Amount", value=response[0][3], inline=True)
                embed_imperial.add_field(name="Description", value=response[0][4], inline=False)
                embed_imperial.add_field(name=response[1][0], value=response[1][1], inline=True)
                embed_imperial.add_field(name=response[1][2].split()[0], value=response[1][2].split()[1]+"°F", inline=True)
                embed_imperial.add_field(name="Rain Chance / Amount", value=response[1][3], inline=True)
                embed_imperial.add_field(name="Description", value=response[1][4], inline=False)
                embed_imperial.add_field(name=response[2][0], value=response[2][1], inline=True)
                embed_imperial.add_field(name=response[2][2].split()[0], value=response[2][2].split()[1]+"°F", inline=True)
                embed_imperial.add_field(name="Rain Chance / Amount", value=response[2][3], inline=True)
                embed_imperial.add_field(name="Description", value=response[2][4], inline=True)
                embed_imperial.set_footer(text="Local Time: "+response[3])


                embed_message = await message.channel.send(embed=embed_imperial)
                reactions_embed = await message.channel.fetch_message(embed_message.id)
                reactions = ['\U0001f1eb','\U0001f1e8']
                for emoji in reactions:
                    await reactions_embed.add_reaction(emoji)

        else:
            #Funny idea courtesy of Aidan vC
            await message.channel.send("Piss rain piss rain!")


    async def temp_run(self, code, message):
        await message.channel.send("Recieved! Station Code: " + code + ".")
        response =await  weather.get_temp(code)
        if response == "THIS STATION DOES NOT EXIST":
            await message.channel.send(response)
        elif response == "THIS STATION IS OFFLINE":
            await message.channel.send(response)
        else:
            embed=discord.Embed(title="Current Readings for "+response[3]+":", description="Url: " + URL + code, color=0x193ed2)
            embed.add_field(name="Temperature", value="Current temperature is "+response[0]+" and feels like "+response[1]+"." , inline=True)
        embed.set_footer(text="Current weather response from station "+code+" at "+response[2])
        await message.channel.send(embed=embed)

    async def wind_run(self, code, message):
        await message.channel.send("Recieved! Station Code: " + code + ".")
        response = weather.get_wind(code)
        if response == "THIS STATION DOES NOT EXIST":
            await message.channel.send(response)
        elif response == "THIS STATION IS OFFLINE":
            await message.channel.send(response)
        else:
            embed=discord.Embed(title="Current Readings for "+response[3]+":", description="Url: " + URL + code, color=0x193ed2)
            embed.add_field(name="Wind", value="Current wind speed  is "+response[0]+" and has gusted to "+response[1]+"." , inline=True)
        embed.set_footer(text="Current weather response from station "+code+" at "+response[2])
        await message.channel.send(embed=embed)

    def validate_code(self,message):
        flag = False
        try:
            station_code = message.content.split()[1]
        except IndexError:
            return("Invalid code!")
        for i, town in enumerate(towns):
            if station_code.upper() == town:
                return(codes[i])
                flag = True
        if not flag:
            try:
                print(int(station_code[-1]))
            except ValueError as err:
                if not station_code.upper() == 'WPI':
                    station_code = "1"
            if station_code.upper() == 'WPI':
                return("KMAWORCE57")
            elif len(station_code)>11:
                return("Invalid code!")
            elif len(station_code)<7:
                return("Invalid code!")
            else:
                return(station_code)



    async def on_ready(self):
        print('Logged on as', self.user)

        await self.change_presence(activity=discord.Game("~help to use me!"));

    async def edit_message(self,reaction,user):
        if reaction.emoji == '\U0001f1f2' and user.id != 731989043713146990:
            if reaction.message.author.id == 731989043713146990:
                embed = reaction.message.embeds[0]
                embed_fields = embed.fields
                if embed_fields[0].value.split("°")[1] == "F":
                    try:
                        temperature = str(round(((float(embed_fields[0].value.split("°")[0])-32)*5/9),1))
                    except ValueError:
                        temperature = "--"
                    try:
                        feels_like = str(round(((float(embed_fields[1].value.split("°")[0])-32)*5/9),1))
                    except ValueError:
                        feels_like = "--"
                    try:
                        dew_point = str(round(((float(embed_fields[2].value.split("°")[0])-32)*5/9),1))
                    except ValueError:
                        dew_point = "--"
                    try:
                        wind_speed = str(round(float(embed_fields[3].value.split("mph")[0])*1.609344,1))
                    except ValueError:
                        wind_speed = "--"
                    try:
                        wind_gust = str(round(float(embed_fields[4].value.split("mph")[0])*1.609344,1))
                    except ValueError:
                        wind_gust = "--"
                    try:
                        rainfall_rate = str(round(float(embed_fields[6].value.split("in")[0])/0.3937,2))
                    except ValueError:
                        rainfall_rate = "--"
                    try:
                        rainfall_today = str(round(float(embed_fields[7].value.split("in")[0])/0.3937,2))
                    except ValueError:
                        rainfall_today= "--"
                    new_description = embed.description.text.split("\n")[0] + "\n Units: Imperial / **Metric**"
                    new_embed = discord.Embed(title=embed.title, description=new_description, color=0x193ed2)
                    new_embed.add_field(name="Temperature", value=temperature +"°C", inline=True)
                    new_embed.add_field(name="Feels Like Temperature", value=feels_like+"°C", inline=True)
                    new_embed.add_field(name="Dew Point", value=dew_point+"°C", inline=True)
                    new_embed.add_field(name="Wind Speed", value=wind_speed+"km/h", inline=True)
                    new_embed.add_field(name="Wind Gust", value=wind_gust+"km/h", inline=True)
                    new_embed.add_field(name="Wind Direction", value=embed_fields[5].value, inline=True)
                    new_embed.add_field(name="Rainfall Rate", value=rainfall_rate+"cm/hr", inline=True)
                    new_embed.add_field(name="Rainfall Today", value=rainfall_today+"cm", inline=True)
                    new_embed.add_field(name="Humidity", value=embed_fields[8].value, inline=True)
                    new_embed.add_field(name="Pressure", value=embed_fields[9].value, inline=True)
                    new_embed.add_field(name="UV Radiation Value", value=embed_fields[10].value, inline=True)
                    new_embed.add_field(name="Solar Radiation", value=embed_fields[11].value, inline=True)
                    new_embed.set_footer(text=embed.footer.text)

                    await reaction.message.edit(embed=new_embed)

        if reaction.emoji == '\U0001f1ee' and user.id != 731989043713146990:
            if reaction.message.author.id == 731989043713146990:
                embed = reaction.message.embeds[0]
                embed_fields = embed.fields
                if embed_fields[0].value.split("°")[1] == "C":
                    try:
                        temperature = str(round(((float(embed_fields[0].value.split("°")[0])*(9/5))+32),1))
                    except ValueError:
                        temperature = "--"
                    try:
                        feels_like = str(round(((float(embed_fields[1].value.split("°")[0])*(9/5))+32),1))
                    except ValueError:
                        feels_like = "--"
                    try:
                        dew_point = str(round(((float(embed_fields[2].value.split("°")[0])*(9/5))+32),1))
                    except ValueError:
                        dew_point = "--"
                    try:
                        wind_speed = str(round(float(embed_fields[3].value.split("km")[0])/1.609344,1))
                    except ValueError:
                        wind_speed = "--"
                    try:
                        wind_gust = str(round(float(embed_fields[4].value.split("km")[0])/1.609344,1))
                    except ValueError:
                        wind_gust = "--"
                    try:
                        rainfall_rate = str(round(float(embed_fields[6].value.split("cm")[0])*0.3937,2))
                    except ValueError:
                        rainfall_rate = "--"
                    try:
                        rainfall_today = str(round(float(embed_fields[7].value.split("cm")[0])*0.3937,2))
                    except ValueError:
                        rainfall_today= "--"
                    new_description = embed.description.text.split("\n")[0] + "\n Units: **Imperial** / Metric"
                    new_embed = discord.Embed(title=embed.title, description=new_description, color=0x193ed2)
                    new_embed.add_field(name="Temperature", value=temperature +"°F", inline=True)
                    new_embed.add_field(name="Feels Like Temperature", value=feels_like+"°F", inline=True)
                    new_embed.add_field(name="Dew Point", value=dew_point+"°F", inline=True)
                    new_embed.add_field(name="Wind Speed", value=wind_speed+"mph", inline=True)
                    new_embed.add_field(name="Wind Gust", value=wind_gust+"mph", inline=True)
                    new_embed.add_field(name="Wind Direction", value=embed_fields[5].value, inline=True)
                    new_embed.add_field(name="Rainfall Rate", value=rainfall_rate+"in/hr", inline=True)
                    new_embed.add_field(name="Rainfall Today", value=rainfall_today+"in", inline=True)
                    new_embed.add_field(name="Humidity", value=embed_fields[8].value, inline=True)
                    new_embed.add_field(name="Pressure", value=embed_fields[9].value, inline=True)
                    new_embed.add_field(name="UV Radiation Value", value=embed_fields[10].value, inline=True)
                    new_embed.add_field(name="Solar Radiation", value=embed_fields[11].value, inline=True)
                    new_embed.set_footer(text=embed.footer.text)

                    await reaction.message.edit(embed=new_embed)


        if reaction.emoji == '\U0001f1eb' and user.id != 731989043713146990:
            if reaction.message.author.id == 731989043713146990:

                embed = reaction.message.embeds[0]
                embed_fields = embed.fields

                temperature1 = str(int(round(((float(embed_fields[1].value.split("°")[0])*(9/5))+32),0)))
                temperature2 = str(int(round(((float(embed_fields[5].value.split("°")[0])*(9/5))+32),0)))
                temperature3 = str(int(round(((float(embed_fields[9].value.split("°")[0])*(9/5))+32),0)))
                rain_field1 = embed_fields[2].value.split("/ ")[1]
                rain_field2 = embed_fields[6].value.split("/ ")[1]
                rain_field3 = embed_fields[10].value.split("/ ")[1]
                amount1 = str(round(float(rain_field1.split("cm")[0])*0.3937,2))
                amount2 = str(round(float(rain_field2.split("cm")[0])*0.3937,2))
                amount3 = str(round(float(rain_field3.split("cm")[0])*0.3937,2))
                rain1 = embed_fields[2].value.split("/")[0]+"/ "+amount1
                rain2 = embed_fields[6].value.split("/")[0]+"/ "+amount2
                rain3 = embed_fields[10].value.split("/")[0]+"/ "+amount3
                new_description = embed.description.split("\n")[0] + "\n Units: Imperial / **Metric**"
                new_embed = discord.Embed(title="Forecast", description=new_description, color=0x002aff)
                new_embed.add_field(name=embed_fields[0].name, value=embed_fields[0].value, inline=True)
                new_embed.add_field(name=embed_fields[1].name, value=temperature1+"°F", inline=True)
                new_embed.add_field(name="Rain Chance / Amount", value=rain1+" in", inline=True)
                new_embed.add_field(name="Description", value=embed_fields[3].value, inline=False)
                new_embed.add_field(name=embed_fields[4].name, value=embed_fields[4].value, inline=True)
                new_embed.add_field(name=embed_fields[5].name, value=temperature2+"°F", inline=True)
                new_embed.add_field(name="Rain Chance / Amount", value=rain2+" in", inline=True)
                new_embed.add_field(name="Description", value=embed_fields[7].value, inline=False)
                new_embed.add_field(name=embed_fields[8].name, value=embed_fields[8].value, inline=True)
                new_embed.add_field(name=embed_fields[9].name, value=temperature3+"°F", inline=True)
                new_embed.add_field(name="Rain Chance / Amount", value=rain3+" in", inline=True)
                new_embed.add_field(name="Description", value=embed_fields[11].value, inline=True)
                new_embed.set_footer(text=embed.footer.text)

                await reaction.message.edit(embed=new_embed)


        if reaction.emoji == '\U0001f1e8' and user.id != 731989043713146990:
            if reaction.message.author.id == 731989043713146990:

                embed = reaction.message.embeds[0]
                embed_fields = embed.fields

                temperature1 = str(int(round(((float(embed_fields[1].value.split("°")[0])-32)*5/9),0)))
                temperature2 = str(int(round(((float(embed_fields[5].value.split("°")[0])-32)*5/9),0)))
                temperature3 = str(int(round(((float(embed_fields[9].value.split("°")[0])-32)*5/9),0)))
                rain_field1 = embed_fields[2].value.split("/ ")[1]
                rain_field2 = embed_fields[6].value.split("/ ")[1]
                rain_field3 = embed_fields[10].value.split("/ ")[1]
                amount1 = str(round(float(rain_field1.split("in")[0])/0.3937,2))
                amount2 = str(round(float(rain_field2.split("in")[0])/0.3937,2))
                amount3 = str(round(float(rain_field3.split("in")[0])/0.3937,2))
                rain1 = embed_fields[2].value.split("/")[0]+"/ "+amount1
                rain2 = embed_fields[6].value.split("/")[0]+"/ "+amount2
                rain3 = embed_fields[10].value.split("/")[0]+"/ "+amount3
                new_description = embed.description.split("\n")[0] + "\n Units: Imperial / **Metric**"
                new_embed = discord.Embed(title="Forecast", description=new_description, color=0x002aff)
                new_embed.add_field(name=embed_fields[0].name, value=embed_fields[0].value, inline=True)
                new_embed.add_field(name=embed_fields[1].name, value=temperature1+"°C", inline=True)
                new_embed.add_field(name="Rain Chance / Amount", value=rain1+" cm", inline=True)
                new_embed.add_field(name="Description", value=embed_fields[3].value, inline=False)
                new_embed.add_field(name=embed_fields[4].name, value=embed_fields[4].value, inline=True)
                new_embed.add_field(name=embed_fields[5].name, value=temperature2+"°C", inline=True)
                new_embed.add_field(name="Rain Chance / Amount", value=rain2+" cm", inline=True)
                new_embed.add_field(name="Description", value=embed_fields[7].value, inline=False)
                new_embed.add_field(name=embed_fields[8].name, value=embed_fields[8].value, inline=True)
                new_embed.add_field(name=embed_fields[9].name, value=temperature3+"°C", inline=True)
                new_embed.add_field(name="Rain Chance / Amount", value=rain3+" cm", inline=True)
                new_embed.add_field(name="Description", value=embed_fields[11].value, inline=True)
                new_embed.set_footer(text=embed.footer.text)

                await reaction.message.edit(embed=new_embed)


    async def on_reaction_add(self,reaction, user):
        await self.edit_message(reaction,user)




    async def on_message(self, message):

        if message.author == self.user:
            return

        # ping (Grant's command I took)
        if message.content == '~ping':
            before = time()
            await message.channel.send('Pong!')
            ms = (time() - before) * 1000
            await message.channel.send('Ping took: {}ms'.format(int(ms)))

        if message.content == '~pingo':
            before = time()
            await message.channel.send('Pongo!')
            ms = (time() - before) * 1000
            await message.channel.send('Ping took: {}ms'.format(int(ms)))

        if message.content == '~help':
            embed=discord.Embed(title="Help:", description="All the commands currently callable for the bot.", color=0x193ed2)
            embed.add_field(name="~ping", value="Tests the latency to the bot", inline=False)
            embed.add_field(name="~weather ***code*** (see ~code)", value="Gives the current weather conditions of a specific location", inline=False)
            embed.add_field(name="~weather ***town state abbreviation***", value="Gives the current weather conditions of a specific location.\n Town names with a space: Replace spaces with a - \n Internationals: Do Town, Country Abbrevation then an i to get yours", inline=False)
            embed.add_field(name="~forecast ***town state abbreviation*** ", value="Gives you the forecast of a specific location.\n Town names with a space: Replace spaces with a - \n Internationals: Do Town, Country Abbrevation then an i to get yours", inline=False)
            embed.add_field(name="~currentTemp ***code*** (see ~code)", value="Gives you the current temperature of a specific location", inline=False)
            embed.add_field(name="~code", value="Tells you how to input a correct code", inline=False)
            embed.add_field(name="~weather or ~weather WPI", value="Gives you the current weather at WPI", inline=False)
            embed.add_field(name="~forecast", value="Gives you the forecast for WPI", inline=False)
            embed.add_field(name="~currentTemp or ~currentTemp WPI", value="Gives you the current temperature for WPI", inline=False)
            embed.set_footer(text="Command called: ~help")
            await message.channel.send(embed=embed)

        if message.content == '~code':
            embed=discord.Embed(title="Code:", description="How to type the code for a weather station", color=0x193ed2)
            embed.add_field(name="First letter:", value="K for USA", inline=False)
            embed.add_field(name="Second and third letter:", value="Your state abbreviation.", inline=False)
            embed.add_field(name="The Next 3 to 5 letters:", value="First 5 letters of town name or whole town name if it's less than 5.", inline=False)
            embed.add_field(name="Last 1 to 3 characters:", value="Station # in that town, most towns have under 30 but if it has a common first 5 letters (Southborough/Southbrige), it can be well over 100 or normal", inline=False)
            embed.set_footer(text="Example: K(USA)MA(Massachusetts)OXFOR(Oxford)33(Station #) KMAOXFOR33 \n DISCLAIMER: Some stations may be offline or no longer exist so certain #s will not work")
            await message.channel.send(embed=embed)



        if message.content == '~weather':
            await self.weather_run('KMAWORCE57', message, True)
        elif message.content.startswith('~weather'):
            message_length = len(message.content.split(" "))
            if message_length == 2:
                code = self.validate_code(message)
                if code == "Invalid code!":
                    await message.channel.send("Invalid code!")
                else:
                    await self.weather_run(code,message,True)
            elif message_length==3 or (message_length == 4 and message.content.split(" ")[-1].upper()=="I"):
                async with aiohttp.ClientSession() as session:
                    if message_length == 3:
                        link = 'https://www.wunderground.com/weather/us/'
                    else:
                        link = 'https://www.wunderground.com/weather/'
                    html = await fetch(session, link+message.content.split(" ")[2]+"/"+message.content.split(" ")[1])
                    soup = BeautifulSoup(html,'html.parser')
                    try:
                        new_code = soup.find("span", attrs = {'class':'station-id'}).text
                        try:
                            new_code = new_code[1:-1]
                            if len(new_code)==4:
                                await message.channel.send("The nearest station is an airport and only a forecast is availible")
                                if message.content.split(" ")[-1].upper()=="I": flag = True
                                else: flag = false
                                await self.forecast_run(message.content.split(" ")[1],message.content.split(" ")[2],flag,message)
                            else:
                                await self.weather_run(new_code,message,True)
                        except IndexError:
                            await message.channel.send("Invalid code!")
                    except AttributeError:
                        await message.channel.send("Invalid code!")
            else:
                await message.channel.send("Invalid code!")





        if message.content == '~simple':
            await self.weather_run('KMAWORCE57', message, False)
        elif message.content.startswith('~simple'):
            code = self.validate_code(message)
            if code == "Invalid code!":
                await message.channel.send("Invalid code!")
            else:
                await self.weather_run(code,message,False)

        if message.content == '~currentTemp':
            await self.temp_run('KMAWORCE57', message)
        elif message.content.startswith('~currentTemp'):
            code = self.validate_code(message)
            if code == "Invalid code!":
                await message.channel.send("Invalid code!")
            else:
                await self.temp_run(code,message)

        if message.content == '~currentWind':
            await self.wind_run('KMAWORCE57', message)
        elif message.content.startswith('~currentWind'):
            code = self.validate_code(message)
            if code == "Invalid code!":
                await message.channel.send("Invalid code!")
            else:
                await self.wind_run(code,message)

        if message.content == '~forecast':
            await self.forecast_run("Worcester","MA",False, False, message,"NULL")
        elif message.content.startswith('~forecast'):
            message_length = len(message.content.split(" "))
            if message.content.split()[-1].upper()=="I":
                flag = True
            else:
                flag = False
            if message_length == 2:
                code = self.validate_code(message)
                print(code)
                if code == "Invalid code!":
                    await message.channel.send("Invalid code!")
                else:
                    await self.forecast_run("Special Case","No Town Provided",flag,True,message,code)
            else:
                town = message.content.split()[1]
                try:
                    state = message.content.split()[2]
                    await self.forecast_run(town,state,flag,False,message,"NULL")
                except IndexError:
                    await message.channel.send("Invalid code!")



async def fetch(session, url):
    async with session.get(url) as response:
        return await response.text()




client = Client()
client.run(TOKEN)
