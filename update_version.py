import json

config = json.load(open("config.json"))
current_version = config["version"]

v1, v2, v3 = current_version.split(".")

if v3 == "9":
    v3 = "0"
    v2 = str(int(v2) + 1)

elif v2 == "9":
    v2 = "0"
    v1 = str(int(v1) + 1)

else:
    v3 = str(int(v3) + 1)

new_version = ".".join([v1, v2, v3])
config["version"] = new_version

json.dump(config, open("config.json", "w"), indent=4)

with open('kivy4/__init__.py', 'r') as f:
    lines = f.readlines()

    for line in lines:
        if line.startswith('__version__'):
            lines[lines.index(line)] = f"__version__ = '{new_version}'\n"
            break

    with open('kivy4/__init__.py', 'w') as f1:
        f1.writelines(lines)