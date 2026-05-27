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

const int N = 2e5 + 5;
int t, n, k, a[N];

void solve()
{
    scanf("%d", &n);
    
    map<int, int> freq;
    set<int> excl;

    for (int i = 0; i <= n; i++) excl.insert(i);

    for (int i = 1; i <= n; i++)
    {
        scanf("%d", &a[i]);
        freq[a[i]]++;
        excl.erase(a[i]);
    }

    map<int, vector<int>> invfreq;

    for (auto &e: freq)
    {
        invfreq[e.second].push_back(e.first);
    }

    int mex = *excl.begin();
    set<int> vals;

    vals.insert(mex);

    for (int i = 0; i <= n; i++)
    {
        vals.erase(n - i + 1);

        for (auto e: invfreq[i])
        {
            if (e <= min(mex, n - i)) vals.insert(e);
        }

        printf("%d ", vals.size());
    }

    puts("");
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