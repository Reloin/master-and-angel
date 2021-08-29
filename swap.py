import json

angel_file = open("angel.json", "w")

angel_file.write("{\n")
with open("master.json") as f:
    data = json.load(f)
    for key, value in data.items():
        angel_file.write("\t\"{}\":\"{}\",\n".format(value, key))
angel_file.write("\t\"eof\":\"eof\"\n")
angel_file.write("}")

angel_file.close()