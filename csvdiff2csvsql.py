import json

def diff2sql(diff):
    result = ''
    obj = json.loads(diff)
    index=obj["_index"]
    #result += 'index size: ' + str(len(index))
    changed = obj["changed"]
    for change in changed:
        result += str(change["key"])
        result += '\n'
    return result

