#!/bin/sh

mkdir local/potential_models/rockfall/

for i in $(seq 0 9); do
  surface_num=1000
  ./build/bin/netdem_example_potential_models 93 \
    0 1.0e4 ${surface_num} local/potential_models/rockfall/tmp/ > \
    local/potential_models/rockfall/log.txt
  rm -rf local/potential_models/rockfall/linear_kne4_${surface_num}_0$i
  mv local/potential_models/rockfall/tmp \
    local/potential_models/rockfall/linear_kne4_${surface_num}_0$i
done

for i in $(seq 0 9); do
  surface_num=2000
  ./build/bin/netdem_example_potential_models 93 \
    0 1.0e4 ${surface_num} local/potential_models/rockfall/tmp/ > \
    local/potential_models/rockfall/log.txt
  rm -rf local/potential_models/rockfall/linear_kne4_${surface_num}_0$i
  mv local/potential_models/rockfall/tmp \
    local/potential_models/rockfall/linear_kne4_${surface_num}_0$i
done

for i in $(seq 0 9); do
  surface_num=1000
  ./build/bin/netdem_example_potential_models 93 \
    0 1.0e5 ${surface_num} local/potential_models/rockfall/tmp/ > \
    local/potential_models/rockfall/log.txt
  rm -rf local/potential_models/rockfall/linear_kne5_${surface_num}_0$i
  mv local/potential_models/rockfall/tmp \
    local/potential_models/rockfall/linear_kne5_${surface_num}_0$i
done

for i in $(seq 0 9); do
  surface_num=2000
  ./build/bin/netdem_example_potential_models 93 \
    0 1.0e5 ${surface_num} local/potential_models/rockfall/tmp/ > \
    local/potential_models/rockfall/log.txt
  rm -rf local/potential_models/rockfall/linear_kne5_${surface_num}_0$i
  mv local/potential_models/rockfall/tmp \
    local/potential_models/rockfall/linear_kne5_${surface_num}_0$i
done

# for i in $(seq 0 1); do
#   surface_num=1000
#   ./build/bin/netdem_example_potential_models 93 \
#     0 1.0e6 ${surface_num} local/potential_models/rockfall/tmp/ > \
#     local/potential_models/rockfall/log.txt
#   rm -rf local/potential_models/rockfall/linear_kne6_${surface_num}_0$i
#   mv local/potential_models/rockfall/tmp \
#     local/potential_models/rockfall/linear_kne6_${surface_num}_0$i
# done

# for i in $(seq 0 1); do
#   surface_num=2000
#   ./build/bin/netdem_example_potential_models 93 \
#     0 1.0e6 ${surface_num} local/potential_models/rockfall/tmp/ > \
#     local/potential_models/rockfall/log.txt
#   rm -rf local/potential_models/rockfall/linear_kne6_${surface_num}_0$i
#   mv local/potential_models/rockfall/tmp \
#     local/potential_models/rockfall/linear_kne6_${surface_num}_0$i
# done

# for i in $(seq 0 0); do
#   surface_num=1000
#   ./build/bin/netdem_example_potential_models 93 \
#     0 1.0e7 ${surface_num} local/potential_models/rockfall/tmp/ > \
#     local/potential_models/rockfall/log.txt
#   rm -rf local/potential_models/rockfall/linear_kne7_${surface_num}_0$i
#   mv local/potential_models/rockfall/tmp \
#     local/potential_models/rockfall/linear_kne7_${surface_num}_0$i
# done

# for i in $(seq 0 0); do
#   surface_num=2000
#   ./build/bin/netdem_example_potential_models 93 \
#     0 1.0e7 ${surface_num} local/potential_models/rockfall/tmp/ > \
#     local/potential_models/rockfall/log.txt
#   rm -rf local/potential_models/rockfall/linear_kne7_${surface_num}_0$i
#   mv local/potential_models/rockfall/tmp \
#     local/potential_models/rockfall/linear_kne7_${surface_num}_0$i
# done
