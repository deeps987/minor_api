import json
from os import path
 
queries = None
prompts = None
menu = None
inputs = None
constant = None
 
path_current_directory = path.dirname(__file__)
 
 
filepath = path.join(path_current_directory , "../data.json")
with open(filepath, "r") as file:
    data = json.load(file)
    queries = data["queries"]
    menu = data["menu"]
    prompts = data["prompts"]
    inputs = data["inputs"]
    constant = data["constant"]