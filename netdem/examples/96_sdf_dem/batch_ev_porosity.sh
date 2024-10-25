#!/bin/sh 

# # eta 0.4 ~ 0.9
# for i in $(seq 0 5); do
#   echo $i
#   ./build/bin/netdem_tool_packing_porosity \
#     tmp/examples/sdf_dem/packing/eta_v2_$i/particle/particle_000_000000000050000.vtk \
#     2650 -0.5 -0.5 -0.5 0.5 0.5 0.2
# done

# ./build/bin/netdem_tool_packing_porosity \
#     tmp/examples/sdf_dem/packing/zeta_6/particle/particle_000_000000000050000.vtk \
#     2650 -0.5 -0.5 -0.5 0.5 0.5 0.2

# # eta 1/0.9 ~ 1/0.4
# for i in $(seq 5 -1 0); do
#   echo $i
#   ./build/bin/netdem_tool_packing_porosity \
#     tmp/examples/sdf_dem/packing/eta_v1_$i/particle/particle_000_000000000050000.vtk \
#     2650 -0.5 -0.5 -0.5 0.5 0.5 0.2
# done

# # zeta 0.4 ~ 1.4
# for i in $(seq 0 10); do
#   echo $i
#   ./build/bin/netdem_tool_packing_porosity \
#     tmp/examples/sdf_dem/packing/zeta_$i/particle/particle_000_000000000050000.vtk \
#     2650 -0.5 -0.5 -0.5 0.5 0.5 0.1
# done