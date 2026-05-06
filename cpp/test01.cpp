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
int t, n, a[3][N];
vector<pair<int, int>> pos[N << 1];

void add(int a, set<int> st[])
{
    for (auto [i, j]: pos[a]) st[i].erase(j);
}

void del(int a, set<int> st[])
{
    for (auto [i, j]: pos[a]) st[i].insert(j);
}

int check(set<int> st[])
{
    if (st[0].count(1)) return 0;
    if (st[1].count(n)) return 0;
    if (*st[0].begin() - 1 <= *st[1].rbegin()) return 0;

    return 1;
}

int main()
{
    scanf("%d", &t);

    while (t--)
    {
        scanf("%d", &n);
        for (int i = 1; i <= n; i++) scanf("%d", &a[1][i]);
        for (int i = 1; i <= n; i++) scanf("%d", &a[2][i]);
        for (int i = 1; i <= n << 1; i++) pos[i].clear();

        ll ans = 0;

        set<int> st[2];

        for (int i = 1; i <= 2; i++)
        {
            for (int j = 1; j <= n; j++) pos[a[i][j]].push_back({i, j});
        }

        for (int i = 1; i <= n; i++) st[0].insert(1), st[1].insert(1);


    }

    return 0;
}