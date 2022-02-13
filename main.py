# Version - v1.0.2
import discord
from discord.ext import commands
import requests
import json

# If you want to run this bot yourself, you can either make a token.json
# file and make a value called "token",
# Then leave this code and it should work.
# --------
# If you arent in danger of exposing your token,
# you can just replace those 3 token lines below with
# --------
# token = "Your token here"
# --------


# Importing token from token.json file. I did this so you cant see the bot token im using.
tokenfile = open('token.json')
tokenjson = json.load(tokenfile)
token = tokenjson['token']

bot = commands.Bot(command_prefix='wtb ', help_command=None)


@bot.event
async def on_ready():
    # Changes the bot presence to "Listening to WTB Users👍"
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name="WTB Users👍"))
    print(f'{bot.user} has connected to Discord!')


@bot.command()
async def lookup(ctx, arg):
    userid = arg
    # Sends a request to the WTB API for a users profile data
    r = requests.get(
        'https://worldtobuild.com/api/user/FetchProfilePreview?UserID=' + userid).json()

    # If the request was invalid
    if r["Success"] == False:
        embed = discord.Embed(title="Lookup", color=0xf40b0b)
        embed.set_author(name="World To Build Bot",
                         icon_url="https://github.com/toadpen/world-to-build-bot/blob/master/world-to-build-logo-main-300x300.png?raw=true",)
        embed.add_field(
            name="❌Error", value="User not found.", inline=False)

        # Reply with embed
        await ctx.reply(embed=embed)

    # If the request was successful
    elif r["Success"] == True:

        # Embed settings
        embed = discord.Embed(title="Lookup", color=0xf40b0b)
        embed.set_author(name="World To Build Bot",
                         icon_url="https://github.com/toadpen/world-to-build-bot/blob/master/world-to-build-logo-main-300x300.png?raw=true")
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

        embed.add_field(
            name="Link", value="https://worldtobuild.com/user/" + userid + "/profile", inline=False)

        # Reply with embed
        await ctx.reply(embed=embed)


@bot.command()
async def design(ctx, arg):

    assetid = arg

    # Sends a request to the WTB API for specific asset data
    r = requests.get(
        'https://www.worldtobuild.com/api/marketplace/GetDesignDataById?AssetID=' + assetid).json()

    # If the request was invalid
    if r["Success"] == False:
        embed = discord.Embed(title="Design", color=0xf40b0b)
        embed.set_author(name="World To Build Bot",
                         icon_url="https://github.com/toadpen/world-to-build-bot/blob/master/world-to-build-logo-main-300x300.png?raw=true")
        embed.add_field(
            name="❌Error", value="Design not found.", inline=False)
        await ctx.reply(embed=embed)

    # If the request was successful
    elif r["Success"] == True:

        # Embed settings
        embed = discord.Embed(title="Design", color=0xf40b0b)
        embed.set_author(name="World To Build Bot",
                         icon_url="https://github.com/toadpen/world-to-build-bot/blob/master/world-to-build-logo-main-300x300.png?raw=true")

        # Embed fields
        if r['Name'] == None or r['Name'] == "":
            embed.add_field(name="Name",
                            value="No Name", inline=False)
        else:
            embed.add_field(name="Name",
                            value=r['Name'], inline=False)

        if r['Description'] == None or r['Description'] == "":
            embed.add_field(name="Description",
                            value="No Description", inline=False)
        else:
            embed.add_field(name="Description",
                            value=r['Description'], inline=False)

        if r['Rating'] == None or r['Rating'] == "":
            embed.add_field(name="Rating",
                            value="No Rating", inline=False)
        else:
            embed.add_field(name="Rating",
                            value=r['Rating'], inline=False)

        embed.add_field(
            name="Link", value="https://worldtobuild.com/community/designs/" + assetid, inline=False)

    # Reply with embed
    await ctx.reply(embed=embed)


# Help command
@bot.command(name="help")
async def _help(ctx):
    embed = discord.Embed(title="Help", color=0xf40b0b)
    embed.set_author(name="World To Build Bot",
                     icon_url="https://github.com/toadpen/world-to-build-bot/blob/master/world-to-build-logo-main-300x300.png?raw=true")
    embed.add_field(
        name="About", value="World To Build Bot is an unofficial WTB discord bot. There are currently 3 commands.", inline=False)

    embed.add_field(
        name="wtb lookup (**USERID**)", value="Returns the selected users profile data.", inline=False)

    embed.add_field(
        name="wtb design (**DESIGNID**)", value="Returns the selected designs data.", inline=False)

    embed.add_field(
        name="wtb help", value="Returns some information about the bot.", inline=False)

    embed.add_field(
        name="Github", value="https://github.com/toadpen/world-to-build-bot", inline=False)

    # Reply with embed
    await ctx.reply(embed=embed)

@bot.command()
async def ping(ctx: commands.Context):
    await ctx.send(f"Pong, server-wide latency is {round(bot.latency * 1000)}ms")
    
bot.run(token)
