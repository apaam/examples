import netdem
import math

sim = netdem.Simulation()
sim.domain_manager.SetBound(-0.6, -0.6, -1, 0.6, 0.6, 1)
sim.domain_manager.SetCellSpacing(0.2, 0.2, 0.2)

cnt_model = netdem.LinearSpring(2.0e5, 1.0e5, 0.5, 0.0)
cnt_model_prt = sim.scene.InsertContactModel(cnt_model)
sim.scene.SetNumberOfMaterials(1)
sim.scene.SetCollisionModel(0, 0, cnt_model_prt)

#sphere=netdem.Sphere(0.03)
#particle_shape_ptr=sim.scene.InsertShape(sphere)


tri_mesh = netdem.TriMesh()
tri_mesh.InitFromSTL("data/particle_template.stl")
tri_mesh.Decimate(200)
tri_mesh.MakeConvex()
tri_mesh.AlignAxes()
tri_mesh.SetSize(0.03)
tri_mesh_ptr = sim.scene.InsertShape(tri_mesh)


pack_generator = netdem.PackGenerator()
particle_list = pack_generator.GetGridPack(
     0.6, 0.6, 0.1, 0, 0, 0.9, 10, 10, 1, tri_mesh_ptr
)
for p in particle_list:
    p.SetVelocity(0, 0, -2.0)
    p.damp_numerical = 0.7

cylinder_stl=netdem.STLModel()
cylinder_stl.InitFromSTL("data/funnel_1.stl")

for facet in cylinder_stl.facets:
    triangel=netdem.Triangle(cylinder_stl.vertices[facet[0]],cylinder_stl.vertices[facet[1]],cylinder_stl.vertices[facet[2]])
    shape_ptr=sim.scene.InsertShape(triangel)
    wall=netdem.Wall(shape_ptr)
    sim.scene.InsertWall(wall)

cylinder2_stl=netdem.STLModel()
cylinder2_stl.InitFromSTL("data/funnel_2.stl")

for facet in cylinder2_stl.facets:
    triangel=netdem.Triangle(cylinder2_stl.vertices[facet[0]],cylinder2_stl.vertices[facet[1]],cylinder2_stl.vertices[facet[2]])
    shape_ptr=sim.scene.InsertShape(triangel)
    wall=netdem.Wall(shape_ptr)
    sim.scene.InsertWall(wall)

grav = netdem.Gravity()
grav.Init(sim)
sim.modifier_manager.Insert(grav)
sim.modifier_manager.Enable(grav.label)

data_dumper = netdem.DataDumper()
data_dumper.Init(sim)
data_dumper.SetRootPath("tmp/out_funnel/")
data_dumper.SetSaveByCycles(100)
data_dumper.dump_wall_info = True
data_dumper.dump_mesh = True
data_dumper.dump_shape_info= True
data_dumper.SaveShapeInfoAsSTL()
sim.modifier_manager.Insert(data_dumper)
sim.modifier_manager.Enable(data_dumper.label)

for i in range(50):
    sim.scene.InsertParticle(particle_list)
    sim.Run(0.2)

sim.Run(1.0)

for wall_ptr in sim.scene.wall_list:
    sim.scene.RemoveWall(wall_ptr)

cylinder_stl=netdem.STLModel()
cylinder_stl.InitFromSTL("data/funnel_1.stl")

for facet in cylinder_stl.facets:
    triangel=netdem.Triangle(cylinder_stl.vertices[facet[0]],cylinder_stl.vertices[facet[1]],cylinder_stl.vertices[facet[2]])
    shape_ptr=sim.scene.InsertShape(triangel)
    wall=netdem.Wall(shape_ptr)
    sim.scene.InsertWall(wall)

sim.Run(20.0)