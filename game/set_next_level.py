import bge

def find_scene(name):
    for scene in bge.logic.getSceneList():
        print(scene.name)
        if scene.name == name:
            return True
    return False
    
def main(cont):
    camera_dummy = cont.owner
    scene = bge.logic.getCurrentScene()
    next_scene = "menu"
    if not "next_level" in camera_dummy or not scene.replace(camera_dummy["next_level"]):
        scene.replace("menu")
