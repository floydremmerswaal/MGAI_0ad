import numpy as np	
from pyrsistent import v	
from scipy import rand	
from pcg import PCG, entities	
import math	
import random	
from scipy.spatial import Voronoi, voronoi_plot_2d	
import matplotlib.pyplot as plt
from shapely.geometry import Point
from shapely.geometry.polygon import Polygon

pi = math.pi
COUNTRIES = ['athen', 'pers', 'kush', 'han', 'rome']
class City:
    def __init__(self) -> None:
        self.SEGMENT_LENGTH = 12.3
        self.district_centers = []
        self.vor = None

    def pointsInCircum(self, r,n=100):
        return [(math.cos(2*np.pi/n*x)*r,math.sin(2*np.pi/n*x)*r) for x in range(0,n+1)]

    def build_short_wall(self, builder: PCG, coord, orientation):
        builder.addBareEntity(entitytype=entities.skirmish__structures__default_wall_short, team=0, posx=coord[0], posz=coord[1], orientation=orientation)

    def build_gate(self, builder: PCG, coord, orientation):
        builder.addBareEntity(entitytype=entities.skirmish__structures__default_wall_gate, team=0, posx=coord[0], posz=coord[1], orientation=orientation)

    def generate_circle(self, builder: PCG, radius, center_coords):
        # compute circumference of circle with radius
        circum = 2 * math.pi * radius
        n_segments = math.ceil(circum / self.SEGMENT_LENGTH)
        
        points = self.pointsInCircum(radius, n=n_segments)
        for point in points:
            p = point + center_coords
            direction = np.subtract(p, center_coords)
            rads = math.atan2(direction[0], direction[1])
            
            self.build_short_wall(builder, p, rads)
            
    def generate_watch_towers_circle(self, builder:PCG, radius, center_coords):
        # compute circumference of circle with radius
        circum = 2 * math.pi * radius
        segment_spread = 200
        n_segments = math.ceil(circum / segment_spread)
        
        points = self.pointsInCircum(radius, n=n_segments)
        for point in points:
            p = point + center_coords
            direction = np.subtract(p, center_coords)
            rads = math.atan2(direction[0], direction[1])
            
            self.build_watch_tower(builder, p, rads)

    def build_watch_tower(self, builder:PCG, coord, orientation):
        builder.addBareEntity(entitytype=entities.skirmish__structures__default_wall_tower, team=0, posx=coord[0], posz=coord[1], orientation=orientation)

    def build_wall(self, from_coord, to_coord, center_point, builder: PCG, min_dist, max_dist):
        d1 = np.linalg.norm(np.subtract(from_coord, center_point))
        d2 = np.linalg.norm(np.subtract(to_coord, center_point))
        if d1 > d2:
            # swap variables
            t = from_coord.copy()
            from_coord = to_coord.copy()
            to_coord = t
            
        direction = np.subtract(to_coord, from_coord)
        distance = np.linalg.norm(direction)
        n_segments = math.ceil(distance / self.SEGMENT_LENGTH)
        
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
                self.build_watch_tower(builder, pos, rads)
            if distance < min_dist:
                continue
            if distance > max_dist:
                break
            self.build_short_wall(builder, pos, rads)

    def generate_district_boundaries(self, builder, outer_radius, inner_radius, center_coords, district_centers):
        self.vor = Voronoi(district_centers)
        fig = voronoi_plot_2d(self.vor)
        plt.savefig("voronoi.png")
        # draw a line between all the vertices
        for (n1,n2), (ridge_from, ridge_to) in self.vor.ridge_dict.items():
            if ridge_from == -1:
            # or (ridge_from in out_of_bounds) or (ridge_to in out_of_bounds):
                # Do more complicated computation
                n1_world = self.vor.points[n1]
                n2_world = self.vor.points[n2]
                
                ridge_point = self.vor.vertices[ridge_to]

                avg_point = (n1_world + n2_world) / 2
                avg_direction = avg_point - ridge_point
                
                # Rotate the direction in case it is pointing the center 
                # (we expect infinite points to go outwards)
                avg_center =np.average(self.vor.points, axis=0)
                direction_to_center = avg_center - ridge_point
                if np.dot(direction_to_center, avg_direction) > 0.0:
                    avg_direction = -avg_direction

                # calculate the mean of all of the points in points
                
                wall_end_point = avg_point
                while np.linalg.norm(wall_end_point - np.array(center_coords)) < outer_radius:
                    wall_end_point += (avg_direction / 100)
                to_point = wall_end_point
                self.build_wall(ridge_point, to_point, center_coords, builder, inner_radius, outer_radius)
                continue
            
            # get points for ridge vertices
            from_point = self.vor.vertices[ridge_from]
            to_point = self.vor.vertices[ridge_to]

            self.build_wall(from_point, to_point, center_coords, builder, inner_radius, outer_radius)

    def generate_districts(self, builder, outer_radius, inner_radius, center_coords, no_districts, no_highways=3):
        for i in range(no_highways):
            # calculating coordinates
            for _ in range(no_districts):
                lower = (i / no_highways * 2 * math.pi)
                upper = ((i + 1) / no_highways * 2 * math.pi)
                alpha = np.random.uniform(lower, upper)
                r = (outer_radius - inner_radius) * np.random.rand() + inner_radius
                x = r * math.cos(alpha) + center_coords[0]
                y = r * math.sin(alpha) + center_coords[1]
                self.district_centers.append((x, y))

        # To identify the district centers
        # for district in self.district_centers:
        #     builder.addBareEntity(entitytype=entities.structures__maur__tower_double, team=0, posx=district[0], posz=district[1], orientation=2.35621)
        return self.district_centers

    # get polygon coordinates from the voronoi regions
    def generate_polygons_coords_from_voronoi(self):
        polygons = {}
        for id, region_index in enumerate(self.vor.point_region):
            points = []
            for vertex_index in self.vor.regions[region_index]:
                if vertex_index != -1:
                    points.append(tuple(self.vor.vertices[vertex_index]))
            points.append(points[0])
            polygons[id]=points
        return polygons

    def generate_structures_in_district_polygon(self, builder):
        polygons = self.generate_polygons_coords_from_voronoi()
        range = 100
        step = 5
        for key, value in polygons.items():
            polygon = Polygon(value)
            district = self.district_centers[key]
            occupied_coords = []
            country = random.choice(COUNTRIES)
            # print("checking new polygon", key) 
            rand_offset_count = 0
            struct_candidates = [item for item in dir(entities) if item.startswith("structures__"+country) and not item.startswith("structures__"+country+"__wall")]
            while len(occupied_coords) < 6: # until atleast 6 structures are built
                rand_offset = random.randrange(-(range), range, step)
                #hacky, if no random placement coord are found in the polygon after a certain values skip rest of the polygon
                if rand_offset_count == (2 * range / step): 
                    break
                placement_coord = (district[0]+rand_offset, district[1]+rand_offset)
                if polygon.contains(Point(placement_coord)) and not placement_coord in occupied_coords:
                    # print("adding structures at", placement_coord)
                    rand_structure = random.choice(struct_candidates)
                    builder.addBareEntity(entities.__dict__.get(rand_structure), team=0, posx=placement_coord[0], posz=placement_coord[1], orientation=2.35621)
                    occupied_coords.append(placement_coord)
                rand_offset_count += 1 

