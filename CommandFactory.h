#ifndef DEF_COMMAND_FACTORY
#define DEF_COMMAND_FACTORY

#include <string>
#include <vector>
#include "Player.h"
#include "CommandAbstract.h"

class CommandFactory
{
        public:
        static CommandAbstract* create(Player*, std::vector<std::string>);
}

#endif
