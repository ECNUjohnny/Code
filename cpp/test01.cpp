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

const int N = 2e5 + 5;
int t, n;
ll h, k, a[N], b[N];

int main()
{
    scanf("%d", &t);

    while (t--)
    {
        scanf("%d%lld%lld", &n, &h, &k);
        
        ll sum = 0, ans = 0;
        
        for (int i = 1; i <= n; i++)
        {
            scanf("%lld", &a[i]);
            sum += a[i];
            b[i] = a[i] + b[i - 1];
        }

        ans += (n + k) * (h / sum);
        h %= sum;

        int i;
        for (i = 1; i <= n; i++)
        {
            if (b[i] <= h && h < b[i + 1]) break;
        }

        int min_i = min_element(a + 1, a + i + 1) - a;
        int max_i = max_element(a + i, a + n + 1) - a;

        if (a[max_i] > a[min_i])
        {
            
        }
    }
}