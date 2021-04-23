import json
file = open("records.json","r")
print(json.dumps(file.read()))