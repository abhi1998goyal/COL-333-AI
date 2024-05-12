
#ifndef SPORTSLAYOUT_H
#define	SPORTSLAYOUT_H

#include <fstream>
#include <iostream>
#include <bits/stdc++.h>
using namespace std;

class SportsLayout{

    public:
    int z,l;
    int** T;
    int **N;
    int time;
    int *mapping;
    vector<int> result;

    public:
    SportsLayout(string inputfilename);

    bool check_output_format();

    // void readOutputFile(string output_filename);
    
   long long cost_fn(vector<int> &mapp);

    void write_to_file(string outputfilename);

    void readInInputFile(string inputfilename);

    void compute_allocation();

    vector<vector<int>> compute_neighbour(vector<int>& map_loc);

    pair<vector<int>,long long> get_greedy_best(vector<vector<int>> neighbours);

    pair<vector<int>,int> try_BFS(pair<vector<int>,int> local_max);

    long long calc_state_cost(vector<int> state);

    pair<vector<int>,long long> try_random_sampling(pair<vector<int>,long long> local_max,random_device& rd);

    vector<int> mapped_zone(vector<int> map_loc);

    void print_vec(vector<int> vec);


};


#endif