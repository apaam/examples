import netdem

# units: mm, 1000 kg, N, s
pd_sim = netdem.PeriDigmSimulator()
pd_sim.settings.result_dir = "tmp/out/peridigm/single_cubic/"

mesh_res = 20

pd_sim.discretization.type = netdem.PeriDigmDiscretization.Type.level_set
pd_sim.discretization.InitFromGrid(-2.5, -2.5, -2.5, 5.0, 5.0, 5.0, mesh_res)
pd_sim.discretization.MakePorosity(0.2)
pd_sim.InitDefaultSetup()

# density is scaled by 1e6 times to enlarge the timestep
pd_sim.materials[0].density = 2650e-6
pd_sim.materials[0].youngs_modulus = 15e3
pd_sim.materials[0].poissons_ratio = 0.15
energy_release_rate = 60e-3
pd_sim.damage_models[0].InitFromEnergyReleaseRate(
    pd_sim.materials[0].youngs_modulus,
    pd_sim.materials[0].poissons_ratio,
    pd_sim.blocks[0].horizon,
    energy_release_rate,
)
pd_sim.InitAutoTimestep()

bc_fixed = pd_sim.InsertBoundaryCondition()
for i in range(0, len(pd_sim.discretization.nodes)):
    if abs(pd_sim.discretization.nodes[i][2] + 2.5) < 5.0 / mesh_res:
        bc_fixed.InsertNode(i)
bc_fixed.SetActivatedDimensions(False, False, True)

bc_compress = pd_sim.InsertBoundaryCondition()
for i in range(0, len(pd_sim.discretization.nodes)):
    if abs(pd_sim.discretization.nodes[i][2] - 2.5) < 5.0 / mesh_res:
        bc_compress.InsertNode(i)

# units: mm/s
loading_rate = -0.5
utimate_disp = -0.5

bc_compress.SetByDisplacementRate(0, 0, loading_rate)
bc_fixed.SetActivatedDimensions(False, False, True)

pd_sim.settings.output_freqency = 100
pd_sim.Solve(utimate_disp / loading_rate)
