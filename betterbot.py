import discord
import random
import json
import subprocess
import time

from discord.ext import commands
path = "/home/valkyrie_pilot/valkyrie_autopilot/"
TOKEN = 'Token'
intents = discord.Intents().all()
valkyriebot = commands.Bot(command_prefix = '&', case_insensitive=True, intents=intents)

animetxt = open(path + "anime.json", "r")
animes = json.loads(animetxt.read())
swearstxt = open(path +'embedtexts/swears.json', "r")
swears = json.loads(swearstxt.read())
swearstxt.close()
with open(path + 'embedtexts/helpfun.txt', 'r') as file:
    helpfun = file.read()
with open(path + 'embedtexts/helputility.txt', 'r') as file:
    helputility = file.read()
with open(path + 'embedtexts/helpmod.txt', 'r') as file:
    helpmod = file.read()
animetxt.close()
crystalball = ["Yes","No","Perhaps","Maybe","It Is Certain","Impossible"]
embedcolor = 0xFD6A02

@valkyriebot.event
async def on_ready():
    print('Logged on as valkyrie_autopilot!')
    await valkyriebot.change_presence(activity=discord.Game(name="My prefix is `&`, have fun!"))


valkyriebot.remove_command('help')

@valkyriebot.command()
async def hello(ctx):
    await ctx.message.delete()
    await ctx.channel.send('https://tenor.com/view/hello-there-hi-there-greetings-gif-9442662')

@valkyriebot.command()
async def test(ctx):
    await ctx.message.delete()
    embed = discord.Embed(color=embedcolor)
    embed.add_field(name="TEST", value="Test received!")
    embed.set_footer(text=f"Request by {ctx.author}")
    await ctx.send(embed=embed)

@valkyriebot.command()
async def restart(ctx):
    await ctx.message.delete()
    embed = discord.Embed(color=embedcolor)
    embed.add_field(name="Restart", value="valkyrie_autopilot restarting!")
    embed.set_footer(text=f"Request by {ctx.author}")
    await ctx.send(embed=embed)
    await valkyriebot.close()
    time.sleep(5)
    cmd = 'python3 /home/valkyrie_pilot/valkyrie_autopilot/betterbot.py'
    subprocess.run('gnome-terminal -- ' + cmd, shell=True)
    print("exiting")
    subprocess.run(exit, shell=True)

@valkyriebot.command()
async def spam(ctx):
    await ctx.message.delete()
    args = ctx.message.content.split(" ")
    if args[2]:
        spam = args[1]
        title = args[2]
        times = int(args[3])
        for x in range(0,times):
            embed = discord.Embed(color=embedcolor)
            embed.add_field(name=title, value=spam)
            embed.set_footer(text=f"Request by {ctx.author}")
            await ctx.send(embed=embed)

@valkyriebot.command()
async def estop(ctx):
    await ctx.message.delete()
    quit()

@valkyriebot.command()
async def ball(ctx):
    await ctx.message.delete()
    send8ball = random.choice(crystalball)
    embed = discord.Embed(color=embedcolor)
    embed.add_field(name="Result", value=f"{send8ball}")
    embed.set_footer(text=f"Request by {ctx.author}")
    await ctx.send(embed=embed)

@valkyriebot.command()
async def bruh(ctx):
    await ctx.messasge.delete()
    await ctx.channel.send("That is quite bruh.")

@valkyriebot.command()
async def ping(ctx):
    await ctx.message.delete()
    embed = discord.Embed(color=embedcolor)
    embed.add_field(name="Ping", value=f'🏓 Pong! {round(valkyriebot.latency * 1000)}ms')
    embed.set_footer(text=f"Request by {ctx.author}")
    await ctx.send(embed=embed)

@valkyriebot.command()
async def help(ctx):
    await ctx.message.delete()
    await  ctx.channel.send("You'll figure it out eventually! (or say `&please`)")

@valkyriebot.command()
async def please(ctx):
    await ctx.message.delete()
    embed = discord.Embed(color=embedcolor, title="Commands")
    embed.add_field(name="Fun commands:",
                    value=helpfun,
                    inline=True)
    embed.add_field(name="Bot utilities:",
                    value=helputility,
                    inline=True)
    embed.add_field(name="Moderation commands:",
                    value=helpmod,
                    inline=True)
    embed.set_footer(text=f"Request by {ctx.author}")
    await ctx.send(embed=embed)

@valkyriebot.command()
async def clear(ctx):
    await ctx.message.delete()
    args = ctx.message.content.split(" ")
    if args[1]:
        amount = int(args[1])
        await ctx.channel.purge(limit=amount)
        embed = discord.Embed(color=embedcolor)
        embed.add_field(name="Clear", value="cleared " + args[1] + " messages")
        embed.set_footer(text=f"Request by {ctx.author}")
        await ctx.send(embed=embed)

@valkyriebot.command()
async def addanime(ctx):
    await ctx.message.delete()
    args = ctx.message.content.split(" ")
    try:
        if args[1] and args[1].startswith("http"):
            animetxt = open("anime.json", "w")
            anime.append(args[1])
            animetxt.write(json.dumps(anime))
            animetxt.close()
            embed = discord.Embed(color=embedcolor)
            embed.add_field(name="Add successful", value="Added " + args[1] + " successfully")
            embed.set_footer(text=f"Request by {ctx.author}")
            await ctx.send(embed=embed)
        else:
            await ctx.channel.send("Invalid url!")
    except NameError:
        await ctx.channel.send("Invalid attachment!")

@valkyriebot.command()
async def anime(ctx):
    await ctx.message.delete()
    send = random.choice(animes)
    await ctx.channel.send(send)
@valkyriebot.command()
async def badwords(ctx):
    await ctx.message.delete()
    args = ctx.message.content.split(" ")
    if args[1]:
        swearsjson = open(path + "embedtexts/swears.json", "w")
        swears.append(args[1])
        swearsjson.write(json.dumps(swears))
        swearsjson.close()
        embed = discord.Embed(color=embedcolor)
        embed.add_field(name="Add successful", value="Added " + args[1] + "to banned words list successfully")
        embed.set_footer(text=f"Request by {ctx.author}")
        await ctx.send(embed=embed)
@valkyriebot.event
async def on_message(message):
    ctx = message
    print(f"{ctx.author}:{ctx.content}")
    if ctx.content in swears:
        await ctx.delete()
        await ctx.channel.send("Ay, mate. You're not allowed to say that here >:<")
        await valkyriebot.process_commands(message)

valkyriebot.run(TOKEN)
