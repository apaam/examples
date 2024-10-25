import netdem
import math

# simulation settings
sim = netdem.Simulation()
sim.domain_manager.SetBound(-16, -16, -16, 16, 16, 16)
sim.domain_manager.SetCellSpacing(0.6, 0.6, 0.6)

cnt_model = netdem.LinearSpring(2.0e6, 1.0e6, 0.5, 0.3)
cnt_model_ptr = sim.scene.InsertContactModel(cnt_model)
sim.scene.SetNumberOfMaterials(1)
sim.scene.SetCollisionModel(0, 0, cnt_model_ptr)

# create a particle and two walls
stl_model = netdem.STLModel()
stl_model.InitFromSTL("data/particle_template.stl")
stl_model.Decimate(200)
stl_model.Standardize()
stl_model.SetSize(1.0)

bond_model = netdem.ParallelBond(2.0e6, 1.0e6, 1.0e6, 1.0e6, 0.3)
bond_model.label = "bond_model"
bond_model_ptr = sim.scene.InsertContactModel(bond_model)

bonded_spheres = netdem.BondedSpheres()
bonded_spheres.SetBondModel(bond_model_ptr)
bonded_spheres.InitFromSTL(stl_model, 0.1)
sim.scene.InsertParticle(bonded_spheres)

plane_1 = netdem.Plane(0, 0, 0.39, 0, 0, -1)
plane_2 = netdem.Plane(0, 0, -0.44, 0, 0, 1)

plane_1_ptr = sim.scene.InsertShape(plane_1)
plane_2_ptr = sim.scene.InsertShape(plane_2)

w_1 = netdem.Wall(plane_1_ptr)
w_2 = netdem.Wall(plane_2_ptr)

sim.scene.InsertWall(w_1)
sim.scene.InsertWall(w_2)

# gravity
grav = netdem.Gravity()
grav.Init(sim)
sim.modifier_manager.Insert(grav)
sim.modifier_manager.Enable(grav.label)
sim.scene.gravity_coef = [0, 0, -9.81e-3]

# save results
data_dumper = netdem.DataDumper()
data_dumper.Init(sim)
data_dumper.SetRootPath("tmp/out/")
data_dumper.SetSaveByCycles(100)
data_dumper.SaveShapeInfoAsSTL()
data_dumper.dump_shape_info = True
data_dumper.dump_wall_info = True
data_dumper.dump_contact_info = True
sim.modifier_manager.Insert(data_dumper)
sim.modifier_manager.Enable(data_dumper.label)

# add deformation drived loading for top wall
disp_control = netdem.WallMotionControl()
disp_control.Init(sim)
disp_control.SetWall([0])
disp_control.SetVelocity(0, 0, -0.1)
sim.modifier_manager.Insert(disp_control)
sim.modifier_manager.Enable(disp_control.label)

# run the simulation
sim.dem_solver.timestep = 1.0e-4
sim.Run(2.0)
