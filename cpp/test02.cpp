#include <iostream>
#include <cstring>
#include <vector>
#include <algorithm>
#include <unordered_map>
#include <unordered_set>
#include <cmath>
#include <set>
#include <map>
#include <queue>

using namespace std;


template<class T>
class UniquePtr
{



};

class MyUniquePtr
{

public:
    MyUniquePtr(int elem_int): elem_int{elem_int}, idx{1} {}
    MyUniquePtr(long long elem_llong): elem_llong{elem_llong}, idx{2} {}
    MyUniquePtr(double elem_double): elem_double{elem_double}, idx{3} {}
    MyUniquePtr(): idx{0} {}

    MyUniquePtr(const MyUniquePtr &o)
    {
        idx = o.idx;
        
        switch(idx)
        {
        case 1:
            elem_int = o.elem_int;
            break;
            
        case 2:
            elem_llong = o.elem_llong;
            break;

        case 3:
            elem_double = o.elem_double;
            break;


        }           

    }

    ~MyUniquePtr()
    {
        idx = 0;
    }

    MyUniquePtr operator+= (const MyUniquePtr &o)
    {
        
        if (o.idx != idx)
        {
            throw "Type Different!";   
        }

        switch(o.idx)
        {
        case 1:
            elem_int += o.elem_int;
            break;
        
        case 2:
            elem_llong += o.elem_llong;
            break;

        case 3:
            elem_double += o.elem_double;
            break;

        }
    
        MyUniquePtr a(*this);
        
        return a;
    }

private:
    int idx;
    int elem_int;
    long long elem_llong;
    double elem_double;

};

int main()
{
    
}