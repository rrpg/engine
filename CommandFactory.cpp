//      Command.cpp
//

#include <vector>
#include <string>
#include "CommandFactory.h"
#include "Command.h"

CommandAbstract* CommandFactory::create(Player* &player, std::vector <std::string> commandFull)
{
    std::string cmd = commandFull[0];
    commandFull.erase(commandFull.begin());

    CommandAbstract* command;

    if (cmd.compare("talk") == 0) {
        if (!player->isConnected() || !player->connect()) {
            throw "A player must be connected to launch the command talk";
        }
        command = new CommandTalk();
    }
    else if (cmd.compare("createPlayer") == 0) {
        if (player->isConnected()) {
            throw "There must not be a connected player to create a new player";
        }
    }
    else {
        return NULL;
    }

    command->setArgs(commandFull);
    command->setPlayer(player);
    return command;
}
