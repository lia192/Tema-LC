#include<bits/stdc++.h> //:3
using namespace std;
typedef long long LL;
#define all(a) (a).begin(), (a).end()
#define ff first
#define ss second
#define pb push_back
#define pi pair<int, int>
#define sz(x) (int)((x).size())
//#define int long long
/*
#define cin in
#define cout out

ifstream in(".in");
ofstream out(".out");
*/


const int dx[] = {0, 1, 0, -1};
const int dy[] = {1, 0, -1, 0};

const LL inf = 2e9;
const int INF = 0x3f3f3f3f;
const LL mod = 1e9 + 7;
const int N = 2e6 + 11;
const LL INF64 = 3e18 + 1;
const double eps = 1e-14;
const double PI = acos(-1);

int n, m;
string s;
set<char> O;

int rec(string s, int l, int r){

    if(l == r){
        if(s[l] >= 'A' && s[l] <= 'Z')return 1;
        return 0;
    }
    if(s[l] != '(' || s[r] != ')'){
        return 0;
    }
    if((O.find(s[l + 1]) != O.end()) && (s[l + 1] != '?') && (s[r - 1] >= 'A') && (s[r - 1] <= 'Z') && (r - l + 1 == 4)){
        return 1;
    }
    if((O.find(s[l + 1]) != O.end()) && (s[l + 1] != '?')){
        return rec(s, l + 2, r - 1);
    }
    int now = 0;
    for(int i = l + 1; i < r; i++){
        if(s[i] == '(')now++;
        if(s[i] == ')')now--;
        if((O.find(s[i]) != O.end()) && !now){
            return (rec(s, l + 1, i - 1) && rec(s, i + 1, r - 1));
        }
    }
    return 0;
}

void solve(){

    string g;
    getline(cin, g);

    for(auto it : g){
        if(it == ' ')continue;
        s += it;
    }

    for(auto it : s){
        if(it == ' ' || it == ')' || it == '(')continue;
        if((it >= 'A') && (it <= 'Z'))continue;
        O.insert(it);
    }

    n = sz(s);
    s = '.' + s;

    if(rec(s, 1, n)){
        cout << "Este o formula propozitionala" << '\n';
        return;
    }

    cout << "Nu este o formula propozitionala" << '\n';

}

//(((P⇒Q)∨S)⇔T)
//(A^B)
//((P⇒(Q∧(S⇒T))))
//(¬(B(¬Q))∧R)
//(P∧((¬Q)∧(¬(¬(Q⇔(¬R))))))
//((P∨Q)⇒¬(P∨Q))∧(P∨(¬(¬Q)))
//(P⇒((Q∧A)⇒(S⇒T)))

int32_t main(){
ios_base :: sync_with_stdio(0); cin.tie(0); cout.tie(0);

    //cout << setprecision(3) << fixed;

    int T = 1;
    //cin >> T;
    while(T--){
        solve();
    }
}
