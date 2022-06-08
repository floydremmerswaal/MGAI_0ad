import numpy as np
from pyrsistent import v
from scipy import rand
from pcg import PCG, entities
import math
import random
from scipy.spatial import Voronoi, voronoi_plot_2d
import matplotlib.pyplot as plt
from city_generator import City

if __name__ == '__main__':
    civs =['athen', 'brit', 'cart','gaul', 'iber', 'kush', 'mace','maur', 'pers', 'ptol', 'rome', 'sele', 'spart']
    print("Building")
    map_height = 2048
    map_width =  2048
    
    # builder.addBareEntity(posix=)
    
    outer_radius = int(map_height / 2) - 100
    inner_radius = int(outer_radius / 3)
    center_coords = np.array([map_height / 2, map_width / 2])
    
    builder = PCG()
    
    civ = np.random.choice(civs)
    print('Picked civ:', civ)
    city = City(builder, center_coords, [inner_radius, outer_radius], civ, 0)
    city.generate()
    
    builder.write("CavalryVsInfantryDistricts.xml")
    with open("C:/Users/Savaa/Documents/My Games/0ad/mods/user/maps/scenarios/CavalryVsInfantryDistricts.xml", 'w') as f:
        f.write(str(builder))
        
    
    print("Done.")