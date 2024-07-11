#!/bin/python3 

# This file will create the json file appropriate for files within a folder
# so they can be imported into Wonderdraft.

import os
import argparse

parser = argparse.ArgumentParser(description='MMORPDND Creator Tool.')
parser.add_argument('-f', '--folder', action='store', help='The folder to parse for files.', required=True)

args = parser.parse_args()

def get_files(folder_path):
    """
    Returns the list of PNG image files in the directory.
    """
    files = []
    for dirpath, dirnames, filenames in os.walk(folder_path):
        for filename in filenames:
            if ".png" in filename:
                print(f"Found file: {filename}")
                files.append(f"{filename}")

    return files
    

def make_json_block(file_name):
    return "\t\"{0}\": {{\n\t\t\"name\": \"{0}\",\n\t\t\"radius\": 27,\n\t\t\"offset_x\": 0,\n\t\t\"offset_y\": 0,\n\t\t\"draw_mode\": \"normal\"\n\t}},\n".format(file_name)


if __name__ == '__main__':
    print(f"Input folder: {args.folder}")
    json_content = "{\n"
    files = get_files(args.folder)
    for file in files:
        json_block = make_json_block(file[:-4])
        json_content += json_block
        print(json_block)
        
    json_content = json_content[:-2]
    json_content += "\n}"
    
    print(json_content)
    
    json_file = args.folder + "\.wonderdraft_symbols"
    
    with open(json_file, 'w') as f:
        f.write(json_content)