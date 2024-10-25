import sys
import os

dir_path = os.path.dirname(os.path.realpath(__file__))
sys.path.append(dir_path + "/../../build/lib/")
import netdem

# units: mm, 1000 kg, N, s
sim = netdem.Simulation()
sim.domain_manager.SetBound(-12, -12, -12, 12, 12, 12)
sim.domain_manager.SetCellSpacing(1.0, 1.0, 1.0)

cnt_model = netdem.LinearSpring(1.4e4, 0.7e4, 0.3, 0.0)
cnt_model_prt = sim.scene.InsertContactModel(cnt_model)
sim.scene.SetNumberOfMaterials(1)
sim.scene.SetCollisionModel(0, 0, cnt_model_prt)

bond_model = netdem.ParallelBond(1.4e4, 0.7e4, 7.0e4, 3.5e4, 0.01)
bond_model.label = "bond_model"
bond_model_ptr = sim.scene.InsertContactModel(bond_model)

bonded_spheres = netdem.BondedSpheres()
bonded_spheres.SetBondModel(bond_model_ptr)
bonded_spheres.InitFromGrid(-2.5, -2.5, -2.5, 5.0, 5.0, 5.0, 0.25)
bonded_spheres.MakePorosity(0.2)
sim.scene.InsertParticle(bonded_spheres)

sim.scene.SetGravity(0, 0, -9.81e-3)
for p in sim.scene.particle_list:
    p.SetDensity(2650)

wall_box = netdem.WallBoxPlane(10, 10, 5.0, 0, 0, 0)
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
data_dumper.SaveShapeInfoAsSTL()
sim.modifier_manager.Insert(data_dumper)
sim.modifier_manager.Enable(data_dumper.label)

# add deformation drived loading for top wall
disp_control = netdem.WallMotionControl()
disp_control.Init(sim)
disp_control.SetWall([5])
disp_control.SetVelocity(0, 0, -0.25)
sim.modifier_manager.Insert(disp_control)
sim.modifier_manager.Enable(disp_control.label)

sim.Run(2.0)
