#!/bin/python3
import os
import re
import shutil
import json
import requests
import argparse
import random
import numpy as np
import matplotlib.pyplot as plt

parser = argparse.ArgumentParser(description='S.T.O.C.K.P.I.L.E System Update.')
parser.add_argument('-g', '--general', action='store', help='The file containing general store items.')
parser.add_argument('-t', '--trade', action='store', help='The file contianing random and trade items.')
parser.add_argument('-o', '--output', action='store', help='The output file to compare to and update. This should be a .input file with the lists formatted in the dnd-table format (see documentation).')

args = parser.parse_args()

def generate_and_plot_values(mean, percent_variance, num_values):
    """
    Generate a specified number of random values using the random_with_variance method and plot them.

    Args:
        mean (float): The mean value around which the random numbers will be generated.
        percent_variance (float): The percentage variance allowed from the mean.
        num_values (int): The number of random values to generate and plot.
    """
    values = [random_with_variance(mean, percent_variance) for _ in range(num_values)]

    plt.figure(figsize=(10, 6))
    plt.hist(values, bins=30, density=True, alpha=0.7, color='blue', edgecolor='black')
    plt.title(f"Random Numbers with {percent_variance}% Variance from Mean {mean}")
    plt.xlabel("Random Values")
    plt.ylabel("Frequency")
    plt.grid(True)
    plt.show()
    

def random_with_variance(mean, percent_variance):
    """
    Generate a random number with a specified percentage variance from a given mean value based on a normal distribution.

    Args:
        mean (float): The mean value around which the random number will be generated.
        percent_variance (float): The percentage variance allowed from the mean.

    Returns:
        float: A random number with the specified percentage variance from the mean.
    """
    if percent_variance < 0 or percent_variance > 100:
        raise ValueError("Percentage variance should be between 0 and 100")

    # Calculate standard deviation based on percent variance
    std_deviation = (percent_variance / 100) * mean

    # Generate a random number from a normal distribution
    random_value = np.random.normal(mean, std_deviation)

    return random_value
    

def convert_to_list(input_line):
    """
    This will take a string (raw list from the input file) formatted as "int,string,string,string,string,..." and convert it to a python list.

    Args:
        input (str): The input string to parse.

    Returns:
        output_list (list): The output list
    """
    if "," not in input_line:        
        return None
    elements = input_line.split(",")
    num_columns = int(elements[0])
    num_rows = int((len(elements)-1) / num_columns)
    print(f"num_columns: {num_columns}")
    print(f"num_rows: {num_rows}")

    output_list = []
    for i in range(0, num_rows):
        list_item = []
        for j in range (0, num_columns):
            list_item.append(elements[i*num_columns + j + 1]) #+1 to omit the first item.
        output_list.append(list_item)
                             
    return output_list


def get_old_lists(output_file):
    """
    This will return the list of items contained in the secified output list (the current list to be updated).

    Args:
        output_file (str): The output file name to retrieve the data from.
        
    Returns:
        old_general_list (list): A list of the old general items that were available.
        old_trade_list (list): A list of the old trade items that were available.
    """
    try:
        with open(output_file, 'r') as file:
            # Read all lines into a list
            lines = file.readlines()

            # remove newline characters from the end of each line
            lines = [line.strip() for line in lines]

        for line in lines:
            if "General Items[dnd-table]=" in line:
                old_general_list = convert_to_list(line.split("=")[1])
                
            if "Specialty Items[dnd-table]=" in line:
                old_trade_list = convert_to_list(line.split("=")[1])
                
    except FileNotFoundError:
        print(f"File not found: {file_path}")
        return None
    except Exception as e:
        print(f"Error reading file: {e}")
        return None

    return old_general_list, old_trade_list


def output_text(text, option = "text"):
    """
    Print text in different colors based on the provided option.`

    Args:
        option (str): The color option for the text. Valid options are "text", "warning", "error", "note", and "success".
        text (str): The text to be printed.

    Returns:
        None

    Note:
        This function uses ANSI escape codes for color formatting. Colors may not be displayed correctly in all environments.
    """
    color_codes = {
        "text": "\033[0m",  # Reset color
        "warning": "\033[93m",  # Yellow
        "error": "\033[91m",  # Red
        "note": "\033[94m",  # Blue
        "success": "\033[92m"  # Green
    }

    if option in color_codes:
        color_code = color_codes[option]
        reset_code = color_codes["text"]
        print(f"{color_code}{text}{reset_code}")
    else:
        print(text)


