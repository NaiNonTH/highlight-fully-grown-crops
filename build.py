import json
import os
import shutil
import re

shutil.rmtree("pack", ignore_errors=True)
os.makedirs("pack")
os.makedirs("pack/assets/minecraft/blockstates")

shutil.copyfile("templates/pack.mcmeta", "pack/pack.mcmeta")
shutil.copytree("templates/models", "pack/assets/minecraft/models/block")
shutil.copytree("templates/textures", "pack/assets/minecraft/textures/block")

with open("blockstates.json", "r") as data:
    blockstates = json.load(data)

for highlight_name in blockstates.keys():
    stopper = highlight_name.find("__")

    if stopper == -1:
        blockstate_file = highlight_name
    else:
        blockstate_file = highlight_name[:stopper]

    with open(f"templates/blockstates/{blockstate_file}.json", "r") as bs_file:
        template = bs_file.read()

    parsed_templ = template.replace("{", "{{")      \
                           .replace("}", "}}")
    parsed_templ = re.sub(r"%(.+)%", r"{\1}", parsed_templ)

    i_blockstate = blockstates[highlight_name]

    if type(i_blockstate) == list:
        for block_name in i_blockstate:
            to_write = parsed_templ.format(template=highlight_name, name=block_name)

            with open(f"pack/assets/minecraft/blockstates/{block_name}.json", "w") as writer:
                writer.write(to_write)
    elif type(i_blockstate) == dict:
        for block_name in i_blockstate["blocks"]:
            to_write = parsed_templ.format(template=i_blockstate["model"], name=block_name)

            with open(f"pack/assets/minecraft/blockstates/{block_name}.json", "w") as writer:
                writer.write(to_write)


print("success!")