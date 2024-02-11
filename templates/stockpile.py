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
from prettytable import PrettyTable

parser = argparse.ArgumentParser(description='S.T.O.C.K.P.I.L.E System Update.')
parser.add_argument('-g', '--general',
                    required=True,
                    action='store',
                    help='The file containing general store items.')
parser.add_argument('-t', '--trade',
                    required=True,
                    action='store',
                    help='The file containing random and trade items.')
parser.add_argument('-o', '--output',
                    required=True,
                    action='store',
                    help='The output file to compare to and update. This should be a .input file with the lists '
                         'formatted in the dnd-table format (see documentation).')

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
    if ";" not in input_line:
        return None
    elements = input_line.split(";")
    num_columns = int(elements[0])
    num_rows = int((len(elements) - 1) / num_columns)
    output_text(f"num_columns: {num_columns}", "note")
    output_text(f"num_rows: {num_rows}", "note")

    output_list = []
    for i in range(0, num_rows):
        list_item = []
        for j in range(0, num_columns):
            list_item.append(elements[i * num_columns + j + 1])  # +1 to omit the first item.
        output_list.append(list_item)

    return output_list


def get_master_list(input_file):
    """
    This will get the items from the master lists and convert them to python lists. These files should be formatted with a single item per line (csv like). They should have 3 elements, item name, price, and description separated by a comma delimiter.
    
    Args:
        input_file (str): The file name of the items list.
        
    Returns:
        output_list (list): The list of general items.
    """
    try:
        output_list = []
        with open(input_file, 'r') as file:
            # Read all lines into a list
            lines = file.readlines()

            # remove newline characters from the end of each line
            lines = [line.strip() for line in lines]

        for line in lines:
            if ";" in line:
                list_items = line.split(";")
                output_list.append(list_items)

    except FileNotFoundError:
        print(f"File not found: {file_path}")
        return None
    except Exception as e:
        print(f"Error reading file: {e}")
        return None

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
        old_general_list = ""
        old_trade_list = ""

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

        return old_general_list, old_trade_list

    except FileNotFoundError:
        print(f"File not found: {output_file}")
        return None
    except Exception as e:
        print(f"Error reading file: {e}")
        return None


def output_text(text, option="text"):
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


def find_items_not_in_old_list(old_list, master_list):
    """
    Compare the old list to the master list and return items that are in the master list but not the old list.

    Args:
        old_list (list): The old list.
        master_list (list): The current master list.

    Returns:
        list: Items from master_list that are not found in the old_list.
    """
    old_item_names = set(item[0] for item in old_list)
    items_not_in_old_list = [item for item in master_list if item[0] not in old_item_names]

    return items_not_in_old_list


def randomly_remove_elements(input_list, num_elements_to_remove):
    """
    Randomly remove a specified number of elements from a list.

    Args:
        input_list (list): The input list.
        num_elements_to_remove (int): The number of elements to randomly remove.

    Returns:
        tuple: A tuple containing the modified list (without removed elements) and the removed elements.
    """
    if num_elements_to_remove >= len(input_list):
        return input_list, []

    random_indices = random.sample(range(len(input_list)), num_elements_to_remove)
    removed_elements = [input_list.pop(index) for index in sorted(random_indices, reverse=True)]

    return input_list, removed_elements


def print_table(data, header=None, max_width=60):
    """
    Print a list in a nicely formatted table with word wrap. This will automatically set the header for tables of
    length 3 or 4 based on the expected headers of ["item", "base price", "description"] or ["item", "base price",
    "sell price", "description"] respectively.

    Args:
        data (list): The list to be printed.
        header (list): The header of the table.
        max_width (int): The maximum width for each column. Default is 20.
    """
    if len(data[0]) == 3:
        header = ["item", "base price", "description"]
    elif len(data[0]) == 4:
        header = ["item", "base price", "sell price", "description"]
    table = PrettyTable()
    table.field_names = header

    # Set max width for each column
    for col in header:
        table.max_width[col] = max_width

    for row in data:
        table.add_row(row)

    print(table)


