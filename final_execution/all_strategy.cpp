#include<bits/stdc++.h>
using namespace std;

typedef long long ll;
typedef long double ld;
typedef pair<int,int> pint;
typedef pair<long long,long long> pll;
typedef pair<long double,long double> pld;

typedef vector<int> vi;
typedef vector<vector<int> > vvi;
typedef vector<ll> vl;
typedef vector<vector<ll> > vvl;
typedef vector<ld> vd;
typedef vector<vector<ld> > vvd;

#define PB push_back
#define MP make_pair
#define F first
#define S second
#define fast ios::sync_with_stdio(0);cin.tie(0);cout.tie(0);

bool valid(ll x,ll y,vector<vector<char> > &board){
	ll n=board[0].size();
	bool ans=false;
	if(x>=0 && y>=0 && x<n && y<n && board[x][y]=='.'){
		ans=true;
	}
	return ans;
}

void printboard(vector<vector<char> > &board){
	ll n=board[0].size();
	for (ll i=1;i<2*n;i++){
		cout<<"-";
	}
	cout<<endl;
	for (ll i=0;i<n;i++){
		// cout<<"| ";
		for (ll j=0;j<n;j++){
			cout<<board[i][j]<<" ";
		}
		// cout<<" |";
		cout<<endl;
	}
	for (ll i=1;i<2*n;i++){
		cout<<"-";
	}
	cout<<endl;
}

bool check(vector<vector<char> > &board){
	ll n=board[0].size();
	bool terminated = false;
	for (ll i=0;i<n;i++){
		bool psb=true;
		for (ll j=0;j<n;j++){
			psb=psb&&(board[i][j]=='x');
			if(psb==false){
				break;
			}
		}
		if(psb==true){
			terminated=true;
			break;
		}
	}
	if(terminated==false){
		for (ll j=0;j<n;j++){
			bool psb=true;
			for (ll i=0;i<n;i++){
				psb=psb&&(board[i][j]=='x');
				if(psb==false){
					break;
				}
			}
			if(psb==true){
				terminated=true;
				break;
			}
		}
	}
	if(terminated==false){
		bool psb=true;
		for (ll i=0;i<n;i++){
			psb=psb&&(board[i][i]=='x');
			if(psb==false){
				break;
			}
		}
		if(psb==true){
			terminated=true;
		}
	}
	if(terminated==false){
		bool psb=true;
		for (ll i=0;i<n;i++){
			psb=psb&&(board[i][n-1-i]=='x');
			if(psb==false){
				break;
			}
		}
		if(psb==true){
			terminated=true;
		}
	}
	return terminated;
}

ll xcount(ll i,ll j,vector<vector<char> > &board){
	ll n=board[0].size();
	ll val=0;
	if(board[i][j]=='x'){
		val=val+n*n+1;
	}
	else{
		for (int itr=0;itr<n;itr++){
			if(board[itr][j]=='x'){
				val++;
			}
		}
		for (int itr=0;itr<n;itr++){
			if(board[i][itr]=='x'){
				val++;
			}
		}
		if(i==j){
			for (int itr=0;itr<n;itr++){
				if(board[itr][itr]=='x'){
					val++;
				}
			}
		}
		if(i==n-1-j){
			for (int itr=0;itr<n;itr++){
				if(board[itr][n-1-itr]=='x'){
					val++;
				}
			}
		}
	}
	return val;
}

pll play_greedy(vector<vector<char> > &board){
	ll n=board[0].size();
	vvl xsum(n);
	for (ll i=0;i<n;i++){
		for (ll j=0;j<n;j++){
			xsum[i].PB(-1);
		}
	}
	for (ll i=0;i<n;i++){
		for (ll j=0;j<n;j++){
			ll cnt=xcount(i,j,board); // involve checking of x present or not
			xsum[i][j]=cnt;
		}
	}
	pll greedy_move=MP(-1,-1);
	ll min_cnt=n*n+1;
	for (ll i=0;i<n;i++){
		for (ll j=0;j<n;j++){
			if(xsum[i][j]<min_cnt){
				greedy_move=MP(i,j);
				min_cnt=xsum[i][j];
			}
		}
	}
	return greedy_move;
}

