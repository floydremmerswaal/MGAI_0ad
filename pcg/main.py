from city import City
from pcg import PCG
from math import radians
from maze import Maze
import numpy as np

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

    builder.write("CavalryVsInfantryF1.xml")

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

    builder.write("CavalryVsInfantryF2.xml")


def cavalryVsInfantryMaze(maze_height, maze_width):
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

    builder.write("CavalryVsInfantryMaze.xml")

def cavalryVsInfantryDistrict():
    builder = PCG()
    city_generator = City()
    map_height = 2048
    map_width =  2048
    
    outer_radius = int(map_height / 2) - 100
    inner_radius = int(outer_radius / 3)
    center_coords = np.array([map_height / 2, map_width / 2])

    city_generator.generate_circle(builder, inner_radius, center_coords)
    city_generator.generate_circle(builder, outer_radius, center_coords)
    city_generator.generate_watch_towers_circle(builder, outer_radius, center_coords)

    no_districts = 10
    district_centers = city_generator.generate_districts(builder, outer_radius, inner_radius, center_coords, no_districts)

    city_generator.generate_district_boundaries(builder, outer_radius, inner_radius, center_coords, district_centers)
    
    district_centers2 = city_generator.generate_districts(builder, inner_radius, 0, center_coords, no_districts=1, no_highways=10)

    city_generator.generate_district_boundaries(builder, inner_radius, 0, center_coords, district_centers2)
    
    city_generator.generate_structures_in_district_polygon(builder)

    builder.write("CavalryVsInfantryDistricts.xml")

if __name__ == '__main__':
    print("Building scenarios...")
    # cavalryVsInfantry()
    # cavalryVsInfantryF1()
    # cavalryVsInfantryF2()
    # cavalryVsInfantryMaze(maze_height=10, maze_width=12)
    cavalryVsInfantryDistrict()
    print("Done.")
