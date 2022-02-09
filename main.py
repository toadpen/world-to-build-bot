import discord
import requests
import json
from discord_webhook import *

tokenfile = open('token.json')

tokenjson = json.load(tokenfile)

token = tokenjson['token']

client = discord.Client()


@client.event
async def on_ready():
    print(f'{client.user} has connected to Discord!')


@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith("w2b lookup"):
        rawmsg = message.content
        splitted = rawmsg.split("lookup ")
        userid = splitted[1]

        r = requests.get(
            'https://worldtobuild.com/api/user/FetchProfilePreview?UserID=' + userid).json()

        if r["Success"] == False:
            embed = discord.Embed(title="Lookup", color=0xf40b0b)
            embed.set_author(name="World To Build Bot")
            embed.add_field(
                name="❌Error", value="User not found.", inline=False)
            await message.reply(embed=embed)

        elif r["Success"] == True:

            # Embed settings
            embed = discord.Embed(title="Lookup", color=0xf40b0b)
            embed.set_author(name="World To Build Bot")
            embed.set_thumbnail(url=r['Data']['Headshot'])

            # Embed fields

            if r['Data']["UserName"] == None or r['Data']["UserName"] == "":
                embed.add_field(name="Username",
                                value="No Username", inline=False)
            else:
                embed.add_field(name="Username",
                                value=r['Data']["UserName"], inline=False)

            if r['Data']["NickName"] == None or r['Data']["NickName"] == "":
                embed.add_field(name="Nickname",
                                value="No Nickname", inline=False)
            else:
                embed.add_field(name="Nickname",
                                value=r['Data']["NickName"], inline=False)

            if r['Data']["Blurb"] == None or r['Data']["Blurb"] == "":
                embed.add_field(name="About", value="No About", inline=False)
            else:
                embed.add_field(
                    name="About", value=r['Data']["Blurb"], inline=False)

            # Reply to message with embed
            await message.reply(embed=embed)

client.run(token)
