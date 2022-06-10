
import math
import random
from typing import List
from matplotlib import pyplot as plt
from shapely.geometry import Point, GeometryCollection
from shapely.geometry.multipoint import MultiPoint
from shapely.geometry.polygon import Polygon, LineString
from shapely.ops import voronoi_diagram
from shapely import affinity

import numpy as np

from pcg import entities
from pcg import PCG

class City():
    # Radii = plural of radius.
    def __init__(self, builder: PCG, city_center, radii: List, civilization, team):
        self.SEGMENT_LENGTH = 12.3
        self.builder = builder
        self.city_center = city_center
        self.radii = radii
        self.civilization = civilization
        self.team = team
    
    def points_in_circum(self, r, n=100):
        return [(math.cos(2*np.pi/n*x)*r,math.sin(2*np.pi/n*x)*r) for x in range(0,n+1)]

    def build_short_wall(self, coord, orientation):
        self.builder.addBareEntity(entitytype=entities.__dict__.get(f"structures__{self.civilization}__wall_short"), team=self.team, posx=coord[0], posz=coord[1], orientation=orientation)
        
    def build_gate(self, coord, orientation):
        self.builder.addBareEntity(entitytype=entities.__dict__.get(f"structures__{self.civilization}__wall_gate"), team=self.team, posx=coord[0], posz=coord[1], orientation=orientation)

    def build_watch_tower(self, coord, orientation):
        self.builder.addBareEntity(entitytype=entities.__dict__.get(f"structures__{self.civilization}__wall_tower"), team=self.team, posx=coord[0], posz=coord[1], orientation=orientation)

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

    def build_wall_line(self, from_coord, to_coord, max_dist):
            direction = np.subtract(to_coord, from_coord)
            total_distance = np.linalg.norm(direction)
            n_segments = math.ceil(total_distance / self.SEGMENT_LENGTH)
            gate = False
            
            self.build_watch_tower(to_coord, math.atan2(direction[0], direction[1]))
            self.build_watch_tower(from_coord, math.atan2(direction[0], direction[1]))
            # convert direction vector to euler angles
            rads = math.atan2(direction[0], direction[1]) + (1/2 * math.pi)
            
            for i in range(n_segments):
                offset = direction * (i / float(n_segments))
                pos = from_coord + offset
                if n_segments / (i + 1) < 2 and not gate:
                    gate = True
                    self.build_gate(pos, rads)
                    continue
                self.build_short_wall(pos, rads)        

                
    def generate(self):
        # generate city
        # self.generate_circle(self.radii[1])
        # self.generate_watch_towers_circle(self.radii[1])

        # Gneerate centers, cities are more dense in the center and thus diff params are used
        centers = self.generate_districts(self.radii[0], self.radii[1], no_districts=10)
        inner_centers = self.generate_districts(0, self.radii[0], no_districts=1, splits=20)
        centers.extend(inner_centers)
        
        # Generate single voronoi
        regions = self.generate_district_boundaries(self.radii[1], centers)

        self.generate_populate_districts(regions)

        #add troops on each team
        circum_points = self.points_in_circum(8, 3)
        district_center_team1 = random.choice(inner_centers)
        district_center_team2 = random.choice(inner_centers)
        for p in circum_points:
            direction_team1 = np.subtract(p, district_center_team1)
            rads_team1 = math.atan2(direction_team1[0], direction_team1[1])
            direction_team2 = np.subtract(p, district_center_team2)
            rads_team2 = math.atan2(direction_team2[0], direction_team2[1])
            self.builder.addCavalryArcher(p[0]+district_center_team1[0], p[1]+district_center_team1[1], rads_team1)
            self.builder.addSpearman(p[0]+district_center_team2[0], p[1]+district_center_team2[1], rads_team2)
            

    def plot_voronoi(self, regions):
        for reg in regions:
            x,y = reg.exterior.xy
            plt.plot(x,y)

        plt.gca().set_aspect('equal', adjustable='box')
        plt.savefig("voronoi.pdf",  bbox_inches='tight')

    def generate_district_boundaries(self, outer_radius, district_centers):
        vor_regions: GeometryCollection = voronoi_diagram(MultiPoint(district_centers))
        
        # Adjust the voronoi regions to be within the outer radius
        # Create shapely circle
        regs = []
        for reg in vor_regions:
            adjusted_coords = []
            
            for x, y in reg.boundary.coords:
                direction = np.subtract([x, y], self.city_center)
                length = np.linalg.norm(direction)
                if length > outer_radius:
                    # clamp to outer radius
                    normalized_direction = np.divide(direction, length)
                    new_coord = np.multiply(normalized_direction, outer_radius)
                    x, y = np.add(self.city_center, new_coord)
                adjusted_coords.append((x, y))
            regs.append(Polygon(adjusted_coords))
        
        done = []
        for reg in regs:
            b = reg.boundary.coords
            linestrings = [LineString(b[k:k+2]).coords for k in range(len(b) - 1)]
            for (fromc, toc) in linestrings:
                if (fromc, toc) not in done and (toc, fromc) not in done:
                    self.build_wall_line(np.array(fromc), np.array(toc), outer_radius)
                    done.append((fromc, toc))
            
        return regs

    def generate_districts(self, inner_radius, outer_radius, no_districts, splits=3):
        # Number of splits determines the amount of splits the circle is divided into
        # Every split will have no_districts districts
        # Upping the number of splits will make the districts more uniformly distributed
        district_centers = []
        disc_size = (outer_radius - inner_radius)
        for i in range(splits):
            # calculating coordinates
            for _ in range(no_districts):
                lower = (i / splits * 2 * math.pi)
                upper = ((i + 1) / splits * 2 * math.pi)
                alpha = np.random.uniform(lower, upper)
                # Exclude last 10th of the radius
                r = (disc_size - (disc_size / 10))  * np.random.rand() + inner_radius
                x = r * math.cos(alpha) + self.city_center[0]
                y = r * math.sin(alpha) + self.city_center[1]
                district_centers.append((x, y))

        for district in district_centers:
            self.builder.addBareEntity(entitytype=entities.structures__maur__tower_double, team=self.team, posx=district[0], posz=district[1], orientation=2.35621)
        return district_centers
            
    def generate_random_in_poly(self, number, polygon, max_gen=1000):
        scaled_poly = affinity.scale(polygon, xfact=0.9, yfact=0.9)
        points: List[Point] = []
        minx, miny, maxx, maxy = polygon.bounds
        count = 0
        while len(points) < number and count < max_gen:
            count += 1
            pnt = Point(np.random.uniform(minx, maxx), np.random.uniform(miny, maxy))
            if scaled_poly.contains(pnt) and all(not p.buffer(22).contains(pnt) for p in points):
                points.append(pnt)
        return points

    def generate_populate_districts(self, district_polygons):
        district_type_map ={
            'military': [['arsenal', 'barracks', 'defense_tower', 'range', 'sentry_tower'], [1,1,1,1,1]],
            'agriculture': [['farmstead', 'field', 'storehouse', 'forge'], [1,10,1,1]],
            'livestock': [['corral', 'stable'], [1,1]],
            'civil': [['civil_centre', 'fortress', 'gymnasium', 'prytaneion', 'royal_stoa', 'temple', 'theater'], [1,1,1,1,1,1,1]],
            'housing': [['house', 'market'], [1,1]],
        }
        
        # create probabilities for each district based on how close they are to the center
        outer_preference = [0.2, 1, 1, 0.01, 0.5]
        inner_preference = [1, 0.01, 0.01, 1, 0.5]
        for poly in district_polygons:
            # the closer the polygon is to the center, the more likely it is to have type civil and housing
            distance = np.linalg.norm(np.subtract(poly.centroid.coords[0], self.city_center)) / self.radii[1]
            # use this to weight the types
            type_odds = [inner_preference[i] * (1 - distance) + (outer_preference[i] * distance) for i in range(len(inner_preference))]
            type_odds = type_odds / np.sum(type_odds)
            key  = np.random.choice(list(district_type_map.keys()), p=type_odds)
            # normalize odds
            buildings, odds = district_type_map[key]
            odds = odds / np.sum(odds)
            points = self.generate_random_in_poly(500, poly)
            for p in points:
                build = np.random.choice(buildings, p=odds)
                direction = np.subtract([p.x, p.y], self.city_center)
                rads = math.atan2(direction[0], direction[1]) + (1/2 * math.pi)
                self.builder.addBareEntity(entitytype=entities.__dict__.get(f"structures__{self.civilization}__{build}"), team=self.team, posx=p.x, posz=p.y, orientation=rads)
        pass