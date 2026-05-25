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
int t, n, k, a[N], b[N];

void solve()
{
    scanf("%d%d", &n, &k);  
    for (int i = 1; i <= n; i++) scanf("%d", &a[i]);
    for (int i = 1; i <= n; i++) scanf("%d", &b[i]);

    ll ans = 0;

    int flg_a = 0, flg_b = 0;
    for (int i = 1; i < n; i++) if (a[i + 1] < a[i]) {flg_a = 1; break;}
    for (int i = 1; i < n; i++) if (b[i + 1] < b[i]) {flg_b = 1; break;}

    if (flg_a || flg_b)
    {
        for (int i = 1; i <= n; i++) ans += abs(a[i] - b[i]);
        printf("%lld\n", ans);
        return;
    }

    
}

int main() 
{
    scanf("%d", &t);

    while (t--)
    {
        solve();
    }
}