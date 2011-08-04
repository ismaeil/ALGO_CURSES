#! /bin/sh
#File : runs all commands i need for each coverage testing
#Directory : this files is in my project directory
#Author : Ismaeil Abouljamal
#WARNING : ce script doit s'executer dans le répértoire parent du répértoire htmlcov

if [ -d htmlcov ]; then
    #0- clean everything
    coverage -e
    #1- go to the right folder
    cd ./table/
    #2- run tests
    coverage -x ./test_all_code.py
    #3- what about the coverage
    coverage -r ordonancement.py import_export.py utils.py
    #4- generate html
    coverage html -d ../htmlcov
else
    echo "\nLe script doit s'exécuter dans le même répértoire que htmlcov\n"
fi
