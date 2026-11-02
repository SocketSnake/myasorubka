from aiogram import BaseMiddleware
from typing import Callable, Dict, Any, Awaitable
from aiogram.types import TelegramObject

from database.base import async_session_maker as mmyaso_asm
from public_bot_db.base import async_session_maker as submeat_asm


class DBmmyasoSessionMiddleware(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: Dict[str, Any]
    ) -> Any:
        async with mmyaso_asm() as session:
            data["db_mmyaso_session"] = session
            return await handler(event, data)

class DBsubmeatSessionMiddleware(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: Dict[str, Any]
    ) -> Any:
        async with submeat_asm() as session:
            data["db_submeat_session"] = session
            return await handler(event, data)