import asyncio
import json

import redis.asyncio as aioredis

from aiogram import Bot
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from config import config


async def start_moderation_worker(bot: Bot):
    redis_client = aioredis.from_url(f"redis://default:{config.redis_password.get_secret_value()}@redis:6379/0")
    ADMIN_CHAT_ID = config.superuser_tg_id
    
    print("🟢 Воркер модерации второго бота запущен...")

    while True:
        try:
            result = await redis_client.brpop("moderation_queue", timeout=0)
            if result:
                _, raw_data = result
                data = json.loads(raw_data.decode("utf-8"))

                _type = data["_type"]

                if _type == "registration":
                
                    user_id = data["user_id"]
                    name = data["name"]
                    portfolio = data["portfolio"]
                    about = data["about"]

                    # Кнопки для модератора
                    kb = InlineKeyboardMarkup(inline_keyboard=[
                        [
                            InlineKeyboardButton(text="✅ Принять", callback_data=f"mod_registration_approve:{user_id}"),
                            InlineKeyboardButton(text="❌ Отклонить", callback_data=f"mod_registration_reject:{user_id}")
                        ]
                    ])

                    # Отправляем карточку в чат модераторов
                    await bot.send_message(
                        chat_id=ADMIN_CHAT_ID,
                        text=(
                            f"🚨 <b>Новый участник на мясорубку!</b>\n\n"
                            f"👤 Имя: <b>{name}</b>\n"
                            f"🔗 Портфолио: {portfolio}\n"
                            f"📝 О себе: {about}\n"
                            f"🆔 ID: <code>{user_id}</code>"
                        ),
                        parse_mode="HTML",
                        reply_markup=kb
                    )

                elif _type == "project_submit":

                    user_id = data["user_id"]
                    username = data["username"]
                    name = data["name"]
                    link = data["link"]
                    desc = data["desc"]
                    project_id = data["project_id"]

                    # Кнопки для модератора
                    kb = InlineKeyboardMarkup(inline_keyboard=[
                        [
                            InlineKeyboardButton(text="✅ Принять", callback_data=f"mod_project_submit_approve:{user_id}:{project_id}"),
                            InlineKeyboardButton(text="❌ Отклонить", callback_data=f"mod_project_submit_reject:{user_id}:{project_id}")
                        ]
                    ])

                    user_info = f'👤 От: <a href="https://t.me/{username}">{user_id}</a>' if username else f"👤 От: неизвестно, ID - <code>{user_id}</code>"

                    await bot.send_message(
                        chat_id=ADMIN_CHAT_ID,
                        text=(
                            f"🆕 <b>Новый проект на мясорубку!</b>\n\n"
                            f"{user_info}\n"
                            f"💼 Название: {name}\n"
                            f"🔗 Ссылка: {link}\n"
                            f"📝 Описание: {desc}"
                        ),
                        parse_mode="HTML",
                        reply_markup=kb
                    )


        except Exception as e:
            print(f"Ошибка в воркере модерации: {e}")
            await asyncio.sleep(3)