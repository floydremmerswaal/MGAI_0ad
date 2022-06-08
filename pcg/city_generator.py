
import math
from typing import List
from matplotlib import pyplot as plt

import numpy as np

from pcg import entities
from pcg import PCG
from scipy.spatial import Voronoi, voronoi_plot_2d

class City():
    # Radii = plural of radius.
    def __init__(self, builder: PCG, city_center, radii: List):
        self.SEGMENT_LENGTH = 12.3
        self.builder = builder
        self.city_center = city_center
        self.radii = radii
    
    def points_in_circum(self, r, n=100):
        return [(math.cos(2*np.pi/n*x)*r,math.sin(2*np.pi/n*x)*r) for x in range(0,n+1)]

    def build_short_wall(self, coord, orientation):
        self.builder.addBareEntity(entitytype=entities.skirmish__structures__default_wall_short, team=0, posx=coord[0], posz=coord[1], orientation=orientation)

    def generate_circle(self, radius):
        # compute circumference of circle with radius
        circum = 2 * math.pi * radius
        n_segments = math.ceil(circum / self.SEGMENT_LENGTH)
        
        points = self.points_in_circum(radius, n=n_segments)
        for point in points:
            p = point + self.city_center
            direction = np.subtract(p, self.city_center)
            rads = math.atan2(direction[0], direction[1])
            
            self.build_short_wall(p, rads)

    def build_watch_tower(self, coord, orientation):
        self.builder.addBareEntity(entitytype=entities.skirmish__structures__default_wall_tower, team=0, posx=coord[0], posz=coord[1], orientation=orientation)
        
    def generate_watch_towers_circle(self, radius):
        # compute circumference of circle with radius
        circum = 2 * math.pi * radius
        segment_spread = 200
        n_segments = math.ceil(circum / segment_spread)
        
        points = self.points_in_circum(radius, n=n_segments)
        for point in points:
            p = point + self.city_center
            direction = np.subtract(p, self.city_center)
            rads = math.atan2(direction[0], direction[1])
            
            self.build_watch_tower(p, rads)

    def build_wall_line(self, from_coord, to_coord, min_dist, max_dist):
            
            d1 = np.linalg.norm(np.subtract(from_coord, self.city_center))
            d2 = np.linalg.norm(np.subtract(to_coord, self.city_center))
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

                distance = np.linalg.norm(pos - self.city_center)
                if distance > min_dist and not close_tower and distance < max_dist:
                    close_tower = True
                    self.build_watch_tower(pos, rads)
                if distance < min_dist:
                    continue
                if distance > max_dist:
                    break
                self.build_short_wall(pos, rads)        
                
    def generate(self):
        # generate city
        self.generate_circle(self.radii[0])
        self.generate_circle(self.radii[1])
        self.generate_watch_towers_circle(self.radii[1])

        # outer city
        district_centers = self.generate_districts(self.radii[1], self.radii[0], no_districts=10)
        self.generate_district_boundaries(self.radii[1], self.radii[0], district_centers)
        
        # inner city
        district_centers2 = self.generate_districts(self.radii[0], 0, no_districts=1, no_highways=10)
        self.generate_district_boundaries(self.radii[0], 0, district_centers2)


    def generate_district_boundaries(self, outer_radius, inner_radius, district_centers):
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
                while np.linalg.norm(wall_end_point - np.array(self.city_center)) < outer_radius:
                    wall_end_point += (avg_direction / 100)
                to_point = wall_end_point
                self.build_wall_line(ridge_point, to_point, inner_radius, outer_radius)
                continue
            
            # get points for ridge vertices
            from_point = vor.vertices[ridge_from]
            to_point = vor.vertices[ridge_to]

            self.build_wall_line(from_point, to_point, inner_radius, outer_radius)

    def generate_districts(self, outer_radius, inner_radius, no_districts, no_highways=3):
        district_centers = []
        for i in range(no_highways):
            # calculating coordinates
            for _ in range(no_districts):
                lower = (i / no_highways * 2 * math.pi)
                upper = ((i + 1) / no_highways * 2 * math.pi)
                alpha = np.random.uniform(lower, upper)
                r = (outer_radius - inner_radius) * np.random.rand() + inner_radius
                x = r * math.cos(alpha) + self.city_center[0]
                y = r * math.sin(alpha) + self.city_center[1]
                district_centers.append((x, y))

        for district in district_centers:
            self.builder.addBareEntity(entitytype=entities.structures__maur__tower_double, team=0, posx=district[0], posz=district[1], orientation=2.35621)
        return district_centers
            
