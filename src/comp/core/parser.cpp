#include <unistd.h>
#include <stdio.h>
#include <limits.h>
#include <string>
#include <iostream>
#include <unordered_map>
#include <fstream>

using namespace std;

class Parser{
    public:
        string file = "<stdin>";

        bool auto_run;

        string userpath;
        
        unordered_map<string, string> functions;

        unordered_map<string, string> variables;

        unordered_map<string, string> function_params;

        unordered_map<string, string> data;

        unordered_map<string, string> process_cache;

        unordered_map<string, string> imported_modules;

        string add_to_output;

};