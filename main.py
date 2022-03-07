import requests
import discord
from discord.ext import commands
import requests
import shutil
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
    else:
        r = requests.get(ctx.message.attachments[0].url, stream=True)
        if r.status_code == 200:
            r.raw.decode_content = True
            with open("woo.txt", 'wb') as f:
                shutil.copyfileobj(r.raw, f)
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

bot.run('Njg5NTIzNTI5MzI2MTMzMzM2.XnEG1A.zxoCiiiB4H5uV6vr86Nl52cUkL0')
