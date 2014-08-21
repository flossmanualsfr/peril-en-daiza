from bge import logic, render
import blf
import bgl

import codecs
import configparser
config = configparser.ConfigParser()
config.readfp(codecs.open(logic.expandPath("//text/" + logic.globalDict["LANG"] + ".ini"), "r", "utf8"))
l_timer = config.get("HUD", 'timer')

dpi = 76

def init():
    """init function - runs once"""
    # create a new font object, use external ttf file
    font_path = logic.expandPath('//text/Big_Bottom_Cartoon_AD.ttf')
    # store the font indice - to use later
    logic.font_id = blf.load(font_path)

    # set the font drawing routine to run every frame
    scene = logic.getCurrentScene()
    scene.post_draw = [write, save_score]
    if "Timer" in logic.globalDict:
        scene.active_camera["Timer"] = logic.globalDict["Timer"]

def write():
    
    scene = logic.getCurrentScene()
    vortex = scene.objects["Panda"].power
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
    
    # BLF drawing routine
    font_id = logic.font_id
    blf.size(font_id, int(18 * (width/dpi) * 0.06), dpi)
    blf.position(font_id, width*0.02, height*0.95, 0)
    blf.draw(font_id, l_timer + " : " + str(int(scene.active_camera["Timer"])))
    blf.position(font_id, width*0.02, height*0.9, 0)
    blf.draw(font_id, "@ : " + str(vortex))

def save_score():

    scene = logic.getCurrentScene()
    logic.globalDict["Timer"] = scene.active_camera["Timer"]
