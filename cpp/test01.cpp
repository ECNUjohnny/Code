#include <iostream>
#include <algorithm>
#include <cstring>
#include <queue>
#include <unordered_map>
#include <unordered_set>
#include <map>
#include <set>
#include <vector>
#include <bitset>
#include <cmath>

using namespace std;
typedef long long ll;

int t, a[66], tot;
ll s, m, ans, u;

ll num(ll u)
{
    ll ret = 0;

    for (int i = 0; i <= 63; i++)
    {
        if ((u >> i) & 1) ret += (ll)1 << a[i]; 
    }

    return ret;
}

int main()
{
    scanf("%d", &t);
    
    while (t--)
    {
        scanf("%lld%lld", &s, &m);
        ans = 0;
        
        if ((s & 1) && !(m & 1))
        {
            puts("-1");
            continue;
        }

        memset(a, 0, sizeof(a));
        tot = -1;
        
        for (int i = 0; i <= 63; i++) if ((m >> i) & 1) a[++tot] = i;
        for (int i = 0; i <= tot; i++) u += 1 << i;

        //for (int i = 0; i <= tot; i++) printf("%d ", a[i]);
        //puts("");

        int flag = 0;
        while (s)
        {
            ll l = 0, r = u;

            while (l < r)
            {
                ll mid = l + r + 1 >> 1;
                ll c = num(mid);
                if (c <= s) l = mid;
                else r = mid - 1;
            }

            if (!l)
            {
                flag = 1;
                break;
            }

            printf("%d\n", num(l));
            ans += s / num(l);
            s %= num(l);
        }

        if (flag) puts("-1");
        else printf("%d\n", ans);
    }

    return 0;
}