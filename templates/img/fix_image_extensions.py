import os

def rename_jpeg_to_jpg():
    current_folder = os.getcwd()  # Get the current folder path
    files = os.listdir(current_folder)  # List all files in the current folder

    for file in files:
        if file.endswith(".jpeg"):  # Check if the file has a .jpeg extension
            new_name = file.replace(".jpeg", ".jpg")  # Create the new name with .jpg extension
            os.rename(file, new_name)  # Rename the file

rename_jpeg_to_jpg()

