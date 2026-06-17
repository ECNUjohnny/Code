#include <iostream>
#include <cstring>
#include <algorithm>
#include <cmath>
#include <vector>
#include <unordered_map>
#include <unordered_set>
#include <set>
#include <queue>

using namespace std;

const int N = 6005;
int t, n, a[N], cnt[N], c[2][N], b[N];

vector<pair<int, int>> v[N];

int ask(int l, int r, int op)
{
    int ans = -2e9;

    while (l <= r)
    {
        ans = op ? max(ans, a[r--]) : max(ans, b[r--]);
        for (; r - r & -r >= l; r -= r & -r) ans = max(ans, c[op][r]);
    }

    return ans;
}

void add(int x, int y, int op)
{
    for (; x <= n; x += x & -x) c[op][x] = max(c[op][x], y);
}

int check()
{
    int flg = 0;

    for (int i = 1; i <= n; i++)
    {
        if (!cnt[i]) continue;

        if (cnt[i] != 1) return 0;

        if (!flg) flg = 1;
        else return 0;

        int j;
        for (j = i; j < n && cnt[j + 1] == 1; j++);
        
        i = j;
    }

    return flg;
}

void solve()
{
    scanf("%d", &n);
    for (int i = 1; i <= n; i++) scanf("%d", &a[i]), v[i].clear(), cnt[i] = 0, b[i] = -a[i];

    memset(c[0], 0, sizeof(c[0]));
    memset(c[1], 0, sizeof(c[1]));

    for (int i = 1; i <= n; i++) 
    {
        add(i, a[i], 1);
        add(i, b[i], 0);
    }

    // puts("1");

    for (int len = 1; len <= n; len++)
    {
        for (int l = 1; l < 1 + len - 1; l++) cnt[a[l]]++;
        
        for (int l = 1; l + len - 1 <= n; l++)
        {
            int r = l + len - 1;
            cnt[a[r]]++;

            if (check()) v[len].push_back({l, r});
        
            cnt[a[l]]--;
        }
    }

    int ans = 0;

    for (int i = n; i; i--)
    {
        for (int j = 0; j < v[i].size(); j++)
        {
            for (int k = j + 1; k < v[i].size(); k++)
            {
                auto p = v[i][j], q = v[i][k];

                int max_p = ask(p.first, p.second, 1);
                int max_q = ask(q.first, q.second, 1);
                int min_p = -ask(p.first, p.second, 0);
                int min_q = -ask(q.first, q.second, 0);

                if (max_p == min_q - 1 || min_p == max_q + 1)
                {
                    if (p.first >= q.second || q.first >= p.second)
                    {
                        printf("%d\n", i);
                        return;
                    } 
                }
            }
        }
    }

    puts("0");

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