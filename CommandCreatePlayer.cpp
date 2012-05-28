//class CommandCreatePlayer.cpp

#include "CommandCreatePlayer.h"


#include <iostream>

CommandCreatePlayer::CommandCreatePlayer()
{
}


void CommandCreatePlayer::run()
{
    _player->createNewPlayer();
    std::cout << "I create a new player" << std::endl;
}
