#ifndef DEF_PLAYER_MODEL
#define DEF_PLAYER_MODEL

#include <map>
#include "CharacterModel.h"

class PlayerModel : public CharacterModel
{
    public:
    PlayerModel();
    static PlayerModel* loadByLoginAndPassword(std::string login, std::string password);
    void setLogin(std::string login);
    void setPassword(std::string password);
    std::string getLogin();
    std::string getPassword();
    bool save();
    int getPk();

    protected:
    std::map <std::string, std::string> _playerFields;
    void _setPk(int pk);
};

#endif
