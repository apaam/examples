#!/bin/sh

# ./build/bin/netdem_example_netdem 2 > \
#   local/examples/netdem/ann_models/trimesh_plane/log_classifier.txt

# ./build/bin/netdem_example_netdem 4 > \
#   local/examples/netdem/ann_models/trimesh_plane/log_regressor.txt

./build/bin/netdem_example_netdem 12 > \
  local/examples/netdem/ann_models/trimesh_trimesh/log_classifier.txt

./build/bin/netdem_example_netdem 14 > \
  local/examples/netdem/ann_models/trimesh_trimesh/log_regressor.txt

# ./build/bin/netdem_example_netdem 22 > \
#   local/examples/netdem/ann_models/ellipsoid_plane/log_classifier.txt

# ./build/bin/netdem_example_netdem 24 > \
#   local/examples/netdem/ann_models/ellipsoid_plane/log_regressor.txt

# ./build/bin/netdem_example_netdem 32 > \
#   local/examples/netdem/ann_models/ellipsoid_ellipsoid/log_classifier.txt

# ./build/bin/netdem_example_netdem 34 > \
#   local/examples/netdem/ann_models/ellipsoid_ellipsoid/log_regressor.txt
