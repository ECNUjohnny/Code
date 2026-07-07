#include <iostream>
#include <cstring>
#include <algorithm>
#include <map>
#include <set>
#include <unordered_map>
#include <unordered_set>
#include <bitset>
#include <stdio.h>
#include <vector>
#include <queue>

using namespace std;

const int N = 105;

int a[N], b[N], c[N];
int *dev_a, *dev_b, *dev_c;

__global__ void add(int a[], int b[], int c[], int n)
{
    int tid = blockIdx.x;
    if (tid <= n) c[tid] = a[tid] + b[tid];
}

int main()
{
    cudaMalloc(&dev_a, sizeof(int) * N);    
    cudaMalloc(&dev_b, sizeof(int) * N);    
    cudaMalloc(&dev_c, sizeof(int) * N);    

    for (int i = 1; i <= N; i++)
    {
        a[i] = -i;
        b[i] = i * i;
    }

    cudaMemcpy(dev_a, a, sizeof(int) * N, cudaMemcpyHostToDevice);
    cudaMemcpy(dev_b, b, sizeof(int) * N, cudaMemcpyHostToDevice);

    add<<<N, 1>>>(dev_a, dev_b, dev_c, N);

    cudaMemcpy(c, dev_c, sizeof(int) * N, cudaMemcpyDeviceToHost);
 
    cudaFree(dev_a);
    cudaFree(dev_b);
    cudaFree(dev_c);

    for (int i = 1; i <= N; i++)
    {
        printf("%d + %d = %d\n", a[i], b[i], c[i]);
    }

    return 0;
}