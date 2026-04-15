#include <iostream>
#include <algorithm>
#include <cstring>
#include <queue>
#include <unordered_map>
#include <unordered_set>
#include <vector>
#include <bitset>
#include <cmath>

using namespace std;
typedef long long ll;

const int N = 505, M = 1e4 + 5;
int n, m, p[M], f[M], ans = -1;

struct box
{
    int c, e;
} b[N];

int main()
{
    scanf("%d%d", &m, &n);
    for (int i = 1; i <= m; i++) scanf("%d", &p[i]);
    for (int i = 1; i <= n; i++)
    {
        scanf("%d%d", &b[i].c, &b[i].e);
        if (b[i].c > m) b[i].c = m;
    }

    sort(p + 1, p + m + 1);
    reverse(p + 1, p + m + 1);

    memset(f, 0x3f, sizeof(f));
    f[0] = 0;

    for (int i = 2; i <= m; i++) p[i] += p[i - 1];
    for (int i = 1; i <= n; i++)
    {
        for (int j = m; j; j--)
        {
            f[j] = min(f[j], f[max(0, j - b[i].c)] + b[i].e);
        }
    }

    for (int i = 0; i <= m; i++) ans = max(ans, p[i] - f[i]);

    printf("%d\n", ans);

    return 0;
}