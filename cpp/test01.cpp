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

    if (k == 1)
    {
        puts("yes");
        return;
    }

    memcpy(b, a, sizeof(a));

    sort(b + 1, b + n + 1);

    int kth = b[k];
    int tot = 0;

    for (int i = 1; i <= n; i++)
    {
        if (a[i] > kth) continue;
        b[++tot] = a[i];
    }

    int l = 1, r = tot;
    int sum = 0;

    while (l < r)
    {
        if (b[l] == b[r])
        {
            r++, l--;
            continue;
        }
        else
        {
            if (b[l] != kth && b[r] != kth)
            {
                puts("no");
                return;
            } 
            else if (b[l] == kth)
            {
                l++;
                sum++;
            }
            else if (b[r] == kth)
            {
                r--;
                sum++;
            }
            
            if (sum > tot - k + 1)
            {
                puts("no");
                return;
            }
        }

    }

    puts("yes");
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