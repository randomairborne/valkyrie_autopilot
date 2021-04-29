import discord
import random
import csv
import subprocess
import time
from typing import Optional

from discord.ext import commands

path = "/home/pi/valkyrie_autopilot/"
with open(path + 'prefix.txt', 'r') as file:
    prefix = file.read()
with open(path + 'token.txt', 'r') as file:
    TOKEN = file.read()
intents = discord.Intents().all()
valkyriebot = commands.Bot(command_prefix=prefix, case_insensitive=True, intents=intents)


with open(path + 'embedtexts/helpfun.txt', 'r') as file:
    helpfun = file.read()
with open(path + 'embedtexts/helputility.txt', 'r') as file:
    helputility = file.read()
with open(path + 'embedtexts/helpmod.txt', 'r') as file:
    helpmod = file.read()
crystalball = ["Yes", "No", "Perhaps", "Maybe", "It Is Certain", "Impossible"]
embedcolor = 0xFD6A02

valkyriebot.remove_command('help')


@valkyriebot.event
async def on_ready():
    print(f'Logged on as {valkyriebot.user.name}, prefix: {prefix}')
    await valkyriebot.change_presence(
        activity=discord.Game(name=prefix + f"please for a command list, Bot by valkyrie_pilot and superpowers04, running on {valkyriebot.user.name}"))


@valkyriebot.event
async def on_message(message):
    #logs
    print(f"In server: {message.guild} In channel: {message.channel} user: {message.author} said: {message.content}")
    await valkyriebot.process_commands(message)

@valkyriebot.event
async def on_message_edit(message_before, message):
    #logs
    print(f"In server: {message.guild} In channel: {message.channel} user: {message.author} edited their message from: {message_before.content} to: {message.content}")
    await valkyriebot.process_commands(message)

@valkyriebot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        emoji = '❓'
        await ctx.message.add_reaction(emoji)


@valkyriebot.command()
async def hello(ctx):
    await ctx.message.delete()
    await ctx.channel.send('https://tenor.com/view/hello-there-hi-there-greetings-gif-9442662')


@valkyriebot.command()
async def count(ctx):
    await ctx.channel.send(f"This server has {ctx.guild.member_count} members.")


@valkyriebot.command()
async def test(ctx):
    embed = discord.Embed(colour=embedcolor)
    embed.add_field(name="TEST", value="Test received!")
    embed.set_footer(text=f"Request by {ctx.author}")
    await ctx.send(embed=embed)

#kick
@valkyriebot.command(name='kick', pass_context = True)
@commands.has_permissions(kick_members=True)
async def kick(ctx, member: discord.Member):
    
    await member.kick()
    await ctx.send(f"User {member} Has Been Kicked!")
#ban
@valkyriebot.command(name='ban', pass_context = True)
@commands.has_permissions(kick_members=True)
async def ban(ctx, member: discord.Member):
    
    await member.ban()
    await ctx.send(f"User {member} Has Been Banned!")

@valkyriebot.command()
async def ball(ctx):
    await ctx.message.delete()
    send8ball = random.choice(crystalball)
    embed = discord.Embed(colour=embedcolor)
    embed.add_field(name="Result", value=f"{send8ball}")
    embed.set_footer(text=f"Request by {ctx.author}")
    await ctx.send(embed=embed)


@valkyriebot.command()
async def bruh(ctx):
    await ctx.message.delete()
    await ctx.channel.send("That is quite bruh.")


@valkyriebot.command()
async def ping(ctx):
    await ctx.message.delete()
    embed = discord.Embed(colour=embedcolor)
    embed.add_field(name="Ping", value=f'🏓 Pong! {round(valkyriebot.latency * 1000)}ms')
    embed.set_footer(text=f"Request by {ctx.author}")
    await ctx.send(embed=embed)


@valkyriebot.command()
async def help(ctx):
    await ctx.message.delete()
    await ctx.channel.send(f"You'll figure it out eventually! (or say `{prefix}please`)")


@valkyriebot.command()
async def please(ctx):
    await ctx.message.delete()
    embed = discord.Embed(colour=embedcolor, title="Commands")
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
@commands.has_permissions(manage_messages=True)
async def clear(ctx):
    await ctx.message.delete()
    args = ctx.message.content.split(" ")
    if args[1]:
        amount = int(args[1])
        await ctx.channel.purge(limit=amount)
        embed = discord.Embed(colour=embedcolor)
        embed.add_field(name="Clear", value="cleared " + args[1] + " messages")
        embed.set_footer(text=f"Request by {ctx.author}")
        await ctx.send(embed=embed, delete_after=10)



# Hoooo,boy.  Time to play music.
@valkyriebot.command()
async def addanime(ctx):
    await ctx.message.delete()
    args = ctx.message.content.split(" ")
    if args[1] and args[1].startswith("http"):
        with open(path + "anime.csv", "a+") as fp:
            writer = csv.writer(fp, delimiter=",")
            # writer.writerow(["your", "header", "foo"])  # write header
            writer.writerow([args[1]])
        embed = discord.Embed(colour=embedcolor)
        embed.add_field(name="Add successful", value="Added " + args[1] + " successfully")
        embed.set_footer(text=f"Request by {ctx.author}")
        await ctx.send(embed=embed)
    else:
        await ctx.channel.send("Invalid url!")


@valkyriebot.command()
async def anime(ctx):
    await ctx.message.delete()
    with open(path + "anime.csv") as fp:
        reader = csv.reader(fp, delimiter=",", quotechar='"')
        # next(reader, None)  # skip the headers
        animes = [row for row in reader]
    send = random.choice(animes)
    await ctx.channel.send(send[0])
    
@valkyriebot.command()
async def animespam(ctx):
    await ctx.message.delete()
    args = ctx.message.content.split(" ")
    if args[1]:
        amountSpamAnime = int(args[1])
        for x in range(0, amountSpamAnime):
            with open(path + "anime.csv") as fp:
                reader = csv.reader(fp, delimiter=",", quotechar='"')
                # next(reader, None)  # skip the headers
                animes = [row for row in reader]
            send = random.choice(animes)
            await ctx.channel.send(send[0])
            time.sleep(0.5)

@valkyriebot.command()
async def hug(ctx, *, user:str = None):
    if user is not None:
        try: 
            mention = f'<@{int(user)}>'
        except: 
            mention = user
        await ctx.send(f"{mention}, {ctx.author.mention} gave you a hug, aww!")
    await ctx.send("https://media.tenor.com/images/50c2f13c590fdb27c087d6a6736218e0/tenor.gif")
            
@valkyriebot.command()
async def huggle(ctx, member : discord.Member = None):
    if member is not None:
        await ctx.send(f"{member.mention}, {ctx.author.mention} gave you a huggle, aww!")
    await ctx.send("https://media.tenor.com/images/16491d8d332f0e231bb084474e66199c/tenor.gif")
            
@valkyriebot.command()
async def cuddle(ctx, member : discord.Member = None):
    if member is not None:
        await ctx.send(f"{member.mention}, {ctx.author.mention} gave you a cuddle, aww!")
    await ctx.send("https://media.tenor.com/images/9a8b0edf260a4831271c4a83573a1e12/tenor.gif")
    


valkyriebot.run(TOKEN)

