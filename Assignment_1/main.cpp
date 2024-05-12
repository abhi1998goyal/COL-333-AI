#include <iostream>
#include <bits/stdc++.h>
#include <fstream>
#include <chrono>
#include <atomic>
#include <fstream>
#include <thread>
#include "SportsLayout.h"
#include <unistd.h>


using namespace std;

void myFunction(SportsLayout *s)
{
    s->compute_allocation();
}

int main(int argc, char** argv )
{ 
    if ( argc < 3 )

    {   
        cout<<"Missing arguments\n";
        cout<<"Correct format : \n";
        cout << "./main <input_filename> <output_filename>";
        exit ( 0 );
    }
    string inputfilename ( argv[1] );
    string outputfilename ( argv[2] );

     SportsLayout *s  = new SportsLayout( inputfilename );
     cout<<"Time allocated is : "<<s->time<<" \n";

     chrono::seconds timeLimit((s->time)*60);


    thread workerThread(myFunction,s);

    if (workerThread.joinable())
    {
        workerThread.joinable();
        this_thread::sleep_for(timeLimit);

        if (workerThread.joinable())
        {
            workerThread.detach();
            cout << "Code execution timed out." << endl;
        }
    }

     cout << "Thread has been interrupted." << std::endl;

     cout<<"Most optimal result is ";
     s->print_vec(s->mapped_zone(s->result));

    return 0;

}