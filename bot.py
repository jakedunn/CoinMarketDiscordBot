from discord.ext import commands
from bot_logger import logger
import json
import logging

bot = commands.Bot(command_prefix='$', description='Displays market data from https://coinmarketcap.com/')

initial_extensions = [
    'cogs.coin_market_cmd_handler'
]


class CoinMarketBotException(Exception):
    """Exception class for CoinMarketBot"""


class CoinMarketBot:
    """Initiates the Bot"""

    def __init__(self):
        with open('config.json') as config:
            self.config_data = json.load(config)
        bot.run(self.config_data["token"])

    @bot.event
    async def on_ready():
        for extension in initial_extensions:
            try:
                logger.info('Starting bot..')
                bot.load_extension(extension)
                print('CoinMarketDiscordBot is online.')
                print('Bot is currently running on {} servers.'.format(len(bot.servers)))
                logger.info('Bot is online.')
            except Exception as e:
                error_msg = 'Failed to load extension {}\n{}: {}'.format(extension, type(e).__name__, e)
                print(error_msg)
                logger.error(error_msg)

    @bot.event
    async def on_message(message):
        await bot.process_commands(message)

    @bot.event
    async def on_command_error(error, ctx):
        if isinstance(error, commands.errors.MissingRequiredArgument):
            await send_cmd_help(ctx)
        if isinstance(error, commands.errors.BadArgument):
            await send_cmd_help(ctx)


async def send_cmd_help(ctx):
    if ctx.invoked_subcommand:
        pages = bot.formatter.format_help_for(ctx, ctx.invoked_subcommand)
        for page in pages:
            await bot.send_message(ctx.message.channel,
                                   "Please make sure you're entering a valid"
                                   "command:\n{}".format(page))
    else:
        pages = bot.formatter.format_help_for(ctx, ctx.command)
        for page in pages:
            await bot.send_message(ctx.message.channel,
                                   "Command failed. Please make sure you're "
                                   "entering the correct arguments to the "
                                   "command:\n{}".format(page))


def main():
    try:
        CoinMarketBot()
    except Exception as e:
        logging.error('Bot failed to run: {}'.format(str(e)))
        print(e)
    logger.info("Bot is now offline.")


main()
