import openmc
import numpy as np


mats = openmc.Materials()

# set wall material
wall_material = openmc.Material(1, "wall_material")
wall_material.add_nuclide('Pb204', 1) # which pb to use
wall_material.set_density('g/cm3', 1) # ???

# set observation point
detector_material = openmc.Material(2, "detector_material")
detector_material.add_nuclide('Xe135', 1)
detector_material.set_density('g/cm3', 1) # ?

# set source material
source_material = openmc.Material(3, "source_material")
source_material.add_nuclide('U235', 0.8)
source_material.add_nuclide('U238', 0.2)
source_material.set_density('atom/cm3', 10**4)

mats.append(wall_material)
mats.append(detector_material)
mats.append(source_material)
mats.export_to_xml()

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

    x_pos = openmc.XPlane(x0 = max(x_length+start_point.x,start_point.x), boundary_type = boundary_type_set)
    x_neg = openmc.XPlane(x0 = min(x_length+start_point.x,start_point.x), boundary_type = boundary_type_set)
    y_pos = openmc.YPlane(y0 = max(y_length+start_point.y,start_point.y), boundary_type = boundary_type_set)
    y_neg = openmc.YPlane(y0 = min(y_length+start_point.y,start_point.y), boundary_type = boundary_type_set)
    z_pos = openmc.ZPlane(z0 = max(z_length+start_point.z,start_point.z), boundary_type = boundary_type_set)
    z_neg = openmc.ZPlane(z0 = min(z_length+start_point.z,start_point.z), boundary_type = boundary_type_set)

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
rad_source = openmc.Sphere(x0 = 0.5, y0 = 1.0, z0 = 0.5, R=0.08, name = "the_only_source")
inside_rad = -rad_source
fuel = openmc.Cell(fill = source_material, region = inside_rad)

# define the detector
detector_sphere = openmc.Sphere(x0 = 1, y0 = 0.5, z0 = 0.5, R=0.08, name = "detector_point")
inside_detector = -detector_sphere
detector_cell = openmc.Cell(fill = detector_material, region = inside_detector)

# set tally
tallies_file = openmc.Tallies()
tally = openmc.Tally(name='detector')
tally.filters = [openmc.CellFilter([detector_cell])]
energy_filter = openmc.EnergyFilter([0.0, 4.0, 1.0e6])
tally.filters.append(energy_filter)
tally.scores = ['absorption']
tallies_file.append(tally)
tallies_file.export_to_xml()


# define other cell
concrete = openmc.Cell(fill = wall_material, region = basic_cube)
vacuum = openmc.Cell(region = hallway)

# define universe
universe = openmc.Universe(cells=[concrete,vacuum,fuel,detector_cell])
geom = openmc.Geometry()
geom.root_universe = universe

p = openmc.Plot()
p.filename = 'plot'
p.width = (2,2)
p.pixels = (200, 200)
p.color_by = 'material'
p.colors = {wall_material: 'yellow', detector_material: 'blue', source_material: 'red'}
plots = openmc.Plots([p])
plots.export_to_xml()
openmc.plot_geometry()

point = openmc.stats.Point((0, 0, 0))
src = openmc.Source(space=point)
settings = openmc.Settings()
settings.source = src
settings.batches = 100
settings.inactive = 10
settings.particles = 1000
settings.export_to_xml()

openmc.run()
