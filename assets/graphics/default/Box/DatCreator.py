import json
def modify(content):
    option = content["contain"]["options"]
    option["top"] = "fullRepeat"
    option["right"] = "fullRepeat"
    option["left"] = "fullRepeat"
    option["middle"] = "fullRepeat"
    option["bottom"] = "fullRepeat"
    mapping = content["cropping"]
    mapping["top"] = [5,0,4,5]
    mapping["topRight"] = [9,0,5,5]
    mapping["left"] = [0,5,5,4]
    mapping["middle"] = [5,5,4,4]
    mapping["right"] = [9,5,5,4]
    mapping["bottomLeft"] = [0,9,5,5]
    mapping["bottom"] = [5,9,4,5]
    mapping["bottomRight"] = [9,9,5,5]
    

filePath = "redBoard.dat"
modify = modify
default = {}

contents = None

try:
    with open(filePath, mode="r", encoding="utf-16") as file:
        contents = json.load(file, encoding="utf-16")
except NameError:
    print("Could not file so it will be created")
    contents = default
except ValueError:
    print("File could not be read so it will be rewriten")
    contents = default

print(contents)
modify(contents)

with open(filePath, mode="w", encoding="utf-16") as file:
    file.write(json.dumps(contents, ensure_ascii=False))

