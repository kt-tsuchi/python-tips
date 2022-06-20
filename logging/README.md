# Linuxのシステムログにログを出力する方法

PythonのログをLinuxのシステムログに出力するにはloggerの設定を行います。
ハンドラーにシステムログのデバイスファイルパスを渡すとログの出力先がシステムログになります。

<pre>
import logging
from logging import handlers

LOG_DEVICE = '/dev/log'

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG) ##出力の絞りはシステムログ側で行うためDEBUGに設定
ch = logging.handlers.SysLogHandler(LOG_DEVICE) # 出力先をシステムログへ
ch.setLevel(logging.DEBUG) #出力の絞りはシステムロ側で行うためDEBUGに設定
formatter = logging.Formatter('%(name)s [%(process)d]: %(message)s')
ch.setFormatter(formatter)
logger.addHandler(ch)

</pre>

# ログレベルと対応したメソッドをを追加する方法

デフォルトだとLinuxのシステムログで使用できるレベルがloggingモジュールにはなかったりします。
違和感なく使うため、今回はログレベルNoticeとメソッドを追加します。
※ログレベルの追加はあまり推奨されていないようです。今回はLinuxのシステムログで使えるログレベルと合わせたい意図があり追加しています。

<pre>

import logging
from logging import handlers

NOTICE = 25 #被りはNG INFOとWARNINGの間の数字にします。

# loggerクラスを継承したクラスを作成し、noticeメソッドを定義します。
class UnixLogger(logging.Logger):
    def __init__(self, name, level=logging.NOTSET):
        super().__init__(name, level)
    
    def notice(self, msg, *args, **kwargs):
        """
        Log 'msg % args' with severity 'NOTICE (25)'.
        To pass exception information, use the keyword argument exc_info with
        a true value, e.g.
        logger.notice("Houston, we have a %s", "thorny problem", exc_info=1)
        """

        if self.isEnabledFor(NOTICE):
            self._log(NOTICE, msg, args, **kwargs)

logging.addLevelName(NOTICE, 'NOTICE')
logging.handlers.SysLogHandler.priority_map.update({'NOTICE' : 'notice'})
logging.setLoggerClass(UnixLogger)
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

logger.notice('NOTICE') # 定義したnoticeメソッドが使えます。

</pre>