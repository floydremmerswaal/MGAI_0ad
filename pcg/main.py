from pcg.city_generator import City
from pcg.pcg import PCG
from pcg.maze import Maze
import numpy as np
from math import radians
from random import random, randrange


def cavalryVsInfantry(filename: str = "CavalryvsSpearman.xml"): # separated by wall
    builder = PCG()
    builder.addCavalryArcher()
    builder.addSpearman()
    builder.addWall()
    builder.write(filename)


def cavalryVsInfantryF1(filename: str = "CavalryVsInfantryF1.xml"): # surrounded by a fort
    builder = PCG()
    x1 = "483.3144"
    z1 = "116.94448"
    x2 = "510.98841"
    z2 = "143.71137"
    team1_orientation = "2.35621"
    team2_orientation = "-0.95878"
    builder.addSquareBoundary(x1, z1, x2, z2)
    # team 1 Cavalry
    builder.addCavalryArcher(float(x1)+2, float(z1)+3, team1_orientation)
    builder.addCavalryArcher(float(x1)+3, float(z1)+5, team1_orientation)
    builder.addCavalryArcher(float(x1)+4, float(z1)+7, team1_orientation)
    builder.addCavalryArcher(float(x1)+5, float(z1)+9, team1_orientation)
    # team 2 Infantry
    builder.addSpearman(float(x2)-2, float(z2)-3, team2_orientation)
    builder.addSpearman(float(x2)-3, float(z2)-5, team2_orientation)
    builder.addSpearman(float(x2)-4, float(z2)-7, team2_orientation)
    builder.addSpearman(float(x2)-5, float(z2)-9, team2_orientation)

    builder.write(filename)


def cavalryVsInfantryF2(filename: str = "CavalryVsInfantryF2.xml"): # surrounded by a fort with a gate
    builder = PCG()
    x1 = "483.3144"
    z1 = "116.94448"
    x2 = "510.98841"
    z2 = "143.71137"
    team1_orientation = "2.35621"
    team2_orientation = "-0.95878"
    builder.addSquareBoundaryWithGate(x1, z1, x2, z2)
    # team 1 Cavalry
    builder.addCavalryArcher(float(x1)+2, float(z1)+3, team1_orientation)
    builder.addCavalryArcher(float(x1)+3, float(z1)+5, team1_orientation)
    builder.addCavalryArcher(float(x1)+4, float(z1)+7, team1_orientation)
    builder.addCavalryArcher(float(x1)+5, float(z1)+9, team1_orientation)
    # team 2 Infantry
    builder.addSpearman(float(x2)-2, float(z2)-3, team2_orientation)
    builder.addSpearman(float(x2)-3, float(z2)-5, team2_orientation)
    builder.addSpearman(float(x2)-4, float(z2)-7, team2_orientation)
    builder.addSpearman(float(x2)-5, float(z2)-9, team2_orientation)

    builder.write(filename)


