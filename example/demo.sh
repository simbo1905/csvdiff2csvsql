#!/bin/bash
csvdiff one,two left.csv right.csv |../csvdiff2csvsql.py left right | bash 2>/dev/null
echo Added:
cat added | bash 2>/dev/null
echo Modified:
cat modified | bash 2>/dev/null
echo Removed:
cat removed | bash 2>/dev/null
