# csvdiff2csvsql

A script that takes the output of [csvdiff](https://github.com/larsyencken/csvdiff) and generates [csvquery](https://csvkit.readthedocs.io/en/latest/) commands to extract the rows that are added, removed and modified. The motivation for this script is help humans inspect change that appear in large CSV reports.

# Example

```
$ head left.csv right.csv 
==> left.csv <==
one,two,three
d,e,f
j,k,l
m,n,o
p,q,r
w,x,y

==> right.csv <==
one,two,three
a,b,c
d,e,1
j,k,l
m,n,2
s,t,u

$ csvdiff one,two left.csv right.csv |./csvdiff2csvsql.py left right

$ head added removed modified
==> added <==
csvsql --query "select * from right where 1=1 and one='a' and two='b'" right.csv
csvsql --query "select * from right where 1=1 and one='s' and two='t'" right.csv

==> removed <==
csvsql --query "select * from left where 1=1 and one='p' and two='q'" left.csv
csvsql --query "select * from left where 1=1 and one='w' and two='x'" left.csv

==> modified <==
csvsql --query "select * from left where 1=1 and one='d' and two='e'" left.csv
csvsql --query "select * from right where 1=1 and one='d' and two='e'" right.csv
csvsql --query "select * from left where 1=1 and one='m' and two='n'" left.csv
csvsql --query "select * from right where 1=1 and one='m' and two='n'" right.csv
```

Note that csvquery outputs the header for each query and each query selects only one file. You can run all the commands and filter out all the headers using awk with:

```
echo Added
bash < added | awk 'NR % 2 == 0' 2>/dev/null
echo Removed
bash < removed | awk 'NR % 2 == 0' 2>/dev/null
echo Modified
bash < modified | awk 'NR % 2 == 0' 2>/dev/null
```

This will give output:

```
Added
a,b,c
s,t,u
Removed
p,q,r
w,x,y
Modified
d,e,f
d,e,1
m,n,o
m,n,2
```

Note that the modifed query shows each changed line from the first file followed by the new line in the second file. 
