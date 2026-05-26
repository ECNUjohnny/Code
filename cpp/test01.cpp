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

const int N = 1e5 + 5;
int t, n, p[N], s[N];

int gcd(int a, int b)
{
    return b ? gcd(b, a % b) : a;
}

void solve()
{
    scanf("%d", &n);
    
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