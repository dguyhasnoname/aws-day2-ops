import logging


class Logger:
    def get_logger(format):
        logger = logging.getLogger()
        logger.setLevel(logging.INFO)

        if format == "json":
            formatter = logging.Formatter(
                '{"time": "%(asctime)s", "origin": "%(name)s", "log_level": "%(levelname)s", "log": "%(message)s"}'
            )
        else:
            formatter = logging.Formatter(
                "[%(levelname)s] %(asctime)s p%(process)s %(filename)s:%(name)s:%(lineno)d %(message)s"
            )
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.DEBUG)
        console_handler.setFormatter(formatter)
        logger.addHandler(console_handler)

        return logger
