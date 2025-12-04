import discord
from discord.ext import commands
import random
import asyncio
from keep_alive import keep_alive
import os

intents = discord.Intents.all()
bot = commands.Bot(command_prefix=".", intents=intents, help_command=None)

MAIN_COLOR = 0x9B59B6
SUCCESS = "✨"
ERROR = "❌"
MOD = "🛡️"
FUN = "🎉"
GIVE = "🎁"

WELCOME_CHANNEL_ID = 123456789012345678

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")
    await bot.change_presence(activity=discord.Game(".help | aesthetic ✨"))

@bot.event
async def on_member_join(member):
    channel = bot.get_channel(WELCOME_CHANNEL_ID)
    if channel is None:
        return

    embed = discord.Embed(
        title="🌸 Welcome to the Server! 🌸",
        description=(
            f"Hey {member.mention}, we're so happy you joined!\n\n"
            "✨ **Enjoy your stay**\n"
            "🪄 **Make new friends**\n"
            "💜 **Be kind & have fun**\n"
        ),
        color=MAIN_COLOR
    )

    embed.set_thumbnail(url=member.avatar.url if member.avatar else member.default_avatar.url)
    embed.add_field(name="🌐 Member Count", value=f"`{member.guild.member_count}` members", inline=False)
    embed.set_footer(text="Welcome • Enjoy your stay ✨")
    await channel.send(embed=embed)

@bot.command()
async def help(ctx):
    embed = discord.Embed(
        title="🌸 **Aesthetic Bot Commands**",
        description="All commands grouped by category!",
        color=MAIN_COLOR,
    )
    embed.add_field(name=f"{MOD} Moderation",
        value="`.ban` `.kick` `.mute` `.unmute` `.timeout` `.untimeout`\n`.warn` `.warns` `.clear` `.slowmode` `.lock` `.unlock`",
        inline=False)
    embed.add_field(name=f"{GIVE} Giveaways",
        value="`.gstart <time> <prize>`\n`.gend <messageID>`\n`.reroll <messageID>`",
        inline=False)
    embed.add_field(name=f"{FUN} Fun",
        value="`.say` `.avatar` `.userinfo` `.serverinfo` `.ping`",
        inline=False)
    await ctx.send(embed=embed)

warns_db = {}

@bot.command()
async def warn(ctx, member: discord.Member, *, reason="No reason provided"):
    if member.id not in warns_db:
        warns_db[member.id] = []
    warns_db[member.id].append(reason)
    embed = discord.Embed(title=f"{MOD} Warn Issued",
        description=f"**{member}** has been warned.\n📝 Reason: `{reason}`",
        color=MAIN_COLOR)
    await ctx.send(embed=embed)

@bot.command(name="warns")
async def warns(ctx, member: discord.Member):
    user_warns = warns_db.get(member.id, [])
    embed = discord.Embed(title=f"{MOD} Warning List",
        description="\n".join([f"• {w}" for w in user_warns]) or "No warnings.",
        color=MAIN_COLOR)
    await ctx.send(embed=embed)

@bot.command()
async def clear(ctx, amount: int):
    await ctx.channel.purge(limit=amount + 1)
    embed = discord.Embed(title=f"{SUCCESS} Messages Cleared",
        description=f"Deleted `{amount}` messages.",
        color=MAIN_COLOR)
    await ctx.send(embed=embed)

@bot.command()
async def say(ctx, *, text):
    embed = discord.Embed(description=f"💬 {text}", color=MAIN_COLOR)
    await ctx.send(embed=embed)

@bot.command()
async def ping(ctx):
    embed = discord.Embed(title="🏓 Pong!",
        description=f"Latency: `{bot.latency*1000:.0f}ms`",
        color=MAIN_COLOR)
    await ctx.send(embed=embed)

@bot.command()
async def avatar(ctx, member: discord.Member=None):
    member = member or ctx.author
    embed = discord.Embed(title="🖼️ Avatar", color=MAIN_COLOR)
    embed.set_image(url=member.avatar.url)
    await ctx.send(embed=embed)

keep_alive()
bot.run(os.getenv("DISCORD_TOKEN"))
