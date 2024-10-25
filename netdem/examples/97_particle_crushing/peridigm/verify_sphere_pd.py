import netdem

# units: mm, 1000 kg, N, s
pd_sim = netdem.PeriDigmSimulator()
pd_sim.settings.result_dir = "tmp/out/peridigm/verify_sphere/"

# create a particle and two walls
stl_model = netdem.STLModel()
stl_model.InitFromSTL("data/sphere.stl")
stl_model.SetSize(2.0)

mesh_res = 25
pd_sim.discretization.type = netdem.PeriDigmDiscretization.Type.level_set
pd_sim.discretization.InitFromSTL(stl_model, mesh_res)
pd_sim.InitDefaultSetup()

# density is scaled by 1e6 times to enlarge the timestep
pd_sim.materials[0].density = 2650e-6
pd_sim.materials[0].youngs_modulus = 100e3
pd_sim.materials[0].poissons_ratio = 0.15
energy_release_rate = 30e-3
pd_sim.damage_models[0].InitFromEnergyReleaseRate(
    pd_sim.materials[0].youngs_modulus,
    pd_sim.materials[0].poissons_ratio,
    pd_sim.blocks[0].horizon,
    energy_release_rate,
)
pd_sim.InitAutoTimestep()

bc_fixed = pd_sim.InsertBoundaryCondition()
for i in range(0, len(pd_sim.discretization.nodes)):
    if abs(pd_sim.discretization.nodes[i][2] + 1.0) < 2.0 / mesh_res:
        bc_fixed.InsertNode(i)
bc_fixed.SetActivatedDimensions(True, True, True)

bc_compress = pd_sim.InsertBoundaryCondition()
for i in range(0, len(pd_sim.discretization.nodes)):
    if abs(pd_sim.discretization.nodes[i][2] - 1.0) < 2.0 / mesh_res:
        bc_compress.InsertNode(i)

# units: mm/s
loading_rate = -0.1
utimate_disp = -0.01

bc_compress.SetByDisplacementRate(0, 0, loading_rate)
bc_fixed.SetActivatedDimensions(True, True, True)

pd_sim.settings.output_freqency = 10
pd_sim.Solve(utimate_disp / loading_rate)
