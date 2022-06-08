import random

import entities

# some constants
#TODO : randomly choose entities and structures, some units are not working though
CAVARCHER = entities.units__pers__cavalry_archer_a
SPEARMAN = entities.units__pers__infantry_spearman_a
WALL = entities.structures__athen__wall_long
TOWER = entities.structures__athen__wall_tower
GATE = entities.structures__athen__wall_gate

# the 'original' but by all means use different values if you want to

TEAM1_X = "448.57908" 
TEAM1_Z = "271.52103"

TEAM2_X = "465.83927" 
TEAM2_Z = "251.56336"

ORIENTATION = "2.35621"

class Entity():
    def __init__(self, entitytype, team, posx, posz, orientation, id):
        self.entitytype = entitytype
        self.team = team
        self.posx = posx
        self.posz = posz
        self.orientation = orientation
        self.id = id

    def printXML(self):
        return(str(self))

    def __str__(self):
        seed = random.randint(10000, 100000) # I have no idea if this is relevant? looks okay though x)

        return f"""<Entity uid="{self.id}">
			<Template>{self.entitytype}</Template>
			<Player>{self.team}</Player>
			<Position x="{self.posx}" z="{self.posz}"/>
			<Orientation y="{self.orientation}"/>
			<Actor seed="{seed}"/>
		</Entity>\n"""

class PCG():

    entityList = []

    def __init__(self):
        pass

    def __str__(self):
        result = ""
        try:
            start = open("pcg/templates/template_start.xml", "r")
            end = open("pcg/templates/template_end.xml", "r")

            for line in start:
                result += f"{line}"
            
            for entity in self.entityList:
                result += str(entity)

            for line in end:
                result += f"{line}"
            
            start.close()
            end.close()
        except Exception as e: print(e)

        return result

    def addBareEntity(self, entitytype, team, posx, posz, orientation):
        n = len(self.entityList) + 11 # + 11 for some reason that is not apparent to me (crashes otherwise)
        new_entity = Entity(entitytype, team, posx, posz, orientation, n)
        self.addEntity(new_entity)

    def addEntity(self, entity):
        self.entityList.append(entity)

    def addCavalryArcher(self, posx = TEAM1_X, posz = TEAM1_Z, orientation = ORIENTATION, team = 1):
        self.addBareEntity(CAVARCHER, team, posx, posz, orientation)

    def addSpearman(self, posx = TEAM2_X, posz = TEAM2_Z, orientation = ORIENTATION, team = 2):
        self.addBareEntity(SPEARMAN, team, posx, posz, orientation)

    def addWall(self, posx = None, posz = None, orientation = ORIENTATION, team = 0):

        if posx is None:
            posx = f"{((float(TEAM1_X) + float(TEAM2_X)) / 2):.5f}"
        if posz is None:
            posz = f"{((float(TEAM1_Z) + float(TEAM2_Z)) / 2):.5f}"

        self.addBareEntity(WALL, team, posx, posz, orientation)

    def addTower(self, posx = None, posz = None, orientation = ORIENTATION, team = 0):

        if posx is None:
            posx = f"{((float(TEAM1_X) + float(TEAM2_X)) / 2):.5f}"
        if posz is None:
            posz = f"{((float(TEAM1_Z) + float(TEAM2_Z)) / 2):.5f}"

        self.addBareEntity(TOWER, team, posx, posz, orientation)
   
    def addSquareBoundary(self, posx1, posz1, posx2, posz2):
        # orientations are pre-determined as there is no effective way to calculate them(yet).
        self.addWall(posx1, posz1, "-2.41228")
        self.addWall(posx2, posz1, "2.30707")
        self.addWall(posx1, posz2, "2.35621")
        self.addWall(posx2, posz2, "0.73993")
    
    def addSquareBoundaryWithGate(self, posx1, posz1, posx2, posz2, team = 0):
        self.addWall(posx1, posz1, "-2.41228")
        self.addWall(posx2, posz1, "2.30707")
        self.addBareEntity(GATE, team, posx1, posz2, "2.35621")
        self.addWall(posx2, posz2, "0.73993")

    def printXML(self):
        print(str(self))

    def write(self, filename):
        try:
            f = open(filename, "w")
            f.write(str(self))
            f.close()
        except:
            print("Error while writing")



# test = PCG()

# test.addCavalryArcher()
# test.addSpearman()
# test.addWall()

# test.write("test.xml")