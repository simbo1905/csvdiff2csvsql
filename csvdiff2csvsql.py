#!/usr/bin/env python
import sys, json
import argparse


def modified_to_queries(diff, left_name, right_name):
    result = ''
    pk_names = diff["_index"]
    changed = diff["changed"]
    for change in changed:
        pk_values = change["key"]
        result += query_via_pk(left_name, pk_names, pk_values)
        result += query_via_pk(right_name, pk_names, pk_values)
    return result


def query_via_pk(table, pk_names, pk_values):
    result = 'csvsql --query "select * from ' + table + ' where 1=1'
    tuples = zip(pk_names, pk_values)
    for (name, value) in tuples:
        result += " and " + name + "='" + value + "'"
    result += "\" "+table+".csv"
    result += '\n'
    return result


def added_to_queries(diff, right_name):
    return rows_to_queries(diff, right_name, "added")


def rows_to_queries(diff, right_name, operation):
    result = ''
    pk_names = diff["_index"]
    changed = diff[operation]
    for add in changed:
        pk_tuples = map(lambda n: (n, add[n]), pk_names)
        pk_names, pk_values = zip(*pk_tuples)
        result += query_via_pk(right_name, pk_names, pk_values)
    return result


def removed_to_queries(diff, right_name):
    return rows_to_queries(diff, right_name, "removed")


if __name__ == '__main__':
    parser = argparse.ArgumentParser(epilog="This program reads cvsdiff from stdin and generates csvquery commands to execute")
    parser.add_argument("first_csv", help="The first csv file to compare")
    parser.add_argument("second_csv", help="The second csv file to compare")
    args = parser.parse_args()
    left = args.first_csv
    right = args.second_csv
    output_prefix=""
    diff = json.load(sys.stdin)
    f = open("added", "w")
    f.write(added_to_queries(diff, right))
    f.close()
    f = open("removed", "w")
    f.write(removed_to_queries(diff, left))
    f.close()
    f = open("modified", "w")
    f.write(modified_to_queries(diff, left, right))
    f.close()

