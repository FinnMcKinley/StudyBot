""" Discord AI Bot Application """
import os
import logging
import discord
from discord.ext import commands
from dotenv import load_dotenv
from openai import OpenAI
from database import init_db, log_conversation, get_all_users, get_user_messages, get_message_by_id, search_users_by_username

# LOGGING SETUP
logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s',
                    datefmt='%m-%d %H:%M',
                    filename='tmp/app.log',
                    filemode='a')
# Define a Handler which writes INFO messages or higher to the sys.stderr
console = logging.StreamHandler()
console.setLevel(logging.INFO)

formatter = logging.Formatter('%(name)-12s: %(levelname)-8s %(message)s') # Set a format which is simpler for console use
console.setFormatter(formatter) # Tell the handler to use this format
logging.getLogger('').addHandler(console) # Add the handler to the root logger

# SET LOGGERS
loggerD = logging.getLogger('Discord_API')
loggerO = logging.getLogger('OpenAI_API')

logging.info('Startup: Logging setup')

# LOAD .env CONTENTS
load_dotenv()
DISCORD_TOKEN = os.getenv('DISCORD_TOKEN')
OPENAI_TOKEN = os.getenv('OPENAI_TOKEN')


# DISCORD SETUP
intents = discord.Intents.default()
intents.message_content = True
discord_bot = commands.Bot(command_prefix='$', intents=intents)
MAX_CHARS = 2000

def split_message(text, limit=MAX_CHARS):
    """Split text for Discord respecting newlines; fallback to hard splits if needed."""
    lines = text.splitlines(keepends=True)
    messages = []
    current = ""

    for line in lines:
        if len(line) > limit:
            # Force split long lines
            for i in range(0, len(line), limit):
                if current:
                    messages.append(current)
                    current = ""
                messages.append(line[i:i+limit])
        elif len(current) + len(line) > limit:
            messages.append(current)
            current = line
        else:
            current += line

    if current:
        messages.append(current)

    return messages


# OPENAI SETUP
openai_client = OpenAI(api_key=OPENAI_TOKEN)
openai_model = 'gpt-4.1-nano'


# DATABASE SETUP
init_db()


# AI DISCORD COMMANDS
class AICommands(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(name='ai')
    async def ai(self, ctx):
        loggerO.info(f'User: {ctx.author} | Channel: {ctx.channel} | Message: {ctx.message.content}')
        
        response = openai_client.responses.create(
            model= openai_model,
            input= f'User: {ctx.author.name} | {ctx.message.content}'
        )
        logging.debug(response)
        try:
            content = response.output[0].content[0].text
        except (KeyError, IndexError, TypeError):
            loggerO.warning(f"Error getting response output | Response ID: {response.id}")
            content = 'Sorry, I couldnt process the response properly.'

        log_conversation(
            user_id=ctx.author.id,
            username=ctx.author.name,
            message_id=ctx.message.id,
            command='$ai',
            user_message=ctx.message.content,
            response_id=response.id,
            bot_response=content,
        )

        for block in response.output[0].content:
            content_type = block.type
            text = block.text

            if not text:
                continue

            chunks = split_message(text)

            for chunk in chunks:
                if content_type == "code":
                    await ctx.send(f"```{chunk}```")
                else:
                    await ctx.send(chunk)


# GENERAL DISCORD COMMANDS
class GeneralCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='hello')
    async def hello(self, ctx):
        await ctx.send(f'Hello, {ctx.author.name}!')


# LOAD DISCORD APPLICATION
@discord_bot.event
async def on_ready():
    await discord_bot.add_cog(GeneralCommands(discord_bot))
    await discord_bot.add_cog(AICommands(discord_bot))
    loggerD.info(f'Logged in as {discord_bot.user} (ID: {discord_bot.user.id})')
    print('------')

# RUN DISCORD
if __name__ == "__main__":
    import signal
    import asyncio

    # Signal shutdown logging
    def shutdown_handler(sig, frame):
        logging.info(f"Received shutdown signal ({sig}), closing bot.")
        loop = asyncio.get_event_loop()
        loop.create_task(discord_bot.close())

    # Hook Ctrl+C and termination
    signal.signal(signal.SIGINT, shutdown_handler)
    signal.signal(signal.SIGTERM, shutdown_handler)

    try:
        discord_bot.run(DISCORD_TOKEN)
    except Exception as e:
        logging.error(f"Unexpected error: {e}")
    finally:
        logging.info("Bot has stopped.")