def randomly_select_items(input_list, n):
    """
    Randomly select n items from a list and return a new list with those items.

    Args:
        input_list (list): The input list.
        n (int): The number of items to randomly select.

    Returns:
        list: A new list containing the randomly selected items.
    """
    if n >= len(input_list):
        return input_list

    selected_items = random.sample(input_list, n)

    return selected_items


def fix_list(items_list, default_sell_value='default_sell'):
    """
    Fixes some issues with combining the two types of lists. Also updates some values in that list.
        - Add a sell spot to each item with only 3 elements in a list.
        - Alphabetizes the list.

    Args:
        items_list (list): The input list containing items.
        default_sell_value (str): The default value for the sell spot.

    Returns:
        list: A new list with sell spots added to items with only 3 elements.
    """
    updated_list = []

    for item in items_list:
        if len(item) == 3:
            item.insert(2, default_sell_value)
        updated_list.append(item)

    updated_list = alphabetize_list(updated_list)

    return updated_list


def alphabetize_list(input_list):
    """
    Alphabetize a list based on the first element.

    Args:
        input_list (list): The input list.

    Returns:
        list: A new list alphabetized based on the first element.
    """
    return sorted(input_list, key=lambda x: x[0])


def adjust_buy_prices(items_list, variance=10):
    """
    Calculate the buy price as a variance from the base price. 

    Args:
        items_list (list): The input list containing items.
        variance (int): The variance of the buy price to use (default is 10).

    Returns:
        list: A new list with buy prices calculated based on the base/original buy prices.
    """
    updated_list = []

    for item in items_list:
        percentage = random_with_variance(100, 5) / 100
        buy_price = float(item[1])
        new_buy_price = buy_price * percentage
        updated_item = [item[0], new_buy_price, item[2], item[3]]
        updated_list.append(updated_item)

    return updated_list


def calculate_sell_percentage(items_list, percentage=75):
    """
    Calculate the sell price as a percentage of the buy price for each item in a list. The percentage will be somewhat randomized and a 10 percent variance from what is entered. 

    Args:
        items_list (list): The input list containing items.
        percentage (float): The percentage of the buy price to use for the sell price. Default is 95% (0.95).

    Returns:
        list: A new list with sell prices calculated based on the buy prices.
    """
    updated_list = []

    for item in items_list:
        percent_multiplier = random_with_variance(percentage, 10) / 100
        buy_price = float(item[1])
        sell_price = buy_price * percent_multiplier
        updated_item = [item[0], buy_price, sell_price, item[3]]
        updated_list.append(updated_item)

    return updated_list


def convert_to_dnd_currency(value):
    """
    Convert a float value to a string in Dungeons and Dragons currency format.

    Args:
        value (float): The input value in gold units.

    Returns:
        str: A string representing the value in the format (##g ##s ##c).
    """
    # Ensure the value is non-negative
    if value < 0.0:
        output_text(f"ERROR: value {value} is negative! in convert_to_dnd_currency({value}) method!", option='error')
        return

    # Calculate gold, silver, and copper amounts
    gold_amount = int(value)
    silver_amount = int((value - gold_amount) * 10)
    copper_amount = int(((value - gold_amount) * 10 - silver_amount) * 10)

    result_parts = []

    if gold_amount:
        result_parts.append(f"{gold_amount}g")
    if silver_amount:
        result_parts.append(f"{silver_amount}s")
    if copper_amount:
        result_parts.append(f"{copper_amount}c")

    result_string = " ".join(result_parts)

    return result_string


def convert_from_dnd_currency(currency_string):
    """
    Convert a Dungeons and Dragons currency string to a float value.

    Args:
        currency_string (str): The input string in Dungeons and Dragons currency format.

    Returns:
        float: The equivalent value in gold units.
    """
    parts = currency_string.split()

    gold_amount = 0
    silver_amount = 0
    copper_amount = 0

    for part in parts:
        if 'g' in part:
            gold_amount = int(part.replace('g', ''))
        elif 's' in part:
            silver_amount = int(part.replace('s', ''))
        elif 'c' in part:
            copper_amount = int(part.replace('c', ''))

    total_value = gold_amount + (silver_amount / 10) + (copper_amount / 100)

    return total_value


