import random
from .tool import anti_conflict
from hoshino import Service
from .data_source import get_chat_result,no_result,Config
from hoshino.config import NICKNAME
import os
from .setting import DEFAULT_AI_CHANCE,BANNED_WORD

file_name = 'config.json' 
CONFIG_PATH = os.path.join(os.path.dirname(__file__), file_name)

Keywords = ['bot','BOT','Bot','机器人']

NICKNAME_list = list(NICKNAME)
Keywords.extend(NICKNAME_list)

ai_chance = Config(CONFIG_PATH)

sv = Service('ai')

@sv.on_prefix(('调整AI概率'))
async def enable_aichat(bot, ev):
    s = ev.message.extract_plain_text()
    if s:
        if s.isdigit() and 0<=int(s)<51:
            chance = int(s)
        else:
            await bot.finish(ev, '参数错误: 请输入0-50之间的整数.')
    else:
        chance = DEFAULT_AI_CHANCE     # 后面不接数字时调整为默认概率
    ai_chance.set_chance(str(ev.group_id), chance)
    await bot.send(ev, f'人工智障已启用, 当前bot回复概率为{chance}%.')

@sv.on_fullmatch('当前AI概率')
async def enable_aichat(bot, ev):
    try:
        chance = ai_chance.chance[str(ev.group_id)]
    except:
        chance = 0
    await bot.send(ev, f'当前bot回复概率为{chance}%.')

@sv.on_message('group')
@anti_conflict
async def ai_chat(bot, ev):
    if str(ev.group_id) not in ai_chance.chance:
        return
    text = str(ev['message'])
    msg = ev['message'].extract_plain_text().strip()
    #whether @bot
    contains_keyword = False
    if not msg:
        return
    if f'[CQ:at,qq={ev["self_id"]}]' in text:
        contains_keyword = True
    #whether clash with other command
    for words in Keywords:
        if words in msg:
            contains_keyword = True
    if not contains_keyword and not random.randint(1,100) <= int(ai_chance.chance[str(ev.group_id)]):
        return
    qq=str(ev.user_id)
    info = await bot.get_group_member_info(
                group_id=int(ev.group_id), user_id=int(qq)
            )
    username = info.get("card", "") or info.get("nickname", "")
    result = await get_chat_result(msg, qq, username)
    sv.logger.info(
        f"问题：{msg} ---- 回答：{result}"
    )
    if result:
        result = str(result)
        for t in BANNED_WORD:
            result = result.replace(t, "*")
        await bot.send(ev, result)
    else:
        await bot.send(ev,no_result())