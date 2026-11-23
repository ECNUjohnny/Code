#include <cstring>
#include <iostream>

int fun(int a[10][10])
{
    printf("%d\n", a[0]);
}

int a[10][10];

int main()
{
    fun(a);
    return 0;
}