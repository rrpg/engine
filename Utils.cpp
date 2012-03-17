// Utils.cpp

#include <iostream>
#include <string>
#include <vector>
#include "Utils.h"

using namespace std;


vector<string> Utils::explode(string str, char sep)
{
    vector<string> retValue;
    int sizeStr = str.size();
    unsigned int start = 0, length = 0;
    for (int i = 0 ; i < sizeStr ; i++) {
        if (str[i] == sep) {
            retValue.push_back(str.substr(start, length));
            start = i + 1;
            length = 0;
        }
        length++;
    }

    if (start < str.size()) {
        retValue.push_back(str.substr(start, length));
    }

    return retValue;
}
