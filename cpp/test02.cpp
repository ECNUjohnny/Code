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

const int N = 5e5 + 5;
int c[N];
int n, m;

struct seg
{
    int l, r;
    int pos[6], neg[6];
    bool tag[6];

    #define l(p) t[p].l
    #define r(p) t[p].r
    #define pos(p) t[p].pos
    #define neg(p) t[p].neg
    #define tag(p) t[p].tag
} t[N << 2];

void up(int p)
{
    for (int i = 0; i < 6; i++)
    {
        pos(p)[i] = pos(p << 1)[i] + pos(p << 1 | 1)[i];
        neg(p)[i] = neg(p << 1)[i] + neg(p << 1 | 1)[i];
    }
}

void build(int p, int l, int r)
{
    l(p) = l, r(p) = r;

    if (l == r)
    {
        pos(p)[l % 6] = c[l] ? 1 : 0;
        neg(p)[l % 6] = c[l] ? 0 : 1;

        return;
    }

    int mid = l + r >> 1;

    build(p << 1, l, mid);
    build(p << 1 | 1, mid + 1, r);

    up(p);
}

void spread(int p)
{
    for (int i = 0; i < 6; i++)
    {
        if (!tag(p)[i]) continue;

        tag(p << 1)[i] ^= 1;
        tag(p << 1 | 1)[i] ^= 1;

        swap(pos(p << 1)[i], neg(p << 1)[i]);
        swap(pos(p << 1 | 1)[i], neg(p << 1 | 1)[i]);

        tag(p)[i] = 0;
    }
}

void change(int p, int l, int r, int op, int st)
{
    if (l <= l(p) && r(p) <= r)
    {
        if (op == 1)
        {
            for (int i = st % 2; i < 6; i += 2) swap(pos(p)[i], neg(p)[i]), tag(p)[i] ^= 1;
        } 
        else if (op == 2)
        {
            for (int i = st % 3; i < 6; i += 3) swap(pos(p)[i], neg(p)[i]), tag(p)[i] ^= 1;
        }
        else
        {
            for (int i = 0; i < 6; i += 1) swap(pos(p)[i], neg(p)[i]), tag(p)[i] ^= 1;
        }

        return;
    }

    spread(p);

    int mid = l(p) + r(p) >> 1;

    if (l <= mid) change(p << 1, l, r, op, st);
    if (mid < r) change(p << 1 | 1, l, r, op, st);

    up(p);
}

int ask(int p, int l, int r)
{
    if (l <= l(p) && r(p) <= r)
    {
        int sum = 0;
        for (int i = 0; i < 6; i++) sum += pos(p)[i];

        return sum;
    }

    spread(p);

    int mid = l(p) + r(p) >> 1;

    int sum = 0;

    if (l <= mid) sum += ask(p << 1, l, r);
    if (mid < r) sum += ask(p << 1 | 1, l, r);

    return sum;
}

int main()
{
    scanf("%d%d", &n, &m);
    for (int i = 1; i <= n; i++) scanf("%d", &c[i]);

    build(1, 1, n);

    while (m--)
    {
        int a, x, y;
        scanf("%d%d%d", &a, &x, &y);

        if (a < 4) change(1, x, y, a, x);
        else printf("%d\n", ask(1, x, y));
    }

    return 0;
}