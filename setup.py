import json
import setuptools

with open("README.md", "r") as f:
    description = f.read()

config = json.load(open("config.json"))
config["long_description"] = description

setuptools.setup(**config)
