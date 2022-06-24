# Version - v1.0.4
import discord
import requests
import json
from discord.ext import commands
from datetime import datetime

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


# Make sure to tick the check that says server members intent on the bot tab in the developer panel.
intents = discord.Intents.default()
intents.members = True

bot = commands.Bot(command_prefix='wtb ', help_command=None, intents=intents)


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
        'https://api.worldtobuild.com/WebService/Player/FetchPlayerDataById?PlayerID=' + userid).json()

    # If the request was invalid
    if r["Success"] == False:
        embed = discord.Embed(title="Lookup", color=0xf40b0b)
        embed.set_author(name="World To Build Bot",
                         icon_url="https://cdn.discordapp.com/attachments/687762794661281864/943268414196178994/bubble-spirit-red.png",)
        embed.add_field(
            name="❌Error", value="User not found.", inline=False)

        # Reply with embed
        await ctx.reply(embed=embed)

    # If the request was successful
    elif r["Success"] == True:

        # Embed settings
        embed = discord.Embed(title="Lookup", color=0xf40b0b)
        embed.set_author(name="World To Build Bot",
                         icon_url="https://cdn.discordapp.com/attachments/687762794661281864/943268414196178994/bubble-spirit-red.png")
        embed.set_thumbnail(url=r['Data']['CharacterHeadshot'])

        # Embed fields
        if r['Data']["Username"] == None or r['Data']["Username"] == "":
            embed.add_field(name="Username",
                            value="No Username", inline=False)
        else:
            embed.add_field(name="Username",
                            value=r['Data']["Username"], inline=False)

        if r['Data']["Nickname"] == None or r['Data']["Nickname"] == "":
            embed.add_field(name="Nickname",
                            value="No Nickname", inline=False)
        else:
            embed.add_field(name="Nickname",
                            value=r['Data']["Nickname"], inline=False)

        if r['Data']["About"] == None or r['Data']["About"] == "":
            embed.add_field(name="About", value="No About", inline=False)
        else:
            embed.add_field(
                name="About", value=r['Data']["About"], inline=False)

        if r['Data']["RegisterDate"] == None or r['Data']["RegisterDate"] == "":
            embed.add_field(name="RegisterDate",
                            value="Error", inline=False)
        else:
            embed.add_field(name="Register Date",
                            value=r['Data']["RegisterDate"], inline=False)

        if r['Data']["LastOnline"] == None or r['Data']["LastOnline"] == "":
            embed.add_field(name="LastOnline", value="Cannot find Last Online", inline=False)
        else:
            embed.add_field(
                name="Last Online", value=r['Data']["LastOnline"], inline=False)

        if r['Data']["IsMembership"] == None or r['Data']["IsMembership"] == "":
            embed.add_field(name="IsMembership", value="Cannot find Membership", inline=False)
        else:
            embed.add_field(
                name="Membership", value=r['Data']["IsMembership"], inline=False)

        if r['Data']["MembershipLevel"] == None or r['Data']["MembershipLevel"] == "":
            embed.add_field(name="Membership Level", value="None", inline=False)
        else:
            embed.add_field(
                name="Membership Level", value=r['Data']["MembershipLevel"], inline=False)

        embed.add_field(
            name="Link", value="https://worldtobuild.com/user/" + userid + "/profile", inline=False)

        # Reply with embed
        await ctx.reply(embed=embed)


# Design command
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
                         icon_url="https://cdn.discordapp.com/attachments/687762794661281864/943268414196178994/bubble-spirit-red.png")
        embed.add_field(
            name="❌Error", value="Design not found.", inline=False)
        await ctx.reply(embed=embed)

    # If the request was successful
    elif r["Success"] == True:

        # Embed settings
        embed = discord.Embed(title="Design", color=0xf40b0b)
        embed.set_author(name="World To Build Bot",
                         icon_url="https://cdn.discordapp.com/attachments/687762794661281864/943268414196178994/bubble-spirit-red.png")

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


