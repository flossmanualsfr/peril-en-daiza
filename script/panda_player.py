from bge import logic, events, types, constraints
from mathutils import Vector

def keyDown(kevt):
    return logic.keyboard.events[kevt] == logic.KX_INPUT_ACTIVE
def keyHit(kevt):
    return logic.keyboard.events[kevt] == logic.KX_INPUT_JUST_ACTIVATED

class Panda(types.KX_GameObject):
    
    def __init__(self, own):
        self.speed = .06
        #self.speed = .2
        self.factor = 0.70710678
        self.KX_Char = constraints.getCharacter(self)
        self.BL_Armature = self.children[0]
        self.stop = False
        self.frame = 0
        self.score = 0
        self.power = 3
    
    def main(self):
        self.move()
        self.anim()
        self.action()
    
    def move(self):
        x = 0
        y = 0
        if not self.stop:
            y = keyDown(events.UPARROWKEY) - keyDown(events.DOWNARROWKEY)
            x = keyDown(events.RIGHTARROWKEY) - keyDown(events.LEFTARROWKEY)
        if x and y and not self.frame:
            self.KX_Char.walkDirection = [x*self.speed*self.factor, y*self.speed*self.factor, 0.0]
        elif (x or y) and not self.frame:
            self.KX_Char.walkDirection = [x*self.speed, y*self.speed, 0.0]
        else:
            self.KX_Char.walkDirection = (0.0, 0.0, 0.0)
        vec = Vector((x, y, 0.0))
        if x != 0 or y != 0:
            self.alignAxisToVect(vec, 0)
    
    def miam(self):
        hitObj = self.sensors["Eat"].hitObject
        if hitObj:
            self.sensors["Eat"].hitObject.endObject()
            self.score += 1
    
    def action(self):
        if keyHit(events.SPACEKEY) and self.frame < 2 and self.power > 0:
            magic = logic.getCurrentScene().addObject("Magic", self.children[0])
            magic.localScale = (1, 1, 1)
            magic.worldPosition.z += 0.1
            self.power -= 1
            
    
    def anim_win(self):
        self.BL_Armature.stopAction(1)
        self.BL_Armature.stopAction(2)
        self.BL_Armature.playAction(
                "WinDance",
                0,
                90,
                0,
                0,
                5,
                logic.KX_ACTION_MODE_PLAY)
    
    def anim_loose(self):
        self.BL_Armature.stopAction(1)
        self.BL_Armature.stopAction(2)
        self.BL_Armature.playAction(
                "panda_death",
                0,
                80,
                0,
                0,
                4,
                logic.KX_ACTION_MODE_PLAY)
    def anim_action(self):
        self.BL_Armature.stopAction(2)
        self.BL_Armature.playAction(
                "panda_baton",
                0,
                27,
                1,
                0,
                3,
                logic.KX_ACTION_MODE_PLAY)
    
    def anim_walk(self):
        self.BL_Armature.stopAction(2)
        # ou panda_walk_cycle_smooth panda_run_cycle
        self.BL_Armature.playAction(
                "panda_walk_cycle_smooth",
                0,
                24,
                1,
                1,
                4,
                logic.KX_ACTION_MODE_LOOP,
                layer_weight=0.0,
                ipo_flags=0,
                speed=3.0)
    
    def anim_idle(self):
        self.BL_Armature.stopAction(1)
        self.BL_Armature.playAction(
                "panda_idle",
                0,
                310,
                2,
                0,
                5,
                logic.KX_ACTION_MODE_LOOP)
    
    def anim(self):
        """
        0 : Death (layer 0)
        1 : Win (layer 0)
        2 : Action (layer 1)
        3 : Walk (layer 1)
        4 : Idle (layer 2)
        self.playAction(
                        name,
                        start_frame,
                        end_frame,
                        layer=0,
                        priority=0,
                        blendin=0,
                        play_mode=KX_ACTION_MODE_PLAY,
                        layer_weight=0.0,
                        ipo_flags=0,
                        speed=1.0,
                        blend_mode=KX_ACTION_BLEND_BLEND
                       )
        """
        #if True: #WIN
        #    self.anim_win()
        if self.stop: #Death
            self.anim_loose()
        elif events.SPACEKEY in logic.keyboard.active_events and not self.frame and self.power: #Action
            self.anim_action()
            self.frame += 1
        elif self.frame and self.frame < 67:
            self.frame += 1
        elif self.frame == 67:
            self.frame = 0
        elif self.KX_Char.walkDirection != Vector((0.0, 0.0, 0.0)):
            self.anim_walk()
        else:
            self.anim_idle()
        #END ANIM
    
    def kill(self):
        self.stop = True

def main(cont):
    own = cont.owner
    if not "init" in own:
        own["init"] = True
        Panda(own)
    else:
        own.main()

def miam(cont):
    own = cont.owner
    own.miam()

def kill(cont):
    own = cont.owner
    own.kill()
