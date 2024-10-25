import sys
import os
import math

dir_path = os.path.dirname(os.path.realpath(__file__))
sys.path.append(dir_path + "/../../build/lib/")
import netdem

sim = netdem.Simulation()
sim.domain_manager.SetBound(-0.6, -0.6, -0.6, 0.6, 0.6, 0.6)
sim.domain_manager.SetCellSpacing(0.1, 0.1, 0.1)

sim.dem_solver.contact_solver_factory.settings.solver_type \
    = netdem.ContactSolverSettings.SolverType.sdf
sim.dem_solver.contact_solver_factory.settings.sdf_potential_type = 0

cnt_model = netdem.LinearSpring(2.0e6, 1.0e6, 0.5, 0.0)
cnt_model_prt = sim.scene.InsertContactModel(cnt_model)
sim.scene.SetNumberOfMaterials(1)
sim.scene.SetCollisionModel(0, 0, cnt_model_prt)

sphere = netdem.Sphere(0.005)
sim.scene.InsertShape(sphere)

shape_list = sim.scene.GetShapes()
pack_generator = netdem.PackGenerator()
particle_list = pack_generator.GetGridPack(
    0.2, 0.2, 0.1, 0, 0, 0.05, 5, 5, 3, shape_list)
for p in particle_list:
    p.SetVelocity(0, 0, -0.6)
    p.SetDensity(2650e3)
    p.damp_numerical = 0.7

wall_box = netdem.WallBoxPlane(0.2, 0.2, 0.2, 0, 0, 0)
wall_box.ImportToScene(sim.scene)
sim.scene.RemoveWall(sim.scene.wall_list[5])

tri_mesh = netdem.TriMesh()
tri_mesh.InitFromSTL("examples/10_cone_penetration/cone_cad.stl")
tri_mesh.MakeConvex()
tri_mesh.AlignAxes()
tri_mesh.SetSize(0.01)
trimesh_ptr = sim.scene.InsertShape(tri_mesh)

grav = netdem.Gravity()
grav.Init(sim)
sim.modifier_manager.Insert(grav)
sim.modifier_manager.Enable(grav.label)

data_dumper = netdem.DataDumper()
data_dumper.Init(sim)
data_dumper.SetRootPath("tmp/cone_penetration/out/")
data_dumper.SetSaveByCycles(100)
data_dumper.dump_wall_info = True
data_dumper.SaveShapeInfoAsSTL()
sim.modifier_manager.Insert(data_dumper)
sim.modifier_manager.Enable(data_dumper.label)

for i in range(1):
    sim.scene.InsertParticle(particle_list)
    sim.Run(0.1)

cone = netdem.Particle(trimesh_ptr)
cone.SetDensity(7650e3)
cone.SetPosition(0, 0, 0.2)
cone.SetRodrigues(math.radians(90), 0, 1, 0)
sim.scene.InsertParticle(cone)

sim.Run(2.0)
