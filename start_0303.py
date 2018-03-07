import openmc
import numpy as np

# set wall material
wall = openmc.Material(1, "wall")
wall.add_nuclide('Pb205', 1) # which pb to use
wall.set_density('g/cm3', 1) # ???

# set observation point
detector = openmc.Material(2, "detector")
detector.add_nuclide('Xe135', 1)
detector.set_density('g/cm3', 1) # ?

# set source material
source = openmc.Material(3, "source")
source.add_nuclide('Pt196', 1) # which pt to use?
source.set_density('atom/cm3', 10**4)

class Start_point:
    def __init__(self, x_, y_, z_):
    	self.x = x_;
    	self.y = y_;
    	self.z = z_;

def truncation_create(plane_list):
#list[][0] pos plane list[][1] neg plane
    shape = (-plane_list[0][0]) & (+plane_list[0][1])
    for oppo_planes in plane_list:
        shape = shape & ((-oppo_planes[0]) & (+oppo_planes[1]))
    return shape


def create_cube(x_length, y_length, z_length, start_point, boundary_type_set = 'reflective'):

    x_pos = openmc.XPlane(x0 = max(x_length,start_point.x), boundary_type = boundary_type_set)
    x_neg = openmc.XPlane(x0 = min(x_length,start_point.x), boundary_type = boundary_type_set)
    y_pos = openmc.YPlane(y0 = max(y_length,start_point.y), boundary_type = boundary_type_set)
    y_neg = openmc.YPlane(y0 = min(y_length,start_point.y), boundary_type = boundary_type_set)
    z_pos = openmc.ZPlane(z0 = max(z_length,start_point.z), boundary_type = boundary_type_set)
    z_neg = openmc.ZPlane(z0 = min(z_length,start_point.z), boundary_type = boundary_type_set)

    plane_list = []
    plane_list.append([x_pos,x_neg])
    plane_list.append([y_pos,y_neg])
    plane_list.append([z_pos,z_neg])
    return truncation_create(plane_list)

## create geometry
#  1*1 meter square
#  1cm3 detector and source
start_point_hallway= Start_point(0.25,0.25,0.25)
cavity_y = create_cube(0.5,0.75,0.5,start_point_hallway)
cavity_z = create_cube(0.5,0.5,0.75,start_point_hallway)

# define hallway region
hallway = cavity_y | cavity_z

# define wall region
basic_start = Start_point(0.0,0.0,0.0)
basic_cube_entity = create_cube(1.0,1.0,1.0,basic_start)
basic_cube = basic_cube_entity & (~hallway)
# define the source
rad_source = openmc.Sphere(x0 = 0.5, y0 = 1.0,z0 = 0.5, R=0.08, name = "the_only_source")
inside_rad = -rad_source
fuel = openmc.Cell(fill = source, region = inside_rad)
# define cell
concrete = openmc.Cell(fill = wall, region = basic_cube)
vacuum = openmc.Cell(region = hallway)
# define universe
universe = openmc.Universe(cells=[concrete,vacuum,fuel])

openmc.run()
