#!/bin/bash

if [ -z "$1" ] || [ ! -f tests/commands/$1.py ]
then
	commands='testLook testTake testDrop testMove testEnter testExit testHelp testInventory testTalk testCreatePlayer'
else
	commands=$1
fi
python_versions='python2 python3'

for l in 'fr_FR' 'en_GB'
do
	echo "Locale $l"

	for p in $python_versions
	do
		if [ ! -z "$(which $p)" ]
		then
			echo "$p"
			for c in $commands
			do
				echo "Processing $c"
				LC_MESSAGES=$l $p tests/commands/$c.py
				if [ $? == 1 ]
				then
					exit
				fi
			done
		fi
	done
done
