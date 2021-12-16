from tqdm import tqdm
from time import time, sleep
import numpy as np
import os
import argparse

parser = argparse.ArgumentParser()

parser.add_argument('--runs', type=int, default=10)
args = parser.parse_args()



size_list = []
tflops_list = {
    "single": [],
    "double": [],
}

def get_tflops(size, iterations, dtype):
    print(size, dtype)
    A, B = np.random.random((size, size)), np.random.random((size, size))
    if dtype == "single":
        A, B = A.astype(np.float32), B.astype(np.float32)
    elif dtype == "double":
        A, B = A.astype(np.float64), B.astype(np.float64)
    else:
        print("Unknown dtype", dtype, "using system default")
    
    np.matmul(A, B)
    st = time()
    for i in range(1):
        np.matmul(A, B)
    et = time()
    overhead = et-st
    sleep(2.0)
    st = time()
    for i in range(iterations+1):
        np.matmul(A, B)
    et = time()
    duration = et-st
    if duration < 3:
        extend_ratio = 3/duration
        new_iterations = int(extend_ratio*iterations)
        print("new_iterations", new_iterations)
        st = time()
        for i in range(new_iterations+1):
            np.matmul(A, B)
        et = time()
        duration = et-st - overhead
        fps = new_iterations/duration
    else:
        duration -= overhead
        fps = iterations/duration
    matmul_flops = 2 * (size**3)
    TFLOPS = fps*matmul_flops/(1e12)
    size_list.append(size)
    tflops_list[dtype].append(TFLOPS)

for size in tqdm([128, 256, 512, 1024, 2048, 4096, 8192]):
    get_tflops(size, iterations=args.runs, dtype="single")

print(tflops_list)

for size in tqdm([128, 256, 512, 1024, 2048, 4096, 8192]):
    get_tflops(size, iterations=args.runs, dtype="double")

print(tflops_list)



