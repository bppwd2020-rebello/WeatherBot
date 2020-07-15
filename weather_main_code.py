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

towns = ["SYC","MICHAEL","AUSTIN","IMMI","NORTHRIDGE","SOUTHBOROUGH","HELOTES","BOSTON","NORFOLK","METHUEN","SPRINGFIELD","MOSCOW","BUCHAREST","PASADENA","CHARLTON","SOUTHBRIDGE","LOVELL","AMMAN","WINCHESTER","BOGOTA","WEYMOUTH","LANTANA"]
codes = ["KNHPLYMO6","KMDSILVE171","KMAOXFOR33","IBANIJAM2","KCANORTH365","KMASOUTH43","KTXHELOT27","KMABOSTO124","KMANORFO14","KMAMETHU40","KMASPRIN28","IMOSCOW299","IBUCHARE87","KCAPASAD140","KMACHARL47","KMAWESTV8","KMEBRIDG15","IVALLE48","KMAWINCH55","IBOGOT76","KMAWEYMO41","KFLLANTA2"]


TOKEN = ""

with open("token.txt", 'r') as f:
    TOKEN = f.readline()




class Client(discord.Client):
    def __init__(self):
        super().__init__()
        self.voice = None
        self.channel = None
        self.roles = {
            "mod": 699644834629288007,
            "hipster": 710844902585532416
        }
        self.user_ids = {
            "grant": 454052089979600897,
            "elisabeth": 696911603068829836
        }
        self.channel = "Weather Channel"

    #Ben helped me fix this method, credit given
    async def weather_run(self, code, message, flag):
        await message.channel.send("Recieved! Station Code: " + code + ".")
        response = weather.get_weather(code)
        if response == "THIS STATION DOES NOT EXIST":
            await message.channel.send(response)
        elif response == "THIS STATION IS OFFLINE":
            await message.channel.send(response)
        else:
            embed=discord.Embed(title="Current Readings for "+response[13]+":", description="Url: " + URL + code, color=0x193ed2)
            embed.add_field(name="Temperature", value=response[0], inline=True)
            embed.add_field(name="Feels Like Temperature", value=response[1], inline=True)
            embed.add_field(name="Dew Point", value=response[5], inline=True)
            embed.add_field(name="Wind Speed", value=response[3], inline=True)
            embed.add_field(name="Wind Gust", value=response[4], inline=True)
            embed.add_field(name="Wind Direction", value=response[2], inline=True)
            embed.add_field(name="Rainfall Rate", value=response[6], inline=True)
            embed.add_field(name="Rainfall Today", value=response[7], inline=True)
            embed.add_field(name="Humidity", value=response[8], inline=True)
            if flag:
                embed.add_field(name="Pressure", value=response[9], inline=True)
                embed.add_field(name="UV Radiation Value", value=response[10], inline=True)
                embed.add_field(name="Solar Radiation", value=response[11], inline=True)
            embed.set_footer(text="Current weather response from station "+code+" at "+response[12])
            await message.channel.send(embed=embed)

    async def forecast_run(self, code, message):
        await message.channel.send("Recieved! Station Code: " + code + ".")
        response = weather.get_forecast(code)
        #print(response)
        if response == "THIS FORECAST DOES NOT EXIST":
            await message.channel.send(response)
        else:
            embed=discord.Embed(title="Forecast", description="Current forecast for "+response[4]+".", color=0x002aff)
            embed.add_field(name=response[0][0], value=response[0][1], inline=True)
            embed.add_field(name=response[0][2].split()[0], value=response[0][2].split()[1]+"°F", inline=True)
            embed.add_field(name="Rain Chance / Amount", value=response[0][3], inline=True)
            embed.add_field(name="Description", value=response[0][4], inline=False)
            embed.add_field(name=response[1][0], value=response[1][1], inline=True)
            embed.add_field(name=response[1][2].split()[0], value=response[1][2].split()[1]+"°F", inline=True)
            embed.add_field(name="Rain Chance / Amount", value=response[1][3], inline=True)
            embed.add_field(name="Description", value=response[1][4], inline=False)
            embed.add_field(name=response[2][0], value=response[2][1], inline=True)
            embed.add_field(name=response[2][2].split()[0], value=response[2][2].split()[1]+"°F", inline=True)
            embed.add_field(name="Rain Chance / Amount", value=response[2][3], inline=True)
            embed.add_field(name="Description", value=response[2][4], inline=True)
            embed.set_footer(text="Local Time: "+response[3])
            await message.channel.send(embed=embed)

    async def on_ready(self):
        print('Logged on as', self.user)

        await self.change_presence(activity=discord.Game("~help to use me!"));


    async def on_message(self, message):

        if message.author == self.user:
            return
        
        # ping (Grant's command I took)
        if message.content.startswith('~ping'):
            before = time()
            await message.channel.send('Pong!')
            ms = (time() - before) * 1000
            await message.channel.send('Ping took: {}ms'.format(int(ms)))

        if message.content == '~help':
            embed=discord.Embed(title="Help:", description="All the commands currently callable for the bot.", color=0x193ed2)
            embed.add_field(name="~ping", value="Tests the latency to the bot", inline=False)
            embed.add_field(name="~weather ***code*** (see ~code)", value="Gives the current weather conditions of a specific location", inline=False)
            embed.add_field(name="~forecast ***code*** (see ~code)", value="Gives you the forecast of a specific location", inline=False)
            embed.add_field(name="~code", value="Tells you how to input a correct code", inline=False)
            embed.add_field(name="~weather or ~weather WPI", value="Gives you the current weather at WPI", inline=False)
            embed.add_field(name="~forecast or ~forecast WPI", value="Gives you the forecast for WPI", inline=False)
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





        flag = False
        if message.content == '~weather':
            await self.weather_run('KMAWORCE57', message, True)
        elif message.content.startswith('~weather'):
            station_code = message.content.split()[1]
            for i, town in enumerate(towns):
                if station_code.upper() == town:
                    await self.weather_run(codes[i], message, True)
                    flag = True
            if not flag:
                if station_code.upper() == 'WPI':
                    await self.weather_run('KMAWORCE57', message, True)
                elif len(station_code)>11:
                    await message.channel.send("Invalid code!")
                elif len(station_code)<7:
                    await message.channel.send("Invalid code!")
                else:
                    await self.weather_run(station_code, message, True)

        if message.content == '~simple':
            await self.weather_run('KMAWORCE57', message, False)
        elif message.content.startswith('~simple'):
            station_code = message.content.split()[1]
            for i, town in enumerate(towns):
                if station_code.upper() == town:
                    await self.weather_run(codes[i], message, False)
                    flag = True
            if not flag:
                if station_code.upper() == 'WPI':
                    await self.weather_run('KMAWORCE57', message, False)
                elif len(station_code)>11:
                    await message.channel.send("Invalid code!")
                elif len(station_code)<7:
                    await message.channel.send("Invalid code!")
                else:
                    await self.weather_run(station_code, message, False)

        if message.content == '~forecast':
            await self.forecast_run('KMAWORCE57', message)
        elif message.content.startswith('~forecast'):
            forecast_flag = False
            station_code = message.content.split()[1]
            for i, town in enumerate(towns):
                if station_code.upper() == town:
                    forecast_flag = True
                    await self.forecast_run(codes[i], message)
            if not forecast_flag:
                try:
                    print(int(station_code[-1]))
                except ValueError as err:
                    station_code = "1"
                if station_code.upper() == 'WPI':
                    await self.forecast_run('KMAWORCE57', message)
                elif len(station_code)>11:
                    await message.channel.send("Invalid code!")
                elif len(station_code)<7:
                    await message.channel.send("Invalid code!")
                else:
                    await self.forecast_run(station_code, message)







client = Client()
client.run(TOKEN)
