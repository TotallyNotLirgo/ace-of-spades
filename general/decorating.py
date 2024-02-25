class Color:
    WHITE = "\x1b[37;20m"
    GRAY = "\x1b[90;20m"
    GREEN = "\x1b[32;20m"
    YELLOW = "\x1b[33;20m"
    RED = "\x1b[31;20m"
    BOLD_RED = "\x1b[31;1m"
    RESET = "\x1b[0m"


def colorize(text: str, color: Color) -> str:
    return color + text + Color.RESET