def append_to_file(file_path, string_to_append):
    """
    Append a string to a file.

    Parameters:
        file_path: The path to the file to append to.
        string_to_append: The string to append to the file.
    """
    with open(file_path, 'a') as file:
        file.write(string_to_append + '\n')


def read_lines_from_file(file_name):
    """
    Reads lines from a file and returns them as a list.

    Parameters:
        file_name (str): The name of the file to read.

    Returns:
        A list of strings, where each string represents a line from the file.
        Any leading and trailing whitespace is stripped from each line.

    Raises:
        FileNotFoundError: If the specified file does not exist.
        PermissionError: If the specified file cannot be opened due to insufficient permissions.
    """
    lines = []
    with open(file_name, 'r') as f:
        for line in f:
            line = line.strip()
            lines.append(line)
    return lines


def copy_file_to_directory(file_path, directory_path):
    """
    Copy a file to a directory.

    Args:
        file_path (str): The path to the file to copy.
        directory_path (str): The path to the directory to copy the file to.

    Raises:
        ValueError: If the file or directory doesn't exist.

    Returns:
        None
    """

    # Check if the file exists
    if not os.path.isfile(file_path):
        raise ValueError("File does not exist")

    # Check if the directory exists
    if not os.path.isdir(directory_path):
        output_text(f"Directory {directory_path} does not exist. Creating directory...", "note")
        os.makedirs(directory_path)

    new_file = directory_path + "/" + file_path.split('/')[-1].strip()
    if not os.path.isfile(new_file):
        # Copy the file to the directory
        output_text(f"Copying {file_path} to {directory_path}", "note")
        shutil.copy(file_path, directory_path)
        output_text(f"File {file_path} copied to {directory_path}", "note")
    else:
        output_text(f"file {new_file} already exists!", "warning")


def move_file_to_directory(file_path, directory_path):
    """
    Move a file to a directory.

    Args:
        file_path (str): The path to the file to move.
        directory_path (str): The path to the directory to move the file to.

    Raises:
        ValueError: If the file or directory doesn't exist.

    Returns:
        None
    """
    # Check if the file exists
    if not os.path.isfile(file_path):
        raise ValueError("File does not exist")

    # Check if the directory exists
    if not os.path.isdir(directory_path):
        output_text(f"Directory {directory_path} does not exist. Creating directory...", "note")
        os.makedirs(directory_path)

    new_file = os.path.join(directory_path, os.path.basename(file_path))
    if not os.path.isfile(new_file):
        # Move the file to the directory
        output_text(f"Moving {file_path} to {directory_path}", "note")
        shutil.move(file_path, directory_path)
        output_text(f"File {file_path} moved to {directory_path}", "note")
    else:
        output_text(f"File {new_file} already exists!", "warning")


def move_file(source_file_path, destination_folder_path):
    """
    Move a file from the source path to the destination folder.

    Args:
        source_file_path (str): The path to the file to be moved.
        destination_folder_path (str): The path to the destination folder.

    Returns:
        None
    """

    # Create the destination folder if it doesn't exist
    if not os.path.exists(destination_folder_path):
        os.makedirs(destination_folder_path)

    # Use shutil.move() to move the file to the destination folder
    shutil.move(source_file_path, destination_folder_path)


def get_random_line(file_path):
    """
    Return a random line from a file.

    Args:
        file_path (str): The path to the file.

    Returns:
        str: A random line from the file.

    Raises:
        FileNotFoundError: If the file does not exist.
        IOError: If there is an error reading the file.
    """
    try:
        with open(file_path, "r") as file:
            lines = file.readlines()
            random_line = random.choice(lines)
            return random_line.strip()
    except FileNotFoundError:
        raise FileNotFoundError(f"File not found: {file_path}")
    except IOError:
        raise IOError(f"Error reading file: {file_path}")


if __name__ == '__main__':
    print("Running app")
    if args.output is not None:
        old_general_list, old_trade_list = get_old_lists(args.output)
    print(old_general_list)
    print(old_trade_list)
        
    # Test usage:
    mean_value = 100  # mean value
    percent_variance = 5  # percentage variance
    num_values = 1000 # number of test values 
    generate_and_plot_values(mean_value, percent_variance, num_values)
