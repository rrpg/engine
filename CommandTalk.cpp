//class Command/Talk.cpp

#include "CommandTalk.h"
#include <iostream>
#include <string>
#include "Character.h"
//~ #include "Sentence.h"

CommandTalk::CommandTalk()
{
}


void CommandTalk::run()
{
    if (_args.size() == 0) {
        throw "Who must I talk to ?";
    }
    else if (_args.size() == 1) {
        throw "What must I say ?";
    }

    std::string characterName = _args[0];
    std::string triggerWord = _args[1];

    Character* character = Character::searchByNameAndPlayer(characterName, _player);

    //~ Sentence s = Sentence::loadBy
    std::cout << character->getName() << std::endl;
}
