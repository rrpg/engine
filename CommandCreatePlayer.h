#ifndef DEF_COMMAND_CREATE_PLAYER
#define DEF_COMMAND_CREATE_PLAYER

#include "CommandAbstract.h"

class CommandCreatePlayer : public CommandAbstract
{
    public:
    CommandCreatePlayer();
    void run();
};

#endif

