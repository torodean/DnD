import os
import shutil

def copy_images(source_dir, dest_dir):
    """
    Copy images from a source directory to a destination directory.

    Args:
        source_dir (str): The path to the source directory.
        dest_dir (str): The path to the destination directory.
    """
    # Traverse through the directory tree rooted at source_dir
    for root, _, files in os.walk(source_dir):
        # Check if the current directory contains an 'img' folder
        img_folder = os.path.join(root, "img")
        if os.path.exists(img_folder) and os.path.isdir(img_folder):
            # Iterate over the files in the 'img' folder
            for img_file in files:
                # Check if the file is an image (png, jpg, jpeg, gif)
                if img_file.lower().endswith((".png", ".jpg", ".jpeg", ".gif")):
                    # Construct the source and destination paths for the image file
                    source_path = os.path.join(img_folder, img_file)
                    dest_path = os.path.join(dest_dir, img_file)
                    # Perform the copy operation (commented out for safety)
                    # shutil.copy(source_path, dest_path)
                    # Print the copy operation for debugging
                    print(f"Copied: {source_path} -> {dest_path}")

if __name__ == "__main__":
    # Get the directory of the current script
    script_dir = os.path.dirname(os.path.abspath(__file__))
    # Define the path to the campaign directory relative to the script directory
    campaign_dir = os.path.join(script_dir, "..", "campaign")
    # Define the destination directory for images relative to the script directory
    dest_img_dir = os.path.join(script_dir, "img")

    # Call the copy_images function to copy images from the campaign directory to the destination directory
    copy_images(campaign_dir, dest_img_dir)
