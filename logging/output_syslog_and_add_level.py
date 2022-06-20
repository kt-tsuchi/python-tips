import logging
from logging import handlers

LOG_DEVICE = '/dev/log'
NOTICE = 25

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

if __name__ == "__main__":
    # Add log level and notice method
    logging.addLevelName(NOTICE, 'NOTICE')
    logging.handlers.SysLogHandler.priority_map.update({'NOTICE' : 'notice'})
    logging.setLoggerClass(UnixLogger)

    # Set the logger
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.DEBUG)
    ch = logging.handlers.SysLogHandler(LOG_DEVICE)
    ch.setLevel(logging.DEBUG)
    formatter = logging.Formatter('%(name)s [%(process)d]: %(message)s')
    ch.setFormatter(formatter)
    logger.addHandler(ch)

    # Output to system log
    logger.debug('DEBUG')
    logger.info('INFO')
    logger.notice('NOTICE')
    logger.error('ERROR')
    logger.warning('WARNING')
    logger.critical('CRITICAL')
