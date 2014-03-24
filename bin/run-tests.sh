#!/bin/sh

cd database
./createDb.sh
cd ..
python tests/commands/look.py
