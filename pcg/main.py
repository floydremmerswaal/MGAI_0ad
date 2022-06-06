from numpy import outer
import numpy
from pyrsistent import v
from scipy import rand
from pcg import PCG, entities
from maze import Maze, init # remove init() when done debugging
import math
import random
pi = math.pi
from scipy.spatial import Voronoi, voronoi_plot_2d
import matplotlib.pyplot as plt

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

def pointsInCircum(r,n=100):
    return [(math.cos(2*pi/n*x)*r,math.sin(2*pi/n*x)*r) for x in range(0,n+1)]

def generateCircle(builder, radius, center_coords):
    ORIENTATION = 2.35621
    points = pointsInCircum(radius)
    
    for point in points:
        x = point[0] + center_coords[0]
        z = point[1] + center_coords[1]
        
        builder.addBareEntity(entities.skirmish__structures__default_defense_tower,team=0, posx= x, posz=z,orientation=ORIENTATION)

def generateRandomPoints(low_bound, high_bound):
    rand_offset_x = random.sample(range(int(low_bound[0]), int(high_bound), 10), 10)
    rand_offset_y = random.sample(range(int(low_bound[1]), int(high_bound), 10), 10)
    return list(zip(rand_offset_x, rand_offset_y))

def build_wall(from_coord, to_coord, center_point, builder: PCG):
        SEGMENT_LENGTH = 25.6
        direction = numpy.subtract(to_coord, from_coord)
        distance = numpy.linalg.norm(direction)
        n_segments = int(distance / SEGMENT_LENGTH)
        
        # convert direction vector to euler angles
        rads = math.atan2(direction[0], direction[1]) + (1/2 * math.pi)
        
        for i in range(n_segments):
            offset = direction * (i / float(n_segments))
            posx = from_coord[0] + offset[0]
            posy = from_coord[1] + offset[1]
            if numpy.linalg.norm([posx, posy] - numpy.array(center_point)) > int(2048 / 2) - 100:
                continue
            builder.addWall(posx=posx, posz=posy, orientation=rads)
            
            
