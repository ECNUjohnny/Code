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

int t;
ll k, f[20], g[20];

void solve()
{
    scanf("%lld", &k);

    ll ans = 0;

    while (k)
    {
        ll dig = 0, m = 1;

        for (; m <= 16; m++)
        {
            if (dig + g[m] > k) break;
            dig += g[m];
        }

        ll r = (k - dig) / m;

        for (int i = 1; i < m; i++) ans += f[i];

        k = r;
    }

    

}

int main() 
{
    scanf("%d", &t);

    for (ll i = 1; i <= 16; i++)
    {
        ll p = pow(10, i - 1);

        for (ll j = 1; j <= 9; j++) f[i] += p * j * f[i - 1];
    
        g[i] = p * 9 * i;
    }
    
    while (t--)
    {
        solve();
    }

    return 0;
}