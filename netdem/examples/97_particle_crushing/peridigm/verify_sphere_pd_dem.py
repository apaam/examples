import netdem

# simulation settings. units: mm, 1000 kg, N, s
sim = netdem.Simulation()
sim.domain_manager.SetBound(-16, -16, -16, 16, 16, 16)
sim.domain_manager.SetCellSpacing(0.6, 0.6, 0.6)

# contact settings
sim.dem_solver.contact_solver_factory.settings.solver_type = (
    netdem.ContactSolverSettings.SolverType.sdf
)
sim.dem_solver.contact_solver_factory.settings.sdf_potential_type = 0

cnt_model = netdem.LinearSpring(2.0e4, 1.0e4, 0.5, 0.0)
cnt_model_ptr = sim.scene.InsertContactModel(cnt_model)
sim.scene.SetNumberOfMaterials(1)
sim.scene.SetCollisionModel(0, 0, cnt_model_ptr)

# create a particle and two walls
trimesh = netdem.TriMesh()
trimesh.InitFromSTL("data/sphere.stl")
trimesh.AlignAxes()
trimesh.SetSize(2.0)

plane_1 = netdem.Plane(0, 0, 1.0, 0, 0, -1)
plane_2 = netdem.Plane(0, 0, -1.0, 0, 0, 1)

trimesh_ptr = sim.scene.InsertShape(trimesh)
plane_1_ptr = sim.scene.InsertShape(plane_1)
plane_2_ptr = sim.scene.InsertShape(plane_2)

p = netdem.Particle(trimesh_ptr)
p.SetDensity(2650e-6)

w_1 = netdem.Wall(plane_1_ptr)
w_2 = netdem.Wall(plane_2_ptr)

sim.scene.InsertParticle(p)
sim.scene.InsertWall(w_1)
sim.scene.InsertWall(w_2)

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

# breakage modifier
breakage_analysis = netdem.BreakageAnalysisPD()
breakage_analysis.Init(sim)
breakage_analysis.SetRootPath("tmp/out/")
breakage_analysis.SetParticleFromScene()
breakage_analysis.SetExecuteByCycles(1000)

breakage_analysis.pd_dem_coupler.mesh_res = 30
breakage_analysis.pd_dem_coupler.loading_steps = 1000
breakage_analysis.pd_dem_coupler.fragment_vol_limit = 0.001

strength_params = breakage_analysis.pd_dem_coupler.strength_params
strength_params.ref_size = 2.0
strength_params.ref_energy_release_rate = 30e-3
strength_params.min_breakable_size = 1.9

material_params = breakage_analysis.pd_dem_coupler.material_params
material_params.density = 2650e-6
material_params.youngs_modulus = 100e3
material_params.poissons_ratio = 0.15

sim.modifier_manager.Insert(breakage_analysis)
sim.modifier_manager.Enable(breakage_analysis.label)

# add deformation drived loading for top wall
disp_control = netdem.WallMotionControl()
disp_control.Init(sim)
disp_control.SetWall([0])
disp_control.SetVelocity(0, 0, -0.02)
sim.modifier_manager.Insert(disp_control)
sim.modifier_manager.Enable(disp_control.label)

# run the simulation
sim.dem_solver.timestep = 1.0e-4
sim.Run(1.0)
