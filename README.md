# CSCI-596 Fall 2021 Project

This project is done by Tianjian Huang and Yue (Julien) Yu. In this project, we compare the performance of several off-the-shelf Basic Linear Algebra Subprograms (BLAS): Intel Math Kernel Library ([MKL](https://www.intel.com/content/www/us/en/developer/tools/oneapi/onemkl.html)), Apple [Accelerate](https://developer.apple.com/documentation/accelerate), and Basic Linear Algebra Subprograms ([OpenBLAS](https://www.openblas.net/)). BLAS provides common linear algebra operations, such as vector addition, scalar multiplication, dot products, linear combinations, and matrix multiplication. They are no doubt the fundamental building blocks of modern numerical software and machine learning as well. We start from the most basic General Matrix Multiply (GEMM) and move to complicated operations such as matrix factorization. We try to give some performance recommendations and also try to analysis what happened behind the scenes.

## Numpy Benchmarks

We build numpy against three BLAS libraries and perform the following tests:

### GEMM Flops

We use Matmul which is the most fundamental linear algebra operation to measure the GFlops of each BLAS library. The tests have been conducted in FP32 and FP64.

| FP64 | FP32 | 
| ---- | ---- |
| ![](images/NumPy_MatMul_FP64.jpg) | ![](images/NumPy_MatMul_FP32.jpg) |

### Other Linear Algebra Operations


Time taken for each operation is reported; lower is better. Each operation has been run for 8 times and the average time is reported.

| Task       | MKL | Accelerate | OpenBLAS |
| :---------- | :----------: | :-----: | :-----: |
| datagen    | 0.731 | 0.703 | 0.722 |
| special    | 0.710 | 0.446 | 0.707 |
| stats      | 1.721 | 1.306 | 1.683 |
| matmul     | 0.898 | 0.843 | 0.860 |
| svd        | 0.384 | 0.506 | 1.204 |
| cholesky   | 0.109 | 0.088 | 0.206 |
| eigendecomp| 3.668 | 6.450 | 4.226 |
| inverse    | 0.270 | 0.251 | 0.345 |
| qr         | 0.393 | 0.530 | 0.783 |


| NumPy Linear Algebra Performance|
| -------- |
| ![](images/Numpy_Other.jpg) |


### Some observations:

* For GEMM:
It seems that all BLAS library leverage all the potential of the CPU when the matrix size is large (All BLAS library take advantage of AVX-512).

* For other linear algebra operations:

	* For sequential operations dominated tasks such as datagen, special functions and stats, all BLAS work the same.
	* For complicated tasks, in particular SVD decomposition, MKL is far better compared with Accelerate and OpenBLAS.

These observations are expected since we are using Intel CPU and the BLAS provided by Intel could better leverage the hardware. Without any doubt, it is a good idea to stick to MKL if on Intel CPU.

### Vtune Profiler Analysis:

In the next section, we try to use Intel Vtune Profiler to find out why MKL is much better than OpenBLAS in SVD. 

| Vtune MKL|
| -------- |
| ![](images/mkl_vtune.PNG) |

| VTune OpenBLAS|
| -------- |
| ![](images/openblas_vtune.PNG) |

The images above suggest that both BLAS are very good parallel programs which have more than 80% effective CPU Utilization. Also both BLAS take advantage of the modern SIMD instructions (AVX-512). However, it can be seen that the bottleneck of OpenBLAS compared with MKL is at the Memory Bound. In particular, we can see 100.0% LLC Miss from OpenBLAS. The reason behind this might be that OpenBLAS uses a cache-unfriendly memory access pattern, making CPU stall and wait for data from the slower main memory.
