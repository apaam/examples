1. To run the triaxial compression test:

        ./build/bin/netdem_example_gjk_erosion_issue 1 [out_dir] [use_erosion] [erosion_ratio] > [out_dir/log.txt]

2. To generate random contact configurations:

        ./build/bin/netdem_example_gjk_erosion_issue 2

It will create 1000000 samples of random contact configurations, and save the results to ``local/examples/gjk_erosion_issue/result_data/ev_perf/``. The proctol is discribed in Zhao & Zhao 2019, IJNAME paper. Four types of results, namely 1) EPA contact cases, 2) EPA noncontact cases, 3) GJK-erosion contact cases, and 4) GJK-erosion noncontact cases.