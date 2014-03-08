# rRpg Engine

Text-based role playing game engine written in python.

## Requirements

You'll need the following packages to run the game:
* python (2.7 or above)
* sqlite3

## Installation
## Setup

This program uses submodules. First thing to do is to compile the dungeon
generator:
```bash
git submodule init
git submodule update

cd externals/dungeon-generator/
make

cd ..
```

Then, you can use the test world (containing 2 cells, 1 dungeon, 1 PC,
2 objects):
```bash
# First, create the database
cd database
./createDb.sh
# Go back in the game folder
cd ..
# Then launch the game
# This will run the editor with the system locale
./rRpg

# This will run the editor in french
./rRpg-francais

# This will run the editor in english
./rRpg-english
```

Or you can use your own world (created with the game editor,
https://github.com/rrpg/world-editor ):
```bash
./rRpg -w /path/to/your/world.db
```
