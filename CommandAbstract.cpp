//      CommandAbstract.cpp
//

#include "CommandAbstract.h"
#include "Player.h"
#include <vector>
#include <string>

CommandAbstract::CommandAbstract()
{

}

void CommandAbstract::setArgs(std::vector <std::string> args)
{
    _args = args;
}

void CommandAbstract::setPlayer(Player* &player)
{
    _player = player;
}
