#!/bin/sh 

# # eta 0.4 - 0.9
# for i in $(seq 0 5); do
#   scp lzhshou@143.89.247.159:~/Documents/lzhshou/myProjects/apaam/netdem/tmp/examples/sdf_dem/packing/eta_v1_$i/particle/particle_000_000000000050000.vtk \
#     tmp/examples/sdf_dem/packing/eta_v1_$i/particle/
#   scp lzhshou@143.89.247.159:~/Documents/lzhshou/myProjects/apaam/netdem/tmp/examples/sdf_dem/packing/eta_v1_$i/shape/shape_0000000000.stl \
#     tmp/examples/sdf_dem/packing/eta_v1_$i/shape/      
# done

# # eta 1/0.4 - 1/0.9
# for i in $(seq 0 5); do
#   scp lzhshou@143.89.247.159:~/Documents/lzhshou/myProjects/apaam/netdem/tmp/examples/sdf_dem/packing/eta_v2_$i/particle/particle_000_000000000050000.vtk \
#     tmp/examples/sdf_dem/packing/eta_v2_$i/particle/
#   scp lzhshou@143.89.247.159:~/Documents/lzhshou/myProjects/apaam/netdem/tmp/examples/sdf_dem/packing/eta_v2_$i/shape/shape_0000000000.stl \
#     tmp/examples/sdf_dem/packing/eta_v2_$i/shape/      
# done

# # zeta 0.4 - 1.4
# for i in $(seq 0 10); do
#   scp lzhshou@143.89.247.159:~/Documents/lzhshou/myProjects/apaam/netdem/tmp/examples/sdf_dem/packing/zeta_$i/particle/particle_000_000000000050000.vtk \
#     tmp/examples/sdf_dem/packing/zeta_$i/particle/
#   scp lzhshou@143.89.247.159:~/Documents/lzhshou/myProjects/apaam/netdem/tmp/examples/sdf_dem/packing/zeta_$i/shape/shape_0000000000.stl \
#     tmp/examples/sdf_dem/packing/zeta_$i/shape/      
# done

# # eta 0.4 - 0.9
# for i in $(seq 0 5); do
#   ./scripts/auto_mesh_particle.sh tmp/examples/sdf_dem/packing/eta_v1_$i/
# done

# # eta 1/0.4 - 1/0.9
# for i in $(seq 0 5); do
#   ./scripts/auto_mesh_particle.sh tmp/examples/sdf_dem/packing/eta_v2_$i/      
# done

# # zeta 0.4 - 1.4
# for i in $(seq 0 10); do
#   ./scripts/auto_mesh_particle.sh tmp/examples/sdf_dem/packing/zeta_$i/      
# done