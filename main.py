import discord
from discord.ext import commands
from discord import Intents, Client, Message
import asyncio
from random import choice, randint
from dotenv import load_dotenv
from responses import get_response  # Assuming this imports your get_response function
from quote import riddles  # Assuming this imports your riddles list
import google.generativeai as genai


# Initialize Discord bot
intents: Intents = Intents.default()
intents.message_content = True
client: Client = Client(intents=intents)
bot = commands.Bot(command_prefix="/", intents=intents)

# Initialize Generative AI model
genai.configure(api_key='API_KEY')
model = genai.GenerativeModel('gemini-pro')

# List to hold ongoing riddle set and finished riddle sets
set = []
finishedset = []


# Function to send responses to users in private or channel
async def send_message(message: Message, user_message: str) -> None:
    if not user_message:
        print('(Message empty)')
    
    is_private = user_message.startswith('?')
    if is_private:
        user_message = user_message[1:]

    try:
        response: str = get_response(user_message)
        await message.author.send(response) if is_private else await message.channel.send(response)
    except Exception as error:
        print(error)


# Event handler for receiving messages
@client.event 
async def on_message(message: Message) -> None:
    if message.author == client.user:
        return
    
    username: str = str(message.author)
    user_message: str = message.content
    channel: str = str(message.channel)
    print(f'[{channel}] {username}: "{user_message}"')
    await send_message(message, user_message)


# Event handler when bot is ready
@bot.event
async def on_ready():
    print(f'Bot is online: {bot.user.name}!')


# Command to generate AI response
@bot.command(name='ai')
async def askai(ctx: commands.Context, *, prompt: str):
    try:
        response = model.generate_content(prompt)
        response_text = response.text
        
        if len(response_text) > 2000:
            response_text = response_text[:1997] + '...'  
        
        await ctx.reply(response_text)
    except Exception as e:
        await ctx.send(f"Error: {e}")


# Command to show list of available commands
@bot.command(name='commands')
async def show_commands(ctx: commands.Context):
    commands_list = [
        '**------Commands available------**\n',
        '`*/commands -- Show list of commands*`\n',
        '`*/ai -- Generate AI response*`\n',
        '`*/quote -- Get a positive quote*`\n',
        '`*/flipcoin -- Flip a coin*`\n',
        '`*/riddle -- Get a riddle*`\n',
        '`*/info -- Get info...*`'
    ]

    await ctx.send('\n'.join(commands_list))


# Command to get a positive quote
@bot.command(name='quote')
async def get_quote(ctx: commands.Context):
    quote = get_response('/quote')  
    await ctx.send(quote)


# Command to get a riddle
@bot.command(name='riddle')
async def spwn_riddle(ctx: commands.Context):
    riddle = get_response('/riddle')
    await ctx.send(riddle)


# Command to flip a coin
@bot.command(name='flipcoin')
async def flip_coin(ctx: commands.Context):
    flipcoin = get_response('/flipcoin')
    await ctx.send(flipcoin)


# Command to get info
@bot.command(name='info')
async def get_info(ctx: commands.Context):
    info = get_response('/info')
    await ctx.send(info)


# Entry point for running the Discord bot
def main() -> None:
    bot.run(token='DISCORD_TOKEN')


if __name__ == '__main__':
    main()
