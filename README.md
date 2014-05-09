# rRpg Engine

Text-based role playing game engine written in python.

## Requirements

You'll need the following packages to run the game:
* python (2.7 or above)
* sqlite3
* coverage.py (for the code coverage only)

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
# If in the editor you exported your world and set it as default
./rRpg
# If you want to use another world than the default world
./rRpg -w /path/to/your/world.db
```

## Documentation

The documentation is being written and is available
[here](http://rrpg.github.io/engine).

## Tests

To run the tests, run the file
```
bin/run-tests.sh
```
All the commands will be tested in french and english in python 2 and/or 3
(depending on which version is installed on the user's computer).

## Code coverage

To run the code coverage, you will need coverage.py
((http://nedbatchelder.com/code/coverage/)).

Once coverage.py is installed, just run:

```
make coverage
```

An HTML output of the coverage will be generated in the folder htmlcov at the
root of the project's folder
