#!/bin/sh

cd database
./createDb.sh
cd ..
python tests/commands/look.py
python tests/commands/take.py
python tests/commands/drop.py
