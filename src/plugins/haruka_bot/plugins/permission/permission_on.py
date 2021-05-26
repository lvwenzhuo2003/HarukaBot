from typing import Union
from nonebot import on_command
from nonebot.adapters.cqhttp import Bot
from nonebot.adapters.cqhttp.event import GroupMessageEvent, PrivateMessageEvent
from nonebot.permission import SUPERUSER
from nonebot.adapters.cqhttp.permission import GROUP_ADMIN, GROUP_OWNER
from nonebot.typing import T_State

from ...database import DB
from ...utils import to_me


permission_on = on_command('开启权限', rule=to_me(), 
    permission=GROUP_OWNER | GROUP_ADMIN | SUPERUSER, 
    priority=5)
permission_on.__doc__ = """开启权限 UID"""

@permission_on.handle()
async def _(bot: Bot, event: Union[PrivateMessageEvent, GroupMessageEvent],
            state: T_State):
    """根据 UID 开启权限"""
    
    if isinstance(event, PrivateMessageEvent):
        await permission_on.finish("只有群里才能开启权限")
        return # IDE 快乐行
    async with DB() as db:
        if await db.set_permission(event.group_id, True):
            await permission_on.finish("已开启权限，只有管理员和主人可以操作")
        await permission_on.finish("请勿重复开启权限")
