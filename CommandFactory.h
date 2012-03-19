#ifndef DEF_COMMAND_FACTORY
#define DEF_COMMAND_FACTORY

#include <string>
#include <vector>
#include "Player.h"
#include "CommandAbstract.h"

using namespace std;

class CommandFactory
{
        public:
        static CommandAbstract* create(Player*, vector<string>);
}

#endif
