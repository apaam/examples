#!/bin/sh

# ./build/bin/netdem_example_potential_models 0 0 1000
#    mv local/potential_models/contact_test/sphere_linear.txt \
#       local/potential_models/contact_test/sphere_linear_c20.txt

# # sphere
# for i in $(seq 0 9); do
#    ./build/bin/netdem_example_potential_models 0 0 1000
#    mv local/potential_models/contact_test/sphere_linear.txt \
#       local/potential_models/contact_test/sphere_linear_0$i.txt
# done

# for i in $(seq 0 9); do
#    ./build/bin/netdem_example_potential_models 0 1 1000
#    mv local/potential_models/contact_test/sphere_hertz.txt \
#       local/potential_models/contact_test/sphere_hertz_0$i.txt
# done

# for i in $(seq 500 500 2000); do
#    ./build/bin/netdem_example_potential_models 0 0 $i
#    mv local/potential_models/contact_test/sphere_linear.txt \
#       local/potential_models/contact_test/sphere_linear_n$i.txt
# done

# for i in $(seq 500 500 2000); do
#    ./build/bin/netdem_example_potential_models 0 1 $i
#    mv local/potential_models/contact_test/sphere_hertz.txt \
#       local/potential_models/contact_test/sphere_hertz_n$i.txt
# done

# # star-shaped
# for i in $(seq 0 9); do
#    ./build/bin/netdem_example_potential_models 1 0 1000
#    mv local/potential_models/contact_test/trimesh_linear.txt \
#       local/potential_models/contact_test/trimesh_linear_0$i.txt
# done

# for i in $(seq 0 9); do
#    ./build/bin/netdem_example_potential_models 1 1 1000
#    mv local/potential_models/contact_test/trimesh_hertz.txt \
#       local/potential_models/contact_test/trimesh_hertz_0$i.txt
# done

# for i in $(seq 500 500 2000); do
#    ./build/bin/netdem_example_potential_models 1 0 $i
#    mv local/potential_models/contact_test/trimesh_linear.txt \
#       local/potential_models/contact_test/trimesh_linear_n$i.txt
# done

# for i in $(seq 500 500 2000); do
#    ./build/bin/netdem_example_potential_models 1 1 $i
#    mv local/potential_models/contact_test/trimesh_hertz.txt \
#       local/potential_models/contact_test/trimesh_hertz_n$i.txt
# done

# # other particles
# for i in $(seq 500 500 2000); do
#   ./build/bin/netdem_example_potential_models 1 0 $i
#   mv local/potential_models/contact_test/trimesh_linear.txt \
#     local/potential_models/contact_test/mms_05_linear_n$i.txt
#   cp local/potential_models/contact_test/p1.stl \
#     local/potential_models/contact_test/mms_05.stl
# done

# for i in $(seq 500 500 2000); do
#   ./build/bin/netdem_example_potential_models 1 1 $i
#   mv local/potential_models/contact_test/trimesh_hertz.txt \
#     local/potential_models/contact_test/mms_05_hertz_n$i.txt
# done
