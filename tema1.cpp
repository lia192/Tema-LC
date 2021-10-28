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

// Data structure to store a binary tree node
struct Node
{
    char data;
    Node *left, *right;

    Node(char data)
    {
        this->data = data;
        this->left = this->right = nullptr;
    }
};

struct Trunk
{
    Trunk *prev;
    string str;

    Trunk(Trunk *prev, string str)
    {
        this->prev = prev;
        this->str = str;
    }
};

// Helper function to print branches of the binary tree
void showTrunks(Trunk *p)
{
    if (p == nullptr) {
        return;
    }

    showTrunks(p->prev);
    cout << p->str;
}

// Recursive function to print a binary tree.
// It uses the inorder traversal.
void printTree(Node* root, Trunk *prev, bool isLeft)
{
    if (root == nullptr) {
        return;
    }

    string prev_str = "    ";
    Trunk *trunk = new Trunk(prev, prev_str);

    printTree(root->right, trunk, true);

    if (!prev) {
        trunk->str = "---";
    }
    else if (isLeft)
    {
        trunk->str = ".---";
        prev_str = "   |";
    }
    else {
        trunk->str = "`---";
        prev->str = prev_str;
    }

    showTrunks(trunk);
    cout << root->data << endl;

    if (prev) {
        prev->str = prev_str;
    }
    trunk->str = "   |";

    printTree(root->left, trunk, false);
}

int n, m;
string s;
set<char> O, op;

Node* root;
int frst = 1;

int rec(Node* &root, string s, int l, int r){

    if(l == r){
        if(s[l] >= 'A' && s[l] <= 'Z'){
            root = new Node(s[l]);
            return 1;
        }
        return 0;
    }
    if(s[l] != '(' || s[r] != ')'){
        return 0;
    }
    if((O.find(s[l + 1]) != O.end()) && (op.find(s[l + 1]) == op.end()) && (s[r - 1] >= 'A') && (s[r - 1] <= 'Z') && (r - l + 1 == 4)){
        root = new Node('n');
        root->left = new Node(s[r - 1]);
        return 1;
    }
    if((O.find(s[l + 1]) != O.end()) && (op.find(s[l + 1]) == op.end())){
        root = new Node('n');
        return rec(root->left, s, l + 2, r - 1);
    }
    int now = 0;
    for(int i = l + 1; i < r; i++){
        if(s[i] == '(')now++;
        if(s[i] == ')')now--;
        if((O.find(s[i]) != O.end()) && !now){
            root = new Node('r');
            return (rec(root->left, s, l + 1, i - 1) && rec(root->right, s, i + 1, r - 1));
        }
    }
    return 0;
}

void solve(){

    cout << "Introduceti expresia : " << endl;

    string g;
    getline(cin, g);

    cout << "Introduceti semnul negatiei : " << endl;
    string c;
    cin >> c;

    for(auto it : g){
        if(it == ' ')continue;
        s += it;
    }


    for(auto it : s){
        if(it == ' ' || it == ')' || it == '(')continue;
        if((it >= 'A') && (it <= 'Z'))continue;
        O.insert(it);
        if(it == c[0])continue;
        op.insert(it);
    }

    n = sz(s);
    s = '.' + s;

    if(rec(root, s, 1, n)){
        cout << "Este o formula propozitionala" << '\n';
        // print constructed binary tree
        printTree(root, nullptr, false);
        cout << " r - conector binar" << endl;
        cout << " n - negatie" << endl;
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
