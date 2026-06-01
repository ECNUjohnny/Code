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
int t, n, k, x, a[N];

struct inter
{
    int d, len, t, m, l, r;
    bool operator < (const inter &o) const
    {
        if (d == o.d) return t < o.t;
        return d < o.d;
    }
};
<<<<<<< Updated upstream
=======
const ll mod = 998244353;

int t;
>>>>>>> Stashed changes

void solve()
{
    scanf("%d%d%d", &n, &k, &x);
    for (int i = 1; i <= n; i++) scanf("%d", &a[i]);

    sort(a + 1, a + n + 1);

    priority_queue<inter> q;

    for (int i = 1; i < n; i++) q.push({a[i + 1] - a[i], a[i + 1] - a[i], 1, 0, a[i], a[i + 1]});
    if (a[1] > 0) q.push({a[1], a[1], 2, 0, 0, a[1]});
    if (a[n] < x) q.push({x - a[n], x - a[n], 3, 0, a[n], x});

    for (int i = 1; i <= k; i++)
    {
        inter p = q.top();
        q.pop();

        if (p.t == 1)
        {
            q.push({max((p.len - p.m) >> 1, 0), p.len, 1, p.m + 1, p.l, p.r});
        }
        else
        {
            q.push({max(p.len - p.m - 1, 0), p.len, p.t, p.m + 1, p.l, p.r});
        }
    }

    while (q.size())
    {
        inter p = q.top();
        q.pop();

        if (p.t == 1)
        {
            int start = p.l + p.d;
            for (int i = 1; i <= p.m; i++) printf("%d ", start + i);
        }
        else if (p.t == 2)
        {
            for (int i = 1; i <= p.m; i++) printf("%d ", i - 1);
        }
        else
        {
            for (int i = 1; i <= p.m; i++) printf("%d ", x - i + 1);
        }
    }

    puts("");
}

int main() 
{
    scanf("%d", &t);

    

    // printf("%lld\n", c[1][13]);

    while (t--)
    {
        solve();
    }

    return 0;
}