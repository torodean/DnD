import os

# Define the directory structure
structure = {
    "campaign": {
        "locations": {
            "dungeons": {},
            "cities": {},
            "landmarks": {},
            "towns": {}
        },
        "items": {
            "consumables": {},
            "magic": {},
            "weapons": {},
            "armor": {}
        },
        "notes": {},
        "creatures": {
            "animals": {},
            "monsters": {}
        },
        "lore": {
            "history": {},
            "factions": {},
            "deities": {}
        },
        "quests": {},
        "characters": {
            "player": {},
            "non-player": {}
        },
        "spells": {}
    }
}

# Define the root directory
root_dir = "."

# Define a function to create directories recursively
def create_dirs(path, structure):
    for key in structure:
        os.makedirs(os.path.join(path, key))
        if structure[key]:
            create_dirs(os.path.join(path, key), structure[key])

# Call the function to create the directories
create_dirs(root_dir, structure)

