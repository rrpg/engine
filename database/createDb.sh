#!/bin/bash
echo "rm existing db"
[ -f rpg.db ] && rm rpg.db

echo "creating db structure"
sqlite3 -init structure.sql rpg.db '.quit'

echo "inserting db values"
sqlite3 -init values.sql rpg.db '.quit'

