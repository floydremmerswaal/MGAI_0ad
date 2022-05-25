from pcg import PCG

# separated by wall
def cavalryVsInfantry():
    builder = PCG()
    builder.addCavalryArcher()
    builder.addSpearman()
    builder.addWall()
    builder.write("CavalryvsSpearman.xml")

# surrounded by a fort
def cavalryVsInfantryF1():
    builder = PCG()
    x1 = "483.3144"
    z1 = "116.94448"
    x2 = "510.98841"
    z2 = "143.71137"
    team1_orientation = "2.35621"
    team2_orientation = "-0.95878"
    builder.addSquareBoundary(x1, z1, x2, z2)
    # team 1 Cavalry
    builder.addCavalryArcher(float(x1)+2, float(z1)+3, team1_orientation, 1)
    builder.addCavalryArcher(float(x1)+3, float(z1)+5, team1_orientation, 1)
    builder.addCavalryArcher(float(x1)+4, float(z1)+7, team1_orientation, 1)
    builder.addCavalryArcher(float(x1)+5, float(z1)+9, team1_orientation, 1)
    # team 2 Infantry
    builder.addSpearman(float(x2)-2, float(z2)-3, team2_orientation, 1)
    builder.addSpearman(float(x2)-3, float(z2)-5, team2_orientation, 1)
    builder.addSpearman(float(x2)-4, float(z2)-7, team2_orientation, 1)
    builder.addSpearman(float(x2)-5, float(z2)-9, team2_orientation, 1)

    builder.write("CavalryVsSpearmanWalls.xml")

# surrounded by a fort with a gate
def cavalryVsInfantryF2():
    builder = PCG()
    x1 = "483.3144"
    z1 = "116.94448"
    x2 = "510.98841"
    z2 = "143.71137"
    team1_orientation = "2.35621"
    team2_orientation = "-0.95878"
    builder.addSquareBoundaryWithGate(x1, z1, x2, z2)
    # team 1 Cavalry
    builder.addCavalryArcher(float(x1)+2, float(z1)+3, team1_orientation, 1)
    builder.addCavalryArcher(float(x1)+3, float(z1)+5, team1_orientation, 1)
    builder.addCavalryArcher(float(x1)+4, float(z1)+7, team1_orientation, 1)
    builder.addCavalryArcher(float(x1)+5, float(z1)+9, team1_orientation, 1)
    # team 2 Infantry
    builder.addSpearman(float(x2)-2, float(z2)-3, team2_orientation, 1)
    builder.addSpearman(float(x2)-3, float(z2)-5, team2_orientation, 1)
    builder.addSpearman(float(x2)-4, float(z2)-7, team2_orientation, 1)
    builder.addSpearman(float(x2)-5, float(z2)-9, team2_orientation, 1)

    builder.write("CavalryVsSpearmanFort.xml")


if __name__ == '__main__':
    print("Building")
    # cavalryVsInfantry()
    cavalryVsInfantryF1()
    print("Done.")