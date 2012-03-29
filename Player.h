#ifndef DEF_PLAYER
#define DEF_PLAYER

#include <string>
#include "PlayerModel.h"

class Player
{
    public:
    Player();
    Player(std::string login, std::string password);
    bool connect();
    bool isConnected();
    void createNewPlayer();
    PlayerModel* getModel();

    protected:
    void _setModelFromLoginInfos();
    void _readLoginAndPassword();

    private:
    std::string _login;
    std::string _password;
    PlayerModel *_model;
};

#endif
