#include <fstream>
#include <iostream>
#include <bits/stdc++.h>

using namespace std;

#include "SportsLayout.h"

    SportsLayout::SportsLayout(string inputfilename)
    {
          
        readInInputFile(inputfilename);
        mapping= new int[z];

    }

    bool SportsLayout::check_output_format()
    {

        vector<bool> visited(l,false);
        for(int i=0;i<z;i++)
        {
            if((mapping[i]>=1 && mapping[i]<=l))
            {
                if(!visited[mapping[i]-1])
                visited[mapping[i]-1]=true;
                else
                {
                    cout<<"Repeated locations, check format\n";
                    return false;
                }
            }
            else
            {
                cout<<"Invalid location, check format\n";
                return false;
            }
        }

        return true;

    }

    // void SportsLayout::readOutputFile(string output_filename)
    // {
    //         fstream ipfile;
	//         ipfile.open(output_filename, ios::in);
    //         if (!ipfile) {
    //             cout << "No such file\n";
    //             exit( 0 );
    //         }
    //         else {
                
    //             vector<int> ip;

    //             while (1) {
    //                 int t;
    //                 ipfile >> t;
    //                 ip.push_back(t);
    //                 if (ipfile.eof())
    //                     break;
                    
    //             }
            
    //         if(ip.size()!=z)
    //         {
    //             cout<<"number of values not equal to number of zones, check output format\n";
    //             exit(0);
    //         }
    //         for(int i=0;i<z;i++)
    //         mapping[i]=ip[i];
    //     ipfile.close();

    //     if(!check_output_format())
    //         exit(0);
    //     cout<<"Read output file, format OK"<<endl;

    //         }
        
    // }


    long long SportsLayout::cost_fn(vector<int> &mapp){


        long long cost=0;

        for(int i=0;i<z;i++)
        {
           for(int j=0;j<z;j++) 
           {
                cost+=(long long)N[i][j]*(long long)T[mapp[i]-1][mapp[j]-1];
           }
        }

        return cost;
    }

    void SportsLayout::readInInputFile(string inputfilename)
    {
            fstream ipfile;
	        ipfile.open(inputfilename, ios::in);
            if (!ipfile) {
                cout << "No such file\n";
                exit( 0 );
            }
            else {
                

                ipfile>> time;
                ipfile >> z;
                ipfile >> l;

                if(z>l)
                {
                    cout<<"Number of zones more than locations, check format of input file\n";
                    exit(0);
                }


            

            int **tempT;
            int **tempN;

          tempT = new int*[l];
         for (int i = 0; i < l; ++i)
            tempT[i] = new int[l];
        
        tempN = new int*[z];
        for (int i = 0; i < z; ++i)
            tempN[i] = new int[z];

        for(int i=0;i<z;i++)
        {
            for(int j=0;j<z;j++)
            ipfile>>tempN[i][j];
        }

        for(int i=0;i<l;i++)
        {
            for(int j=0;j<l;j++)
            ipfile>>tempT[i][j];
        }

        ipfile.close();

        T= tempT;
        N= tempN;
            }

    }

    void SportsLayout::write_to_file(string outputfilename)
  {

         // Open the file for writing
    ofstream outputFile(outputfilename);

    // Check if the file is opened successfully
    if (!outputFile.is_open()) {
        cerr << "Failed to open the file for writing." << std::endl;
        exit(0);
    }

    for(int i=0;i<z;i++)
    outputFile<<mapping[i]<<" ";

    // Close the file
    outputFile.close();

    cout << "Allocation written to the file successfully." << endl;

  }

    long long SportsLayout:: calc_state_cost(vector<int> state){
        long long cost=0;
                   for(int i=0;i<l;i++){
                      for(int j=0;j<l;j++){
                             if(state[i]!=0 && state[j]!=0){
                                long long ct=(long long)(N[state[i]-1][state[j]-1]*(long long)T[i][j]);
                                cost +=ct;

                            //  cout<<"zone "<<state[i]<<" to "<<state[j]<<":"<<ct<<"\n";
                             } 
                      }
                   }
        return cost;
    }

    vector<int> SportsLayout::mapped_zone(vector<int> map_loc){
        vector<int> zone(z,0);
        for(int i=0;i<l;i++){
            if(map_loc[i]!=0){
               zone[map_loc[i]-1]=i+1;
            }
        }
       return zone;
    }

    void SportsLayout:: print_vec(vector<int> vec){
        for(int x:vec){
            cout<<x;
        }
        cout<<" :"<<(long long)cost_fn(vec)<<" \n";
    }

    pair<vector<int>,long long> SportsLayout:: get_greedy_best(vector<vector<int>> neighbours){
         vector<int> best;
            long long min_cost=INT_MAX;
               for(auto neighbour:neighbours){
                 long long cost = calc_state_cost(neighbour);
                   if(min_cost>cost){
                    cout<<"neighbour search : "<<cost<<" :";
                    print_vec(mapped_zone(neighbour));
                    
                    min_cost=cost;
                    best=neighbour;

                   }
               }
               return make_pair(best,min_cost);
               
    }

    vector<vector<int>> SportsLayout::compute_neighbour(vector<int>& map_loc){
        vector<vector<int>> neighbours;
              for(int i=0;i<l;i++){
                  for(int j=i+1;j<l;j++){
                       if(map_loc[i]==0 && map_loc[j]==0){
                          continue;
                       }
                       else if (map_loc[i]==0 || map_loc[j]==0) {
                       vector<int> swp=map_loc;
                       int temp=swp[i]; //swap!
                       swp[i]=swp[j];
                       swp[j]=temp;
                       neighbours.push_back(swp);
                       }
                  }
              }
              return neighbours;
    }

    pair<vector<int>,int> SportsLayout::try_BFS(pair<vector<int>,int> local_max){
            queue<vector<int>> state_queue;
            state_queue.push(local_max.first);
            int target = local_max.second;
            while(!state_queue.empty()){
                vector<int> state = state_queue.front();
                int calc_cost = calc_state_cost(state);
                 if(calc_cost<target){
                    return make_pair(state,calc_cost);
                 }

                 for(auto neighbour:compute_neighbour(state)){
                      state_queue.push(neighbour);
                 }
               state_queue.pop();
            }

            return local_max;

    }

    pair<vector<int>,long long> SportsLayout::try_random_sampling(pair<vector<int>,long long> local_max,random_device& rd)
    {
            mt19937 re(rd());
            long long target = local_max.second;
            vector<int> best_now=local_max.first;
            vector<int> perm_order(best_now.begin(), best_now.end());
            
            long long random_cost=INT_MAX;//calc cost of random state
            uniform_real_distribution<double> distribution(0.0, 1.0);

            while(true){
            shuffle(perm_order.begin(), perm_order.end(), re);
            random_cost=calc_state_cost(perm_order);
            float prob = distribution(re);

              if(target>random_cost){
                    if(prob<=0.7){

                      return make_pair(perm_order,random_cost);
                  }

              }



            // }

             else if(target<random_cost){
                  if(prob>0.7){
                       cout<<"Random State : ";
                      print_vec(mapped_zone(perm_order));
                      return make_pair(perm_order,random_cost);
                  }
               //   return make_pair(perm_order,random_cost);
             }

            // if(target>random_cost){
            //      cout<<"random search :";
            //      print_vec(mapped_zone(perm_order));
            //      return make_pair(perm_order,random_cost);
            // }

            }
               //  cout<<"random search :";
               //  print_vec(mapped_zone(perm_order));
                 return make_pair(best_now,target);

    }


    void SportsLayout::compute_allocation()
    {  //const int desired_duration_minutes = time;
       vector<int> present_state(l,0);

        for(int i=0;i<l;i++){
         if(i<z){
          present_state[i]=i+1;
         }
         else{
            present_state[i]=0;
         }
          
       } //cross mapping

    

       random_device rd;

       result=present_state;
      

       while(true){

      //  chrono::time_point<chrono::system_clock> current_time = chrono::system_clock::now();
       // chrono::duration<double> elapsed_seconds = current_time - start_time;

        // if (elapsed_seconds.count() >= desired_duration_minutes * 60) {
         //   break;
       // }

    //  for(int i=0;i<l;i++){
     //   cout<<present_state[i];
    //  }
     //  cout<<" "<<current_cost<<"\n";
        long long current_cost=calc_state_cost(present_state);

       long long neighbour_cost=get_greedy_best(compute_neighbour(present_state)).second;
       vector<int> neighbour_state=get_greedy_best(compute_neighbour(present_state)).first;

       while(current_cost>neighbour_cost){

           present_state=neighbour_state;
           current_cost=neighbour_cost;

           pair<vector<int>,long long> neighbour_pair = get_greedy_best(compute_neighbour(present_state));

           neighbour_state=neighbour_pair.first;
           neighbour_cost=neighbour_pair.second;
        
       }
       
       if(calc_state_cost(result)>calc_state_cost(present_state)){
          result=present_state;//save the result before program is intrupted
       }



      // while(elapsed_seconds.count() >= desired_duration_minutes * 60){
        
         pair<vector<int>,long long> ran_state=try_random_sampling(make_pair(present_state,calc_state_cost(result)),rd);

         cout<<"Random State : ";
         print_vec(mapped_zone(ran_state.first));
         

      // }
        present_state=ran_state.first;
       // neighbour_cost=ran_state.second;
       // neighbour_state = ran_state.first;
       // result=neighbour_state; //save the result before program is intrupted

       }

    //    for(int i=0;i<l;i++){
    //     cout<<result[i];
    //    }


      // print_vec(mapped_zone(result));
      // cout<<calc_state_cost(result);

  
    }




