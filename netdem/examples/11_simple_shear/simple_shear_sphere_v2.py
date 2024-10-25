from signal import pause
import sys
import os
import math

# env
dir_path = os.path.dirname(os.path.realpath(__file__))
sys.path.append(dir_path + "/../../build/lib/")
from netdem import *

# sim settings
sim = Simulation()
sim.domain_manager.SetBound(-0.6, -0.6, -0.6, 0.6, 0.6, 1.2)
sim.domain_manager.SetCellSpacing(0.02, 0.02, 0.02)

# solver settings
sim.dem_solver.contact_solver_factory.settings.solver_type\
    = ContactSolverSettings.SolverType.automatic
sim.dem_solver.contact_solver_factory.settings.sdf_potential_type = 0

# contact model
cnt_model_1 = LinearSpring(2.0e6, 1.0e6, 0.0, 0.0)
cnt_model_1.label = "cnt_model_1"
cnt_model_1_prt = sim.scene.InsertContactModel(cnt_model_1)

cnt_model_2 = LinearSpring(2.0e6, 1.0e6, 0.0, 0.0)
cnt_model_2.label = "cnt_model_2"
cnt_model_2_prt = sim.scene.InsertContactModel(cnt_model_2)

sim.scene.SetNumberOfMaterials(2)
sim.scene.SetCollisionModel(0, 0, cnt_model_1_prt)
sim.scene.SetCollisionModel(0, 1, cnt_model_1_prt)
sim.scene.SetCollisionModel(1, 1, cnt_model_2_prt)

sim.dem_solver.timestep = 1.0e-5

# container geometries
stl_bot = STLModel()
stl_bot.InitFromSTL(dir_path + "/data/ring_bot.stl")
stl_mid = STLModel()
stl_mid.InitFromSTL(dir_path + "/data/ring_mid.stl")

stl_top = STLModel()
stl_top.InitFromSTL(dir_path + "/data/ring_mid.stl")
tmp_vertices = stl_top.vertices
for i in range(0, len(tmp_vertices)):
    tmp_vertices[i] = [tmp_vertices[i][0],
                       tmp_vertices[i][1], tmp_vertices[i][2] * 4.0]
stl_top.vertices = tmp_vertices

# create walls as ring
bot_wall_ids = list([])
for facet in stl_bot.facets:
    triangle = Triangle(stl_bot.vertices[facet[0]],
                        stl_bot.vertices[facet[1]],
                        stl_bot.vertices[facet[2]])
    shape_ptr = sim.scene.InsertShape(triangle)
    wall = Wall(shape_ptr)
    wall.material_type = 1
    w_ptr = sim.scene.InsertWall(wall)
    bot_wall_ids.append(w_ptr.id)

num_mid_rings = 16

stl_mid.Translate([0, 0, 0.02])
stl_mid.Translate([0, 0, -0.00665])

for i in range(0, num_mid_rings):
    stl_mid.Translate([0, 0, 0.00665])

    mid_wall_ids = list([])
    for facet in stl_mid.facets:
        triangle = Triangle(stl_mid.vertices[facet[0]],
                            stl_mid.vertices[facet[1]],
                            stl_mid.vertices[facet[2]])
        shape_ptr = sim.scene.InsertShape(triangle)
        wall = Wall(shape_ptr)
        wall.material_type = 1
        w_ptr = sim.scene.InsertWall(wall)
        mid_wall_ids.append(w_ptr.id)

    tmp_integrator = WallMotionIntegrator()
    tmp_integrator.label = "wall_motion_integrator_" + str(i)
    tmp_integrator.enable_translation = [True, False, False]
    tmp_integrator.update_with_scene = False
    tmp_integrator.mass = 0.0378
    tmp_integrator.Init(sim)
    tmp_integrator.Add(mid_wall_ids)
    sim.modifier_manager.Insert(tmp_integrator)

stl_top.Translate([0, 0, 0.02])
stl_top.Translate([0, 0, 0.00665 * num_mid_rings])

for facet in stl_top.facets:
    triangle = Triangle(stl_top.vertices[facet[0]],
                        stl_top.vertices[facet[1]],
                        stl_top.vertices[facet[2]])
    shape_ptr = sim.scene.InsertShape(triangle)
    wall = Wall(shape_ptr)
    wall.material_type = 1
    w_ptr = sim.scene.InsertWall(wall)

# gravity
grav = Gravity()
grav.Init(sim)
sim.modifier_manager.Insert(grav)
sim.modifier_manager.Enable(grav.label)

# unbalanced force ratio
unbal = UnbalancedForceRatioEvaluator()
unbal.Init(sim)
sim.modifier_manager.Insert(unbal)
sim.modifier_manager.Enable(unbal.label)

# output
data_dumper = DataDumper()
data_dumper.Init(sim)
data_dumper.SetRootPath(dir_path + "/../../tmp/simple_shear/out/")
data_dumper.SetSaveByTime(0.01)
data_dumper.dump_wall_info = True
data_dumper.dump_contact_info = True
data_dumper.dump_mesh = True
data_dumper.SaveShapeInfoAsSTL()
sim.modifier_manager.Insert(data_dumper)
sim.modifier_manager.Enable(data_dumper.label)

# particle shape templates
sphere = Sphere(0.01)
particle_shape_ptr = sim.scene.InsertShape(sphere)

# generate particles
pack_generator = PackGenerator()
particle_list = pack_generator.GetGridPack(
    0.2, 0.2, 0.4, 0, 0, 0.22, 18, 18, 36, particle_shape_ptr)
for p in particle_list:
    p.SetDensity(7530)
    p.damp_numerical = 0.7

# insert particles and rest
sim.scene.InsertParticle(particle_list)
sim.Run(1.0)

# remove extra particles
for p in sim.scene.particle_list:
    if p.pos[2] < 0 or p.pos[2] > 0.12 \
            or math.sqrt(p.pos[0] * p.pos[0] + p.pos[1] * p.pos[1]) > 0.154:
        sim.scene.RemoveParticle(p)

cnt_model_2_prt.SetProperty('mu', 0.1)

# add top wall and apply servo-control
plane = Plane(0, 0, 0.13, 0, 0, -1)
plane.SetExtent(0.5)
plane_ptr = sim.scene.InsertShape(plane)
wall_top = Wall(plane_ptr)
wall_top_ptr = sim.scene.InsertWall(wall_top)

servo_top = WallServoControl(2e6, Math.PI * 0.308 * 0.308 / 4)
servo_top.label = "servo_top"
servo_top.Init(sim)
servo_top.target_pressure = 4e5
servo_top.SetWall([wall_top_ptr.id])
tmp = sim.modifier_manager.Insert(servo_top)
sim.modifier_manager.Enable(servo_top.label)
servo_top_ptr = WallServoControl.Cast(tmp)

# keep loading until target pressure is achieved
while True:
    sim.Run(0.01)
    if servo_top_ptr.achieved:
        break

# moving the bot ring
wall_motion_control = WallMotionControl()
wall_motion_control.Init(sim)
wall_motion_control.SetWall(bot_wall_ids)
wall_motion_control.SetVelocity(0.005, 0, 0)
sim.modifier_manager.Insert(wall_motion_control)
sim.modifier_manager.Enable(wall_motion_control.label)

# allow the middle ring stacks to move
for i in range(0, num_mid_rings):
    tmp_label = "wall_motion_integrator_" + str(i)
    sim.modifier_manager.Enable(tmp_label)

# run
sim.Run(3.0)
