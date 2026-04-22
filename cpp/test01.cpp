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
int t, n, ans, fa[N], d[N];
vector<int> g[N];

void dfs(int a, int c)
{
    fa[a] = c;

    for (int b: g[a])
    {
        if (b == c) continue;
        dfs(b, a);
    }
}

void bfs()
{
    queue<int> q;

    q.push(1);
    d[1] = 0;

    while (q.size())
    {
        int dep = d[q.front()], sum = 0, flag = 0;

        while (d[q.front()] == dep)
        {
            int a = q.front();
            flag++;
            q.pop();

            for (int b: g[a])
            {

            }
        }
    }
}

int main()
{
    scanf("%d", &t);
    
    while (t--)
    {
        scanf("%d", &n);
        for (int i = 1; i <= n; i++) g[i].clear(), fa[i] = i, d[i] = -1;
        ans = 0;

        for (int i = 1; i < n; i++)
        {
            int a, b;
            scanf("%d%d", &a, &b);
            g[a].push_back(b);
            g[b].push_back(a);
        }


    }

    return 0;
}