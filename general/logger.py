from general.decorating import colorize, Color
import logging

DEBUG_COLORS = {
    'DEBUG': Color.WHITE,
    'INFO': Color.GREEN,
    'WARNING': Color.YELLOW,
    'ERROR': Color.RED,
    'CRITICAL': Color.BOLD_RED
}


def format_template(
        level_format: callable,
        name_format: callable,
        record: logging.LogRecord,
        header: str = ""
        ):
    format_string: str
    level_spacing = " " * (9 - len(record.levelname))
    name_spacing = " " * (25 - len(record.name))
    format_string = header
    format_string += level_format('%(levelname)s') + ':' + level_spacing
    format_string += name_format('%(name)s') + ':' + name_spacing
    format_string += '%(message)s'
    formatter = logging.Formatter(format_string)
    return formatter.format(record)


class ColorFormatter(logging.Formatter):
    def format(self, record: logging.LogRecord):
        color = DEBUG_COLORS[record.levelname]
        return format_template(
            lambda level: colorize(level, color),
            lambda name: colorize(name, Color.GRAY),
            record
        )


class RegularFormatter(logging.Formatter):
    def format(self, record):
        return format_template(
            lambda level: level,
            lambda name: name,
            record,
            '%(asctime)s: '
        )


def init_logger(
        level: str | int = "DEBUG",
        filename: str | None = None,
        console: bool = True
        ) -> None:
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)
    logging.getLogger('asyncio').setLevel(logging.WARNING)
    logging.getLogger('asyncssh').setLevel(logging.WARNING)
    logging.getLogger('multipart.multipart').setLevel(logging.WARNING)
    if console:
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(ColorFormatter())
        console_handler.setLevel(level)
        logger.addHandler(console_handler)
    if not filename:
        return
    file_handler = logging.FileHandler(filename)
    file_handler.setFormatter(RegularFormatter())
    logger.addHandler(file_handler)
