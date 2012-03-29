#ifndef DEF_COMMAND_ABSTRACT
#define DEF_COMMAND_ABSTRACT

#include <vector>
#include <string>
#include "Player.h"

class CommandAbstract
{
    public:
    CommandAbstract();
    virtual void run() = 0;
    void setArgs(std::vector <std::string> args);
    void setPlayer(Player* &player);

    protected:
    std::vector <std::string> _args;
    Player* _player;
};

#endif