# World command
@bot.command()
async def world(ctx, arg):
    gameid = arg
    # Sends a request to the WTB API for a worlds data
    r = requests.get(
        'https://api.worldtobuild.com/WebService/World/FetchWorldDataById?WorldID=' + gameid).json()

    # If the request was invalid
    if r["Success"] == False:
        embed = discord.Embed(title="World", color=0xf40b0b)
        embed.set_author(name="World To Build Bot",
                         icon_url="https://cdn.discordapp.com/attachments/687762794661281864/943268414196178994/bubble-spirit-red.png",)
        embed.add_field(
            name="❌Error", value="World not found.", inline=False)

        # Reply with embed
        await ctx.reply(embed=embed)

    # If the request was successful
    elif r["Success"] == True:

        # Embed settings
        embed = discord.Embed(title="World", color=0xf40b0b)
        embed.set_author(name="World To Build Bot",
                         icon_url="https://cdn.discordapp.com/attachments/687762794661281864/943268414196178994/bubble-spirit-red.png")
        embed.set_thumbnail(url=r['Data']['Preview'])

        # Embed fields

        if r['Data']["Name"] == None or r['Data']["Name"] == "":
            embed.add_field(name="Name",
                            value="No Name", inline=False)
        else:
            embed.add_field(name="Name",
                            value=r['Data']["Name"], inline=False)

        if r['Data']["About"] == None or r['Data']["About"] == "":
            embed.add_field(name="About",
                            value="No About", inline=False)
        else:
            embed.add_field(name="About",
                            value=str(r['Data']["About"]), inline=False)

        if r['Data']["OwnerID"] == None or r['Data']["OwnerID"] == "":
            embed.add_field(name="Owner", value="No Owner", inline=False)
        else:

            req = requests.get(
                'https://worldtobuild.com/api/user/FetchProfilePreview?UserID=' + str(r['Data']['OwnerID'])).json()

        if r['Data']["OwnerUsername"] == None or r['Data']["OwnerUsername"] == "":
            embed.add_field(name="Owner",
                            value="No Owner", inline=False)
        else:
            embed.add_field(name="Owner",
                            value=r['Data']['OwnerUsername'], inline=False)

        if r['Data']["TotalPlays"] == None or r['Data']["TotalPlays"] == "":
            embed.add_field(name="TotalPlays",
                            value="No Visits", inline=False)
        else:
            embed.add_field(name="Total Plays",
                            value=r['Data']['TotalPlays'], inline=False)

        if r['Data']["CreationDate"] == None or r['Data']["CreationDate"] == "":
            embed.add_field(name="Creation Date",
                            value="No Creation Date", inline=False)
        else:
            embed.add_field(name="Creation Date",
                            value=r['Data']['CreationDate'], inline=False)

                            
        if r['Data']["LastUpdated"] == None or r['Data']["LastUpdated"] == "":
            embed.add_field(name="Last Updated",
                            value="No Last Updated", inline=False)
        else:
            embed.add_field(name="Last Updated",
                            value=r['Data']['LastUpdated'], inline=False)

        if r['Data']["Public"] == None or r['Data']["Public"] == "":
            embed.add_field(name="Public",
                            value="No Public", inline=False)
        else:
            embed.add_field(name="Public",
                            value=r['Data']['Public'], inline=False)

        if r['Data']["AllowsComments"] == None or r['Data']["AllowsComments"] == "":
            embed.add_field(name="AllowsComments",
                            value="No Public", inline=False)
        else:
            embed.add_field(name="Comments Allowed",
                            value=r['Data']['AllowsComments'], inline=False)

        if r['Data']["Featured"] == None or r['Data']["Featured"] == "":
            embed.add_field(name="Featured",
                            value="No Feature", inline=False)
        else:
            embed.add_field(name="Featured",
                            value=r['Data']['Featured'], inline=False)

        embed.add_field(
            name="Link", value="https://worldtobuild.com/worlds/" + gameid + "/play", inline=False)

        # Reply with embed
        await ctx.reply(embed=embed)


        # Club command
