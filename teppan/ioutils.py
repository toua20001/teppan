from logging import getLogger
import configparser
import pandas as pd
from udexception import SaveTypeException, NotFoundArgsException
import sqlite3

# logger
logger = getLogger(__name__)
# config
config = configparser.ConfigParser()
config.read("config/teppan.conf", encoding="utf-8")


