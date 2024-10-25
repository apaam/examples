import netdem

sim = netdem.Simulation()

sim.domain_manager.SetBound(-12, -12, -12, 12, 12, 12)
sim.domain_manager.GetSelfSubDomain().cell_manager.SetSpacing(0.3, 0.3, 0.3)
# sim.dem_solver.contact_solver_factory.settings.gjk_use_erosion = True

collision_model = netdem.LinearSpring(2.0e6, 1.0e6, 0.5, 0.3)
collision_model_ptr = sim.scene.InsertContactModel(collision_model)
sim.scene.SetNumberOfMaterials(1)
sim.scene.SetCollisionModel(0, 0, collision_model_ptr)

bond_model = netdem.ParallelBond(2.0e6, 1.0e6, 1.0e6, 1.0e6, 0.3)
bond_model.label = "bond_model"
bond_model_ptr = sim.scene.InsertContactModel(bond_model)

stl_vase = netdem.STLModel()
stl_vase.InitFromSTL("data/particle_template.stl")
stl_vase.Standardize()
stl_vase.SetSize(0.2)

# tetmesh = netdem.TetMesh(stl_vase, 0.02)
# stl_vase = tetmesh.GetSurfaceSTL()

bonded_voronois = netdem.BondedVoronois()
bonded_voronois.SetBondModel(bond_model_ptr)
bonded_voronois.InitFromSTL(stl_vase, 20)
bonded_voronois.SaveAsVTK("tmp/out/shape/bonded_voronois.vtk")

sim.scene.InsertParticle(bonded_voronois)
# for p in sim.scene.particle_list:
#     p.damp_numerical = 0.7

plane = netdem.Plane(0, 0, -0.5, 0, 0, 1)
plane_ptr = sim.scene.InsertShape(plane)
wall = netdem.Wall(plane_ptr)
sim.scene.InsertWall(wall)

grav = netdem.Gravity()
grav.Init(sim)
sim.modifier_manager.Insert(grav)
sim.modifier_manager.Enable(grav.label)

data_dumper = netdem.DataDumper()
data_dumper.Init(sim)
data_dumper.SetRootPath("tmp/out/")
data_dumper.SetSaveByCycles(1000)
data_dumper.dump_wall_info = True
data_dumper.dump_contact_info = True
data_dumper.dump_mesh = True
data_dumper.SaveShapeInfoAsSTL()
sim.modifier_manager.Insert(data_dumper)
sim.modifier_manager.Enable(data_dumper.label)

sim.dem_solver.timestep = 1.0e-5
sim.Run(2.0)