def convert_prices_to_dnd_format(item_list):
    """
    Convert buy and sell prices in a list to Dungeons and Dragons currency format.

    Args:
        item_list (list): The input list containing items.

    Returns:
        list: A new list with buy and sell prices in Dungeons and Dragons currency format.
    """
    updated_list = []

    for item in item_list:
        item_name = item[0]
        buy_price = item[1]
        sell_price = item[2]
        description = item[3]

        dnd_buy_price = convert_to_dnd_currency(buy_price)
        dnd_sell_price = convert_to_dnd_currency(sell_price)

        updated_item = [item_name, dnd_buy_price, dnd_sell_price, description]
        updated_list.append(updated_item)

    return updated_list


def convert_to_one_line(list_of_lists):
    """
    Convert a list of lists to a single line string with comma delimiters.

    Args:
        list_of_lists (list): The input list of lists.

    Returns:
        str: A single line string with comma delimiters.
    """
    result = ""

    for sublist in list_of_lists:
        line = ", ".join(sublist)
        result += line + ", "

    # Remove the trailing comma and space
    result = result.rstrip(", ")

    return result


def check_semicolons_in_file(filename):
    """
    Check a file to ensure each line has only two semicolons.

    Args:
        filename (str): The name of the file to check.

    Returns:
        None
    """
    try:
        print(f"-------------------------------------------------------")
        print(f"Searching for inconsistencies in {filename} formatting:")
        with open(filename, 'r') as file:
            for line_number, line in enumerate(file, start=1):
                if line.count(';') != 2:
                    print(f"Line {line_number}: {line.rstrip()}")
        print(f"-------------------------------------------------------")

    except FileNotFoundError:
        print(f"Error: File '{filename}' not found.")
    except IOError:
        print(f"Error reading file '{filename}'.")


def detect_currency_format(input_str):
    """
    Detect the format of a currency input.

    Args:
        input_str (str): The currency input string.

    Returns:
        str: The detected format ('dnd_currency', 'float', or 'unknown').
    """
    # Regular expressions for different currency formats
    dnd_currency_pattern = r'^(\d+g)?\s*(\d+s)?\s*(\d+c)?$'
    float_pattern = r'^\d+(\.\d+)?$'

    # Check if the input matches the D&D currency pattern
    if re.match(dnd_currency_pattern, input_str):
        return 'dnd_currency'
    # Check if the input matches the float pattern
    elif re.match(float_pattern, input_str):
        return 'float'
    else:
        return 'unknown'


