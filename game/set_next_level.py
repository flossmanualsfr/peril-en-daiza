import bge

def find_scene(name):
    for scene in bge.logic.getSceneList():
        print(scene.name)
        if scene.name == name:
            return True
    return False
    
def main(cont):
    camera_dummy = cont.owner
    logic = bge.logic
    scene = logic.getCurrentScene()
    if "level" not in logic.globalDict:
        logic.globalDict["level"] = 1
    else:
        logic.globalDict["level"] += 1
    if not "next_level" in camera_dummy or not scene.replace(camera_dummy["next_level"]):
        scene.replace("menu")
        logic.globalDict["level"] = 0
