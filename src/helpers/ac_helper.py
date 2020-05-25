import discord
import requests
import json

def getVillagerEmbed(id):
    resp = requests.get('http://acnhapi.com/v1/villagers/' + str(id))
    if resp.ok:
        embed = discord.Embed(title=resp.json()["name"]["name-USen"], color=0xA7D2A4)
        embed.set_thumbnail(url=resp.json()["image_uri"])
        embed.add_field(name="Personality", value=resp.json()["personality"], inline=True)
        embed.add_field(name="Species", value=resp.json()["species"], inline=True)
        embed.add_field(name="Gender", value=resp.json()["gender"], inline=True)
        embed.add_field(name="Birthday", value=resp.json()["birthday-string"], inline=True)
        embed.add_field(name="Catchphrase", value=resp.json()["catch-phrase"], inline=False)

        return embed


def getSongEmbed(id):
    resp = requests.get('http://acnhapi.com/v1/songs/' + str(id))
    if resp.ok:
        embed = discord.Embed(title=resp.json()["name"]["name-USen"], color=0xA7D2A4)
        embed.set_thumbnail(url=resp.json()["image_uri"])
        embed.add_field(name="Buy Price", value=resp.json()["buy-price"], inline=True)
        embed.add_field(name="Sell Price", value=resp.json()["sell-price"], inline=True)

        if resp.json()["isOrderable"]:
            embed.add_field(name="Orderable", value="Yes", inline=True)
            embed.add_field(name="Orderable", value="No", inline=True)

        name = resp.json()["name"]["name-USen"]
        musicLink = resp.json()["music_uri"]
        embed.add_field(name="Link to MP3", value=f"[{name}]({musicLink})")

        return embed



def getFishEmbed(id):
    resp = requests.get('http://acnhapi.com/v1/fish/' + str(id))
    if resp.ok:
        embed = discord.Embed(title=resp.json()["name"]["name-USen"], color=0xA7D2A4)
        embed.set_thumbnail(url=resp.json()["icon_uri"])

        embed.add_field(name="Rarity", value=resp.json()["availability"]["rarity"], inline=True)
        embed.add_field(name="Price", value=resp.json()["price"], inline=True)
        embed.add_field(name="Price (C.J.)", value=resp.json()["price-cj"], inline=True)

        if not resp.json()["availability"]["isAllYear"]:
            embed.add_field(name="Northern Hemisphere months", value=resp.json()["availability"]["month-northern"], inline=True)
            embed.add_field(name="Southern Hemisphere months", value=resp.json()["availability"]["month-southern"], inline=True)
        else:
            embed.add_field(name="Availability", value="All Year", inline=True)

        if not resp.json()["availability"]["isAllDay"]:
            embed.add_field(name="Times", value=resp.json()["availability"]["time"], inline=True)
        else:
            embed.add_field(name="Times", value="All Day", inline=True)

        embed.add_field(name="Location", value=resp.json()["availability"]["location"], inline=True)
        embed.add_field(name="Catchphrase", value=resp.json()["catch-phrase"], inline=True)
        embed.add_field(name="Museum phrase", value=resp.json()["museum-phrase"], inline=False)

        return embed


def getBugEmbed(id):
    resp = requests.get('http://acnhapi.com/v1/bugs/' + str(id))
    if resp.ok:
        embed = discord.Embed(title=resp.json()["name"]["name-USen"], color=0xA7D2A4)
        embed.set_thumbnail(url=resp.json()["icon_uri"])

        embed.add_field(name="Rarity", value=resp.json()["availability"]["rarity"], inline=True)
        embed.add_field(name="Price", value=resp.json()["price"], inline=True)
        embed.add_field(name="Price (Flick)", value=resp.json()["price-flick"], inline=True)


        if not resp.json()["availability"]["isAllYear"]:
            embed.add_field(name="Northern Hemisphere months", value=resp.json()["availability"]["month-northern"], inline=True)
            embed.add_field(name="Southern Hemisphere months", value=resp.json()["availability"]["month-southern"], inline=True)
        else:
            embed.add_field(name="Availability", value="All Year", inline=True)

        if not resp.json()["availability"]["isAllDay"]:
            embed.add_field(name="Times", value=resp.json()["availability"]["time"], inline=True)
        else:
            embed.add_field(name="Times", value="All Day", inline=True)

        embed.add_field(name="Location", value=resp.json()["availability"]["location"], inline=True)
        embed.add_field(name="Catchphrase", value=resp.json()["catch-phrase"], inline=True)
        embed.add_field(name="Museum phrase", value=resp.json()["museum-phrase"], inline=False)

        return embed


def getFossilEmbed(name):
    resp = requests.get('http://acnhapi.com/v1/fossils/' + name.replace(" ", "_").lower())
    if resp.ok:
        embed = discord.Embed(title=resp.json()["name"]["name-USen"], color=0xA7D2A4)
        embed.set_thumbnail(url=resp.json()["image_uri"])
        embed.add_field(name="Price", value=resp.json()["price"], inline=True)
        embed.add_field(name="Museum phrase", value=resp.json()["museum-phrase"], inline=False)
        return embed
