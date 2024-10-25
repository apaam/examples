import netdem
import math

sim = netdem.Simulation()
sim.domain_manager.SetBound(-0.6, -0.6, -0.6, 0.6, 0.6, 0.6)
sim.domain_manager.SetCellSpacing(0.2, 0.2, 0.2)

cnt_model = netdem.LinearSpring(2.0e6, 1.0e6, 0.5, 0.0)
cnt_model_prt = sim.scene.InsertContactModel(cnt_model)
sim.scene.SetNumberOfMaterials(1)
sim.scene.SetCollisionModel(0, 0, cnt_model_prt)

# sphere=netdem.Sphere(0.05)
# sphere_ptr=sim.scene.InsertShape(sphere)

tri_mesh = netdem.TriMesh()
tri_mesh.InitFromSTL("data/particle_template.stl")
tri_mesh.Decimate(200)
tri_mesh.MakeConvex()
tri_mesh.AlignAxes()
tri_mesh.SetSize(0.05)
tri_mesh_ptr = sim.scene.InsertShape(tri_mesh)

pack_generator = netdem.PackGenerator()
particle_list = pack_generator.GetGridPack(
    0.9, 0.3, 0.1, 0, 0, 0.2, 10, 4, 1, tri_mesh_ptr
)

for p in particle_list:
    p.SetVelocity(0, 0, -2.0)
    p.damp_numerical = 0.7

cylinder_stl = netdem.STLModel()
cylinder_stl.InitFromSTL("data/rotate_drum.stl")

for facet in cylinder_stl.facets:
    triangel = netdem.Triangle(
        cylinder_stl.vertices[facet[0]],
        cylinder_stl.vertices[facet[1]],
        cylinder_stl.vertices[facet[2]],
    )
    shape_ptr = sim.scene.InsertShape(triangel)
    wall = netdem.Wall(shape_ptr)
    wall.SetVelocitySpin(0, -0.1 * math.pi, 0)
    wall_ptr = sim.scene.InsertWall(wall)

    # the following treatment improves the efficiency
    [bound_aabb_min, bound_aabb_max] = shape_ptr.GetBoundAABB()
    tmp_pos = wall_ptr.pos
    tmp_pos[0] = 0.5 * (bound_aabb_min[0] + bound_aabb_max[0])
    tmp_pos[1] = 0.5 * (bound_aabb_min[1] + bound_aabb_max[1])
    tmp_pos[2] = 0.5 * (bound_aabb_min[2] + bound_aabb_max[2])
    wall_ptr.pos = tmp_pos
    shape_ptr.Translate([-wall_ptr.pos[0], -wall_ptr.pos[1], -wall_ptr.pos[2]])

grav = netdem.Gravity()
grav.Init(sim)
sim.modifier_manager.Insert(grav)
sim.modifier_manager.Enable(grav.label)

data_dumper = netdem.DataDumper()
data_dumper.Init(sim)
data_dumper.SetRootPath("tmp/out_rotate_drum/")
data_dumper.SetSaveByCycles(200)
data_dumper.dump_wall_info = True
data_dumper.dump_mesh = True
data_dumper.dump_shape_info = True
data_dumper.SaveShapeInfoAsSTL()
sim.modifier_manager.Insert(data_dumper)
sim.modifier_manager.Enable(data_dumper.label)

for i in range(20):
    sim.scene.InsertParticle(particle_list)
    sim.Run(0.2)

sim.Run(15.0)
