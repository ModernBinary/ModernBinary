#include <iostream>
#include <string>
#include <vector>
#include <stdlib.h>
#include <locale>
#include <cctype>
#include <algorithm>
#include <sstream>
#include <fstream>
#include "core/convert.cpp"
#include "core/parser.cpp"

using namespace std;

bool replace(std::string& str, const std::string& from, const std::string& to) {
    size_t start_pos = str.find(from);
    if(start_pos == std::string::npos)
        return false;
    str.replace(start_pos, from.length(), to);
    return true;
}

static inline string &ltrim(string &s) {
    s.erase(s.begin(), find_if(s.begin(), s.end(),
            not1(ptr_fun<int, int>(isspace))));
    return s;
}

static inline string &rtrim(string &s) {
    s.erase(find_if(s.rbegin(), s.rend(),
            not1(ptr_fun<int, int>(isspace))).base(), s.end());
    return s;
}

static inline string &trim(string &s) {
    return ltrim(rtrim(s));
}

inline bool mbexist(const string& name) {
    ifstream f(name.c_str());
    return f.good();
}

int main(int argc, char *argv[])
{
    string current_exec_name = argv[0];
    vector<string> all_args;
    
    all_args.assign(argv+1, argv + argc);
    argc--;

    if(!argc){
        cout<<"[Error] You must enter the file name in the input arguments."<<endl;
        exit(0);
    }else if(all_args[0] == "--texttomb" || all_args[0] == "--mbtotext"){

        ostringstream stream;
        string arr[all_args.size()];
        int k = 0;
        bool first = false;
        for (string const &i: all_args) {
            if(!first){
                first = true;
                continue;
            }
            arr[k++] = i;
        }
        for (char i = 0; i < sizeof(arr) / sizeof(arr[0]); ++i) {
            if (i) stream << ' ';
            stream << arr[i];
        }
        string to_convert = stream.str();
        to_convert = trim(to_convert);
        string to_output;
        if(all_args[0] == "--texttomb"){
            to_output = texttomb(to_convert);
        }else{
            to_output = mbtotext(to_convert);
        }
        to_output = trim(to_output);
        cout<<to_output<<endl;
        exit(0);
    }else{
        string f_name = all_args[0];
        if(!hasEnding(f_name, ".mb")){
            cout<<"[Error] Your file format must be mb."<<endl;
            exit(0);
        }else{
            if(mbexist(f_name)){
                Parser parser(f_name);
            }else{
                cout<<"[Error] There is no file named "<<f_name<<"."<<endl;
                exit(0);
            }
        }
    }
    cout<<endl;
}