import logging

LEVEL_SPACING = 9
NAME_SPACING = 20


class Color:
    """ANSI escape codes for colors."""

    WHITE = "\x1b[37;20m"
    GRAY = "\x1b[90;20m"
    GREEN = "\x1b[32;20m"
    YELLOW = "\x1b[33;20m"
    RED = "\x1b[31;20m"
    BOLD_RED = "\x1b[31;1m"
    RESET = "\x1b[0m"


DEBUG_COLORS = {
    "DEBUG": Color.WHITE,
    "INFO": Color.GREEN,
    "WARNING": Color.YELLOW,
    "ERROR": Color.RED,
    "CRITICAL": Color.BOLD_RED,
}


def colorize(text: str, color: str) -> str:
    """Colorize text with ANSI escape codes."""
    return color + text + Color.RESET


def format_template(
    level_format: callable,
    name_format: callable,
    record: logging.LogRecord,
    header: str = "",
) -> str:
    """Format a log record using a template."""
    format_string = ""
    level_spacing = " " * (LEVEL_SPACING - len(record.levelname))
    name_spacing = " " * (NAME_SPACING - len(record.name))
    format_string += header
    format_string += level_format("%(levelname)s") + ":" + level_spacing
    format_string += name_format("%(name)s") + ":" + name_spacing
    format_string += "%(message)s"
    formatter = logging.Formatter(format_string)
    return formatter.format(record)


class ColorFormatter(logging.Formatter):
    """A logging formatter that colorizes the output."""

    def format(self, record: logging.LogRecord) -> str:
        color = DEBUG_COLORS[record.levelname]
        return format_template(
            lambda level: colorize(level, color),
            lambda name: colorize(name, Color.GRAY),
            record,
        )


class RegularFormatter(logging.Formatter):
    """A logging formatter that does not colorize the output."""

    def format(self, record: logging.LogRecord) -> str:
        return format_template(
            lambda level: level, lambda name: name, record, "%(asctime)s: "
        )


def init_logger(
    level: str | int = "DEBUG",
    filename: str | None = None,
    console: bool = True,
):
    """Initialize the logger."""
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)
    logging.getLogger("aiomysql").setLevel("WARNING")
    fastapi_logger = logging.getLogger("uvicorn.access")
    fastapi_logger.handlers.clear()
    fastapi_logger.setLevel(logging.DEBUG)
    if console:
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(ColorFormatter())
        console_handler.setLevel(level)
        logger.addHandler(console_handler)
        fastapi_logger.addHandler(console_handler)
    if not filename:
        return
    file_handler = logging.FileHandler(filename)
    file_handler.setFormatter(RegularFormatter())
    logger.addHandler(file_handler)
