//      Command.cpp
//

#include <vector>
#include <string>
#include "CommandAbstract.h"
#include "CommandFactory.h"
#include "Command.h"

CommandAbstract* CommandFactory::create(Player*, std::vector <std::string>)
{
    return new CommandAbstract();
}
