import netdem

sim = netdem.Simulation()
sim.domain_manager.SetBound(-0.6, -0.6, -0.6, 0.6, 0.6, 0.6)
sim.domain_manager.SetCellSpacing(0.3, 0.3, 0.3)

cnt_model = netdem.LinearSpring(2.0e6, 1.0e6, 0.5, 0.7)
cnt_model_prt = sim.scene.InsertContactModel(cnt_model)
sim.scene.SetNumberOfMaterials(1)
sim.scene.SetCollisionModel(0, 0, cnt_model_prt)

tri_mesh = netdem.TriMesh()
tri_mesh.InitFromSTL("data/particle_template.stl")
tri_mesh.Decimate(200)
tri_mesh.MakeConvex()
tri_mesh.AlignAxes()
tri_mesh.SetSize(0.1)
tri_mesh_ptr = sim.scene.InsertShape(tri_mesh)

pack_generator = netdem.PackGenerator()
particle_list = pack_generator.GetGridPack(
    1, 1, 0.2, 0, 0, 0.4, 5, 5, 1, tri_mesh_ptr
)
for p in particle_list:
    p.SetVelocity(0, 0, -2.0)
    p.damp_numerical = 0.0
    p.damp_viscous = 0.0

wall_box = netdem.WallBoxPlane(1, 1, 1, 0, 0, 0)
wall_box.ImportToScene(sim.scene)

grav = netdem.Gravity()
grav.Init(sim)
sim.modifier_manager.Insert(grav)
sim.modifier_manager.Enable(grav.label)

data_dumper = netdem.DataDumper()
data_dumper.Init(sim)
data_dumper.SetRootPath("tmp/out/")
data_dumper.SetSaveByCycles(100)
data_dumper.dump_contact_info = True
data_dumper.dump_wall_info = True
data_dumper.dump_mesh = True
data_dumper.SaveShapeInfoAsSTL()
sim.modifier_manager.Insert(data_dumper)
sim.modifier_manager.Enable(data_dumper.label)

for i in range(20):
    sim.scene.InsertParticle(particle_list)
    sim.Run(0.1)

sim.Run(2.0)
