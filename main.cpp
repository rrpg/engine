//      main.cpp


#include <iostream>
#include <string>
#include <vector>
#include <stdio.h>
#include <stdlib.h>
#include "Rpg.h"

using namespace std;

int main(int argc, char **argv)
{
    //list of expected arguments
    string expectedArgs[2];
    expectedArgs[0] = "--login";
    expectedArgs[1] = "--password";

    //action to launch, index 1 : action name ; indexes 2..n : params
    vector <string> rpgAction;
    string login, password, action, argName, argValue;

    for (int i = 1 ; i < argc ; i++) {
        argName = string(argv[i]);
        //if the arg is an option label
        if (argName.substr(0, 2).compare("--") == 0) {
            i++;
        }
        //get the value of the argument
        argValue = string(argv[i]);

        //argument is option label, but no value provided
        if (i > argc && argValue.substr(0, 2).compare("--") == 0) {
            cerr << "Missing argument value" << endl;
            exit(1);
        }
        //set the login
        if (argName == "--login") {
            login = argValue;
        }
        //set the password
        else if (argName == "--password") {
            password = argValue;
        }
        else {
            //populate the action
            rpgAction.push_back(argValue);
        }
    }

    //creation of the game
    Rpg* rpg = new Rpg(login, password, rpgAction);
    //game launched !
    rpg->run();
}
