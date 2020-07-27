import discord
from discord.ext import commands
from discord.ext.commands import Bot
from discord import FFmpegPCMAudio
import asyncio
import filecmp
from datetime import datetime
from time import time
from urllib.request import *
import sys
from weather_code import Weather
import random

URL = 'https://www.wunderground.com/dashboard/pws/'
weather = Weather()

towns = ["SYC","MICHAEL","MERVE","AUSTIN","IMMI","NORTHRIDGE","SOUTHBOROUGH","HELOTES","BOSTON","NORFOLK","METHUEN","SPRINGFIELD","MOSCOW","BUCHAREST","PASADENA","CHARLTON","SOUTHBRIDGE","LOVELL","AMMAN","WINCHESTER","BOGOTA","WEYMOUTH","LANTANA","MEDIA","PLAINVIEW","MILLIS","SANFERNANDO","NORWELL"]
codes = ["KNHASHLA2","KMDSILVE171","KMDSILVE171","KMAOXFOR33","IBANIJAM2","KCANORTH365","KMASOUTH43","KTXHELOT27","KMABOSTO124","KMANORFO14","KMAMETHU40","KMASPRIN28","IMOSCOW299","IBUCHARE87","KCAPASAD140","KMACHARL47","KMAWESTV8","KMEBRIDG15","IVALLE48","KMAWINCH55","IBOGOT76","KMAWEYMO41","KFLLANTA2","KPAMEDIA30","KNYPLAIN9","KMAMILLI11","ISANFERN13","KMANORWE20"]


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
        response = weather.get_weather(code)
        if response == "THIS STATION DOES NOT EXIST":
            await message.channel.send(response)
        elif response == "THIS STATION IS OFFLINE":
            await message.channel.send(response)
        else:
            global embed_fahrenheit
            embed_fahrenheit=discord.Embed(title="Current Readings for "+response[13]+":", description="Url: " + URL + code+"\n Units: **Imperial** / Metric", color=0x193ed2)
            embed_fahrenheit.add_field(name="Temperature", value=response[0]+"°F", inline=True)
            embed_fahrenheit.add_field(name="Feels Like Temperature", value=response[1]+"°F", inline=True)
            embed_fahrenheit.add_field(name="Dew Point", value=response[5]+"°F", inline=True)
            embed_fahrenheit.add_field(name="Wind Speed", value=response[3]+"mph", inline=True)
            embed_fahrenheit.add_field(name="Wind Gust", value=response[4]+"mph", inline=True)
            embed_fahrenheit.add_field(name="Wind Direction", value=response[2], inline=True)
            embed_fahrenheit.add_field(name="Rainfall Rate", value=response[6]+"in/hr", inline=True)
            embed_fahrenheit.add_field(name="Rainfall Today", value=response[7]+"in", inline=True)
            embed_fahrenheit.add_field(name="Humidity", value=response[8], inline=True)
            if flag:
                embed_fahrenheit.add_field(name="Pressure", value=response[9], inline=True)
                embed_fahrenheit.add_field(name="UV Radiation Value", value=response[10], inline=True)
                embed_fahrenheit.add_field(name="Solar Radiation", value=response[11], inline=True)
            embed_fahrenheit.set_footer(text="Current weather response from station "+code+" at "+response[12])


            global embed_celcius
            embed_celcius=discord.Embed(title="Current Readings for "+response[13]+":", description="Url: " + URL + code+"\n Units: Imperial / **Metric**", color=0x193ed2)
            temperature = str(round(((float(response[0])-32)*5/9),1))
            feels_like = str(round(((float(response[1])-32)*5/9),1))
            dew_point = str(round(((float(response[5])-32)*5/9),1))
            wind_speed = str(round(float(response[3])*1.609344,1))
            wind_gust = str(round(float(response[4])*1.609344,1))
            rainfall_rate = str(round(float(response[6])/0.3937,2))
            rainfall_today = str(round(float(response[7])/0.3937,2))
            embed_celcius.add_field(name="Temperature", value=temperature +"°C", inline=True)
            embed_celcius.add_field(name="Feels Like Temperature", value=feels_like+"°C", inline=True)
            embed_celcius.add_field(name="Dew Point", value=dew_point+"°C", inline=True)
            embed_celcius.add_field(name="Wind Speed", value=wind_speed+"km/h", inline=True)
            embed_celcius.add_field(name="Wind Gust", value=wind_gust+"km/h", inline=True)
            embed_celcius.add_field(name="Wind Direction", value=response[2], inline=True)
            embed_celcius.add_field(name="Rainfall Rate", value=rainfall_rate+"cm/hr", inline=True)
            embed_celcius.add_field(name="Rainfall Today", value=rainfall_today+"cm", inline=True)
            embed_celcius.add_field(name="Humidity", value=response[8], inline=True)
            if flag:
                embed_celcius.add_field(name="Pressure", value=response[9], inline=True)
                embed_celcius.add_field(name="UV Radiation Value", value=response[10], inline=True)
                embed_celcius.add_field(name="Solar Radiation", value=response[11], inline=True)
            embed_celcius.set_footer(text="Current weather response from station "+code+" at "+response[12])



            embed_message = await message.channel.send(embed=embed_fahrenheit)
            reactions_embed = await message.channel.fetch_message(embed_message.id)
            reactions = ['\U0001f1ee','\U0001f1f2']
            for emoji in reactions:
                await reactions_embed.add_reaction(emoji)


    async def forecast_run(self, town, state, flag, message):
        await message.channel.send("Recieved! Town Name: "+town+", "+state+".")
        response = weather.get_forecast(town,state,flag)
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


                global embed_metric
                temperature1 = str(int(round(((float(response[0][2].split()[1])-32)*5/9),0)))
                temperature2 = str(int(round(((float(response[1][2].split()[1])-32)*5/9),0)))
                temperature3 = str(int(round(((float(response[2][2].split()[1])-32)*5/9),0)))
                rain1 = response[0][3].split("/")[0]+"/ "+str(round(float(response[0][3].split(" ")[3].split('\xa0')[0])/0.3937,2))
                rain2 = response[1][3].split("/")[0]+"/ "+str(round(float(response[1][3].split(" ")[3].split('\xa0')[0])/0.3937,2))
                rain3 = response[2][3].split("/")[0]+"/ "+str(round(float(response[2][3].split(" ")[3].split('\xa0')[0])/0.3937,2))
                embed_metric =discord.Embed(title="Forecast", description="Current forecast for "+response[4]+"."+"\n Units: Imperial / **Metric**", color=0x002aff)
                embed_metric.add_field(name=response[0][0], value=response[0][1], inline=True)
                embed_metric.add_field(name=response[0][2].split()[0], value=temperature1+"°C", inline=True)
                embed_metric.add_field(name="Rain Chance / Amount", value=rain1+" cm", inline=True)
                embed_metric.add_field(name="Description", value=response[0][4], inline=False)
                embed_metric.add_field(name=response[1][0], value=response[1][1], inline=True)
                embed_metric.add_field(name=response[1][2].split()[0], value=temperature2+"°C", inline=True)
                embed_metric.add_field(name="Rain Chance / Amount", value=rain2+" cm", inline=True)
                embed_metric.add_field(name="Description", value=response[1][4], inline=False)
                embed_metric.add_field(name=response[2][0], value=response[2][1], inline=True)
                embed_metric.add_field(name=response[2][2].split()[0], value=temperature3+"°C", inline=True)
                embed_metric.add_field(name="Rain Chance / Amount", value=rain3+" cm", inline=True)
                embed_metric.add_field(name="Description", value=response[2][4], inline=True)
                embed_metric.set_footer(text="Local Time: "+response[3])

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
        response = weather.get_temp(code)
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
        station_code = message.content.split()[1]
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
                await reaction.message.edit(embed=embed_celcius)
        if reaction.emoji == '\U0001f1ee' and user.id != 731989043713146990:
            if reaction.message.author.id == 731989043713146990:
                await reaction.message.edit(embed=embed_fahrenheit)
        if reaction.emoji == '\U0001f1eb' and user.id != 731989043713146990:
            if reaction.message.author.id == 731989043713146990:
                await reaction.message.edit(embed=embed_imperial)
        if reaction.emoji == '\U0001f1e8' and user.id != 731989043713146990:
            if reaction.message.author.id == 731989043713146990:
                await reaction.message.edit(embed=embed_metric)

    async def on_reaction_add(self,reaction, user):
        await self.edit_message(reaction,user)

    async def on_reaction_remove(self,reaction, user):
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
            code = self.validate_code(message)
            if code == "Invalid code!":
                await message.channel.send("Invalid code!")
            else:
                await self.weather_run(code,message,True)


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
            await self.forecast_run("Worcester","MA",False, message)
        elif message.content.startswith('~forecast'):
            if message.content.split()[-1].upper()=="I":
                flag = True
            else:
                flag = False
            town = message.content.split()[1]
            try:
                state = message.content.split()[2]
                await self.forecast_run(town,state,flag,message)
            except IndexError:
                await message.channel.send("Invalid code!")







client = Client()
client.run(TOKEN)
