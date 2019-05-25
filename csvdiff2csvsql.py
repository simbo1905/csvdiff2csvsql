#!/usr/bin/env python
import sys, json
import argparse


def modified_to_queries(diff, left_name, right_name):
    result = ''
    pk_names = diff["_index"]
    changed = diff["changed"]
    keys = map(lambda c: c["key"], changed)
    result += query_via_pk(left_name, pk_names, keys)
    result += query_via_pk(right_name, pk_names, keys)
    return result


def query_via_pk(table, pk_names, keys):
    predicate = ''
    key_count = 0
    for key in keys:
        if key_count > 0:
            predicate += " or "
        pk_tuples = zip(pk_names, key)
        predicate += key_predicate(pk_tuples)
        key_count = key_count + 1
    result = 'csvsql --query "select * from ' + table + ' where '
    result += predicate
    result += "\" "+table+".csv"
    result += '\n'
    return result


def key_predicate(tuples):
    result = '( '
    key_count = 0
    for (name, value) in tuples:
        if key_count > 0:
            result += " and "
        result += name + "='" + value + "'"
        key_count = key_count + 1
    result += ' )'
    return result


def added_to_queries(diff, right_name):
    return rows_to_queries(diff, right_name, "added")


def rows_to_queries(diff, table, operation):
    pk_names = diff["_index"]
    changed = diff[operation]
    predicate = ''
    key_count = 0
    for add in changed:
        if key_count > 0:
            predicate += " or "
        pk_tuples = map(lambda n: (n, add[n]), pk_names)
        predicate += key_predicate(pk_tuples)
        key_count = key_count + 1
    result = 'csvsql --query "select * from '+table+" where "+predicate+'" '+table+'.csv'
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

