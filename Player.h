#ifndef DEF_PLAYER
#define DEF_PLAYER

using namespace std;

class Player
{
    public:
    Player(string, string);
    Player();
    bool connect();

    private:
    string _login;
    string _password;
};

#endif
