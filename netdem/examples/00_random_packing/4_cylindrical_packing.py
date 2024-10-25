import netdem

netdem.omp_set_num_threads(1)

sim = netdem.Simulation()
sim.domain_manager.SetBound(-0.6, -0.6, -0.6, 0.6, 0.6, 0.6)
sim.domain_manager.SetCellSpacing(0.3, 0.3, 0.3)

sim.dem_solver.contact_solver_factory.settings.solver_type = (
    netdem.ContactSolverSettings.SolverType.sdf
)
sim.dem_solver.contact_solver_factory.settings.sdf_potential_type = 0

cnt_model = netdem.LinearSpring(2.0e4, 1.0e4, 0.5, 0.0)
cnt_model_prt = sim.scene.InsertContactModel(cnt_model)
sim.scene.SetNumberOfMaterials(1)
sim.scene.SetCollisionModel(0, 0, cnt_model_prt)

num_insertion = 20
scale = pow(20.0 / num_insertion, 1.0 / 3.0)

# tri_mesh = netdem.TriMesh()
# for i in range(5):
#     tri_mesh.InitFromSTL("data/copyleft/ballast/ballast_" + str(i + 1) + ".stl")
#     tri_mesh.Decimate(200)
#     tri_mesh.AlignAxes()
#     tri_mesh.SetSize(0.01 * scale)
#     sim.scene.InsertShape(tri_mesh)

level_set = netdem.LevelSet()
for i in range(5):
    level_set.InitFromSTL(
        "data/copyleft/ballast/ballast_" + str(i + 1) + ".stl", 20
    )
    level_set.AlignAxes()
    level_set.SetSize(0.01 * scale)
    sim.scene.InsertShape(level_set)

shape_list = sim.scene.GetShapes()
pack_generator = netdem.PackGenerator()
particle_list = pack_generator.GetGridPack(
    0.035, 0.035, 0.06, 0, 0, 0.07, 2, 2, 3, shape_list
)
for p in particle_list:
    p.SetVelocity(0, 0, -0.6)
    p.damp_numerical = 0.7

# bottom wall
plane_bot = netdem.Plane(0, 0, -0.05, 0, 0, 1)
plane_bot.SetExtent(0.1)
plane_bot_ptr = sim.scene.InsertShape(plane_bot)
wall_bot = netdem.Wall(plane_bot_ptr)
wall_bot_ptr = sim.scene.InsertWall(wall_bot)

# membrane
membrane_wall = netdem.MembraneWall(0.025, 0.2, 0.0025)
membrane_wall.facing_outside = False
membrane_wall.enable_deformation = False
membrane_wall.dump_info = True
membrane_wall.Init(sim)
membrane_wall.SetRootPath("tmp/out_tri_comp/")
membrane_wall.SetSaveByCycles(100)
modifier_ptr = sim.modifier_manager.Insert(membrane_wall)
modifier_ptr.Enable()

# gravity
grav = netdem.Gravity()
grav.Init(sim)
sim.modifier_manager.Insert(grav)
sim.modifier_manager.Enable(grav.label)

# save data
data_dumper = netdem.DataDumper()
data_dumper.Init(sim)
data_dumper.SetRootPath("tmp/out_n" + str(num_insertion * 12) + "/")
data_dumper.SetSaveByCycles(100)
data_dumper.dump_wall_info = True
data_dumper.dump_contact_info = True
data_dumper.SaveShapeInfoAsSTL()
sim.modifier_manager.Insert(data_dumper)
sim.modifier_manager.Enable(data_dumper.label)

for i in range(num_insertion):
    sim.scene.InsertParticle(particle_list)
    sim.Run(0.1)

sim.Run(2.0 + 0.1 * (20 - num_insertion))
