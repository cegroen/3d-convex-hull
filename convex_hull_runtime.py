import incremental_hull_3d as ih
import brute_hull_3d as bh
import convex_hull_helper as chh
import time

trials = 10

# testing runtime for the randomized incremental algorithm
for i in range(4, 10000, 500):
    test_points = chh.random_points(i, 10000)
    start = time.time()
    
    for j in range(trials):
        ih.IncrementalHull3D(test_points)
    
    end = time.time() 
    runtime = (end - start) / trials
    print(runtime)
    
# # testing runtime for the randomized incremental algorithm
# for i in range(4, 50, 2):
#     test_points = chh.random_points(i, 1000)
#     start = time.time()
# 
#     for j in range(trials):
#         bh.brute_force_hull_3d(test_points)
# 
#     end = time.time() 
#     runtime = (end - start) / trials
#     print(runtime)
