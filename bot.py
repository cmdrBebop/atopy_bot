import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.contrib.fsm_storage.redis import RedisStorage2

from tgbot.config import load_config

from tgbot.handlers.start import register_start
from tgbot.handlers.get_data import register_main

from tgbot.handlers.admin import register_admin
from tgbot.middlewares.environment import EnvironmentMiddleware

from tgbot.services.db.database import Database
from tgbot.services.mindbox import MindBox
from tgbot.services.google_sheets import GoogleSheets


logger = logging.getLogger(__name__)


def register_all_middlewares(dp, config):
    dp.setup_middleware(EnvironmentMiddleware(config=config))


def register_all_handlers(dp):
    register_start(dp)
    register_admin(dp)
    register_main(dp)


async def main():
    logging.basicConfig(
        level=logging.INFO,
        format=u'%(filename)s:%(lineno)d #%(levelname)-8s [%(asctime)s] - %(name)s - %(message)s',
    )
    logger.info("Starting bot")
    config = load_config(".env")

    storage = RedisStorage2() if config.tg_bot.use_redis else MemoryStorage()
    bot = Bot(token=config.tg_bot.token, parse_mode='HTML')
    dp = Dispatcher(bot, storage=storage)

    database = Database(
        host=config.db.host,
        password=config.db.password,
        user=config.db.user,
        database=config.db.database,
    )

    mindbox = MindBox(config.misc.mindbox_secret_key)
    google_sheets = GoogleSheets(config.google_sheets.credentials_file, config.google_sheets.spreadsheet_id)

    bot['config'] = config
    bot['database'] = database
    bot['mindbox'] = mindbox
    bot['google_sheets'] = google_sheets
    # await database.create_all()
    # await database.messages_worker.insert_default_messages()

    register_all_middlewares(dp, config)
    register_all_handlers(dp)

    # start
    try:
        await dp.start_polling()
    finally:

        await database.close_pools()
        
        await dp.storage.close()
        await dp.storage.wait_closed()
        await bot.session.close()


if __name__ == '__main__':
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logger.error("Bot stopped!")
        raise
