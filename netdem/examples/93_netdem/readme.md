The general energy-conserving contact theory (by Feng 2021, CMAME) and volume-based contact model is used as the benchmark results (i.e., the truth). By default, the dataset and ann models will be saved in ``local/example/netdem/ann_models/trimesh_plane/``, where ``trimesh_plane`` indicate the pair of shape templates.

0. To generate dataset:

        ./build/bin/netdem_example_netdem 0 10000000

The number ``1000000`` indicate the number of samples to be generated. The dataset will be saved in as ``dataset_detection.txt`` and ``dataset_resolution.txt``.

1. To test the dataset:

        ./build/bin/netdem_example_netdem 1 

It will print the contact status and geometric features (data vs truth) onto the screen.

2. To train the classifer

        ./build/bin/netdem_example_netdem 2

By default, it will use the dataset in file ``archived/dataset_detection.txt``. One can rename the dataset generated in step 1 to obtain the default dataset for ANN training. After taining, the classifier model is saved to ``ann_classifier.xml``

1. To test the classifier 

        ./build/bin/netdem_example_netdem 3

It will use the dataset in file ``dataset_detection.txt`` and the classifier model in file ``ann_classifier.xml``. The results of prediction and truth will be printed onto the screen. 

1. To train the regressor

        ./build/bin/netdem_example_netdem 4

By default, it will use the dataset in file ``archived/dataset_resolution.txt``. One can rename the dataset generated in step 1 to obtain the default dataset for ANN training. After taining, the regressor model is saved to ``ann_regressor.xml``

1. To test the regressor 

        ./build/bin/netdem_example_netdem 5

It will use the dataset in file ``dataset_resolution.txt`` and the regressor model in file ``ann_regressor.xml``. The results of prediction and truth will be printed onto the screen. 

1. To test the ANN-based contact solver:

        ./build/bin/netdem_example_netdem 6

It will random 100 cases of contact configurations and output the results of prediction and truth onto the screen. 