def cavalryVsInfantryDistrict():
    builder = PCG()
    map_height = 2048
    map_width =  2048
    
    # builder.addBareEntity(posix=)
    
    outer_radius = int(map_height / 2) - 100
    inner_radius = int(outer_radius / 3)
    center_coords = (map_height / 2, map_width / 2)

    generateCircle(builder, inner_radius, center_coords)
    generateCircle(builder, outer_radius, center_coords)

    three_points = []
    
    items = 3
    for i in range(items):  
        x = float(f"{map_height/2 + outer_radius * math.cos(2 * pi * i / items):.5f}")
        y = float(f"{map_width/2 + outer_radius * math.sin(2 * pi * i / items):.5f}")
        three_points.append((x, y))
        builder.addBareEntity(entitytype=entities.structures__maur__tower_double, team=0, posx=x, posz=y, orientation=2.35621)
        
    # print(three_points)
    
    # Seperate circle into districts
    # for destx, desty in three_points:
    #     build_wall(center_coords, (destx, desty), builder)


    random_points = []
    # calculating coordinates
    for i in range(10):
        alpha = 2 * math.pi * random.random()
        r = (outer_radius - inner_radius) * random.random() + inner_radius
        x = r * math.cos(alpha) + center_coords[0]
        y = r * math.sin(alpha) + center_coords[1]
        random_points.append((x, y))

    chosen_districts = random_points
    # chosen_districts.append(random_points[0])
    # random_points.pop(0)

    # for _ in range(4):
    #     s = []
    #     for i in range(len(random_points)):
    #         s_d = 0
    #         for j in range(len(chosen_districts)):
    #             delta_min = 1000
    #             diff = numpy.subtract(random_points[i],chosen_districts[j])
    #             delta_dist = numpy.linalg.norm(diff)
    #             s_d = s_d + (delta_dist - delta_min)
    #         s.append((i, s_d))
    #     highest_score = max(s, key = lambda i : i[1])
    #     chosen_districts.append(random_points[highest_score[0]])
    #     random_points.pop(highest_score[0])
    
    for district in chosen_districts:
        builder.addBareEntity(entitytype=entities.structures__maur__tower_double, team=0, posx=district[0], posz=district[1], orientation=2.35621)

    vor = Voronoi(chosen_districts)
    print(vor.vertices)
    ax = plt.gca()
    ax.set_xticks(numpy.arange(0, map_width, 200))
    ax.set_yticks(numpy.arange(0, map_width, 200))
    ax.set_xlim([0, map_width])
    ax.set_ylim([0, map_width])
    ax.set_autoscale_on(False)
    
    fig = voronoi_plot_2d(vor, ax=ax, show_vertices=True)
    plt.savefig("voronoi.png")
    
    # for i, reg in enumerate(vor.regions):
    #     if len(reg) == 0:
    #         continue
    #     print(numpy.where(vor.point_region == i)[0][0])# draw a line between ridge vertices

    # draw a line between all the vertices
    for (n1,n2), (ridge_from, ridge_to) in vor.ridge_dict.items():
        if ridge_from == -1:
        # or (ridge_from in out_of_bounds) or (ridge_to in out_of_bounds):
            # Do more complicated computation
            n1_world = vor.points[n1]
            n2_world = vor.points[n2]
            
            ridge_point = vor.vertices[ridge_to]

            avg_point = (n1_world + n2_world) / 2
            avg_direction = avg_point - ridge_point
            
            # Rotate the direction in case it is pointing the center 
            # (we expect infinite points to go outwards)
            avg_center =numpy.average(vor.points, axis=0)
            direction_to_center = avg_center - ridge_point
            if numpy.dot(direction_to_center, avg_direction) > 0.0:
                avg_direction = -avg_direction

            # calculate the mean of all of the points in points
            
            wall_end_point = avg_point
            while numpy.linalg.norm(wall_end_point - numpy.array(center_coords)) < outer_radius:
                wall_end_point += (avg_direction / 100)
            to_point = wall_end_point
            build_wall(ridge_point, to_point, center_coords, builder)
            continue
        
        # get points for ridge vertices
        from_point = vor.vertices[ridge_from]
        to_point = vor.vertices[ridge_to]

        build_wall(from_point, to_point, center_coords, builder)
    
    # maze = Maze(maze_height, maze_width)
    # maze.generate()
    # # maze.print_maze()

    # flag = False

    # for i in range(maze_height):
    #     for j in range(maze_width):
    #         if maze.maze[i][j] == maze.wall:
    #             builder.addWall((x + (i*WALL_LENGTH)), ((z + (j*WALL_LENGTH)) - WALL_LENGTH / 2), orientation=0)
    #             builder.addWall(((x + (i*WALL_LENGTH)) - WALL_LENGTH / 2), (z + (j*WALL_LENGTH)), orientation=ORIENTATION_1)
    #             builder.addWall((x + (i*WALL_LENGTH)), ((z + (j*WALL_LENGTH)) + WALL_LENGTH / 2), orientation=0)
    #             builder.addWall(((x + (i*WALL_LENGTH)) + WALL_LENGTH / 2), (z + (j*WALL_LENGTH)), orientation=ORIENTATION_1)
    #         if maze.maze[i][j] == maze.exit:
    #             if not flag:
    #                 builder.addCavalryArcher((x + (i*WALL_LENGTH)), (z + (j*WALL_LENGTH)) + 3, orientation=ORIENTATION_1)
    #                 builder.addCavalryArcher((x + (i*WALL_LENGTH)), (z + (j*WALL_LENGTH)) + 1, orientation=ORIENTATION_1)
    #                 builder.addCavalryArcher((x + (i*WALL_LENGTH)), (z + (j*WALL_LENGTH)) - 1, orientation=ORIENTATION_1)
    #                 builder.addCavalryArcher((x + (i*WALL_LENGTH)), (z + (j*WALL_LENGTH)) - 3, orientation=ORIENTATION_1)
    #                 flag = True
    #             else:
    #                 builder.addSpearman((x + (i*WALL_LENGTH)), (z + (j*WALL_LENGTH)) + 3, orientation=ORIENTATION_2)
    #                 builder.addSpearman((x + (i*WALL_LENGTH)), (z + (j*WALL_LENGTH)) + 1, orientation=ORIENTATION_2)
    #                 builder.addSpearman((x + (i*WALL_LENGTH)), (z + (j*WALL_LENGTH)) - 1, orientation=ORIENTATION_2)
    #                 builder.addSpearman((x + (i*WALL_LENGTH)), (z + (j*WALL_LENGTH)) - 3, orientation=ORIENTATION_2)
    
    # # reinforce exterior wall so troops stay in maze
    # for j in range(maze_width):
    #     builder.addWall((x - (WALL_LENGTH / 2 + 5)), (z + (j*WALL_LENGTH)), orientation=ORIENTATION_1)
    #     builder.addWall(((x + (maze_height - 1) * WALL_LENGTH) + (WALL_LENGTH / 2 + 5)), (z + (j*WALL_LENGTH)), orientation=ORIENTATION_1)

    builder.write("CavalryVsInfantryDistricts.xml")
    with open("C:/Users/Savaa/Documents/My Games/0ad/mods/user/maps/scenarios/CavalryVsInfantryDistricts.xml", 'w') as f:
        f.write(str(builder))
        
    # builder.write("/C:/Users/Savaa/source/repos/MGAI_0ad/CavalryVsInfantryDistricts.xml")


if __name__ == '__main__':
    print("Building")
    cavalryVsInfantryDistrict()
    print("Done.")