import os
import shutil

def copy_images(source_dir, dest_dir):
    """
    Copy images from a source directory to a destination directory.

    Args:
        source_dir (str): The path to the source directory.
        dest_dir (str): The path to the destination directory.
    """
    print(f"Running copy_images({source_dir}, {dest_dir})")
    # Traverse through the directory tree rooted at source_dir
    for root, _, files in os.walk(source_dir):
        # Check if the current directory is the 'img' folder
        if os.path.basename(root) == 'img':
            print(f"Detected image directory: {root}")
            # Iterate over the files in the 'img' folder
            for img_file in files:
                print(f"File found: {img_file}")
                # Check if the file is an image (png, jpg, jpeg, gif)
                if img_file.lower().endswith((".png", ".jpg", ".jpeg", ".gif")):
                    print(f"Image file detected: {img_file}")
                    # Construct the source and destination paths for the image file
                    source_path = os.path.join(root, img_file)
                    dest_path = os.path.join(dest_dir, img_file)
                    print(f"Source path of image: {source_path}")
                    print(f"Destination path of image: {dest_path}")
                    # Perform the copy operation
                    shutil.copy(source_path, dest_path)
                    # Print the copy operation for debugging
                    print(f"Copied: {source_path} -> {dest_path}")


def delete_html_files(directory):
    """
    Delete all .html files in a directory and its subdirectories.

    Args:
        directory (str): The path to the directory.
    """
    print(f"Running delete_html_files({directory})")
    # Traverse through the directory tree rooted at directory
    for root, _, files in os.walk(directory):
        # Iterate over the files in the directory
        print(f"Detected directory: {root}")
        for html_file in files:
            # Check if the file is an HTML file
            if html_file.lower().endswith(".html"):
                # Construct the path to the HTML file
                file_path = os.path.join(root, html_file)
                print(f"HTML file detected: {file_path}")
                # Delete the HTML file
                os.remove(file_path)
                # Print the deletion operation for debugging
                print(f"Deleted: {file_path}")


def move_input_files(source_dir, dest_dir):
    """
    Move .input or .char files from a source directory to a destination directory.

    Args:
        source_dir (str): The path to the source directory.
        dest_dir (str): The path to the destination directory.
    """
    print(f"Running move_input_files({source_dir}, {dest_dir})")
    # Ensure destination directory exists
    if not os.path.exists(dest_dir):
        os.makedirs(dest_dir)

    # Traverse through the directory tree rooted at source_dir
    for root, _, files in os.walk(source_dir):
        print(f"Detected directory: {root}")
        # Iterate over files in the current directory
        for file in files:
            print(f"File found: {file}")
            # Check if the file ends with ".input" or ".char"
            if file.lower().endswith((".input", ".char")):
                print(f".input or .char file detected: {file}")
                # Construct source and destination paths
                source_path = os.path.join(root, file)
                dest_path = os.path.join(dest_dir, file)
                # Move the file
                shutil.move(source_path, dest_path)
                # Print for debugging
                print(f"Moved: {source_path} -> {dest_path}")


if __name__ == "__main__":
    # Get the directory of the current script
    script_dir = os.path.dirname(os.path.abspath(__file__))
    # Define the path to the campaign directory relative to the script directory
    campaign_dir = os.path.join(script_dir, "..", "campaign")
    # Define the destination directory for images relative to the script directory
    dest_img_dir = os.path.join(script_dir, "img")
    # Define the trash directory relative to the script directory
    trash_dir = os.path.join(script_dir, "trash")
    # Define the input_files directory relative to the script directory
    input_files_dir = os.path.join(script_dir, "input_files")

    # Call the copy_images function to copy images from the campaign and trash directory to the destination directory
    copy_images(campaign_dir, dest_img_dir)
    copy_images(trash_dir, dest_img_dir)
    
    # Call the delete_html_files function to delete HTML files from the specified directory
    delete_html_files(campaign_dir)
    
    # Call move_input_files function to move input files
    move_input_files(trash_dir, input_files_dir)
