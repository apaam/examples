import netdem

netdem.omp_set_num_threads(1)

cylinder = netdem.Cylinder(0.025, 0.1)
cylinder_stl = cylinder.GetSTLModel(200)

num_p = 10

[vt_nodes, vt_cells, vt_seeds] = netdem.Voronoi.Solve(
    cylinder_stl, num_p, 1000, 1.0e-3, 1
)

netdem.Voronoi.SaveAsVTK(
    "tmp/tests/voronoi_cylinder.vtk", vt_nodes, vt_cells, vt_seeds
)

eq_size = pow(0.025 * 0.025 * 0.1 * 0.2 / num_p * 6.0, 1.0 / 3.0)

stl_ref = netdem.STLModel()
stl_ref.InitFromSTL("tmp/lin2022/shapes/ballast3_8.stl")
stl_ref.SetSize(eq_size)

stl_template = netdem.STLModel()
for i in range(8):
    stl_template.InitFromSTL(
        "tmp/lin2022/shapes/ballast3_" + str(i + 1) + ".stl"
    )
    stl_template.SetSize(eq_size)
    print(stl_template.GetVolume() / 3.1415926 / 0.025 / 0.025 / 0.1)

    stl_model = netdem.STLModel()

    for j in range(num_p):
        stl_tmp = netdem.STLModel(stl_template.vertices, stl_template.facets)
        stl_voro = netdem.STLModel(vt_nodes, vt_cells[j])
        stl_tmp.CopyPoseDev(stl_voro, stl_ref)

        stl_tmp.SaveAsSTL(
            "tmp/lin2022/specimen/ballast3_"
            + str(i + 1)
            + "_"
            + str(j + 1)
            + ".stl"
        )

        stl_model.MergeSTLModel(stl_tmp)

    stl_model.SaveAsSTL("tmp/lin2022/specimen/ballast3_" + str(i + 1) + ".stl")
