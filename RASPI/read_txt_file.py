import ast

with open("config.txt", "r") as data:
    configuration_settings = ast.literal_eval(data.read())
    
    print(configuration_settings["email"])