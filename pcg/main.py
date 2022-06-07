import numpy as np
from pyrsistent import v
from scipy import rand
from pcg import PCG, entities
import math
import random
from scipy.spatial import Voronoi, voronoi_plot_2d
import matplotlib.pyplot as plt

SEGMENT_LENGTH = 12.3

def pointsInCircum(r,n=100):
    return [(math.cos(2*np.pi/n*x)*r,math.sin(2*np.pi/n*x)*r) for x in range(0,n+1)]


def build_short_wall(builder: PCG, coord, orientation):
    builder.addBareEntity(entitytype=entities.skirmish__structures__default_wall_short, team=0, posx=coord[0], posz=coord[1], orientation=orientation)

def generateCircle(builder: PCG, radius, center_coords):
    # compute circumference of circle with radius
    circum = 2 * math.pi * radius
    n_segments = math.ceil(circum / SEGMENT_LENGTH)
    
    points = pointsInCircum(radius, n=n_segments)
    for point in points:
        p = point + center_coords
        direction = np.subtract(p, center_coords)
        rads = math.atan2(direction[0], direction[1])
        
        build_short_wall(builder, p, rads)
        
def generateWatchTowers(builder:PCG, radius, center_coords):
    # compute circumference of circle with radius
    circum = 2 * math.pi * radius
    segment_spread = 200
    n_segments = math.ceil(circum / segment_spread)
    
    points = pointsInCircum(radius, n=n_segments)
    for point in points:
        p = point + center_coords
        direction = np.subtract(p, center_coords)
        rads = math.atan2(direction[0], direction[1])
        
        build_watch_tower(builder, p, rads)

def build_watch_tower(builder:PCG, coord, orientation):
    builder.addBareEntity(entitytype=entities.skirmish__structures__default_wall_tower, team=0, posx=coord[0], posz=coord[1], orientation=orientation)

def generateRandomPoints(low_bound, high_bound):
    rand_offset_x = random.sample(range(int(low_bound[0]), int(high_bound), 10), 10)
    rand_offset_y = random.sample(range(int(low_bound[1]), int(high_bound), 10), 10)
    return list(zip(rand_offset_x, rand_offset_y))

def build_wall(from_coord, to_coord, center_point, builder: PCG, min_dist, max_dist):
        
        d1 = np.linalg.norm(np.subtract(from_coord, center_point))
        d2 = np.linalg.norm(np.subtract(to_coord, center_point))
        if d1 > d2:
            # swap variables
            t = from_coord.copy()
            from_coord = to_coord.copy()
            to_coord = t
            
        direction = np.subtract(to_coord, from_coord)
        distance = np.linalg.norm(direction)
        n_segments = math.ceil(distance / SEGMENT_LENGTH)
        
        # buildWatchTower(builder, to_coord, math.atan2(direction[0], direction[1]))
        far_tower = False
        close_tower = False
        # convert direction vector to euler angles
        rads = math.atan2(direction[0], direction[1]) + (1/2 * math.pi)
        
        for i in range(n_segments):
            offset = direction * (i / float(n_segments))
            pos = from_coord + offset

            distance = np.linalg.norm(pos - center_point)
            if distance > min_dist and not close_tower and distance < max_dist:
                close_tower = True
                build_watch_tower(builder, pos, rads)
            if distance < min_dist:
                continue
            if distance > max_dist:
                break
            build_short_wall(builder, pos, rads)        
            
            
def cavalryVsInfantryDistrict():
    builder = PCG()
    map_height = 2048
    map_width =  2048
    
    # builder.addBareEntity(posix=)
    
    outer_radius = int(map_height / 2) - 100
    inner_radius = int(outer_radius / 3)
    center_coords = np.array([map_height / 2, map_width / 2])

    generateCircle(builder, inner_radius, center_coords)
    generateCircle(builder, outer_radius, center_coords)
    generateWatchTowers(builder, outer_radius, center_coords)

    no_districts = 10
    district_centers = generate_districts(builder, outer_radius, inner_radius, center_coords, no_districts)

    generate_district_boundaries(builder, outer_radius, inner_radius, center_coords, district_centers)
    
    district_centers2 = generate_districts(builder, inner_radius, 0, center_coords, no_districts=1, no_highways=10)

    generate_district_boundaries(builder, inner_radius, 0, center_coords, district_centers2)
    
    builder.write("CavalryVsInfantryDistricts.xml")
    with open("C:/Users/Savaa/Documents/My Games/0ad/mods/user/maps/scenarios/CavalryVsInfantryDistricts.xml", 'w') as f:
        f.write(str(builder))

def generate_district_boundaries(builder, outer_radius, inner_radius, center_coords, district_centers):
    vor = Voronoi(district_centers)
    fig = voronoi_plot_2d(vor)
    plt.savefig("voronoi.png")
    
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
            avg_center =np.average(vor.points, axis=0)
            direction_to_center = avg_center - ridge_point
            if np.dot(direction_to_center, avg_direction) > 0.0:
                avg_direction = -avg_direction

            # calculate the mean of all of the points in points
            
            wall_end_point = avg_point
            while np.linalg.norm(wall_end_point - np.array(center_coords)) < outer_radius:
                wall_end_point += (avg_direction / 100)
            to_point = wall_end_point
            build_wall(ridge_point, to_point, center_coords, builder, inner_radius, outer_radius)
            continue
        
        # get points for ridge vertices
        from_point = vor.vertices[ridge_from]
        to_point = vor.vertices[ridge_to]

        build_wall(from_point, to_point, center_coords, builder, inner_radius, outer_radius)

def generate_districts(builder, outer_radius, inner_radius, center_coords, no_districts, no_highways=3):
    district_centers = []
    for i in range(no_highways):
        # calculating coordinates
        for _ in range(no_districts):
            lower = (i / no_highways * 2 * math.pi)
            upper = ((i + 1) / no_highways * 2 * math.pi)
            alpha = np.random.uniform(lower, upper)
            r = (outer_radius - inner_radius) * np.random.rand() + inner_radius
            x = r * math.cos(alpha) + center_coords[0]
            y = r * math.sin(alpha) + center_coords[1]
            district_centers.append((x, y))

    for district in district_centers:
        builder.addBareEntity(entitytype=entities.structures__maur__tower_double, team=0, posx=district[0], posz=district[1], orientation=2.35621)
    return district_centers
        

if __name__ == '__main__':
    print("Building")
    cavalryVsInfantryDistrict()
    print("Done.")