pll play_knight(ll i,ll j,vector<vector<char> > &board){
	ll n=board[0].size();
	bool knight_played=false;
	pll knight_move;
	vector<ll> change;
	for (ll diff=1;diff<=2;diff++){
		change.push_back(diff);
		change.push_back(-1*diff);
	}

	ll l=change.size();
	for (ll itr0=0;itr0<l;itr0++){
		for (ll itr1=0;itr1<l;itr1++){
			ll x_new=i+change[itr0];
			ll y_new=j+change[itr1];
			if(abs(change[itr0])!=abs(change[itr1]) && valid(x_new,y_new,board)){
				knight_played=true;
				knight_move=MP(x_new,y_new);
				// vector<vector<char> > board1=board;
				// int to_play1=to_play;
				// board1[x_new][y_new]='x';
				// to_play1=3-to_play1;
				// play_knight(board1,to_play1,p1_win,total);
			}
		}
	}
	if(knight_played==false){
		ll psn=rand()%(n*n);
		while(board[psn/n][psn%n]!='.'){
			psn=rand()%(n*n);
		}
		knight_move=MP(psn/n,psn%n);
		// board[psn/n][psn%n]='x';
		// vector<vector<int> > board1=board;
	// recent_move_by_p2=make_pair(psn/n,psn%n);
		// to_play=3-to_play;
		// play_knight(board,to_play,p1_win,total);
	}
	return knight_move;
}

pll play_random(vector<vector<char> > &board){
	ll n=board[0].size();
	pll random_move;
	ll psn=rand()%(n*n);
	while(board[psn/n][psn%n]!='.'){
		psn=rand()%(n*n);
	}
	random_move=MP(psn/n,psn%n);
	return random_move;
}

int main(){
	cout<<"Enter Number of Iterations: "<<endl;
	ll max_iter;
	cin>>max_iter;
	cout<<"Enter Board Size: "<<endl;
	ll n;
	cin>>n;
	ll p1_win=0;
	ll total=0;
	cout<<"0 - greedy, 1 - knight, 2 - random"<<endl;
	cout<<"choose the strategy for player 1: "<<endl;
	ll p1_strategy;
	cin>>p1_strategy;
	cout<<"choose the strategy for player 2: "<<endl;
	ll p2_strategy;
	cin>>p2_strategy;

	for (int num=0;num<max_iter;num++){
	vector<vector<char> > board(n);
	for (ll i=0;i<n;i++){
		for (ll j=0;j<n;j++){
			board[i].PB('.');
		}
	}

	ll to_play=1;
	pll last_move;

	ll init=rand()%(n*n);
	ll x=init/n;
	ll y=init%n;
	board[x][y]='x';
	last_move=MP(x,y);
	to_play=3-to_play;

	while(check(board)==false){
		if (to_play==1){
			ll i=last_move.F;
			ll j=last_move.S;
			ll x,y;
			pll move;
			if(p1_strategy==0){
				move=play_greedy(board);
				// x=greedy_move.F;
				// y=greedy_move.S;
			}
			else if(p1_strategy==1){
				move=play_knight(i,j,board);
				// x=knight_move.F;
				// y=knight_move.S;
			}
			else{
				move=play_random(board);
			}

			x=move.F;
			y=move.S;
			board[x][y]='x';
			last_move=move;
		}
		else if(to_play==2){
			// ll i=last_move.F;
			// ll j=last_move.S;
			// pll knight_move=play_knight(i,j,board);

			// ll x=knight_move.F;
			// ll y=knight_move.S;
			// board[x][y]='x';
			// last_move=knight_move;
			ll i=last_move.F;
			ll j=last_move.S;
			ll x,y;
			pll move;
			if(p2_strategy==0){
				move=play_greedy(board);
				// x=greedy_move.F;
				// y=greedy_move.S;
			}
			else if(p2_strategy==1){
				move=play_knight(i,j,board);
				// x=knight_move.F;
				// y=knight_move.S;
			}
			else{
				move=play_random(board);
			}

			x=move.F;
			y=move.S;
			board[x][y]='x';
			last_move=move;
		}
		to_play=3-to_play;
	}
	total++;
	if(to_play==1){
		p1_win++;
	}
	// printboard(board);
	}
	cout<<"p1 winning = "<<p1_win*100.0/total<<"%"<<endl;
}