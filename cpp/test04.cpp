#include<cstdio>
#include<cstring>
#include<algorithm>
using namespace std;
const int N=1e4+10;
inline int mymin(int a,int b) {return a<b?a:b;}
inline int mymax(int a,int b) {return a>b?a:b;}
inline int read()
{
    int x=0;bool f=false;
    char ch=getchar();
    while(ch<'0' || ch>'9') f|=(ch=='-'),ch=getchar();
    while(ch>='0'&&ch<='9') x=x*10+(ch^48),ch=getchar();
    return f?-x:x;
}
int n,k,ans,point;//point为点数 
struct node{int y,d,next;}a[N<<1];int len,last[N];
inline void ins(int x,int y,int d) {a[++len].y=y;a[len].d=d;a[len].next=last[x];last[x]=len;}
/*找到一个点，其所有的子树中最大的子树节点数最少，
那么这个点就是这棵树的重心，删去重心后，生成的多棵树尽可能平衡。*/
int maxx,root,size[N],smax[N];//size->以己为跟的子树大小  smax->最大子树的大小
bool vis[N];//求重心时避免重复访问
void get_root(int x,int fa)
{
    siz[x]=1;smax[x]=0;
    for(int k=last[x];k;k=a[k].next)
    {
        int y=a[k].y;
        if(y==fa || vis[y]) continue;
        get_root(y,x);
        siz[x]+=siz[y];
        smax[x]=mymax(smax[x],siz[y]);
    }
    smax[x]=mymax(smax[x],point-siz[x]);
    minn=mymin(minn,smax[x]);
    root=minn==smax[x]?x:root;
}
int num,dis[N];
void dfs(int x,int fa,int Dis)
{
    for(int k=last[x];k;k=a[k].next)
    {
        int y=a[k].y;
        if(y==fa || vis[y]) continue;
        dis[++num]=Dis+a[k].d;
        dfs(y,x,Dis+a[k].d);
    }
}
int dd[N];
int calc(int x)//计算以x为根的所有情况的答案
{
    int ret=0;
    dis[num=1]=0;
    for(int k=last[x];k;k=a[k].next)
    {
        int y=a[k].y;
        if(vis[y]) continue;
        dis[++num]=a[k].d;
        int st=num;
        dfs(y,x,a[k].d);
        sort(dis+st,dis+num+1);//对这棵子树进行排序，不要和之前的打乱成一坨了
        for(int l=1,r=num;l<st && r>=st;)
        {
            if(dis[l]+dis[r]<=limit) ret+=r-st+1,l++;
            else r--;
        }
        int len=0,i=1,j=st;//因为前面子树的 dis 已经有序，所以直接归并起来即可，用 sort 会 T ！！！
        while(i<st || j<=num)
        {
            if(j>num || (i<st && dis[i]<=dis[j])) dd[++len]=dis[i++];
            else dd[++len]=dis[j++];
        }
        memcpy(dis,dd,sizeof(dis));
    }
    return ret;
}
int ans;
void solve(int x)//求解以x为重心的情况
{
    vis[x]=true;
    ans+=calc(x);
    for(int k=last[x];k;k=a[k].next)
    {
        int y=a[k].y;
        if(vis[y]) continue;
        minn=point=siz[y];
        get_root(y,x);
        solve(root);
    }
}
void clear()
{
    len=0;memset(last,0,sizeof(last));
    memset(vis,false,sizeof(vis));ans=0;
}
int main()
{
    n=read();limit=read();
    while(n || limit)
    {
        clear();
        for(int i=1;i<n;i++)
        {
            int x=read(),y=read(),d=read();
            ins(x,y,d);ins(y,x,d);
        }
        minn=point=n;
        get_root(1,0);
        solve(root);
        printf("%d\n",ans);
        n=read();limit=read();
    }
    return 0;
}
