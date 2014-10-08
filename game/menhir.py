import bge

def up(cont):
    menhir = cont.owner
    menhir.position.z = 1

def down(cont):
    menhir = cont.owner
    menhir.position.z = -1
