from .pcg import PCG

# separted by wall
def cavalryVsInfantry():
    builder = PCG()
    builder.addCavalryArcher()
    builder.addSpearman()
    builder.addWall()
    builder.write("CavalryvsInfantry.xml")

# surrounded by a fort
def cavalryVsInfantryF1():
    builder = PCG()
    # builder.addCavalryArcher()
    # builder.addSpearman()
    # # builder.addWall()
    # builder.write("CavalryvsInfantryF1.xml")


if __name__ == '__main__':
    print("Building")
    cavalryVsInfantry()
    # cavalryVsInfantryF1()
    print("Done.")