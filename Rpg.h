#ifndef DEF_RPG
#define DEF_RPG

#include "Player.h"

using namespace std;

class Rpg
{
    public:
    Rpg(string, string, vector <string>);
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
