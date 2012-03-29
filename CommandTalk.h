#ifndef DEF_COMMAND_TALK
#define DEF_COMMAND_TALK

#include "CommandAbstract.h"

class CommandTalk : public CommandAbstract
{
    public:
    CommandTalk();
    void run();
};

#endif

