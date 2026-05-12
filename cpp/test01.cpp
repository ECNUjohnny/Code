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

const int N = 2e5 + 5;
int t, n;
ll a[N];

void solve()
{
    scanf("%d", &n);
    for (int i = 1; i <= n; i++) scanf("%lld", &a[i]);

    map<ll, int> mp;
    ll ans = 0, line = 0;

    for (int i = 1; i <= n; i++) mp[a[i]]++;

    for (auto it = mp.begin(); it != mp.end(); )
    {
        if (it -> second == 1)
        {
            it++;
            continue;
        }

        else if (it -> second & 1)
        {
            ans += it -> first * (it -> second - 1);
            line += it -> second - 1;
            it -> second = 1;
            it++;
        }

        else
        {
            ans += it -> first * (it -> second);
            line += it -> second;
            it = mp.erase(it);
        }
    }

    auto it = mp.lower_bound(ans);

    if (line == 2 && it == mp.begin()) puts("0");
 
    else if (it == mp.begin()) printf("%lld\n", ans);

    else if (it == next(mp.begin())) printf("%lld\n", ans + (*(--it)).first);

    else
    {
        ans += (*(--it)).first;
        ans += (*(--it)).first;
        printf("%lld\n", ans);
    }
}

int main() 
{
    scanf("%d", &t);

    while (t--)
    {
        solve();
    }

    return 0;
}