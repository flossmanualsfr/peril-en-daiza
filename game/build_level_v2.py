import math
import json
import bpy
import os

TILE_SIZE = 32

def rename(obj, name):
    for i in range(2):
        obj.name = name

def load_tiles_info():
    tiles_info_ground = {}
    tiles_info_object = {}
    i = 1
    
    for tiles_info, level_name in [(tiles_info_ground, "tiles_info_ground"), (tiles_info_object, "tiles_info_object")]:
        f = open(bpy.path.abspath("//levels/"+level_name+".dat"), 'r')
        for line in f.readlines():
            text = line.strip()
            if text != "":
                typename, angle = text.split()
                tiles_info[i] = (typename, math.radians(int(angle)))
                i += 1
        f.close()
    return tiles_info_ground, tiles_info_object

def read_layer(level_name, layer, tiles_info, width, height, physic_level = None):
    objs = layer["data"]
    j = 0
    for i_tile in range(len(objs)):
        type = objs[i_tile]
        x = i_tile % width
        y = -(i_tile // width)
        try:
            typename, angle = tiles_info[type]
        except KeyError:
            continue
        if typename != "none":
            loc = (2*x, 2*y, 0)
            rot = (0, 0, angle)
            
            print(typename, loc)
            
            bpy.ops.object.add(location = loc, rotation = rot)
            graphic_obj = bpy.context.object
            graphic_obj.dupli_type = 'GROUP'
            graphic_obj.dupli_group = bpy.data.groups[typename]
            
            if physic_level != None:
                rename(graphic_obj, "ground_{0}_{1:04}".format(level_name, j))
                graphic_obj.empty_draw_type = 'CUBE'
                physic_obj = bpy.data.objects.new("temp", bpy.data.meshes[typename+"_mesh"])
                physic_obj.location = loc
                physic_obj.rotation_euler = rot
                bpy.context.scene.objects.link(physic_obj)
                physic_obj.select = True
                physic_level.select = True
                bpy.context.scene.objects.active = physic_level
                bpy.ops.object.join()
            else:
                rename(graphic_obj, "object_{0}_{1:04}".format(level_name, j))
                graphic_obj.empty_draw_type = 'SPHERE'
            j += 1

def read_layer_target(level_name, layer, width, height):
    objs = layer["objects"]
    j = 0
    for object in objs:
        type = object["type"]
        x = object["x"]/TILE_SIZE
        y = -object["y"]/TILE_SIZE
        if type == "target":
            loc = (2*x, 2*y, 0)
            bpy.ops.object.add(location = loc)
            target_obj = bpy.context.object
            target_obj.empty_draw_type = 'SINGLE_ARROW'
            target_obj.empty_draw_size = 4
            rename(target_obj, "target_{0}_{1:04}".format(level_name, j))
            for prop_name, value in object["properties"].items():
                bpy.ops.object.game_property_new(name = prop_name)
                if value.isdigit():
                    target_obj.game.properties[prop_name].type = 'INT'
                    target_obj.game.properties[prop_name].value = int(value)
                else:
                    target_obj.game.properties[prop_name].type = 'STRING'
                    target_obj.game.properties[prop_name].value = value
            j += 1

def load_level(filepath):
    f = open(filepath, 'r')
    level_data = json.load(f)
    f.close()

    width = level_data["width"]
    height = level_data["height"]
    next_level_name = level_data["properties"].get("next_level", "")
    
    layer_ground = {"data":[]}
    layer_object = {"data":[]}
    layer_target = {"objects":[]}
    for layer in level_data["layers"]:
        name = layer["name"]
        if name == "ground":
            layer_ground = layer
        if name == "object":
            layer_object = layer
        if name == "target":
            layer_target = layer
    return layer_ground, layer_object, layer_target, width, height, next_level_name

def create_scene(level_name):
    print(level_name)
    for scene in bpy.data.scenes:
        if scene.name == level_name:
            bpy.context.screen.scene = scene
            bpy.ops.scene.delete()
    bpy.ops.scene.new(type = 'EMPTY')
    bpy.context.scene.name = level_name
    bpy.context.scene.world = bpy.data.worlds["World_level"]

def create_lamp(level_name, width, height):
    #the lamp is added at the middle of the level
    bpy.ops.object.lamp_add(location = (width, -height, 35), type = 'POINT')
    lamp = bpy.context.object
    lamp.data = bpy.data.lamps["light_day"]
    rename(lamp, "lamp_{0}".format(level_name))

def create_level_logic(level_name):
    bpy.ops.object.add(location = (0, 0, 10))
    logic_master = bpy.context.object
    logic_master.dupli_type = 'GROUP'
    logic_master.dupli_group = bpy.data.groups["level_logic"]
    rename(logic_master, "level_logic_{0}".format(level_name))

def create_camera(level_name, next_level_name, width, height):
    bpy.ops.object.camera_add(location = (width, -height, 20), rotation = (0, 0, 0))
    camera = bpy.context.object
    camera.data = bpy.data.cameras["camera_dummy"]
    rename(camera, "camera_dummy_{0}".format(level_name))
    bpy.context.scene.camera = camera
    bpy.ops.view3d.viewnumpad(type = 'CAMERA')
    bpy.ops.object.game_property_new(name = "next_level")
    camera.game.properties["next_level"].type = 'STRING'
    camera.game.properties["next_level"].value = next_level_name
    bpy.ops.logic.sensor_add(type = 'MESSAGE', name = 'sMessageFadeOutDone')
    sMessageFadeOutDone = camera.game.sensors["sMessageFadeOutDone"]
    sMessageFadeOutDone.subject = "fade_out_done"
    bpy.ops.logic.controller_add(type = 'PYTHON', name = 'cNextLevel')
    cNextLevel = camera.game.controllers["cNextLevel"]
    cNextLevel.mode = 'MODULE'
    cNextLevel.module = "set_next_level.main"
    sMessageFadeOutDone.link(cNextLevel)

def link_magic():
    magic = bpy.data.objects["Magic"]
    scene = bpy.context.scene
    scene.objects.link(magic)
    magic.layers = (False, False, True, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False)
    for obj in magic.children:
        scene.objects.link(obj)
        obj.layers = (False, False, True, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False)

def read_json_file(context, filepath):
    level_name = os.path.basename(filepath).replace(".json", "")
    
    #create a scene with the correct name
    create_scene(level_name)
    #tiles info are used to know which dupligroup to add
    tiles_info_ground, tiles_info_object  = load_tiles_info()
    #load the level: three layers and a width/size
    layer_ground, layer_object, layer_target, width, height, next_level_name = load_level(filepath)
    
    #prepare a physic mesh for the ground
    bpy.context.scene.cursor_location = (0.0,0.0,0.0)
    bpy.ops.object.add(type='MESH')
    physic_level = bpy.context.object
    rename(physic_level, "physic_"+level_name)
    rename(physic_level.data, "physic_"+level_name+"_mesh")
    physic_level.draw_type = 'WIRE'
    physic_level.game.physics_type = 'STATIC'
    physic_level.game.use_collision_bounds = True
    physic_level.game.collision_bounds_type = 'TRIANGLE_MESH'
    physic_level.hide_render = True
    
    #read the ground layer; the ground's physic mesh gets modified
    read_layer(level_name, layer_ground, tiles_info_ground, width, height, physic_level)
    #read the object layer; no physic mesh to modify is provided
    read_layer(level_name, layer_object, tiles_info_object, width, height)
    #read the target layer; only their location and properties are used
    read_layer_target(level_name, layer_target, width, height)
    
    #cleanup the ground's physic mesh (remove doubles)
    physic_level.select = True
    bpy.context.scene.objects.active = physic_level
    bpy.ops.object.mode_set(mode='EDIT')
    bpy.ops.mesh.select_all(action='SELECT')
    bpy.ops.mesh.remove_doubles(threshold=0.0001)
    bpy.ops.mesh.select_all(action='DESELECT')
    bpy.ops.object.mode_set(mode='OBJECT')
    
    #generate the navmesh
    bpy.ops.mesh.navmesh_make()
    navmesh = bpy.context.object
    rename(navmesh, "Navmesh_"+level_name)
    rename(navmesh.data, "Navmesh_"+level_name)
    navmesh.draw_type = 'WIRE'
    
    #add a lamp, default is light_day
    create_lamp(level_name, width, height)
    
    #add a logic master
    create_level_logic(level_name)
    
    #add a dummy camera
    create_camera(level_name, next_level_name, width, height)
    
    #link the magic power from the resources
    link_magic()
    
    return {'FINISHED'}

# ImportHelper is a helper class, defines filename and
# invoke() function which calls the file selector.
from bpy_extras.io_utils import ImportHelper
from bpy.props import StringProperty, BoolProperty, EnumProperty
from bpy.types import Operator


class ImportPIDLevel(Operator, ImportHelper):
    """Select a .json file that you have created with Tiled"""
    bl_idname = "build_level_pid.json"  # important since its how bpy.ops.build_level_pid.json is constructed
    bl_label = "Import Json File"

    # ImportHelper mixin class uses this
    filename_ext = ".json"

    filter_glob = StringProperty(
            default="*.json",
            options={'HIDDEN'},
            )

    def execute(self, context):
        return read_json_file(context, self.filepath)

class ImportPIDPanel(bpy.types.Panel):
    bl_label = "Build Peril-in-Daiza"
    bl_space_type = "VIEW_3D"
    bl_region_type = "TOOL_PROPS"
    
    def draw(self, context):
        self.layout.operator("build_level_pid.json", text='Import .json level')

# Only needed if you want to add into a dynamic menu
#def menu_json_import(self, context):
#    self.layout.operator(ImportPIDLevel.bl_idname, text="Json Import operator")


def register():
    bpy.utils.register_class(ImportPIDLevel)
    bpy.utils.register_class(ImportPIDPanel)
    #bpy.types.INFO_MT_file_import.append(menu_json_import)


def unregister():
    bpy.utils.unregister_class(ImportPIDLevel)
    bpy.utils.unregister_class(ImportPIDPanel)
    #bpy.types.INFO_MT_file_import.remove(menu_json_import)


if __name__ == "__main__":
    register()
