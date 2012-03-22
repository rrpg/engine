//      Command.cpp
//

#include <vector>
#include <string>
#include "CommandAbstract.h"
#include "CommandFactory.h"
#include "Command.h"

using namespace std;

CommandAbstract* CommandFactory::create(Player*, vector<string>)
{
    return new CommandAbstract();
}
