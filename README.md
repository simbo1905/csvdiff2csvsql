# csvdiff2csvsql

A script that takes the output of [csvdiff](https://github.com/larsyencken/csvdiff) and generates [csvquery](https://csvkit.readthedocs.io/en/latest/) commands to extract the rows that are added, removed and modified. The motivation for this script is to help people inspect sparse differences in large CSV reports.

# Prerequisites

```
pip install csvdiff
pip install csvkit
```

# Example

The following example is in the folder `example` which you can run as `demo.sh`.

Here are the two files we want to diff based on a compound key of the first two columns:

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
```

We run diff and pipe it to csvdiff2csvsql:

```bash
$ csvdiff one,two left.csv right.csv |./csvdiff2csvsql.py left right
```

This gives us three files. One to extract added lines, one to extract removed lines, and one to extract modified lines:

```bash
$ head added removed modified
==> added <==
csvsql --query "select * from right where ( one='a' and two='b' ) or ( one='s' and two='t' )" right.csv
==> removed <==
csvsql --query "select * from left where ( one='p' and two='q' ) or ( one='w' and two='x' )" left.csv
==> modified <==
csvsql --query "select * from left where ( one='d' and two='e' ) or ( one='m' and two='n' )" left.csv
csvsql --query "select * from right where ( one='d' and two='e' ) or ( one='m' and two='n' )" right.csv
```

We can run one of them by throwing it at bash:

`bash < removed`

Let's run all three with some display output:

```
set echo off
echo
printf 'Added\n====='
bash < added 
echo
printf 'Removed\n====='
bash < removed
echo
printf 'Modified\n====='
bash < modified
set echo on
```

This will give output:

```
Added
=====
one,two,three
a,b,c
s,t,u

Removed
=======
one,two,three
p,q,r
w,x,y

Modified
========
one,two,three
d,e,f
m,n,o
one,two,three
d,e,1
m,n,2
```

The modified output is selecting the changed lines from `left.csv` and then `right.csv`. We can redirect this into 
two files: 

```bash
# first redirect into two files 1.txt and 2.txt
printf ' > 1.txt\n > 2.txt' > redirects
paste modified redirects | bash
```

Which gives us the following two files: 

```bash
head 1.txt 2.txt
==> 1.txt <==
one,two,three
d,e,f
m,n,o

==> 2.txt <==
one,two,three
d,e,1
m,n,2
```

We can use the command `paste` to interlace these two files into a single file with the changes stacked together in pairs which is easier to check by eye: 

```bash
paste -d '\n' 1.txt 2.txt
```

This outputs: 

```bash
one,two,three
one,two,three
d,e,f
d,e,1
m,n,o
m,n,2
```
