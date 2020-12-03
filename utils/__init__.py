import logging
from configparser import ConfigParser
from typing import List
from typing import Optional


def read_config(config_path: str,
                required_fields: Optional[List[str]] = None) -> ConfigParser:
    config = ConfigParser()
    config.read(config_path)

    if required_fields:
        for field in required_fields:
            if not config[config.default_section].get(field):
                raise AttributeError(f'{field} must be defined!')

    return config


def make_logger(debug: bool = False,
                name: Optional[str] = None,
                formatter: Optional[logging.Formatter] = None) -> logging.Logger:
    if not formatter:
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                                      datefmt='%Y-%m-%d-%H:%M:%S')
    logger_level = logging.DEBUG if debug else logging.INFO
    logger_name = name if name else __name__
    logger_formatter = formatter

    logger = logging.getLogger(logger_name)
    logger.setLevel(logger_level)

    ch = logging.StreamHandler()
    ch.setLevel(logger_level)
    ch.setFormatter(logger_formatter)

    logger.addHandler(ch)

    return logger


def pixel_gen(size, pixels):
    width, height = size
    for x in range(width):
        for y in range(height):
            yield (x, y), list(pixels[x, y])
