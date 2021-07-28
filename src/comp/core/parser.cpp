#include <unistd.h>
#include <stdio.h>
#include <limits.h>
#include <string>
#include <regex> 
#include <iostream>
#include <list>
#include <unordered_map>
#include <fstream>

using namespace std;

bool hasEnding(string const &fullString, string const &ending) {
    if (fullString.length() >= ending.length()) {
        return (0 == fullString.compare (fullString.length() - ending.length(), ending.length(), ending));
    } else {
        return false;
    }
}

bool hasStarting(string const &fullString, string const &starting){
    if (fullString.rfind(starting, 0) == 0) {
        return true;
    }
    return false;
}

class Parser{
    public:
        string file = "<stdin>";

        bool run;

        string userpath;
        
        unordered_map<string, string> functions;

        unordered_map<string, string> variables;

        unordered_map<string, string> function_params;

        list<string> datalist;

        unordered_map<string, string> process_cache;

        unordered_map<string, string> imported_modules;

        string add_to_output;

        smatch match_array(string reg, string str){
            regex __regex(reg); 
            smatch match; 
            regex_search(str, match, __regex);
            return match;
        }

        bool command_regex_search(string line)
        {   
            bool discard_first, is_loop = false;

            // Check for comments
            if((line.rfind("#", 0) == 0))
                return false;

            for(auto m: match_array("\\(([^)]+)\\)", line)){
                if(!discard_first){
                    discard_first = true; continue;
                }
                is_loop = true;
            }
            if(!is_loop)
                return false;
            
            if (hasEnding(line, "::()")){
                add_to_output += "\\n";
            }
            else if (hasEnding(line, ":()")){
                add_to_output += " ";
            }

            return false;
        }

        Parser(string file_name, bool auto_run=true)
        {
            file = file_name;
            run = auto_run;
            string linetocheck;
            ifstream MB_FILE(file);
            int line_on_check = 0;

            while (getline (MB_FILE, linetocheck)) {
                datalist.push_back(linetocheck);
            }

            string data[datalist.size()];
            for(string s:datalist){
                data[line_on_check++] = s;
            }
            
            MB_FILE.close();
            command_regex_search(data[1]);
        }
};