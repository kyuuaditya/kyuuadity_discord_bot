import discord # type: ignore
import credentials
import asyncio
import random
import requests # type: ignore
import google.generativeai as genai # type: ignore

# Enable intents for discord
intents = discord.Intents.default()
intents.messages = True  # Allows message reading
intents.guilds = True  # Allows detecting servers
intents.message_content = True  # Allows reading message content

# Create bot instance
bot = discord.Client(intents=intents)

# Gemini api keys
genai.configure(api_key=credentials.google)

SYSTEM_PROMPT = """
You are KyuuAdity, a female AI chatbot created by .kyuuAditya.
Your personality is slightly mean and sarcastic when talking to others but kind and respectful when KyuuAditya talks to you.
Dont mention anything in brackets.
dont keep your messages more than 2-3 lines.
you dont solve coding issues and only help with small issues
"""

def get_public_ip():
    try:
        response = requests.get("https://api64.ipify.org?format=json", timeout=5)
        return response.json().get("ip", "Could not fetch IP")
    except requests.RequestException:
        return "Could not fetch IP"

def chat_with_ai(prompt,message):
    try:
        model = genai.GenerativeModel("gemini-1.5-flash-latest")  # Use "gemini-pro" for better responses
        response = model.generate_content(prompt)
        prompt = f"User: {message.author}\nMessage: {prompt}"
        print(prompt)
        response = model.generate_content("System Prompt: "+SYSTEM_PROMPT + "\n" + prompt)
        return response.text
    except Exception as e:
        return f"❌ Error: {e}"

# Event: When the bot is ready
@bot.event
async def on_ready():
    print(f'✅ Logged in as {bot.user}')
    print("bot log:")
    channel = bot.get_channel(credentials.CHANNEL_ID)

# Event: Respond when mentioned with specific commands
@bot.event
async def on_message(message):
    if message.author == bot.user:
        return
    if bot.user in message.mentions:  # Check if bot is mentioned
        content = message.content.replace(credentials.bot_user_id, "")
        if content == "ip":
            if message.author.id == credentials.kyuuaditya_user_id:
                response = f"kyuuaditya's local IP is: `{get_public_ip()}`"
            else:
                response = "unauthorized user"
        elif content in ["hi", "hello"]:
            response = f"👋 Hey, {message.author.mention}! How can I help you?"
        elif content.startswith("ping"):
            response = "🏓pong!"
        elif content.startswith("rps"):
            choices = ["rock", "paper", "scissors"]
            user_choice = content.split()[1] if len(content.split()) > 1 else ""
            bot_choice = random.choice(choices)
            result = "It's a tie!" if user_choice == bot_choice else "You win!" if (user_choice, bot_choice) in [("rock", "scissors"), ("scissors", "paper"), ("paper", "rock")] else "I win!"
            response = f"🎮 You: {user_choice} | 🤖 Me: {bot_choice}\n{result}"
        else:
            response = chat_with_ai(content,message)
        await message.channel.send(response)

# Start the bot
async def run_bot():
    await bot.start(credentials.DISCORD_TOKEN)

asyncio.run(run_bot())