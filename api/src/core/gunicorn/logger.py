from logging import Formatter

from gunicorn.glogging import Logger

from config import app_settings


class GunicornLogger(Logger):
    def setup(self, cfg) -> None:
        super().setup(cfg)

        self._set_handler(
            log=self.access_log,
            output=cfg.accesslog,
            fmt=Formatter(fmt=app_settings.logging.log_format),
        )
        self._set_handler(
            log=self.error_log,
            output=cfg.errorlog,
            fmt=Formatter(fmt=app_settings.logging.log_format),
        )
