import discord
from discord.ext import commands
import asyncio

intents = discord.Intents.default()
intents.message_content = True
intents.guilds = True
intents.members = True # Needed for role management

bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():
print(f'Bot is ready! Logged in as {bot.user}')

@bot.command(name='setup')
@commands.has_permissions(administrator=True)
async def setup_server(ctx):
guild = ctx.guild
if guild.name != "DonutSMP // Market":
await ctx.send("Please rename your server to **DonutSMP // Market** first!")
return

await ctx.send("🚀 Starting DonutSMP // Market server setup...")

# === ROLE CREATION ===
await ctx.send("Creating roles...")

# Colors
donut_pink = discord.Color.from_rgb(255, 105, 180)
gold = discord.Color.gold()
green = discord.Color.green()

roles_to_create = [
{"name": "🍩 Owner", "color": donut_pink, "hoist": True, "permissions": discord.Permissions.all()},
{"name": "🛡️ Admin", "color": discord.Color.red(), "hoist": True, "permissions": discord.Permissions(administrator=True)},
{"name": "👮 Moderator", "color": discord.Color.blue(), "hoist": True, "permissions": discord.Permissions(kick_members=True, ban_members=True, manage_messages=True, manage_channels=True)},
{"name": "✅ Verified", "color": green, "hoist": True, "permissions": discord.Permissions(send_messages=True, read_messages=True)},
{"name": "💰 Buyer", "color": gold, "hoist": True, "permissions": discord.Permissions(send_messages=True, read_messages=True)},
{"name": "📦 Seller", "color": discord.Color.purple(), "hoist": True, "permissions": discord.Permissions(send_messages=True, read_messages=True)},
{"name": "Member", "color": discord.Color.light_grey(), "hoist": False, "permissions": discord.Permissions(send_messages=True, read_messages=True)},
]

created_roles = {}
for role_data in roles_to_create:
role = discord.utils.get(guild.roles, name=role_data["name"])
if not role:
role = await guild.create_role(
name=role_data["name"],
color=role_data["color"],
hoist=role_data["hoist"],
permissions=role_data.get("permissions", discord.Permissions(send_messages=True))
)
created_roles[role_data["name"]] = role
await asyncio.sleep(1) # Avoid rate limits

await ctx.send("✅ Roles created!")

# === CHANNEL CATEGORIES ===
await ctx.send("Creating channel categories...")

# Delete default channels (optional - be careful)
for channel in guild.channels:
if channel.name in ["general", "rules", "welcome"]:
try:
await channel.delete()
except:
pass

categories = {
"📢 INFORMATION": None,
"💬 GENERAL": None,
"🛒 MARKETPLACE": None,
"🎮 DONUTSMP": None,
"🔧 SUPPORT": None,
}

created_categories = {}
for cat_name in categories:
cat = discord.utils.get(guild.categories, name=cat_name)
if not cat:
cat = await guild.create_category(cat_name)
created_categories[cat_name] = cat

# === CHANNELS ===
await ctx.send("Creating channels...")

# Information
await created_categories["📢 INFORMATION"].create_text_channel("📜-rules")
await created_categories["📢 INFORMATION"].create_text_channel("📢-announcements")
welcome = await created_categories["📢 INFORMATION"].create_text_channel("👋-welcome")

# General
await created_categories["💬 GENERAL"].create_text_channel("💬-general-chat")
await created_categories["💬 GENERAL"].create_text_channel("🖼️-memes")
await created_categories["💬 GENERAL"].create_voice_channel("🎤 Lounge")

# Marketplace
market_cat = created_categories["🛒 MARKETPLACE"]
await market_cat.create_text_channel("💰-buy-donut-coins")
await market_cat.create_text_channel("📦-sell-donut-coins")
await market_cat.create_text_channel("🔄-trade-requests")
await market_cat.create_text_channel("📋-market-listings")

# DonutSMP
smp_cat = created_categories["🎮 DONUTSMP"]
await smp_cat.create_text_channel("🗣️-in-game-chat")
await smp_cat.create_text_channel("📊-server-status")
await smp_cat.create_text_channel("❓-faq")

# Support
support_cat = created_categories["🔧 SUPPORT"]
await support_cat.create_text_channel("📩-support-tickets")
await support_cat.create_text_channel("🤝-partner-inquiries")

await ctx.send("✅ Channels created!")

# === PERMISSIONS SETUP ===
await ctx.send("Setting up permissions...")

everyone = guild.default_role

# Lock information channels to view only for @everyone
for channel in created_categories["📢 INFORMATION"].channels:
await channel.set_permissions(everyone, read_messages=True, send_messages=False)

# Marketplace permissions
for channel in created_categories["🛒 MARKETPLACE"].channels:
await channel.set_permissions(everyone, read_messages=True, send_messages=False)
await channel.set_permissions(created_roles["💰 Buyer"], send_messages=True)
await channel.set_permissions(created_roles["📦 Seller"], send_messages=True)

await ctx.send("✅ Permissions configured!")

# Welcome message
embed = discord.Embed(
title="🍩 Welcome to DonutSMP // Market!",
description="The official marketplace for **Donut SMP** in-game currency!\n\nBuy, sell, and trade Donut Coins safely.",
color=donut_pink
)
embed.add_field(name="How to Get Started", value="1. Get the **Verified** role\n2. Check #rules\n3. Head to the Marketplace", inline=False)
await welcome.send(embed=embed)

await ctx.send("🎉 **Server setup complete!** Enjoy your DonutSMP Marketplace!")

@bot.command(name='help_setup')
async def help_setup(ctx):
embed = discord.Embed(title="DonutSMP Bot Setup", color=discord.Color.gold())
embed.add_field(name="Usage", value="`!setup` - Run this as Administrator to auto-configure the server", inline=False)
embed.add_field(name="Requirements", value="• Server must be named **DonutSMP // Market**\n• Bot needs Administrator permissions", inline=False)
await ctx.send(embed=embed)

bot.run('MTUyNzc5NDcxMjE4MDk1MzEyOA.G9blBQ.c2aIiHkWMPPjI2-W_nTBP1VH4uuBoNMy1k75Fg')
