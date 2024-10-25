#!/bin/sh

mkdir local/potential_models/triaxial_comp_sphere_sdf_x1_2p5/
./build/bin/netdem_example_potential_models \
  96 1.0 0.3 2.0e5 local/potential_models/triaxial_comp_sphere_sdf_x1_2p5/ > \
  local/potential_models/triaxial_comp_sphere_sdf_x1_2p5/log.txt

mkdir local/potential_models/triaxial_comp_sphere_sdf_x0p1_2p5/
./build/bin/netdem_example_potential_models \
  96 0.1 0.3 2.0e5 local/potential_models/triaxial_comp_sphere_sdf_x0p1_2p5/ > \
  local/potential_models/triaxial_comp_sphere_sdf_x0p1_2p5/log.txt

mkdir local/potential_models/triaxial_comp_sphere_sdf_x10_2p5/
./build/bin/netdem_example_potential_models \
  96 10.0 0.3 2.0e5 local/potential_models/triaxial_comp_sphere_sdf_x10_2p5/ > \
  local/potential_models/triaxial_comp_sphere_sdf_x10_2p5/log.txt

mkdir local/potential_models/triaxial_comp_sphere_geom_x1_2p5/
./build/bin/netdem_example_potential_models \
  97 1.0 0.3 2.0e5 local/potential_models/triaxial_comp_sphere_geom_x1_2p5/ > \
  local/potential_models/triaxial_comp_sphere_geom_x1_2p5/log.txt

mkdir local/potential_models/triaxial_comp_sphere_geom_x0p1_2p5/
./build/bin/netdem_example_potential_models \
  97 0.1 0.3 2.0e5 local/potential_models/triaxial_comp_sphere_geom_x0p1_2p5/ > \
  local/potential_models/triaxial_comp_sphere_geom_x0p1_2p5/log.txt

mkdir local/potential_models/triaxial_comp_sphere_geom_x10_2p5/
./build/bin/netdem_example_potential_models \
  97 10.0 0.3 2.0e5 local/potential_models/triaxial_comp_sphere_geom_x10_2p5/ > \
  local/potential_models/triaxial_comp_sphere_geom_x10_2p5/log.txt

