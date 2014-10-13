from bge import logic, render
import blf
import bgl

import codecs
import configparser
config = configparser.ConfigParser()
config.readfp(codecs.open(logic.expandPath("//text/" + logic.globalDict["LANG"] + ".ini"), "r", "utf8"))
l_timer = config.get("HUD", 'timer')
l_score = config.get("HUD", 'score')
l_vortex = config.get("HUD", 'vortex')
l_level = config.get("HUD", 'level')

dpi = 76

# to hold the total game time in seconds
game_timer = 0.0
# the current camera counting the seconds
active_camera = None
# the logic object counting the bamboo
bamboo_counter = None
# the logic object holding the panda object
panda = None
# to hold the level number
level = None

def init(cont):
    """init function - runs once"""
    global active_camera, game_timer, bamboo_counter, panda, level
    scene = logic.getCurrentScene()
    active_camera = cont.owner
    bamboo_counter = scene.objects["bambou_counter"]
    panda = scene.objects["Panda"]
    level = logic.globalDict["level"]
    # create a new font object, use external ttf file
    font_path = logic.expandPath('//text/Big_Bottom_Cartoon_AD.ttf')
    # store the font indice - to use later
    logic.font_id = blf.load(font_path)

    # set the font drawing routine to run every frame
    scene.post_draw = [write]
    # initialize the timer at the start of the scene
    active_camera["Timer"] = game_timer

def write():
    """write on screen"""
    # retrieve timer
    global game_timer
    scene = logic.getCurrentScene()
    game_timer = int(active_camera["Timer"])
    catched = bamboo_counter["catched"]
    total = bamboo_counter["total"]
    vortex = panda.power
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
    if game_timer < 60:
        blf.draw(font_id, "{0} : {1:02d}".format(l_timer,game_timer))
    else:
        blf.draw(font_id, "{0} : {1}:{2:02d}".format(l_timer,game_timer//60,game_timer%60))
    blf.position(font_id, width*0.02, height*0.90, 0)
    blf.draw(font_id, "{0} : {1}".format(l_level, level))
    blf.position(font_id, width*0.02, height*0.85, 0)
    blf.draw(font_id, "{0} : {1} / {2}".format(l_score, catched, total))
    blf.position(font_id, width*0.02, height*0.80, 0)
    blf.draw(font_id, "{0} : {1}".format(l_vortex, vortex))

