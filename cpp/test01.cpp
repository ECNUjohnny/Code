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
typedef long long ll;
typedef unsigned long long ull;

const int N = 2e5 + 5;
int t, n, q, a[N], b[N];
ull h1[N], h2[N], p[N], h[N];

ull get(int l, int r, ull h[])
{
    return h[r] - h[l - 1] * p[r - l + 1];
}

void solve()
{
    scanf("%d%d", &n, &q);

    for (int i = 1; i <= n; i++) scanf("%d", &a[i]), b[i] = b[i - 1] + a[i];

    for (int i = 1; i <= q; i++)
    {
        int l, r;
        scanf("%d%d", &l, &r);

        if ((r - l + 1) % 3 || (b[r] - b[l - 1]) % 3)
        {
            puts("-1");
            continue;
        }

        if (get(l, r, h) == get(1, r - l + 1, h1) || get(l, r, h) == get(1, r - l + 1, h2))
        {
            int num_1 = b[r] - b[l - 1];
            int num_0 = r - l + 1 - num_1;
            printf("%d\n", 2 * min(num_1, num_0) / 3 + max(num_1, num_0) / 3);
        }
        else
        {
            printf("%d\n", (r - l + 1) / 3);
        }
    }
}

int main() 
{
    scanf("%d", &t);
    
    p[0] = 1;
    for (int i = 1; i < N; i++)
    {
        p[i] = p[i - 1] * 131;
        h1[i] = h1[i - 1] * 131 + (i & 1);
        h2[i] = h2[i - 1] * 131 + !(i & 1);
    }

    while (t--)
    {
        solve();   
    }

    return 0;
}