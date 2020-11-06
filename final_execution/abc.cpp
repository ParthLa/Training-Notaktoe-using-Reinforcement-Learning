// #include<bits/stdc++.h>
// using namespace std;

// typedef long long ll;
// // typedef long double ld;
// // typedef pair<int,int> pint;
// // typedef pair<long long,long long> pll;
// // typedef pair<long double,long double> pld;

// // typedef vector<int> vi;
// // typedef vector<vector<int> > vvi;
// // typedef vector<ll> vl;
// // typedef vector<vector<ll> > vvl;
// // typedef vector<ld> vd;
// // typedef vector<vector<ld> > vvd;

// #define PB push_back
// // #define MP make_pair
// // #define F first
// #define S second
// #define fast ios::sync_with_stdio(0);cin.tie(0);cout.tie(0);

// ll exp(ll val,ll power){
// 	ll ans;
// 	if(power==0){
// 		ans=1;
// 	}
// 	else if(val==1){
// 		ans=1;
// 	}
// 	else if(power%2==0){
// 		ll x=exp(val,power/2);
// 		ans=x*x;
// 	}
// 	else{
// 		ans=val*exp(val,power-1);
// 	}
// 	return ans;
// }

// vector<string> generate_all_state(ll m){
// 	vector<string> v;
// 	if(m==0){
// 		v.PB("");
// 	}
// 	else{
// 		vector<string> v1=generate_all_state(m-1);
// 		for (ll i=0;i<v1.size();i++){
// 			string p='0'+v1[i];
// 			v.PB(p);
// 		}
// 		for (ll i=0;i<v1.size();i++){
// 			string p='1'+v1[i];
// 			v.PB(p);
// 		}
// 	}
// 	return v;
// }

// int main(){
// 	ll m;
// 	cout<<"Enter m"<<endl;
// 	cin>>m;
// 	ll k;
// 	cout<<"Enter k"<<endl;
// 	cin>>k;

// 	ll l=exp(2,m);
// 	ll counter=-1*exp(2,k-1);
// 	ll min_counter=-1*exp(2,k-1);
// 	ll max_counter=exp(2,k-1);
// 	// vl tables(l,counter);
// 	map<string,ll> tables,mispred;
// 	string state;
// 	// for (ll i=0;i<l;i++){
// 	// 	state.PB('0');
// 	// }
// 	vector<string> v;
// 	v=generate_all_state(m);
// 	for (ll i=0;i<v.size();i++){
// 		// cout<<v[i]<<endl;
// 		tables[v[i]]=counter;
// 		mispred[v[i]]=0;
// 	}
// 	state=v[0];

// 	ll t3=0;
// 	ll num_iter;
// 	cout<<"Enter num_iter"<<endl;
// 	cin>>num_iter;
// 	ll t0=num_iter;
// 	ll t1,t2;
// 	while(t0!=0){
// 		t1=t0&7;
// 		// cout<<t0<<" "<<t1<<" "<<tables[state]<<endl;
// 		if(t1>2){
// 			if(tables[state]<0){
// 				cout<<t0<<" "<<t1<<" "<<tables[state]<<" 0 1 "<<min(tables[state]+1,max_counter)<<endl;
// 				mispred[state]++;
				
// 			}
// 			tables[state]=min(tables[state]+1,max_counter);
// 			if(tables[state]==0){
// 				tables[state]++;
// 			}
// 			t2=t0*2;
// 			t3=t3-t2;
// 			if(m!=0){
// 				state='1'+state.substr(0,state.size()-1);
// 			}
// 		}
// 		else{
// 			if(tables[state]>0){
// 				cout<<t0<<" "<<t1<<" "<<tables[state]<<" 1 0 "<<max(tables[state]-1,min_counter)<<endl;
// 				mispred[state]++;
				
// 			}
// 			tables[state]=max(tables[state]-1,min_counter);
// 			if(tables[state]==0){
// 				tables[state]--;
// 			}
// 			t2=t0*4;
// 			t3=t3+t2;
// 			if(m!=0){
// 				state='0'+state.substr(0,state.size()-1);
// 			}
// 		}
// 		t0=t0-1;
// 		if(m!=0){
// 			state='1'+state.substr(0,state.size()-1);
// 		}
// 	}

// 	ll total_mispred=0;
// 	for (auto itr=mispred.begin();itr!=mispred.end();itr++){
// 		total_mispred+=itr->S;
// 	}
// 	cout<<"mispred = "<<total_mispred*100.0/num_iter<<"%"<<endl;
// }

// // #include<bits/stdc++.h>
// // using namespace std;

// // typedef long long ll;
// // #define PB push_back
// // #define S second
// // #define fast ios::sync_with_stdio(0);cin.tie(0);cout.tie(0);

// // ll exp(ll val,ll power){
// // 	ll ans;
// // 	if(power==0){
// // 		ans=1;
// // 	}
// // 	else if(val==1){
// // 		ans=1;
// // 	}
// // 	else if(power%2==0){
// // 		ll x=exp(val,power/2);
// // 		ans=x*x;
// // 	}
// // 	else{
// // 		ans=val*exp(val,power-1);
// // 	}
// // 	return ans;
// // }



// // vector<string> generate_all_state(ll m){
// // 	vector<string> v;
// // 	if(m==0){
// // 		v.PB("");
// // 	}
// // 	else{
// // 		vector<string> v1=generate_all_state(m-1);
// // 		for (ll i=0;i<v1.size();i++){
// // 			string p='0'+v1[i];
// // 			v.PB(p);
// // 		}
// // 		for (ll i=0;i<v1.size();i++){
// // 			string p='1'+v1[i];
// // 			v.PB(p);
// // 		}
// // 	}
// // 	return v;
// // }

