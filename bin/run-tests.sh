#!/bin/bash

python_versions='python2 python3'

for l in 'fr_FR' 'en_GB'
do
	echo "Locale $l"

	for p in $python_versions
	do
		if [ ! -z "$(which $p)" ]
		then
			echo "$p"
			LC_MESSAGES=$l $p run-tests.py
			if [ $? == 1 ]
			then
				exit
			fi

		fi
	done
done
