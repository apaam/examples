# path and module
import netdem

# simulation
sim = netdem.Simulation()
sim.domain_manager.SetBound(-0.6, -0.6, -0.6, 0.6, 0.6, 0.6)
sim.domain_manager.SetCellSpacing(0.01, 0.01, 0.01)

# # solver
# sim.dem_solver.contact_solver_factory.settings.solver_type \
#     = netdem.ContactSolverSettings.SolverType.sdf
# sim.dem_solver.contact_solver_factory.settings.sdf_potential_type = 0

# material model
cnt_model = netdem.LinearSpring(2.0e5, 1.0e5, 0.3, 0.0)
cnt_model.label = "particle_&_wall"
cnt_model_0_prt = sim.scene.InsertContactModel(cnt_model)

cnt_model = netdem.LinearSpring(2.0e4, 1.0e4, 0.5, 0.0)
cnt_model.label = "membrane"
cnt_model_1_prt = sim.scene.InsertContactModel(cnt_model)

sim.scene.SetNumberOfMaterials(2)
sim.scene.SetCollisionModel(0, 0, cnt_model_0_prt)
sim.scene.SetCollisionModel(0, 1, cnt_model_1_prt)
sim.scene.SetCollisionModel(1, 1, cnt_model_1_prt)

# particle shape
sphere = netdem.Sphere(0.004)
sim.scene.InsertShape(sphere)

# pack of particles to be inserted
shape_list = sim.scene.GetShapes()
pack_generator = netdem.PackGenerator()
particle_list = pack_generator.GetGridPack(
    0.035, 0.035, 0.06, 0, 0, 0.12, 5, 5, 8, shape_list
)
for p in particle_list:
    p.SetDensity(2650e3)
    p.SetVelocity(0, 0, -0.6)
    p.damp_numerical = 0.1

# bottom wall
plane = netdem.Plane(0, 0, -0.05, 0, 0, 1)
plane.SetExtent(0.1)  # make sure the plane is inside the computing domain
plane_ptr = sim.scene.InsertShape(plane)
wall_bot = netdem.Wall(plane_ptr)
wall_bot_ptr = sim.scene.InsertWall(wall_bot)

# membrane
membrane_wall = netdem.MembraneWall(0.025, 0.2, 0.005)
membrane_wall.neo_k = 6.94e6
membrane_wall.neo_mu = 5.21e6
membrane_wall.density = 500e6
membrane_wall.damp_coef = 0.9
membrane_wall.timestep = 1.0e-5
membrane_wall.enable_deformation = False  # disable deformation during packing
membrane_wall.dump_info = True
membrane_wall.Init(sim)
membrane_wall.SetRootPath("tmp/out_tri_comp/")
membrane_wall.SetSaveByCycles(100)
modifier_ptr = sim.modifier_manager.Insert(membrane_wall)
membrane_wall_ptr = netdem.MembraneWall.Cast(modifier_ptr)
sim.modifier_manager.Enable(membrane_wall.label)

# gravity
sim.scene.gravity_coef = [0, 0, -9.81]
grav = netdem.Gravity()
grav.Init(sim)
sim.modifier_manager.Insert(grav)
sim.modifier_manager.Enable(grav.label)

# out particle, wall and contact data
data_dumper = netdem.DataDumper()
data_dumper.Init(sim)
data_dumper.SetRootPath("tmp/out_tri_comp/")
data_dumper.SetSaveByCycles(100)
data_dumper.dump_contact_info = True
data_dumper.dump_wall_info = True
data_dumper.dump_shape_info = True
sim.modifier_manager.Insert(data_dumper)
sim.modifier_manager.Enable(data_dumper.label)

# insert 20 packs of particles
sim.dem_solver.timestep = 1.0e-4

for i in range(20):
    sim.scene.InsertParticle(particle_list)
    sim.Run(0.1)

# rest for 1.0 s
sim.Run(1.0)

# remove extra particles
sim.scene.gravity_coef = [0, 0, 0]
for p in sim.scene.particle_list:
    if p.pos[2] > 0.05 - 0.5 * p.shape.GetSize():
        sim.scene.RemoveParticle(p)

# add top wall
plane = netdem.Plane(0, 0, 0.05, 0, 0, -1)
plane.SetExtent(0.1)
plane_ptr = sim.scene.InsertShape(plane)
wall_top = netdem.Wall(plane_ptr)
wall_top_ptr = sim.scene.InsertWall(wall_top)

# reset the membrane dimensions
membrane_wall_ptr.SetDimensions(0.025, 0.10)

# fix the bottom and top of the membrane wall
for i in range(0, len(membrane_wall_ptr.nodes)):
    if (
        abs(membrane_wall_ptr.nodes[i][2] + 0.5 * membrane_wall_ptr.height)
        < 1.0e-4
        or abs(membrane_wall_ptr.nodes[i][2] - 0.5 * membrane_wall_ptr.height)
        < 1.0e-4
    ):
        membrane_wall_ptr.SetBCNodalVelocity(i, 0, 0, 0, 1, 1, 1)

# # add two pedestal particles
# super_ellipsoid = netdem.PolySuperEllipsoid(
#     0.025, 0.025, 0.025, 0.025, 0.005, 0.005, 1.0, 0.25)
# super_ellipsoid_ptr = sim.scene.InsertShape(super_ellipsoid)

# pedestal_bot = netdem.Particle(super_ellipsoid_ptr)
# pedestal_bot.SetPosition(0, 0, -0.055)
# pedestal_bot_ptr = sim.scene.InsertParticle(pedestal_bot)
# pedestal_bot_ptr.SetDensity(2650e3)

# pedestal_top = netdem.Particle(super_ellipsoid_ptr)
# pedestal_top.SetPosition(0, 0, 0.055)
# pedestal_top_ptr = sim.scene.InsertParticle(pedestal_top)
# pedestal_top_ptr.SetDensity(2650e3)

# wall_bot_ptr.SetPosition(0, 0, -0.01)
# wall_top_ptr.SetPosition(0, 0, 0.01)

# gradually increase confining pressure
membrane_wall_ptr.enable_deformation = True
for w in membrane_wall_ptr.wall_list:
    w.material_type = 1

membrane_wall_ptr.SetPressure(-1.0e5)
sim.Run(1.0)

# add deformation drived loading for top wall
disp_control = netdem.WallMotionControl()
disp_control.Init(sim)
disp_control.SetWall([wall_top_ptr.id])
disp_control.SetVelocity(0, 0, -0.001)
sim.modifier_manager.Insert(disp_control)
sim.modifier_manager.Enable(disp_control.label)

# press the top of membrane to move with the compression top wall
for i in range(0, len(membrane_wall_ptr.nodes)):
    if (
        abs(membrane_wall_ptr.nodes[i][2] - 0.5 * membrane_wall_ptr.height)
        < 1.0e-4
    ):
        membrane_wall_ptr.SetBCNodalVelocity(i, 0, 0, -0.001, 1, 1, 1)

# # sim.Run(2.0)
# # sim.Run(20.0)
