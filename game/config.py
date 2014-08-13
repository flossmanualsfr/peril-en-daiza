# execute once
from bge import logic
import configparser

def init(cont):
    settings = configparser.ConfigParser()
    settings.read(logic.expandPath("//config.ini"))
    cont.owner["settings"] = settings
    update(cont)

def change(cont):
    cont.owner["settings"].set("CONFIG", "language", cont.owner["language"])
    update(cont)
    save(cont)

def update(cont):
    new_lang = cont.owner["settings"].get("CONFIG", "language")
    logic.globalDict["LANG"] = new_lang
    cont.activate(cont.actuators["set_panel_{0}".format(new_lang)])

def save(cont):
    with open(logic.expandPath("//config.ini"), 'w') as configfile:
        cont.owner["settings"].write(configfile)