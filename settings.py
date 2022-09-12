import random
import time
screen_width=1280
tile_size=64
level_map=[
'XXXXXXXXXXXXXXXXXXXXXXXX',
'X                       ',
'X                       ',
'X                       ',
'X                       ',
'X                       ',
'X                       ',
'X                       ',
'X                      X',
'X                     XX',
'X        P           XXX',
'XXXXXXXXXXXXXXXXXXXXXXXX']
def generate():
    level_map=[
    'XXXXXXXXXXXXXXXXXXXXXXXX',
    'X                       ',
    'X                       ',
    'X                       ',
    'X                       ',
    'X                       ',
    'X                       ',
    'X                       ',
    'X                      X',
    'X                     XX',
    'X        P           XXX',
    'XXXXXXXXXXXXXXXXXXXXXXXX']

    random.seed(int(time.time()))
    for i in range(100):
        level_map[0]=level_map[0]+"X"
        for a in range(1,11):
            if random.randint(0,2)==0 and level_map[a-1][-1]!="X" and level_map[a-2][-1]!="X":
                toset="X"
            else:
                toset=" "
            level_map[a]=level_map[a]+toset
        #make sure no more than 3 wide gaps
        if level_map[11][-3]==" " and level_map[11][-2]==" " and level_map[11][-1]==" ":
            level_map[11]=level_map[11]+"X"
        else:
            if random.randint(0,2)==0:
                level_map[11]=level_map[11]+"X"
            else:
                level_map[11]=level_map[11]+" "
    return level_map
