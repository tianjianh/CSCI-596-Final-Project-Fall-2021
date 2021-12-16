CSCI-596-Final-Project-Fall-2021

Tianjian Huang, Yue (Julien) Yu


We compare Intel's MKL (Math Kernel Library), Apple's Accelerate, and OpenBLAS (Basic Linear Algebra Subprograms).

The conclusions are shown as graphs and are briefly explained as follow:


For the multiplication of two n by n matrices:

• With either 32-bit or 64-bit floating point, GFLOPS converges when n reaches the magnitude of 10e3. Accelerate has slightly lower GFLOPS than the other two.

• When MKL, Accelerate and OpenBLAS are compared across various benchmarks, we notice the following:

    • For easier tasks (special, stats, and even inverse), Accelerate is the fastest.
    
    • For matrix decomposition (SVD, QR), MKL is faster than Accelerate, and OpenBLAS is the slowest.
    
    • For eigenvalue decomposition (i.e., the hardest benchmark), MKL is faster than OpenBLAS, and Accelerate is far slower than the other two.
    
    • MKL's performance dominates that of OpenBLAS.
