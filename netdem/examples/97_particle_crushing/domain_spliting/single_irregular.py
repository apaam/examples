import netdem

sim = netdem.Simulation()
sim.domain_manager.SetBound(-1.6, -1.6, -1.6, 1.6, 1.6, 1.6)
sim.domain_manager.SetCellSpacing(0.3, 0.3, 0.3)

# contact settings
sim.dem_solver.contact_solver_factory.settings.solver_type = (
    netdem.ContactSolverSettings.SolverType.sdf
)
sim.dem_solver.contact_solver_factory.settings.sdf_potential_type = 0

cnt_model = netdem.LinearSpring(2.0e5, 1.0e5, 0.5, 0.0)
cnt_model_ptr = sim.scene.InsertContactModel(cnt_model)
sim.scene.SetNumberOfMaterials(1)
sim.scene.SetCollisionModel(0, 0, cnt_model_ptr)

# create a particle and two walls
trimesh = netdem.TriMesh()
trimesh.InitFromSTL("data/particle_template.stl")
trimesh.Decimate(400)
trimesh.AlignAxes()
trimesh.SetSize(1.0)

plane_1 = netdem.Plane(0, 0, 0.39, 0, 0, -1)
plane_2 = netdem.Plane(0, 0, -0.42, 0, 0, 1)

trimesh_ptr = sim.scene.InsertShape(trimesh)
plane_1_ptr = sim.scene.InsertShape(plane_1)
plane_2_ptr = sim.scene.InsertShape(plane_2)

p = netdem.Particle(trimesh_ptr)
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
data_dumper.dump_mesh = True
sim.modifier_manager.Insert(data_dumper)
sim.modifier_manager.Enable(data_dumper.label)

# stress evaluator
particle_stress_evaluator = netdem.ParticleStressEvaluator()
particle_stress_evaluator.Init(sim)
particle_stress_evaluator.SetParticleFromScene()
sim.modifier_manager.Insert(particle_stress_evaluator)
sim.modifier_manager.Enable(particle_stress_evaluator.label)

# breakage modifier
breakage_analysis = netdem.BreakageAnalysis()
breakage_analysis.Init(sim)
breakage_analysis.strength = 1e3
breakage_analysis.min_breakable_size = 0.5
breakage_analysis.min_ignore_size = 0.1
breakage_analysis.SetParticleFromScene()

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
sim.Run(4.0)
