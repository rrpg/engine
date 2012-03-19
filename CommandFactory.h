#ifndef DEF_COMMAND_FACTORY
#define DEF_COMMAND_FACTORY

#include "Player.h"
#include "CommandAbstract.h"

class CommandFactory
{
        public:
        static CommandAbstract* create(Player*, vector<string>);
}

#endif
