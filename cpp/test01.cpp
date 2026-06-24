#include <iostream>
#include <cstring>
#include <vector>
#include <algorithm>
#include <unordered_map>
#include <unordered_set>
#include <string>
#include <cmath>
#include <set>
#include <map>
#include <queue>

using namespace std;
typedef long long ll;
typedef unsigned long long ull;

const ll mod = 1e9 + 7;
const int N = 1e6 + 5;

int t, a, b, x;
int t, n;

void solve()
{
    scanf("%d%d%d", &a, &b, &x);

    if (a < b) swap(a, b);

    int cnt = 2e9;

    vector<int> a_x, b_x;

    for (; a; a /= x) a_x.push_back(a);
    for (; b; b /= x) b_x.push_back(b);

    a_x.push_back(0);
    b_x.push_back(0);

    for (int i = 0; i < a_x.size(); i++)
    {
        for (int j = 0; j < b_x.size(); j++)
        {
            cnt = min(cnt, abs(a_x[i] - b_x[j]) + i + j);
        }
    }

    printf("%d\n", cnt);
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