from signal import pause
import sys
import os
import math

# env
dir_path = os.path.dirname(os.path.realpath(__file__))
sys.path.append(dir_path + "/../../build/lib/")
from netdem import *


class WallMotionIntegrator(Modifier):
    wall_id_list = set([])
    wall_list = list([])
    mass = 4.6

    def __init__(self):
        super().__init__()
        self.label = "wall_motion_integrator"
        self.cycle_point = DEMSolver.CyclePoint.mid_4
        self.update_with_scene = False

    # need to improve this: Clone should return a deepcopy of self
    def Clone(self):
        tmp = self
        return tmp

    def Add(self, ids):
        for id in ids:
            self.wall_id_list.add(id)
        self.Update()

    def Execute(self):
        dt = sim.dem_solver.timestep

        fx = 0
        for w_ptr in sim.scene.wall_list:
            fx += w_ptr.force[0]

        dv = fx / self.mass * dt
        for w_ptr in self.wall_list:
            w_ptr.SetVelocity(w_ptr.vel[0] + dv, 0, 0)

    def Update(self):
        self.wall_list.clear()
        if not self.scene is None:
            for id in self.wall_id_list:
                w_ptr = self.scene.FindWall(id)
                if not w_ptr is None:
                    self.wall_list.append(w_ptr)
                else:
                    print("warning: null scene, please initialize: ")


# sim settings
sim = Simulation()
sim.domain_manager.SetBound(-0.6, -0.6, -0.6, 0.6, 0.6, 1.2)
sim.domain_manager.SetCellSpacing(0.02, 0.02, 0.02)

# solver settings
sim.dem_solver.contact_solver_factory.settings.solver_type = (
    ContactSolverSettings.SolverType.automatic
)
sim.dem_solver.contact_solver_factory.settings.sdf_potential_type = 0

# contact model
cnt_model_1 = LinearSpring(2.0e4, 1.0e4, 0.5, 0.0)
cnt_model_1.label = "cnt_model_1"
cnt_model_1_prt = sim.scene.InsertContactModel(cnt_model_1)

cnt_model_2 = LinearSpring(2.0e4, 1.0e4, 0.1, 0.0)
cnt_model_2.label = "cnt_model_2"
cnt_model_2_prt = sim.scene.InsertContactModel(cnt_model_2)

sim.scene.SetNumberOfMaterials(2)
sim.scene.SetCollisionModel(0, 0, cnt_model_1_prt)
sim.scene.SetCollisionModel(0, 1, cnt_model_1_prt)
sim.scene.SetCollisionModel(1, 1, cnt_model_2_prt)

# shape templates
sphere = Sphere(0.01)
sphere_ptr = sim.scene.InsertShape(sphere)

stl_bot = STLModel()
stl_bot.InitFromSTL(dir_path + "/data/ring_bot.stl")
stl_mid = STLModel()
stl_mid.InitFromSTL(dir_path + "/data/ring_mid.stl")

# create walls as ring
bot_wall_ids = list([])
for facet in stl_bot.facets:
    triangle = Triangle(
        stl_bot.vertices[facet[0]],
        stl_bot.vertices[facet[1]],
        stl_bot.vertices[facet[2]],
    )
    shape_ptr = sim.scene.InsertShape(triangle)
    wall = Wall(shape_ptr)
    wall.material_type = 1
    w_ptr = sim.scene.InsertWall(wall)
    bot_wall_ids.append(w_ptr.id)

stl_mid.Translate([0, 0, 0.02])
stl_mid.Translate([0, 0, -0.00665])

wall_motion_integrator_list = [None] * 17
for i in range(0, 17):
    stl_mid.Translate([0, 0, 0.00665])

    mid_wall_ids = list([])
    for facet in stl_mid.facets:
        triangle = Triangle(
            stl_mid.vertices[facet[0]],
            stl_mid.vertices[facet[1]],
            stl_mid.vertices[facet[2]],
        )
        shape_ptr = sim.scene.InsertShape(triangle)
        wall = Wall(shape_ptr)
        wall.material_type = 1
        w_ptr = sim.scene.InsertWall(wall)
        mid_wall_ids.append(w_ptr.id)

    wall_motion_integrator_list[i] = WallMotionIntegrator()
    wall_motion_integrator_list[i].label = "wall_motion_integrator_" + str(i)
    wall_motion_integrator_list[i].Init(sim)
    wall_motion_integrator_list[i].Add(mid_wall_ids)
    sim.modifier_manager.Insert(wall_motion_integrator_list[i])
    sim.modifier_manager.Enable(wall_motion_integrator_list[i].label)

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

# generate particles
pack_generator = PackGenerator()
particle_list = pack_generator.GetGridPack(
    0.2, 0.2, 0.36, 0, 0, 0.2, 18, 18, 30, sphere_ptr
)
for p in particle_list:
    p.SetDensity(7530)
    p.damp_numerical = 0.7

# insert particles and rest
sim.scene.InsertParticle(particle_list)
for i in range(0, 100):
    sim.Run(0.01)
    for p in sim.scene.particle_list:
        p.SetVelocity(0, 0, 0)
        p.SetSpin(0, 0, 0)

# remove extra particles
for p in sim.scene.particle_list:
    if (
        p.pos[2] < 0
        or p.pos[2] > 0.12
        or math.sqrt(p.pos[0] * p.pos[0] + p.pos[1] * p.pos[1]) > 0.154
    ):
        sim.scene.RemoveParticle(p)

# add top wall and apply servo-control
plane = Plane(0, 0, 0.13, 0, 0, -1)
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

# moving the bot ring
wall_motion_control = WallMotionControl()
wall_motion_control.Init(sim)
wall_motion_control.SetWall(bot_wall_ids)
wall_motion_control.SetVelocity(0.005, 0, 0)
sim.modifier_manager.Insert(wall_motion_control)
sim.modifier_manager.Enable(wall_motion_control.label)

sim.Run(3.0)
