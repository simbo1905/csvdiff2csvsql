import json


def modified_to_queries(diff, left_name, right_name):
    result = ''
    obj = json.loads(diff)
    pk_names=obj["_index"]
    print str(pk_names)
    changed = obj["changed"]
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

