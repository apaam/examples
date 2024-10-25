import sys
import os
import numpy
from numpy import cos, sin

dir_path = os.path.dirname(os.path.realpath(__file__))
sys.path.append(dir_path + "/../../build/lib/")

import netdem

netdem.omp_set_num_threads(1)

# import the box
stl_box = netdem.STLModel()
stl_box.InitFromSTL("data/box.stl")

# scale
angle = 0
angle_rad = angle / 3.1415926 * 180
quat = (cos(0.5 * angle_rad), sin(0.5 * angle_rad), 0, 0)
stl_box.Rotate(quat)

scale = 2.0
tmp_vertices = stl_box.vertices
for i in range(len(tmp_vertices)):
    tmp_vertices[i][2] = tmp_vertices[i][2] / scale
stl_box.vertices = tmp_vertices

# voronoi
num_p = 100

[vt_nodes, vt_cells, vt_seeds] = netdem.Voronoi.Solve(
    stl_box, num_p, 1000, 1.0e-3, 1
)

for i in range(len(vt_nodes)):
    vt_nodes[i][2] = vt_nodes[i][2] * scale

for i in range(len(vt_seeds)):
    vt_seeds[i][2] = vt_nodes[i][2] * scale

netdem.Voronoi.SaveAsVTK(
    "local/lin2022_v2/voronoi_box.vtk", vt_nodes, vt_cells, vt_seeds
)

# insert particles
solid_frac = 0.05
eq_size = pow(solid_frac / num_p * 6.0 / 3.1415926, 1.0 / 3.0)

stl_ref = netdem.STLModel()
stl_ref.InitFromSTL("local/lin2022_v2/shapes/rocks/ballast_1.stl")
stl_ref.Standardize()
stl_ref.SetSize(eq_size)

num_divs = 50  # number of divisions in each dimension for voxelization
voxel_values = numpy.zeros((num_divs, num_divs, num_divs), dtype=numpy.int8)

stl_template = netdem.STLModel()
for i in range(1):
    stl_template.InitFromSTL(
        "local/lin2022_v2/shapes/rocks/ballast_" + str(i + 1) + ".stl"
    )
    stl_template.Decimate(200)
    stl_template.Standardize()
    stl_template.SetSize(eq_size)
    print(stl_template.GetVolume() * num_p)

    stl_model = netdem.STLModel()

    for j in range(num_p):
        stl_tmp = netdem.STLModel(stl_template.vertices, stl_template.facets)
        stl_voro = netdem.STLModel(vt_nodes, vt_cells[j])
        stl_tmp.CopyPoseDev(stl_voro, stl_ref)

        quat = (cos(-0.5 * angle_rad), sin(-0.5 * angle_rad), 0, 0)
        stl_tmp.Rotate(quat)

        # save individual stl
        # stl_tmp.SaveAsSTL("local/lin2022_v2/specimen/ballast_" +
        #                   str(i + 1) + "_" + str(j + 1) + ".stl")

        stl_model.MergeSTLModel(stl_tmp)

        # discretization
        trimesh_tmp = netdem.TriMesh()
        trimesh_tmp.InitFromSTL(stl_tmp)

        for ii in range(num_divs):
            for jj in range(num_divs):
                for kk in range(num_divs):
                    pos = [
                        (ii + 0.5) / num_divs - 0.5,
                        (jj + 0.5) / num_divs - 0.5,
                        (kk + 0.5) / num_divs - 0.5,
                    ]
                    if trimesh_tmp.CheckEnclose(pos):
                        voxel_values[ii, jj, kk] = 1

        print("finished particle " + str(j))

    stl_model.SaveAsSTL(
        "local/lin2022_v2/specimen/ballast_"
        + str(i + 1)
        + "_r"
        + str(angle)
        + ".stl"
    )

    hf = open(
        "local/lin2022_v2/specimen/ballast_"
        + str(i + 1)
        + "_r"
        + str(angle)
        + ".txt",
        "w",
    )
    for ii in range(num_divs):
        for jj in range(num_divs):
            for kk in range(num_divs):
                hf.write(str(voxel_values[ii, jj, kk]))
                hf.write(" ")
            hf.write("\n")
        hf.write("\n")

    hf.close()

    tecplot_filename = (
        "local/lin2022_v2/specimen/ballast_"
        + str(i + 1)
        + "_r"
        + str(angle)
        + ".dat"
    )
    hf = open(tecplot_filename, "w")
    hf.write('variables="x","y","z","is_solid"\n')
    hf.write(
        'zone t="box"i='
        + str(num_divs)
        + ",j="
        + str(num_divs)
        + ",k="
        + str(num_divs)
        + ",f=point\n"
    )
    for ii in range(num_divs):
        for jj in range(num_divs):
            for kk in range(num_divs):
                hf.write(str((ii + 0.5) / num_divs - 0.5))
                hf.write(" ")
                hf.write(str((jj + 0.5) / num_divs - 0.5))
                hf.write(" ")
                hf.write(str((kk + 0.5) / num_divs - 0.5))
                hf.write(" ")
                hf.write(str(voxel_values[ii, jj, kk]))
                hf.write(" ")
                hf.write("\n")

    hf.close()
    print("data saved to: " + tecplot_filename)