def cavalryVsInfantryMaze(maze_height=10, maze_width=10, filename: str ="CavalryVsInfantryMaze.xml"):
    builder = PCG()

    WALL_LENGTH = 30

    WALL_ORIENTATION_UP_DOWN_DEG = 0 # useless but could be usefull later
    WALL_ORIENTATION_LEFT_RIGHT_DEG = 90

    WALL_ORIENTATION_UP_DOWN = radians(WALL_ORIENTATION_UP_DOWN_DEG) # useless but could be usefull later
    WALL_ORIENTATION_LEFT_RIGHT = radians(WALL_ORIENTATION_LEFT_RIGHT_DEG)

    # center in map
    x = (1024 / 2) - ((maze_height / 2) * WALL_LENGTH)
    z = (1024 / 2) - ((maze_width / 2) * WALL_LENGTH)
    
    maze = Maze(maze_height, maze_width)
    maze.generate()
    # maze.print_maze()

    flag = False

    for h in range(maze_height):
        for w in range(maze_width):
            if maze.maze[h][w] == maze.cell:
                if maze.maze[h][w + 1] == maze.wall:
                    builder.addWall((x + (h*WALL_LENGTH)), ((z + (w*WALL_LENGTH)) + WALL_LENGTH / 2), orientation=WALL_ORIENTATION_UP_DOWN)
                if maze.maze[h][w - 1] == maze.wall:
                    builder.addWall((x + (h*WALL_LENGTH)), ((z + (w*WALL_LENGTH)) - WALL_LENGTH / 2), orientation=WALL_ORIENTATION_UP_DOWN)
                if maze.maze[h + 1][w] == maze.wall:
                    builder.addWall(((x + (h*WALL_LENGTH)) + WALL_LENGTH / 2), (z + (w*WALL_LENGTH)), orientation=WALL_ORIENTATION_LEFT_RIGHT)
                if maze.maze[h - 1][w] == maze.wall:
                    builder.addWall(((x + (h*WALL_LENGTH)) - WALL_LENGTH / 2), (z + (w*WALL_LENGTH)), orientation=WALL_ORIENTATION_LEFT_RIGHT)

            if maze.maze[h][w] == maze.exit:
                builder.addWall((x + (h*WALL_LENGTH)), ((z + (w*WALL_LENGTH)) - WALL_LENGTH / 2), orientation=WALL_ORIENTATION_UP_DOWN)
                builder.addWall((x + (h*WALL_LENGTH)), ((z + (w*WALL_LENGTH)) + WALL_LENGTH / 2), orientation=WALL_ORIENTATION_UP_DOWN)

                if not flag:
                    builder.addCavalryArcher((x + (h*WALL_LENGTH)), (z + (w*WALL_LENGTH)) + 3, orientation=WALL_ORIENTATION_LEFT_RIGHT)
                    builder.addCavalryArcher((x + (h*WALL_LENGTH)), (z + (w*WALL_LENGTH)) + 1, orientation=WALL_ORIENTATION_LEFT_RIGHT)
                    builder.addCavalryArcher((x + (h*WALL_LENGTH)), (z + (w*WALL_LENGTH)) - 1, orientation=WALL_ORIENTATION_LEFT_RIGHT)
                    builder.addCavalryArcher((x + (h*WALL_LENGTH)), (z + (w*WALL_LENGTH)) - 3, orientation=WALL_ORIENTATION_LEFT_RIGHT)
                    flag = True
                else:
                    builder.addSpearman((x + (h*WALL_LENGTH)), (z + (w*WALL_LENGTH)) + 3, orientation=-WALL_ORIENTATION_LEFT_RIGHT)
                    builder.addSpearman((x + (h*WALL_LENGTH)), (z + (w*WALL_LENGTH)) + 1, orientation=-WALL_ORIENTATION_LEFT_RIGHT)
                    builder.addSpearman((x + (h*WALL_LENGTH)), (z + (w*WALL_LENGTH)) - 1, orientation=-WALL_ORIENTATION_LEFT_RIGHT)
                    builder.addSpearman((x + (h*WALL_LENGTH)), (z + (w*WALL_LENGTH)) - 3, orientation=-WALL_ORIENTATION_LEFT_RIGHT)


    builder.addTower((x - (WALL_LENGTH / 2 + 5)), (z - (WALL_LENGTH / 2 + 5)), orientation=WALL_ORIENTATION_LEFT_RIGHT)
    builder.addTower(((x + (maze_height - 1)*WALL_LENGTH) + (WALL_LENGTH / 2 + 5)), (z - (WALL_LENGTH / 2 + 5)), orientation=WALL_ORIENTATION_LEFT_RIGHT)
    builder.addTower((x - (WALL_LENGTH / 2 + 5)), ((z + (maze_width - 1)*WALL_LENGTH) + (WALL_LENGTH / 2 + 5)), orientation=WALL_ORIENTATION_LEFT_RIGHT)
    builder.addTower(((x + (maze_height - 1)*WALL_LENGTH) + (WALL_LENGTH / 2 + 5)), ((z + (maze_width - 1)*WALL_LENGTH) + (WALL_LENGTH / 2 + 5)), orientation=WALL_ORIENTATION_LEFT_RIGHT)

    for w in range(maze_width):
        builder.addWall((x - (WALL_LENGTH / 2 + 5)), (z + (w*WALL_LENGTH)), orientation=WALL_ORIENTATION_LEFT_RIGHT)
        builder.addWall(((x + (maze_height - 1)*WALL_LENGTH) + (WALL_LENGTH / 2 + 5)), (z + (w*WALL_LENGTH)), orientation=WALL_ORIENTATION_LEFT_RIGHT)

    for h in range(maze_height):
        builder.addWall((x + (h*WALL_LENGTH)), (z - (WALL_LENGTH / 2 + 5)), orientation=WALL_ORIENTATION_UP_DOWN)
        builder.addWall((x + (h*WALL_LENGTH)), ((z + (maze_width - 1) * WALL_LENGTH) + (WALL_LENGTH / 2 + 5)), orientation=WALL_ORIENTATION_UP_DOWN)

    builder.write(filename)


def cavalryVsInfantryCity(filename: str = "CavalryVsInfantryCity.xml"):
    civs =['athen', 'brit', 'cart','gaul', 'iber', 'kush', 'mace','maur', 'pers', 'ptol', 'rome', 'sele', 'spart']
    # civ = np.random.choice(civs)
    civ = 'athen'
    map_height = 2048
    map_width =  2048
    
    outer_radius = int(map_height / 2) - 100
    inner_radius = int(outer_radius / 3)
    center_coords = np.array([map_height / 2, map_width / 2])
    
    builder = PCG()
    city = City(builder, center_coords, [inner_radius, outer_radius], civ, 0)
    city.generate()
    
    builder.write(filename)
    

if __name__ == '__main__':
    print("Building scenarios...")
    # cavalryVsInfantry()
    # cavalryVsInfantryF1()
    # cavalryVsInfantryF2()
    # cavalryVsInfantryMaze(maze_height=10, maze_width=12)
    # cavalryVsInfantryCity()
    print("Done.")