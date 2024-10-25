import sys
import os
import math

# env
dir_path = os.path.dirname(os.path.realpath(__file__))
sys.path.append(dir_path + "/../../build/lib/")
from netdem import *

# sim settings
sim = Simulation()
sim.domain_manager.SetBound(-0.6, -0.6, -0.6, 0.6, 0.6, 0.6)
sim.domain_manager.SetCellSpacing(0.02, 0.02, 0.02)

# solver settings
sim.dem_solver.contact_solver_factory.settings.solver_type \
    = ContactSolverSettings.SolverType.automatic
sim.dem_solver.contact_solver_factory.settings.sdf_potential_type = 0

# contact model
cnt_model_1 = LinearSpring(2.0e4, 1.0e4, 0.5, 0.0)
cnt_model_1.label = "cnt_model_1"
cnt_model_1_prt = sim.scene.InsertContactModel(cnt_model_1)

cnt_model_2 = LinearSpring(2.0e4, 1.0e4, 0.0, 0.0)
cnt_model_2.label = "cnt_model_2"
cnt_model_2_prt = sim.scene.InsertContactModel(cnt_model_2)

sim.scene.SetNumberOfMaterials(2)
sim.scene.SetCollisionModel(0, 0, cnt_model_1_prt)
sim.scene.SetCollisionModel(0, 1, cnt_model_1_prt)
sim.scene.SetCollisionModel(1, 1, cnt_model_2_prt)

# shape templates
sphere = Sphere(0.01)
sphere_ptr = sim.scene.InsertShape(sphere)

ring_bot = TriMesh()
ring_bot.InitFromSTL("data/ring_bot.stl")
ring_bot.AlignAxes()
ring_bot_ptr = sim.scene.InsertShape(ring_bot)

ring_mid = TriMesh()
ring_mid.InitFromSTL("data/ring_mid.stl")
ring_mid.AlignAxes()
ring_mid_ptr = sim.scene.InsertShape(ring_mid)

# create particles as ring
h_ref = 0.00749305 - 0.02 + 0.00665

p_bot = Particle()
p_bot.material_type = 1
p_bot.SetShape(ring_bot_ptr)
p_bot.SetPosition(0, 0, h_ref)
p_bot.SetRodrigues(Math.PI, 1, 0, 0)
p_bot.SetDensity(7530)
p_bot.damp_viscous = 3
p_bot_ptr = sim.scene.InsertParticle(p_bot)

for i in range(1, 18):
    p_mid = Particle()
    p_mid.material_type = 1
    p_mid.SetShape(ring_mid_ptr)
    p_mid.SetPosition(0, 0, 0.003325 + i * 0.00665)
    p_mid.SetDensity(7530)
    p_mid.damp_viscous = 3
    p_mid_ptr = sim.scene.InsertParticle(p_mid)

# create a motion control for particles
motion_control = ParticleMotionControl()
motion_control.Init(sim)
motion_control.SetFixed(p_bot_ptr.id)
tmp = sim.modifier_manager.Insert(motion_control)
sim.modifier_manager.Enable(motion_control.label)
motion_control_ptr = ParticleMotionControl.Cast(tmp)

# gravity
grav = Gravity()
grav.Init(sim)
sim.modifier_manager.Insert(grav)
sim.modifier_manager.Enable(grav.label)

# output
data_dumper = DataDumper()
data_dumper.Init(sim)
data_dumper.SetRootPath(dir_path + "/../../tmp/simple_shear/out/")
data_dumper.SetSaveByCycles(100)
data_dumper.dump_wall_info = True
data_dumper.dump_contact_info = True
data_dumper.dump_mesh = True
data_dumper.SaveShapeInfoAsSTL()
sim.modifier_manager.Insert(data_dumper)
sim.modifier_manager.Enable(data_dumper.label)

# relax the rings
sim.Run(2.0)

# fix the top two rings
motion_control_ptr.SetFixed(16)
motion_control_ptr.SetFixed(17)

# generate particles
cylinder = Cylinder(0.154, 0.2)
cylinder_stl = cylinder.GetSTLModel(500)
cylinder_stl.Translate([0, 0, 0.1])

pack_generator = PackGenerator()
particle_list = pack_generator.GetVoronoiPack(
    cylinder_stl, 100, sphere_ptr)
for p in particle_list:
    p.SetDensity(7530)
    p.damp_numerical = 0.7

# insert particles and rest
sim.scene.InsertParticle(particle_list)
sim.Run(1.0)

# remove extra particles
for p in sim.scene.particle_list:
    if p.pos[2] < 0 or p.pos[2] > 0.11 \
            or math.sqrt(p.pos[0] * p.pos[0] + p.pos[1] * p.pos[1]) > 0.154:
        if p.id >= 18:
            sim.scene.RemoveParticle(p)

# add top wall and apply servo-control
plane = Plane(0, 0, 0.11, 0, 0, -1)
plane.SetExtent(0.5)
plane_ptr = sim.scene.InsertShape(plane)
wall_top = Wall(plane_ptr)
wall_top_ptr = sim.scene.InsertWall(wall_top)

servo_top = WallServoControl(2e6, Math.PI * 0.304 * 0.304 / 4)
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

# moving the bot ring, v = a * t + b
motion_control_ptr.SetLinearVelocity(0, 0, 0.005, 0, 0, 0, 0)

sim.Run(3.0)
