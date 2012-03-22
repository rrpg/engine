#ifndef DEF_PLAYER
#define DEF_PLAYER

#include <string>

class Player
{
    public:
    Player();
    Player(std::string login, std::string password);
    bool connect();

    private:
    std::string _login;
    std::string _password;
};

#endif
