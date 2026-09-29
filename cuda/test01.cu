#include "./common/book.h"
#include "./common/cpu_bitmap.h"


struct cuComplex
{
    float a, b;
    __device__ cuComplex( float a, float b ): a{a}, b{b} {}
    __device__ float magnitude()
    {
        return a * a + b * b;
    }

    __device__ cuComplex& operator += ( cuComplex &o )
    {
        this -> a += o.a;
        this -> b += o.b;
        return *this;
    }

    __device__ cuComplex operator + ( cuComplex &o )
    {
        return cuComplex(a + o.a, b + o.b);
    }

    __device__ cuComplex operator * ( cuComplex &o )
    {
        return cuComplex(a * o.a - b * o.b, a * o.b + b * o.a);
    }
};

const int DIM = 512;

__device__ int julia( int x, int y )
{
    float scale = 1.5;
    float jx = (float)(DIM / 2 - x) / (DIM / 2) * scale;
    float jy = (float)(DIM / 2 - y) / (DIM / 2) * scale;

    cuComplex c(-0.8, 0.156);
    cuComplex a(jx, jy);

    for ( int i = 0; i < 200; i++ )
    {
        a = a * a + c;
        if ( a.magnitude() > 1000 )
        {
            return 0;
        }
    }

    return 1;
}

__global__ void kernel( unsigned char *ptr )
{
    int x = blockIdx.x;
    int y = blockIdx.y;
    int offset = y * gridDim.x + x;

    ptr[(offset << 2) + 0] = julia(x, y) * 255;
    ptr[(offset << 2) + 1] = 0;
    ptr[(offset << 2) + 2] = 0;
    ptr[(offset << 2) + 3] = 255;
}



int main()
{
    CPUBitmap bitmap(DIM, DIM);
    unsigned char *dev_bitmap;

    HANDLE_ERROR(cudaMalloc( (void**)&dev_bitmap, bitmap.image_size()));

    dim3 grid( DIM, DIM );
    kernel<<<grid, 1>>>( dev_bitmap );

    HANDLE_ERROR(cudaMemcpy( bitmap.get_ptr(), dev_bitmap, bitmap.image_size(), cudaMemcpyDeviceToHost ));

    bitmap.display_and_exit();

    return 0;
}

