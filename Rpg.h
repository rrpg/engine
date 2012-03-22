#ifndef DEF_RPG
#define DEF_RPG

#include <string>
#include <vector>
#include "Player.h"

using namespace std;

class Rpg
{
    public:
    Rpg(string login, string password, vector <string> action);
    ~Rpg();
    void run();

    protected:
    int _runAction();

    private:
    Player *_player;
    bool _authenticate;
    vector <string> _action;
};

#endif
