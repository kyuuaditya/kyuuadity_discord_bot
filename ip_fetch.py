import discord
import credentials
import socket
import asyncio
import random

# Enable intents
intents = discord.Intents.default()
intents.messages = True  # Allows message reading
intents.guilds = True  # Allows detecting servers
intents.message_content = True  # Allows reading message content

# Create bot instance
bot = discord.Client(intents=intents)

# Function to get local IPv4 address
def get_ipv4():
    hostname = socket.gethostname()
    local_ip = socket.gethostbyname(hostname)
    return local_ip

# Event: When the bot is ready
@bot.event
async def on_ready():
    print(f'✅ Logged in as {bot.user}')
    print("bot log:")
    channel = bot.get_channel(credentials.CHANNEL_ID)
    # if channel:
    #     await channel.send(f"🚀 **Bot is Online!**\nPing me with `@{bot.user.name}` and a command!")

# Event: Respond when mentioned with specific commands
@bot.event
async def on_message(message):
    if message.author == bot.user:
        return  # Ignore own messages

    if bot.user in message.mentions:  # Check if bot is mentioned
        content = message.content.replace(f"<@1354383583573446776> ", "")
        print(f"    {content}")

        if content == "ip":
            response = f"🖥️ My local IP is: `{get_ipv4()}`"
        elif content in ["hi", "hello"]:
            response = f"👋 Hello {message.author.mention}! How can I help you?"
        elif content.startswith("rps"):
            choices = ["rock", "paper", "scissors"]
            user_choice = content.split()[1] if len(content.split()) > 1 else ""
            bot_choice = random.choice(choices)
            result = "It's a tie!" if user_choice == bot_choice else "You win!" if (user_choice, bot_choice) in [("rock", "scissors"), ("scissors", "paper"), ("paper", "rock")] else "I win!"
            response = f"🎮 You: {user_choice} | 🤖 Me: {bot_choice}\n{result}"
        else:
            response = f"🤔 I don't recognize that command '{content}'! Try `@Bot ip` or `@Bot hi`."


        await message.channel.send(response)

# Start the bot
async def run_bot():
    await bot.start(credentials.DISCORD_TOKEN)

asyncio.run(run_bot())
