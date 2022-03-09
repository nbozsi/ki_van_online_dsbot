import requests
import discord
from discord.ext import commands
import requests
import shutil
from txt_dictbe import txt2dict
import os
dirname = os.path.dirname(__file__)
# import <erik része>

bot = commands.Bot(command_prefix='$')


@bot.event
async def on_ready():
    print('We have logged in as {0.user}'.format(bot))
    # await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name="verem a faszom"))


@bot.command()
async def adjhozza(ctx):
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
                dirname, f"orarendek/{ctx.message.author}.txt")
            with open(fajlnev, 'wb') as f:
                shutil.copyfileobj(r.raw, f)
        txt2dict(fajlnev, f"{ctx.message.author}")
        await ctx.message.add_reaction('✅')
        print("KÉSZ")


@bot.command()
async def szabad(ctx):
    z, s, p = (["Erik", "Boldi"], ["Broga", "VeresG"], ["sanyimester"])
    e = discord.Embed(
        title="Mi a fasz van",
        color=discord.Color.orange())
    e.set_author(
        name="bot", icon_url="https://prod.cloud.rockstargames.com/crews/sc/6874/23970745/publish/emblem/emblem_256.png")
    e.set_thumbnail(url="https://i.redd.it/34dnz2hvprl81.jpg")
    e.add_field(name=f":sunglasses:**Nincs órája**",
                value=f"** {'**, **'.join(z)}**", inline=False)
    e.add_field(name=f":face_with_raised_eyebrow:**Egy órán belül lesz órája**",
                value=f" {', '.join(s)}", inline=False)
    e.add_field(name=f":face_vomiting:**Órája van**",
                value=f"{', '.join(p)}", inline=False)

    e.set_footer(text="faszom")
    await ctx.send(embed=e)

with open("token.txt") as f:
    token = f.read().rstrip()
bot.run(token)
