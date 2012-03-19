#ifndef DEF_PLAYER_MODEL
#define DEF_PLAYER_MODEL

using namespace std;

class PlayerModel
{
    public:
    PlayerModel();
    static PlayerModel *loadByLoginAndPassword(string, string);
    void setPk(int);

    protected:
    int _pk;
};

#endif
