import json

a = {
    'a': 'a'
}

b = {
    'b': 'b'
}

c = {
    **a,
    'b': b
}

print(json.dumps(c, indent=4))