#!/bin/sh

# linear
for i in $(seq 1 9); do
  ./build/bin/netdem_example_potential_models 6 0 1000 0.$i
  mv local/potential_models/size_effect/sphere_linear.txt \
    local/potential_models/size_effect/sphere_linear_0p$i.txt
done

./build/bin/netdem_example_potential_models 6 0 1000 1.0
mv local/potential_models/size_effect/sphere_linear.txt \
  local/potential_models/size_effect/sphere_linear_1p0.txt

# hertz
for i in $(seq 1 9); do
  ./build/bin/netdem_example_potential_models 6 1 1000 0.$i
  mv local/potential_models/size_effect/sphere_hertz.txt \
    local/potential_models/size_effect/sphere_hertz_0p$i.txt
done

./build/bin/netdem_example_potential_models 6 1 1000 1.0
mv local/potential_models/size_effect/sphere_hertz.txt \
  local/potential_models/size_effect/sphere_hertz_1p0.txt
