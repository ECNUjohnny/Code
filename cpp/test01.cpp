#include <iostream>
#include <algorithm>
#include <cstring>
#include <queue>
#include <unordered_map>
#include <unordered_set>
#include <vector>
#include <bitset>
#include <cmath>

using namespace std;
typedef long long ll;

const int N = 3005;
double eps = 1e-9;
int t, n, tot, d1[N], d2[N];
struct func
{
    int a, b, c;
} f[N];

vector<int> p[N], q[N];

bool cmp(func a, func b)
{
    if (a.a > b.a) return 0;
    else if (a.a == b.a) return a.b == b.b && b.c > a.c;
    else
    {
        int d = a.a - b.a;
        int e = a.b - b.b;
        int f = a.c - b.c;
        return e * e - 4 * d * f < 0;
    }
}

int main()
{
    scanf("%d", &t);

    while (t--)
    {
        scanf("%d", &n);
        for (int i = 1; i <= n; i++) scanf("%d%d%d", &f[i].a, &f[i].b, &f[i].c);
    
        for (int i = 1; i <= n; i++)
        {
            for (int j = 1; j <= n; j++)
            {
                if (cmp(f[i], f[j]))
                {
                    
                }
            }
        }
    }

    return 0;
}