# execute once
from bge import logic
import configparser

settings = configparser.ConfigParser()
settings.read('config.ini')
logic.globalDict["LANG"] = settings.get("CONFIG", "language")
