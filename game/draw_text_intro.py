# import game engine modules
from bge import render
from bge import logic
# import stand alone modules
import bgl
import blf

import codecs
text = ""
with codecs.open(logic.expandPath("//text/" + logic.globalDict["LANG"] + ".txt"), 'r', 'utf8') as f:
    text = [e.strip() for e in f.readlines()]
import configparser
config = configparser.ConfigParser()
config.readfp(codecs.open(logic.expandPath("//text/" + logic.globalDict["LANG"] + ".ini"), "r", "utf8"))
skip = config.get("ACTION", 'skip')

# camera["Timer"] using 'Timer' type to allow fading
timer = 5
fade = 0.01
wait = 4

dpi = 76

def init():
    """init function - runs once"""
    # create a new font object, use external ttf file
    font_path = logic.expandPath('//text/Big_Bottom_Cartoon_AD.ttf')
    italic_font_path = logic.expandPath('//text/Big_Bottom_Cartoon_Italic_AD.ttf')
    # store the font indice - to use later
    logic.font_id = blf.load(font_path)
    logic.font_id_italic = blf.load(italic_font_path)

    # set the font drawing routine to run every frame
    scene = logic.getCurrentScene()
    scene.post_draw = [write]

def write():
    """write on screen"""
    width = render.getWindowWidth()
    height = render.getWindowHeight()

    # OpenGL setup
    bgl.glMatrixMode(bgl.GL_PROJECTION)
    bgl.glLoadIdentity()
    bgl.gluOrtho2D(0, width, 0, height)
    bgl.glMatrixMode(bgl.GL_MODELVIEW)
    bgl.glLoadIdentity()
    
    bgl.glColor4f(1, 1, 1, 1)
    
    cam = logic.getCurrentScene().active_camera
    t = cam["Timer"]
    c = timer - t
    bgl.glColor4f(1, 1, 1, c)
    if cam["Switch"]:
        cam["Index"] += 1
        cam["Timer"] = 0
        cam["Switch"] = False
    # BLF drawing routine
    font_id = logic.font_id
    font_id_italic = logic.font_id_italic
    blf.position(font_id, width*0.03, height * 0.05, 0)
    blf.position(font_id_italic, width*0.03, height * 0.05, 0)
    blf.size(font_id, int(18 * (width/dpi) * 0.062), dpi)
    blf.size(font_id_italic, int(18 * (width/dpi) * 0.062), dpi)
    if cam["Index"] < 4:
        blf.draw(font_id, text[cam["Index"]])
    elif cam["Index"] < len(text):
        blf.draw(font_id_italic, text[cam["Index"]])
    
    # skip
    if cam["Index"] < 1:
        bgl.glColor4f(0.5, 0.5, 0.5, c)
        blf.position(font_id, width*0.02, height*0.9, 0)

        blf.draw(font_id, skip)
