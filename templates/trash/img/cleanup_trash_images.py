#!/bin/python3

import os


def get_image_files(directory):
    """
    Gets a list of image files in the specified directory.
    
    Args:
        directory (str): The path to the directory to search for image files.
        
    Returns:
        list: A list of image filenames in the directory.
    """
    image_extensions = {'.png', '.jpg', '.jpeg', '.gif', '.bmp', '.tiff'}
    return [f for f in os.listdir(directory) if os.path.isfile(os.path.join(directory, f)) and os.path.splitext(f)[1].lower() in image_extensions]


def find_and_delete_images(script_folder, database_folder):
    """
    Searches for images in the database folder that match the names of images in the script folder,
    and deletes the matching images from the script folder.
    
    Args:
        script_folder (str): The path to the script folder containing images to check.
        database_folder (str): The path to the database folder to search for matching images.
    """
    script_images = get_image_files(script_folder)
    for root, _, files in os.walk(database_folder):
        for file in files:
            if file in script_images:
                print(f"Found matching file: {file}")
                file_path = os.path.join(script_folder, file)
                if os.path.isfile(file_path):
                    os.remove(file_path)
                    print(f"Deleted {file_path}!")

if __name__ == "__main__":
    script_folder = os.path.abspath('.')  # Current directory
    database_folder = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../campaign/'))  # Relative path to database folder
    find_and_delete_images(script_folder, database_folder)

