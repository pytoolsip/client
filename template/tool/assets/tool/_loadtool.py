import os;

from _Global import _GG;
from function.base import *;

CURRENT_PATH = os.path.dirname(os.path.realpath(__file__)); # 当前文件目录

# 初始化命名空间
_GG("CacheManager").initNamespace(CURRENT_PATH);


# 以下进行初始化逻辑，如初始化事件ID和热键配置

