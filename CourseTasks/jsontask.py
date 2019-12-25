import json

inp = input().rstrip()
data = json.loads(inp)
family = {child['name']: child['parents'] for child in data}
for child, parents in family.items():
    relatives = parents
    for relative in relatives:
        relatives += family[relative]
    family[child] = set(relatives)
descendants = {key: 1 for key in family.keys()}
for _, parents in family.items():
    for parent in parents:
        if parent in descendants:
            descendants[parent] += 1
result = list(descendants.items())
result.sort()
for key, value in result:
    print(key + ' : ' + str(value))