// // int main(){
// // 	ll m;
// // 	cout<<"Enter m"<<endl;
// // 	cin>>m;
// // 	ll k;
// // 	cout<<"Enter k"<<endl;
// // 	cin>>k;

// // 	ll l=exp(2,m);
// // 	ll counter=-1*exp(2,k-1);
// // 	ll min_counter=-1*exp(2,k-1);
// // 	ll max_counter=exp(2,k-1);
// // 	map<string,ll> tables,mispred;
// // 	string state;
// // 	vector<string> v;
// // 	v=generate_all_state(m);
// // 	for (ll i=0;i<v.size();i++){
// // 		// cout<<v[i]<<endl;
// // 		tables[v[i]]=counter;
// // 		mispred[v[i]]=0;
// // 	}
// // 	state=v[0];

// // 	ll t3=0;
// // 	ll num_iter;
// // 	cout<<"Enter num_iter"<<endl;
// // 	cin>>num_iter;
// // 	ll t0=num_iter;
// // 	ll t1,t2;
// // 	while(t0!=0){
// // 		t1=t0&7;
// // 		// cout<<t0<<" "<<t1<<" "<<tables[0]<<endl;
// // 		if(t1>2){
// // 			if(tables[state]<0){
// // 				mispred[state]++;
// // 			}
// // 			tables[state]=min(tables[state]+1,max_counter);
// // 			if(tables[state]==0){
// // 				tables[state]++;
// // 			}
// // 			t2=t0*2;
// // 			t3=t3-t2;
// // 			state='1'+state.substr(0,state.size()-1);
// // 		}
// // 		else{
// // 			if(tables[state]>0){
// // 				mispred[state]++;
// // 			}
// // 			tables[state]=max(tables[state]-1,min_counter);
// // 			if(tables[state]==0){
// // 				tables[state]--;
// // 			}
// // 			t2=t0*4;
// // 			t3=t3+t2;
// // 			state='0'+state.substr(0,state.size()-1);
// // 		}
// // 		t0=t0-1;
// // 		state='1'+state.substr(0,state.size()-1);
// // 	}

// // 	ll total_mispred=0;
// // 	for (auto itr=mispred.begin();itr!=mispred.end();itr++){
// // 		total_mispred+=itr->S;
// // 	}
// // 	cout<<"mispred = "<<total_mispred*100.0/num_iter<<"%"<<endl;
// // }


#include<bits/stdc++.h>
using namespace std;

typedef long long ll;
#define PB push_back
#define S second
#define fast ios::sync_with_stdio(0);cin.tie(0);cout.tie(0);

ll exp(ll val,ll power){
	ll ans;
	if(power==0){
		ans=1;
	}
	else if(val==1){
		ans=1;
	}
	else if(power%2==0){
		ll x=exp(val,power/2);
		ans=x*x;
	}
	else{
		ans=val*exp(val,power-1);
	}
	return ans;
}



vector<string> generate_all_state(ll m){
	vector<string> v;
	if(m==0){
		v.PB("");
	}
	else{
		vector<string> v1=generate_all_state(m-1);
		for (ll i=0;i<v1.size();i++){
			string p='0'+v1[i];
			v.PB(p);
		}
		for (ll i=0;i<v1.size();i++){
			string p='1'+v1[i];
			v.PB(p);
		}
	}
	return v;
}

int main(){
	ll m;
	cout<<"Enter m"<<endl;
	cin>>m;
	ll k;
	cout<<"Enter k"<<endl;
	cin>>k;

	ll l=exp(2,m);
	ll counter=-1*exp(2,k-1);
	ll min_counter=-1*exp(2,k-1);
	ll max_counter=exp(2,k-1);
	map<string,ll> tables,mispred;
	string state;
	vector<string> v;
	v=generate_all_state(m);
	for (ll i=0;i<v.size();i++){
		// cout<<v[i]<<endl;
		tables[v[i]]=counter;
		mispred[v[i]]=0;
	}
	state=v[0];

	ll t3=0;
	ll num_iter;
	cout<<"Enter num_iter"<<endl;
	cin>>num_iter;
	ll t0=num_iter;
	ll t1,t2;
	while(t0!=0){
		t1=t0&7;
		// cout<<t0<<" "<<t1<<" "<<tables[0]<<endl;
		if(t1>2){
			if(tables[state]<0){
				mispred[state]++;
			}
			tables[state]=min(tables[state]+1,max_counter);
			if(tables[state]==0){
				tables[state]++;
			}
			t2=t0*2;
			t3=t3-t2;
if(m!=0){
				state='1'+state.substr(0,state.size()-1);
			}
		}
		else{
			if(tables[state]>0){
				mispred[state]++;
			}
			tables[state]=max(tables[state]-1,min_counter);
			if(tables[state]==0){
				tables[state]--;
			}
			t2=t0*4;
			t3=t3+t2;
			if(m!=0){
				state='0'+state.substr(0,state.size()-1);
			}
		}
		t0=t0-1;
		if(m!=0){
			state='1'+state.substr(0,state.size()-1);
		}
	}

	ll total_mispred=0;
	for (auto itr=mispred.begin();itr!=mispred.end();itr++){
		total_mispred+=itr->S;
	}
	cout<<"mispred = "<<total_mispred*100.0/num_iter<<"%"<<endl;
}
