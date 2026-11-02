import asyncio
import logging
import os

from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.redis import RedisStorage, DefaultKeyBuilder
from aiogram.client.session.aiohttp import AiohttpSession

from handlers.user import admin_router

from middlewares.db import DBmmyasoSessionMiddleware, DBsubmeatSessionMiddleware

from config import config

from background import start_moderation_worker

async def main():

    os.makedirs("data", exist_ok=True)

    logging.basicConfig(level=logging.INFO)
    
    storage = RedisStorage.from_url(
        f"redis://default:{config.redis_password.get_secret_value()}@redis:6379/0",
        key_builder=DefaultKeyBuilder(with_bot_id=True)
    )

    session = AiohttpSession(proxy="socks5://unrybJ:MS5PGU@193.254.235.133:9551")
    bot = Bot(token=config.mmyaso_tg_bot_token.get_secret_value(), session=session)
    dp = Dispatcher(storage=storage)

    dp.update.middleware(DBmmyasoSessionMiddleware())
    dp.update.middleware(DBsubmeatSessionMiddleware())

    dp.include_router(admin_router)

    asyncio.create_task(start_moderation_worker(bot))

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
