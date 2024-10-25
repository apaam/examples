import netdem
import math


def genWireNet(
    cell_width, cell_height, num_layers_w, num_layers_h, cell_top_angle
):
    num_total_nodes = (num_layers_w + 1) * 2 + (
        4 * num_layers_w + 2
    ) * num_layers_h

    pos_list = [[0 for col in range(3)] for row in range(num_total_nodes)]

    bind_height = cell_height - cell_width / math.tan(
        cell_top_angle / 2.0 / 180.0 * math.pi
    )
    net_width = cell_width * num_layers_w
    net_height = (cell_height + bind_height) * num_layers_h + bind_height

    id = 0
    cur_height = 0.5 * net_height
    for col in range(num_layers_w + 1):
        pos_list[id] = [-0.5 * net_width + col * cell_width, cur_height, 0]
        id = id + 1

    for row in range(num_layers_h):
        cur_height = cur_height - bind_height
        for col in range(num_layers_w + 1):
            pos_list[id] = [-0.5 * net_width + col * cell_width, cur_height, 0]
            id = id + 1

        cur_height = cur_height - 0.5 * (cell_height - bind_height)
        for col in range(num_layers_w):
            pos_list[id] = [
                -0.5 * net_width + (col + 0.5) * cell_width,
                cur_height,
                0,
            ]
            id = id + 1

        cur_height = cur_height - bind_height
        for col in range(num_layers_w):
            pos_list[id] = [
                -0.5 * net_width + (col + 0.5) * cell_width,
                cur_height,
                0,
            ]
            id = id + 1

        cur_height = cur_height - 0.5 * (cell_height - bind_height)
        for col in range(num_layers_w + 1):
            pos_list[id] = [-0.5 * net_width + col * cell_width, cur_height, 0]
            id = id + 1

    cur_height = -0.5 * net_height
    for col in range(num_layers_w + 1):
        pos_list[id] = [-0.5 * net_width + col * cell_width, cur_height, 0]
        id = id + 1

    return (pos_list, net_width, net_height)


# # simulation settings
sim = netdem.Simulation()
sim.domain_manager.SetBound(-16, -16, -16, 16, 16, 16)
sim.domain_manager.SetCellSpacing(0.6, 0.6, 0.6)

cnt_model = netdem.LinearSpring(2.0e6, 1.0e6, 0.5, 0.7)
cnt_model_ptr = sim.scene.InsertContactModel(cnt_model)
sim.scene.SetNumberOfMaterials(1)
sim.scene.SetCollisionModel(0, 0, cnt_model_ptr)

bond_model = netdem.ParallelBond(1.0e6, 1.0e6, 1.0e16, 1.0e16, 0.7)
bond_model.label = "bond_model"
bond_model_ptr = sim.scene.InsertContactModel(bond_model)
sim.scene.SetBondModel(0, 0, bond_model_ptr)

# create particles and walls
tri_mesh = netdem.TriMesh()
tri_mesh.InitFromSTL("data/particle_template.stl")
tri_mesh.Decimate(200)
tri_mesh.MakeConvex()
tri_mesh.AlignAxes()
tri_mesh.SetSize(0.2)
tri_mesh_ptr = sim.scene.InsertShape(tri_mesh)
p = netdem.Particle()
p.SetShape(tri_mesh_ptr)
p.SetPosition(0, 0, 0.3)
sim.scene.InsertParticle(p)

bonded_spheres = netdem.BondedSpheres()
bonded_spheres.SetBondModel(bond_model_ptr)
bonded_spheres.SetBondMargin(0.05)
[pos_list, net_weight, net_height] = genWireNet(0.1, 0.1, 10, 5, 120)
for pos_row in pos_list:
    bonded_spheres.AddSphere(pos_row[0], pos_row[1], pos_row[2], 0.02)
bonded_spheres.InitBonds()
for p in bonded_spheres.particle_list:
    p.SetMargin(0.1)
    p.SetDensity(7600)
# bonded_spheres.RotateByRodrigues(math.pi / 2, 1, 0, 0)
# bonded_spheres.Translate(0, 0, -0.5)
sim.scene.InsertParticle(bonded_spheres)

motion_control = netdem.ParticleMotionControl()
motion_control.Init(sim)
for p in sim.scene.particle_list:
    if (
        abs(p.pos[0] + 0.5 * net_weight) < 0.02
        or abs(p.pos[0] - 0.5 * net_weight) < 0.02
        or abs(p.pos[1] + 0.5 * net_height) < 0.02
        or abs(p.pos[1] - 0.5 * net_height) < 0.02
    ):
        motion_control.SetFixed(p.id)
motion_control.SyncToAllProcessors()
sim.modifier_manager.Insert(motion_control)
sim.modifier_manager.Enable(motion_control.label)

plane = netdem.Plane(0, 0, -0.5, 0, 0, 1)
plane_ptr = sim.scene.InsertShape(plane)
wall = netdem.Wall(plane_ptr)
sim.scene.InsertWall(wall)

# gravity
grav = netdem.Gravity()
grav.Init(sim)
sim.modifier_manager.Insert(grav)
sim.modifier_manager.Enable(grav.label)

# save results
data_dumper = netdem.DataDumper()
data_dumper.Init(sim)
data_dumper.SetRootPath("tmp/out/")
data_dumper.SetSaveByTime(0.01)
data_dumper.SaveShapeInfoAsSTL()
data_dumper.dump_shape_info = True
data_dumper.dump_wall_info = True
data_dumper.dump_contact_info = True
data_dumper.dump_mesh = True
data_dumper.dump_read_restart = True
data_dumper.SetSaveReadRestartByTime(0.1)
sim.modifier_manager.Insert(data_dumper)
sim.modifier_manager.Enable(data_dumper.label)

# run the simulation
sim.dem_solver.timestep = 1.0e-6
sim.Run(2.0)
