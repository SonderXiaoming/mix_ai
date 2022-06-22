from hoshino.config import NICKNAME as nicknames

TL_ON = False
TL_KEY = ''

ALAPI_ON = False
ALAPI_TOKEN = ''

TENCENT_ON = False
SecretId = '' #  填你的SecretId
SecretKey = ''#  填你的SecretKey

name = 0#从元组选名字
NICKNAME = nicknames[name] if len(list(nicknames)) > 1 else nicknames

DEFAULT_AI_CHANCE = 0

BANNED_WORD = (
    'rbq', 'RBQ', '憨批', '废物', '死妈', '崽种', '傻逼', '傻逼玩意',
    '没用东西', '傻B', '傻b', 'SB', 'sb', '煞笔', 'cnm', '爬', 'kkp',
    'nmsl', 'D区', '口区', '我是你爹', 'nmbiss', '弱智', '给爷爬', '杂种爬','爪巴'
)