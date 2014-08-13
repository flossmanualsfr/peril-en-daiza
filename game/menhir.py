import bge

def up(cont):
    menhir = cont.owner
    menhir.position.z = 1
    print("up")

def down(cont):
    menhir = cont.owner
    menhir.position.z = -1
    print("down")