@bot.command()
async def club(ctx, arg):
    clubid = arg
    # Sends a request to the WTB API for a worlds data
    r = requests.get(
        'https://api.worldtobuild.com/WebService/Club/FetchClubDataById?ClubID=' + clubid).json()

    # If the request was invalid
    if r["Success"] == False:
        embed = discord.Embed(title="Clubs", color=0xf40b0b)
        embed.set_author(name="World To Build Bot",
                         icon_url="https://cdn.discordapp.com/attachments/687762794661281864/943268414196178994/bubble-spirit-red.png",)
        embed.add_field(
            name="❌Error", value="Club not found.", inline=False)

        # Reply with embed
        await ctx.reply(embed=embed)

    # If the request was successful
    elif r["Success"] == True:

        # Embed settings
        embed = discord.Embed(title="Clubs", color=0xf40b0b)
        embed.set_author(name="World To Build Bot",
                         icon_url="https://cdn.discordapp.com/attachments/687762794661281864/943268414196178994/bubble-spirit-red.png")
        embed.set_thumbnail(url=r['Data']['Emblem'])

        # Embed fields

        if r['Data']["Name"] == None or r['Data']["Name"] == "":
            embed.add_field(name="Name",
                            value="No Name", inline=False)
        else:
            embed.add_field(name="Name",
                            value=r['Data']["Name"], inline=False)

        if r['Data']["About"] == None or r['Data']["About"] == "":
            embed.add_field(name="About",
                            value="No About", inline=False)
        else:
            embed.add_field(name="About",
                            value=str(r['Data']["About"]), inline=False)

        if r['Data']["OwnerID"] == None or r['Data']["OwnerID"] == "":
            embed.add_field(name="Owner", value="Error", inline=False)
        else:

            req = requests.get(
                'https://worldtobuild.com/api/user/FetchProfilePreview?UserID=' + str(r['Data']['OwnerID'])).json()

        if r['Data']["CreationDate"] == None or r['Data']["CreationDate"] == "":
            embed.add_field(name="CreationDate",
                            value="No Creation Date", inline=False)
        else:
            embed.add_field(name="Creation Date",
                            value=r['Data']['CreationDate'], inline=False)

        if r['Data']["LastUpdated"] == None or r['Data']["LastUpdated"] == "":
            embed.add_field(name="Last Updated",
                            value="No Last Updated", inline=False)
        else:
            embed.add_field(name="Last Updated",
                            value=r['Data']['LastUpdated'], inline=False)
                            
        if r['Data']["OwnerUsername"] == None or r['Data']["OwnerUsername"] == "":
            embed.add_field(name="OwnerUsername",
                            value="Error", inline=False)
        else:
            embed.add_field(name="Owner",
                            value=r['Data']['OwnerUsername'], inline=False)

        if r['Data']["MemberCount"] == None or r['Data']["MemberCount"] == "":
            embed.add_field(name="MemberCount",
                            value=r['Data']['MemberCount'], inline=False)
        else:
            embed.add_field(name="Members Count",
                            value=r['Data']['MemberCount'], inline=False)

        if r['Data']["JoinType"] == None or r['Data']["JoinType"] == "":
            embed.add_field(name="JoinType",
                            value=r['Data']['JoinType'], inline=False)
        else:
            embed.add_field(name="Join Type",
                            value=r['Data']['JoinType'], inline=False)

        if r['Data']["VerificationIcon"] == None or r['Data']["VerificationIcon"] == "":
            embed.add_field(name="VerificationIcon",
                            value=r['Data']['VerificationIcon'], inline=False)
        else:
            embed.add_field(name="Verified",
                            value=r['Data']['VerificationIcon'], inline=False)

        embed.add_field(
            name="Link", value="https://worldtobuild.com/clubs/" + clubid, inline=False)

        # Reply with embed
        await ctx.reply(embed=embed)


# Ping command
@bot.command()
async def ping(ctx):
    ping = f" {round(bot.latency * 1000)}ms"

    embed = discord.Embed(title="Bot Latency", color=0xf40b0b)
    embed.set_author(name="World To Build Bot",
                     icon_url="https://cdn.discordapp.com/attachments/687762794661281864/943268414196178994/bubble-spirit-red.png")
    embed.add_field(name="Ping", value=ping, inline=False)
    await ctx.reply(embed=embed)


# Serverinfo command
@bot.command()
async def serverinfo(ctx):
    name = str(ctx.guild.name)
    description = str(ctx.guild.description)

    owner = str(ctx.guild.owner)
    id = str(ctx.guild.id)
    memberCount = str(ctx.guild.member_count)

    icon = str(ctx.guild.icon_url)

    embed = discord.Embed(
        title=name + " Server Information",
        description=description,
        color=0xf40b0b
    )
    embed.set_thumbnail(url=icon)
    embed.add_field(name="Owner", value=owner, inline=False)
    embed.add_field(name="Server ID", value=id, inline=False)
    embed.add_field(name="Members", value=memberCount, inline=False)

    await ctx.send(embed=embed)


# Help command
@bot.command(name="help")
async def _help(ctx):
    embed = discord.Embed(title="Help", color=0xf40b0b)
    embed.set_author(name="World To Build Bot",
                     icon_url="https://cdn.discordapp.com/attachments/687762794661281864/943268414196178994/bubble-spirit-red.png")
    embed.add_field(
        name="About", value="This is the official WorldToBuild Bot made by #Toad, and more!", inline=False)

    embed.add_field(
        name="wtb lookup (**USERID**)", value="Returns a users profile data.", inline=False)

    embed.add_field(
        name="wtb design (**DESIGNID**)", value="Returns a designs data.", inline=False)

    embed.add_field(
        name="wtb world (**WORLDID**)", value="Returns a worlds data.", inline=False)
        
    embed.add_field(
        name="wtb club (**CLUBID**)", value="Returns a clubs data.", inline=False)

    embed.add_field(
        name="wtb help", value="Returns some information about the bot.", inline=False)

    embed.add_field(
        name="wtb ping", value="Returns the bot latency.", inline=False)

    embed.add_field(
        name="wtb serverinfo", value="Returns some information on the server.", inline=False)

    embed.add_field(
        name="GitHub", value="https://github.com/toadpen/world-to-build-bot", inline=False)

    # Reply with embed
    await ctx.reply(embed=embed)

bot.run(token)