def test():
    """
    A method for testing.
    :return: 
    """
    print("Running app (TESTING methods for later use)")

    # Get old/current lists.
    print("Get old/current lists.")
    if args.output is not None:
        check_semicolons_in_file(args.output)
        old_general_list, old_trade_list = get_old_lists(args.output)
        # output_text(f"old_general_list: {old_general_list}", "note")
        # output_text(f"old_trade_list: {old_trade_list}", "note")
        print_table(old_general_list)
        print_table(old_trade_list)
    else:
        exit(1)

    # Get master list of general items.
    print("Get master list of general items.")
    if args.general is not None:
        check_semicolons_in_file(args.general)
        general_list = get_master_list(args.general)
        # output_text(f"general_list: {general_list}", "note")
        print_table(general_list)
    else:
        exit(1)

    # Get master list of trade/specialty items.
    print("Get master list of trade/specialty items.")
    if args.general is not None:
        check_semicolons_in_file(args.trade)
        trade_list = get_master_list(args.trade)
        # output_text(f"trade_list: {trade_list}", "note")
        print_table(trade_list)
    else:
        exit(1)

    # Update general list.
    print("Update general list.")
    items_not_in_old_list = find_items_not_in_old_list(old_general_list, general_list)
    print("Potential items to add:")
    # output_text(f"items_not_in_old_list: {items_not_in_old_list}", "note")
    print_table(items_not_in_old_list)

    num_to_remove = random_with_variance(len(old_general_list) * 0.2, 10)
    num_to_add = random_with_variance(num_to_remove, 5)
    print("Items to add:")
    print(f"Adding {int(num_to_add)} items.")
    items_to_add = randomly_select_items(items_not_in_old_list, int(num_to_add))
    # output_text(f"items_to_add: {items_to_add}", "note")
    print_table(items_to_add)

    print(f"Removing {int(num_to_remove)} items.")
    reduced_old_list, _ = randomly_remove_elements(old_general_list, int(num_to_remove))
    reduced_master_list, _ = randomly_remove_elements(old_general_list, int(num_to_remove))
    # output_text(f"reduced_old_list: {reduced_old_list}", "note")
    print("Reducing old/current list to:")
    print_table(reduced_old_list)
    print("New list:")
    new_list = items_to_add + reduced_old_list
    # output_text(f"new_list: {new_list}", "note")
    updated_new_list = fix_list(new_list)
    updated_new_list = adjust_buy_prices(updated_new_list)
    updated_new_list = calculate_sell_percentage(updated_new_list)
    # output_text(f"updated_new_list: {new_list}", "note")
    print_table(updated_new_list)

    print("Convert to DnD values:")
    formatted_list = convert_prices_to_dnd_format(updated_new_list)
    # output_text(f"formatted_list: {formatted_list}", "note")
    print_table(formatted_list)

    print("Convert to .input file format:")
    output_line = convert_to_one_line(formatted_list)
    print(output_line)

    # Test usage:
    mean_value = 100  # mean value
    percent_variance = 5  # percentage variance
    num_values = 1000  # number of test values
    # generate_and_plot_values(mean_value, percent_variance, num_values)


def convert_second_value_to_float(item_list):
    """
    Convert the second value of each sublist in the list to a float using convert_from_dnd_currency method.

    Args:
        item_list (list): The list of sublists.

    Returns:
        list: The list with the second value of each sublist converted to a float.
    """
    converted_list = []
    for sublist in item_list:
        # Assuming the second value is at index 1
        price = sublist[1]
        float_price = convert_from_dnd_currency(price)
        sublist[1] = float_price
        converted_list.append(sublist)
    return converted_list


def generate_initial_list(percent_general, percent_trade):
    """
    This method will generate an initial list from the master lists. IT should only need to be called once and will
    populate the output file in the appropriate format.

    Args:
        percent_general (float): The percentage of items to use from the general list.
        percent_trade (float): The percentage of items to use from the trade list.

    Returns:
        None
    """
    print("Running generate_initial_list() to generate base .input list.")

    # Get master list of general items.
    print("Get master list of general items.")
    check_semicolons_in_file(args.general)
    general_list = get_master_list(args.general)
    print_table(general_list)

    print(f"Update general items based on percentage {percent_general} of initial list size.")
    num_to_remove = len(general_list) * (1 - percent_general)
    general_list, removed_items = randomly_remove_elements(general_list, int(num_to_remove))
    general_list = fix_list(general_list)
    general_list = convert_second_value_to_float(general_list)
    general_list = calculate_sell_percentage(general_list)
    print_table(general_list)

    # Get master list of trade/specialty items.
    print("Get master list of trade/specialty items.")
    check_semicolons_in_file(args.trade)
    trade_list = get_master_list(args.trade)
    print_table(trade_list)

    print(f"Update general items based on percentage {percent_trade} of initial list size.")
    num_to_remove = len(trade_list) * (1 - percent_trade)
    trade_list, removed_items = randomly_remove_elements(trade_list, int(num_to_remove))
    trade_list = fix_list(trade_list)
    trade_list = convert_second_value_to_float(trade_list)
    trade_list = calculate_sell_percentage(trade_list)
    print_table(trade_list)


def general_update():
    """
    This method will update teh list of general items.

    Args:

    Returns:
        None
    """


def trade_update():
    """
    This method will update the list of trade items.

    Args:

    Returns:
        None
    """


def full_update():
    """
    This method will update both the general items and the trade items list.

    Args:

    Returns:
        None
    """


if __name__ == '__main__':
    generate_initial_list(0.2, 0.2)
