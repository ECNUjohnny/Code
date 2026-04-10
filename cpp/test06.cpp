#include <bits/stdc++.h>

using namespace std;

const int N = 6e6 + 5;
int n, d1[N], d2[N], d3[N], d4[N], y[N], dis;

int random(int s, int e)
{
    double ratio = (double)rand() / RAND_MAX;
    if (e > s) return s + (unsigned long long)((e - s) * ratio);
    else return e;
}

void init()
{
    for (int i = 0; i < n * 2; i++)
    {
        d1[i] = d2[i] = d3[i] = d4[i] = 0;
    }
}

void change(int a, int b, int flag)
{
    d1[y[a] + a]--;
    d1[y[b] + b]--;
    d2[y[a] - a + n - 1]--;
    d2[y[b] - b + n - 1]--;
    if (!flag)
    {
        d3[y[a] + a]--;
        d4[y[a] - a + n - 1]--;
    }
    
    swap(y[a], y[b]);

    d1[y[a] + a]++;
    d1[y[b] + b]++;
    d2[y[a] - a + n - 1]++;
    d2[y[b] - b + n - 1]++;

    if (flag & 1)
    {
        d3[y[a] + a]++;
        d4[y[a] - a + n - 1]++;
    }
}

void first()
{
    init();
    for (int i = 0; i < n; i++)
    {
        y[i] = i;
        d1[y[i] + i]++;
        d2[y[i] - i + n - 1]++;
    }

    int j = 0;
    for (int test = 0; j < n && test < n * 4; test++)
    {
        int k = random(j, n);
        change(j, k, 1);
        if (d3[y[j] + j] > 1 || d4[y[j] - j + n - 1] > 1) change(j, k, 0);
        else j++;
    }

    for (int i = j; i < n; i++)
    {
        int k = random(i, n);
        change(i, k, 2);
    }
    dis = n - j;
}

void final()
{
    for (int i = n - dis - 1; i < n; i++)
    {
        int time = 0;
        int b;
        if (d2[y[i] - i + n - 1] > 1 || d1[y[i] + i] > 1)
        {
            do
            {
                int j = random(0, n);
                time++;
                change(i, j, 2);
                int col1 = (d2[y[i] - i + n - 1] > 1) || (d1[y[i] + i] > 1);
                int col2 = (d2[y[j] - j + n - 1] > 1) || (d1[y[j] + j] > 1);
                b = col1 || col2;
                if (b) change(i, j, 2);
                if (time > 10000)
                {
                    first();
                    i = n - dis - 1;
                    break;
                }
            }
            while (b);
        }
    }
}

int main()
{
    scanf("%d", &n);
    if (n == 1) 
    {
        puts("0");
        return 0;
    }
    srand(time(NULL));
    
    first();
    if (dis > 0) final();

    for (int i = 0; i < n; i++) printf("%d\n", y[i]);
}
