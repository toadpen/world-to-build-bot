import discord
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

client = discord.Client()


# On bot startup
@client.event
async def on_ready():
    # Changes the bot presence to "Listening to WTB Users👍"
    await client.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name="WTB Users👍"))
    print(f'{client.user} has connected to Discord!')

# On message sent in discord


@client.event
async def on_message(message):
    if message.author == client.user:
        return

    # If the message content startswith "wtb lookup"
    if message.content.startswith("wtb lookup"):

        # Splits the message into "wtb lookup " and the UserId the user inputted
        rawmsg = message.content
        splitted = rawmsg.split("lookup ")
        userid = splitted[1]

        # Sends a request to the WTB API for a users profile data
        r = requests.get(
            'https://worldtobuild.com/api/user/FetchProfilePreview?UserID=' + userid).json()

        # If the request was invalid
        if r["Success"] == False:
            embed = discord.Embed(title="Lookup", color=0xf40b0b)
            embed.set_author(name="World To Build Bot")
            embed.add_field(
                name="❌Error", value="User not found.", inline=False)
            await message.reply(embed=embed)

        # If the request was successful
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
