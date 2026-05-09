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

const int N = 1e5 + 5;
int t, n, a[N], b[N];

int check()
{
    int vis = 1;

    for (int i = 2; i <= n; i++) vis += b[i];

    for (int i = 1; i <= n; i++)
    {
        if (a[i] != vis) return 0;
        vis -= 1;
        vis += !b[i];
    }

    return 1;
}

int main()
{
    scanf("%d", &t);

    while (t--)
    {
        scanf("%d", &n);
        for (int i = 1; i <= n; i++) scanf("%d", &a[i]);
    
        int flg = 1;

        for (int i = 2; i <= n; i++)
        {
            if (abs(a[i] - a[i - 1]) > 1)
            {
                flg = 0;
                break;
            }
        }

        if (!flg)
        {
            printf("%d\n", 0);
            continue;
        }

        int ans = 0;

        b[1] = 0;

        flg = 1;

        for (int i = 2; i <= n; i++)
        {
            if (a[i] == a[i - 1]) b[i] = !b[i - 1];
            else if (a[i] > a[i - 1])
            {
                if (b[i - 1])
                {
                    flg = 0;
                    break;
                }
                else b[i] = 0;
            }
            else if (a[i] < a[i - 1])
            {
                if (!b[i - 1])
                {
                    flg = 0;
                    break;
                }
                else b[i] = 1;
            }
        }

        if (flg) ans += check();

        flg = 1;

        b[1] = 1;

        for (int i = 2; i <= n; i++)
        {
            if (a[i] == a[i - 1]) b[i] = !b[i - 1];
            else if (a[i] > a[i - 1])
            {
                if (b[i - 1])
                {
                    flg = 0;
                    break;
                }
                else b[i] = 0;
            }
            else if (a[i] < a[i - 1])
            {
                if (!b[i - 1])
                {
                    flg = 0;
                    break;
                }
                else b[i] = 1;
            }
        }

        if (flg) ans += check();

        printf("%d\n", ans);
    }

    return 0;
}