#ifndef DEF_PLAYER_MODEL
#define DEF_PLAYER_MODEL

class PlayerModel
{
    public:
    PlayerModel();
    static PlayerModel* loadByLoginAndPassword(std::string login, std::string password);
    void setPk(int pk);

    protected:
    int _pk;
};

#endif
