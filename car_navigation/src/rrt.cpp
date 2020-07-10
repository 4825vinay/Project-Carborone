#include<iostream>
#include<vector>
#include<cstdlib>
#include<ctime>

using namespace std;

float generate_random_num();

class node{
public:
	node(float x_int, float y_int){
		x = x_int;
		y = y_int;
	}
	void print_params(){
		cout << x << " " << y <<endl;
		cout << parent_x << " " << parent_y <<endl;
	}
	void parent(float x, float y){
		parent_x = x;
		parent_y = y;
	}
private:
	float x;
	float y;
	float parent_x;
	float parent_y;
};

float generate_random_num(float min, float max){
	srand((unsigned)time(NULL));
	
	return min + (float)rand()/(float)(RAND_MAX/(max-min));
}


int main(){
	std::vector<node> v;
	for(int i = 0; i < 10; i++){
		node n1(generate_random_num(0, 1), generate_random_num(0, 1));
		v.push_back(n1);
	}
	for( int i = 0; i < v.size(); i++){
		v[i].print_params();
	}
}

