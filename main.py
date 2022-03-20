import requests
import discord
from discord.ext import commands
from discord.utils import get
import requests
import shutil
from txt_dictbe import txt2dict, kategoriak
from os.path import dirname, abspath
import os

data_dirname = os.path.join(dirname(dirname(abspath(__file__))), 'data')
intents = discord.Intents().all()
bot = commands.Bot(command_prefix='$', intents=intents, help_command=None)
kep_url = "https://i.redd.it/34dnz2hvprl81.jpg"


@bot.event
async def on_ready():
    print('We have logged in as {0.user}'.format(bot))
    # await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name="verem a faszom"))


@bot.command()
async def help(ctx):
    if ctx.message.content[6:] == "adjhozza":
        await ctx.reply("https://streamable.com/sqcgqa")
    else:
        e = discord.Embed(
            title="Commands",
            color=discord.Color.blue())
        e.set_author(
            name="bot", icon_url="https://prod.cloud.rockstargames.com/crews/sc/6874/23970745/publish/emblem/emblem_256.png")
        e.add_field(name=f"**{bot.command_prefix}szabad**",
                    value="megmondja kinek nincs épp órája", inline=False)
        e.add_field(name=f"**{bot.command_prefix}adjhozza**",
                    value=f"hozzáadja az órarendedet az adatbázishoz, bővebben: `{bot.command_prefix}help adjhozza`", inline=False)
        await ctx.send(embed=e)


@bot.command()
async def adjhozza(ctx):
    """hozzáadja az órarendedet az adatbázishoz https://streamable.com/sqcgqa"""
    if len(ctx.message.attachments) == 0:
        await ctx.send("Nem csatoltál semmit")
        await ctx.message.add_reaction('❌')
    elif not ctx.message.attachments[0].filename.endswith('.txt'):
        await ctx.send("Ez nem txt")
        await ctx.message.add_reaction('❌')
    else:
        r = requests.get(ctx.message.attachments[0].url, stream=True)
        if r.status_code == 200:
            r.raw.decode_content = True
            fajlnev = os.path.join(
                data_dirname, f"orarendek/{ctx.message.author}.txt")
            with open(fajlnev, 'wb') as f:
                shutil.copyfileobj(r.raw, f)
        txt2dict(os.path.join(data_dirname, fajlnev), f"{ctx.message.author}")
        await ctx.message.add_reaction('✅')
        print("KÉSZ")


@bot.command()
async def szabad(ctx):
    """megmondja kinek nincs épp órája"""
    z, s, p = kategoriak(ctx.guild.members)
    e = discord.Embed(
        title="Mi a fasz van",
        color=discord.Color.orange())
    e.set_author(
        name="bot", icon_url="https://prod.cloud.rockstargames.com/crews/sc/6874/23970745/publish/emblem/emblem_256.png")
    e.set_thumbnail(url=kep_url)
    if len(z) > 0:
        e.add_field(name=f":sunglasses:**Nincs órája**",
                    value=f"**{', '.join(z)}**", inline=False)
    if len(s) > 0:
        e.add_field(name=f":face_with_raised_eyebrow:**Egy órán belül lesz órája**",
                    value=f"{', '.join(s)}", inline=False)
    if len(p) > 0:
        e.add_field(name=f":face_vomiting:**Órája van**",
                    value=f"{', '.join(p)}", inline=False)

    e.set_footer(text="többiekről nem tudok")
    await ctx.send(embed=e)


@bot.command(hidden=True)
async def ujkep(ctx):
    global kep_url
    if ctx.message.author.id == 413031114446471178:
        kep_url = str(ctx.message.content).split()[1]

with open(os.path.join(data_dirname, "token.txt")) as f:
    token = f.read().rstrip()
bot.run(token)
