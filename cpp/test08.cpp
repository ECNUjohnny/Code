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

const int N = 105;

struct TreeNode {
    int val;
    TreeNode *l;
    TreeNode *r;
    TreeNode(int x) : val(x), l(0), r(0) {}
};


void inverse(TreeNode *x)
{
    if (!x || x -> l == x -> r) return;

    TreeNode *temp = x -> l;
    x -> l = x -> r;
    x -> r = temp;

    temp = 0;

    inverse(x -> l);
    inverse(x -> r);
}

void print(TreeNode *x)
{
    if (!x) return;

    printf("%d\n", x -> val);

    print(x -> l);
    print(x -> r);
}

TreeNode *t;

void init()
{
    t = new TreeNode(4);
    t -> l = new TreeNode(2);
    t -> r = new TreeNode(7);

    t -> l -> l = new TreeNode(1);
    t -> l -> r = new TreeNode(3);
    t -> r -> l = new TreeNode(6);
    t -> r -> r = new TreeNode(9);
}


int main()
{
    init();
    inverse(t);
    print(t);
}