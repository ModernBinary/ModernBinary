#include <string>
#include "convert.h"
#include <ctype.h>
#include <iostream>
#include <list>
#include <sstream>

using namespace std;

string texttomb(string text){
    int index = 0;
    list<int> chars, base2;
    for (char c: text) chars.push_back(__toascii(c));
    for (int c: chars){
        base2.push_back(c*(index+1));
        index++;
    }
    int arr[base2.size()];
    int k = 0;
    for (int const &i: base2) {
        arr[k++] = i;
    }
    ostringstream stream;
    for (int i = 0; i < sizeof(arr) / sizeof(arr[0]); ++i) {
        if (i) stream << ' ';
        stream << arr[i];
    }
    return stream.str();
}

string mbtotext(string text){
    list<char> chars;
    stringstream ss(text);
    string word;
    int index, k = 0;
    char temp;
    while (ss >> word){
        temp = atoi(word.c_str())/(index+1);
        chars.push_back(temp);
        index++;
    }
    char arr[chars.size()];
    for (char const &i: chars) {
        arr[k++] = i;
    }
    ostringstream stream;
    for (char i = 0; i < sizeof(arr) / sizeof(arr[0]); ++i) {
        if (i) stream;
        stream << arr[i];
    }
    return stream.str();
}