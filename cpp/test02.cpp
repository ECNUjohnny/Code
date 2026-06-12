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

const int N = 2e4 + 5;

int n, m, k, ans;

int he[N], ne[N], to[N], ed[N], tot;
int sz[N], max_sz, v[N], d[N], wc, sum_sz, dd[N];

void add(int a, int b, int c)
{
    to[++tot] = b, ed[tot] = c;
    ne[tot] = he[a], he[a] = tot;
}

int get_sz(int a, int fa)
{
    int sz = 1;
    
    for (int i = he[a]; i; i = ne[i])
    {
        int b = to[i];
        if (b == fa || v[b]) continue;

        sz += get_sz(b, a);
    }

    return sz;
}

void get_dep(int a, int fa, int dis)
{
    d[++d[0]] = dis;
    
    for (int i = he[a]; i; i = ne[i])
    {
        int b = to[i];
        if (b == fa || v[b]) continue;

        get_dep(b, a, dis + ed[i]);
    }
}

void get_wc(int a, int fa)
{
    sz[a] = 1;
    int max_lef = -1;

    for (int i = he[a]; i; i = ne[i])
    {
        int b = to[i];
        if (b == fa || v[b]) continue;

        get_wc(b, a);
        sz[a] += sz[b];

        max_lef = max(max_lef, sz[b]);
    }

    max_lef = max(max_lef, sum_sz - sz[a]);

    if (max_lef > max_sz)
    {
        wc = a;
        max_sz = max_lef;
    }
}

int calc(int a)
{
    int ans = 0;
    d[0] = 1;
    d[1] = 0;

    for (int i = he[a]; i; i = ne[i])
    {
        int b = to[i];
        if (v[b]) continue;
    
        int beg = d[0];
        get_dep(b, a, ed[i]);

        sort(d + beg + 1, d + d[0] + 1);

        for (int l = 1, r = d[0]; l <= beg && r > beg; )
        {
            if (d[l] + d[r] <= k) ans += r - beg, l++;
            else r--;
        }

        int len = 0, k = 1, j = beg + 1;

        for (int p = 1; p <= d[0]; p++)
        {
            if (d[k] <= d[j] || j > d[0]) dd[p] = d[k++];
            else dd[p] = d[j++];
        }

        memcpy(d, dd, sizeof(dd));
    }

    return ans;
}

void solve(int a)
{
    v[a] = 1;
    ans += calc(a);

    for (int i = he[a]; i; i = ne[i])
    {
        int b = to[i];
        if (v[b]) continue;

        sum_sz = get_sz(b, a);
        get_wc(b, a);

        solve(wc);
    }
}

int main()
{
    
}