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
        "text": "\033[0m",      # Reset color
        "warning": "\033[93m",  # Yellow
        "error": "\033[91m",    # Red
        "note": "\033[94m",     # Blue
        "success": "\033[92m"   # Green
    }

    if option in color_codes:
        color_code = color_codes[option]
        reset_code = color_codes["text"]
        print(f"{color_code}{text}{reset_code}")
    else:
        print(text)


class Config:
    """
    A class to manage configuration parameters.

    Attributes:
        config_file (str): Path to the configuration file.
        cadence (int): The frequency in seconds at which the configuration parameters are updated.
        general_price_variance (float): The variance factor for general item prices.
        trade_price_variance (float): The variance factor for trade item prices.
        general_items_percent_in_stock (float): The base percentage of general items that are in stock at any given time.
        general_items_percent_in_stock_variance (float): The variance on the general_items_percent_in_stock value.
        trade_items_percent_in_stock (float): The base percentage of trade items that are in stock at any given time.
        trade_items_percent_in_stock_variance (float): The variance on the trade_items_percent_in_stock value.
        sell_price_percentage (float): The base percentage of the buy price to determine sell prices for items.
        sell_price_percentage_variance (float): The variance of the sell prices.
        self.general_items_input_tag (str): The tags that appear as the header for the dnd-table lines in the .input files for general items.
        self.trade_items_input_tag (str): The tags that appear as the header for the dnd-table lines in the .input files for trade items.
    """
    def __init__(self, config_file=None):
        self.config_file = config_file
        self.cadence = 86400                                # Default value for cadence (seconds).
        self.general_price_variance = 0.05                  # Default value for general price variance.
        self.trade_price_variance = 0.2                     # Default value for trade price variance.
        self.general_items_percent_in_stock = 0.9           # Default value for percent of general items in stock.
        self.general_items_percent_in_stock_variance = 0.05 # Default value for variance on general items in stock.
        self.trade_items_percent_in_stock = 0.2             # Default value for percent of trade items in stock.
        self.trade_items_percent_in_stock_variance = 0.1    # Default value for variance on trade items in stock.
        self.sell_price_percentage = 0.75                   # Default value for sell item percentage.
        self.sell_price_percentage_variance = 0.1           # Default value for sell item percentage variance.
        
        # The tags that appear as the headers for the dnd-table lines in the .input files.
        self.general_items_input_tag = "General Items"        
        self.trade_items_input_tag = "Specialty/Trade Items"
        
        if self.config_file:
            self.load_config()
        else:
            output_text(f"WARNING: No config file specified. Using default values. See help message below for constructing a config file.", "warning")
            self.help()
            
        self.print_config()


    def load_config(self):
        """
        Load configuration parameters from a file.

        Reads the specified configuration file line by line. Each line should be formatted as "variable=value".
        Parses each line, extracts the variable name and its corresponding value, and assigns the value to the
        appropriate attribute of the Config object.

        Raises:
            FileNotFoundError: If the specified configuration file is not found.
        """
        if self.config_file is not None:
            try:
                with open(self.config_file, 'r') as file:
                    for line in file:
                        if '=' in line:
                            variable, value = line.strip().split('=')
                            variable = variable.strip()
                            value = value.strip()
                            if variable == 'cadence':
                                self.cadence = int(value)
                            elif variable == 'general_price_variance':
                                self.general_price_variance = float(value)
                            elif variable == 'trade_price_variance':
                                self.trade_price_variance = float(value)
                            elif variable == 'general_items_percent_in_stock':
                                self.general_items_percent_in_stock = float(value)
                            elif variable == 'general_items_percent_in_stock_variance':
                                self.general_items_percent_in_stock_variance = float(value)
                            elif variable == 'trade_items_percent_in_stock':
                                self.trade_items_percent_in_stock = float(value)
                            elif variable == 'trade_items_percent_in_stock_variance':
                                self.trade_items_percent_in_stock_variance = float(value)
                            elif variable == 'sell_price_percentage':
                                self.sell_price_percentage = float(value)
                            elif variable == 'sell_price_percentage_variance':
                                self.sell_price_percentage_variance = float(value)
                            elif variable == 'general_items_input_tag':
                                self.general_items_input_tag = value
                            elif variable == 'sell_price_percentage_variance':
                                self.trade_items_input_tag = value
            except FileNotFoundError:
                output_text("ERROR: Config file not found.", "error")


    def help(self):
        """
        Output information needed to construct a config file.

        Provides a summary of the configuration parameters and their descriptions, guiding the user on how to construct
        a configuration file with appropriate variable=value pairs.
        """
        output_text("...To construct a config file, use the following format:", "note")
        output_text("...variable=value", "note")
        output_text("...Available variables and their descriptions:", "note")
        output_text("...cadence (int): The frequency in seconds at which the configuration parameters are updated.", "note")
        output_text("...general_price_variance (float): The variance factor for general item prices.", "note")
        output_text("...trade_price_variance (float): The variance factor for trade item prices.", "note")
        output_text("...general_items_percent_in_stock (float): The base percentage of general items that are in stock at any given time.", "note")
        output_text("...general_items_percent_in_stock_variance (float): The variance on the general_items_percent_in_stock value.")
        output_text("...trade_items_percent_in_stock (float): The base percentage of trade items that are in stock at any given time.", "note")
        output_text("...trade_items_percent_in_stock_variance (float): The variance on the trade_items_percent_in_stock value.")
        output_text("...sell_price_percentage (float): The base percentage of the buy price to determine sell prices for items.", "note")
        output_text("...sell_price_percentage_variance (float): The variance of the sell prices.", "note")
        output_text("...general_items_input_tag (str): The tags that appear as the header for the dnd-table lines in the .input files for general items.")
        output_text("...trade_items_input_tag (str): The tags that appear as the header for the dnd-table lines in the .input files for trade items.")
        
        
    def print_config(self):
        """
        Print all configuration parameters and their values.
        """
        output_text("\nCurrent configuration parameters and their values:")
        output_text(f"Cadence: {self.cadence} seconds")
        output_text(f"General price variance: {self.general_price_variance}")
        output_text(f"Trade price variance: {self.trade_price_variance}")
        output_text(f"General items percent stock: {self.general_items_percent_in_stock}")
        output_text(f"Trade items percent stock: {self.trade_items_percent_in_stock}")
        output_text(f"Sell item percentage: {self.sell_price_percentage}")
        output_text(f"Sell item percentage variance: {self.sell_price_percentage_variance}\n")
                

parser = argparse.ArgumentParser(description='S.T.O.C.K.P.I.L.E System Interface and Database Updater.')
parser.add_argument('-c', '--config',
                    action='store',
                    help='The config file containing key-value pairs representing configuration parameters, each line formatted as \'variable=value.\'')
parser.add_argument('-g', '--general',
                    required=True,
                    action='store',
                    help='The file containing general store items.')
parser.add_argument('-t', '--trade',
                    required=True,
                    action='store',
                    help='The file containing random and trade items.')
parser.add_argument('-b', '--buy',
                    action='store',
                    help='The file containing the buy price history of the various items. Including this option will update this.')
parser.add_argument('-s', '--sell',
                    action='store',
                    help='The file containing the sell price history of the various items. Including this option will update this.')
parser.add_argument('-o', '--output',
                    required=True,
                    action='store',
                    help='The output file to compare to and update. This should be a .input file with the lists '
                         'formatted in the dnd-table format (see documentation).')
parser.add_argument('-i', '--initial',
                    action='store_true',
                    help='Generates an initial .input file for processing.')
                         
args = parser.parse_args()

# check if the buy history file exists.
if args.buy:
    # Create the file if it doesn't exist
    if not os.path.exists(args.buy):
        with open(args.buy, 'w'):
            pass  # Empty block just to create the file
            
# check if the sell history file exists.
if args.sell:
    # Create the file if it doesn't exist
    if not os.path.exists(args.sell):
        with open(args.sell, 'w'):
            pass  # Empty block just to create the file


# Read in config file.
if args.config == None:
    config = Config()
else:
    config = Config(args.config)


def file_exists(file_path):
    """
    Check if a file exists at the specified path.

    Args:
        file_path (str): The path to the file.

    Returns:
        bool: True if the file exists, False otherwise.
    """
    return os.path.exists(file_path)


def create_empty_file(file_path):
    """
    Create an empty file if it does not exist.

    Args:
        file_path (str): The path to the file.

    Returns:
        bool: True if the file is created or already exists, False if there was an error.
    """
    try:
        # Open the file in append mode ('a') which creates the file if it doesn't exist
        with open(file_path, 'a'):
            pass  # No need to do anything, just create the file
        return True
    except Exception as e:
        output_text(f"Error creating the file: {e}", "Error")
        return False


def write_to_file(file_path, text):
    """
    Write text to a file, overwriting the existing content. This will create the file if it does not exist.

    Args:
        file_path (str): The path to the file.
        text (str): The text to write to the file.

    Returns:
        bool: True if the text is written successfully, False if there was an error.
    """
    try:
        if not file_exists(file_path):
            create_empty_file(file_path)
        # Open the file in write mode ('w') which overwrites existing content
        with open(file_path, 'w') as file:
            file.write(text)
        return True
    except Exception as e:
        output_text(f"Error writing to the file: {e}", "error")
        return False


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
        percent_variance (float): The percentage variance (in units of percentage or unitless) allowed from the mean. This will assume unitless if the value is less than one. Otherwise it will be in units of a percentage.

    Returns:
        float: A random number with the specified percentage variance from the mean.
    """
    if percent_variance < 1:
        percent_variance = percent_variance * 100.0
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
        output_text(f"File not found: {file_path}", "Error")
        return None
    except Exception as e:
        output_text(f"Error reading file: {e}", "Error")
        return None

    return output_list


def remove_header(data):
    """
    Removes the header row from a list of items if it exists.

    Args:
        data (list): The list of items.

    Returns:
        list: The list with the header row removed, if present.
    """
    header_index = -1
    for i, item in enumerate(data):
        if "Item" in item[0] in item:
            header_index = i
            break

    if header_index != -1:
        del data[header_index]

    return data
    

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
            full_tag_line = f"{config.general_items_input_tag}[dnd-table]="
            if full_tag_line in line:
                old_general_list = convert_to_list(line.split("=")[1])
                
            full_tag_line = f"{config.trade_items_input_tag}[dnd-table]="
            if full_tag_line in line:
                old_trade_list = convert_to_list(line.split("=")[1])                
        
        # Remove the headers from the data.
        old_general_list = remove_header(old_general_list)
        old_trade_list = remove_header(old_trade_list)
        
        return old_general_list, old_trade_list

    except FileNotFoundError:
        output_text(f"File not found: {output_file}", "Error")
        return None
    except Exception as e:
        output_text(f"Error reading file: {e}", "Error")
        return None


def find_and_print_duplicates(item_list):
    """
    Find and print possible duplicate items in a list based on the first value (item name).

    Args:
        item_list (list): A list of items where each item is represented as a list.
    """
    # Create a dictionary to store items based on their names
    item_dict = {}

    # Iterate over each item in the list
    for item in item_list:
        name = item[0].lower()  # Get the name of the item

        # If the name is not in the dictionary, add it as a new key
        if name not in item_dict:
            item_dict[name] = [item]
        else:
            # If the name is already in the dictionary, print the duplicate item
            output_text(f"Possible duplicate item: {item}", "warning")

    output_text("Duplicate search complete.")


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
        if not item[3] or item[2].strip() == "":  # Check if description is blank
            item[3] = "--"
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


def adjust_buy_prices(items_list, variance=0.1):
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
        percentage = random_with_variance(100, variance * 100) / 100
        buy_price = float(item[1])
        new_buy_price = buy_price * percentage
        if new_buy_price < 0.01: # less than 1 copper.
            new_buy_price = 0.01
        updated_item = [item[0], new_buy_price, item[2], item[3]]
        updated_list.append(updated_item)

    return updated_list


def calculate_sell_percentage(items_list, percentage=config.sell_price_percentage):
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
        percent_multiplier = random_with_variance(percentage * 100, config.sell_price_percentage_variance * 100) / 100
        buy_price = float(item[1])
        sell_price = buy_price * percent_multiplier
        if sell_price < 0.01: # less than 1 copper.
            sell_price = 0.01
        if sell_price > buy_price:
            sell_price = buy_price
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

    total_value = round(gold_amount + (silver_amount / 10) + (copper_amount / 100),3)

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
    Convert a list of lists to a single line string with semicolon delimiters.

    Args:
        list_of_lists (list): The input list of lists.

    Returns:
        str: A single line string with comma delimiters.
    """
    result = ""

    num_of_columns = len(list_of_lists[0])

    for sublist in list_of_lists:
        line = ";".join(sublist)
        result += line + ";"

    # Remove the trailing comma and space
    result = f"{num_of_columns};Item;Buy Price;Sell Price;Description;" + result.strip(";")

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
        output_text(f"-------------------------------------------------------")
        output_text(f"Searching for inconsistencies in {filename} formatting:")
        with open(filename, 'r') as file:
            for line_number, line in enumerate(file, start=1):
                if line.count(';') != 2:
                    output_text(f"Line {line_number}: {line.rstrip()}")
        output_text(f"-------------------------------------------------------")

    except FileNotFoundError:
        output_text(f"Error: File '{filename}' not found.", "Error")
    except IOError:
        output_text(f"Error reading file '{filename}'.", "Error")


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
    output_text("Running app (TESTING methods for later use)")

    # Get old/current lists.
    output_text("Get old/current lists.")
    if args.output is not None:
        old_general_list, old_trade_list = get_old_lists(args.output)
        # output_text(f"old_general_list: {old_general_list}", "note")
        # output_text(f"old_trade_list: {old_trade_list}", "note")
        print_table(old_general_list)
        print_table(old_trade_list)
    else:
        exit(1)

    # Get master list of general items.
    output_text("Get master list of general items.")
    if args.general is not None:
        check_semicolons_in_file(args.general)
        general_list = get_master_list(args.general)
        # output_text(f"general_list: {general_list}", "note")
        print_table(general_list)
    else:
        exit(1)

    # Get master list of trade/specialty items.
    output_text("Get master list of trade/specialty items.")
    if args.general is not None:
        check_semicolons_in_file(args.trade)
        trade_list = get_master_list(args.trade)
        # output_text(f"trade_list: {trade_list}", "note")
        print_table(trade_list)
    else:
        exit(1)

    # Update general list.
    output_text("Update general list.")
    items_not_in_old_list = find_items_not_in_old_list(old_general_list, general_list)
    output_text("Potential items to add:")
    # output_text(f"items_not_in_old_list: {items_not_in_old_list}", "note")
    print_table(items_not_in_old_list)

    num_to_remove = random_with_variance(len(old_general_list) * 0.2, 10)
    num_to_add = random_with_variance(num_to_remove, 5)
    output_text("Items to add:")
    output_text(f"Adding {int(num_to_add)} items.")
    items_to_add = randomly_select_items(items_not_in_old_list, int(num_to_add))
    # output_text(f"items_to_add: {items_to_add}", "note")
    print_table(items_to_add)

    output_text(f"Removing {int(num_to_remove)} items.")
    reduced_old_list, _ = randomly_remove_elements(old_general_list, int(num_to_remove))
    reduced_master_list, _ = randomly_remove_elements(old_general_list, int(num_to_remove))
    # output_text(f"reduced_old_list: {reduced_old_list}", "note")
    output_text("Reducing old/current list to:")
    print_table(reduced_old_list)
    output_text("New list:")
    new_list = items_to_add + reduced_old_list
    # output_text(f"new_list: {new_list}", "note")
    updated_new_list = fix_list(new_list)
    updated_new_list = adjust_buy_prices(updated_new_list)
    updated_new_list = calculate_sell_percentage(updated_new_list)
    # output_text(f"updated_new_list: {new_list}", "note")
    print_table(updated_new_list)

    output_text("Convert to DnD values:")
    formatted_list = convert_prices_to_dnd_format(updated_new_list)
    # output_text(f"formatted_list: {formatted_list}", "note")
    print_table(formatted_list)

    output_text("Convert to .input file format:")
    output_line = convert_to_one_line(formatted_list)
    output_text(output_line)

    # Test usage:
    mean_value = 100  # mean value
    percent_variance = 5  # percentage variance
    num_values = 1000  # number of test values
    # generate_and_plot_values(mean_value, percent_variance, num_values)


def convert_value_to_float(item_list, index=1):
    """
    Convert the second value of each sublist in the list to a float using convert_from_dnd_currency method.

    Args:
        item_list (list): The list of sublists.
        index (int): The index of the column to convert.

    Returns:
        list: The list with the second value of each sublist converted to a float.
    """
    converted_list = []
    for sublist in item_list:
        price = sublist[index]
        float_price = convert_from_dnd_currency(price)
        sublist[index] = float_price
        converted_list.append(sublist)
    return converted_list
    

def replace_line_in_file(file_path, text_to_match, new_line):
    """
    Replace a line in a file with another line based on the start of the line matching some text.

    Args:
        file_path (str): The path to the file.
        text_to_match (str): The text to match at the start of the line.
        new_line (str): The new line to replace the matching line.

    Returns:
        None
    """
    # Read the contents of the file
    with open(file_path, 'r') as file:
        lines = file.readlines()

    # Replace the line if it starts with the specified text
    for i, line in enumerate(lines):
        if line.startswith(text_to_match):
            lines[i] = new_line + '\n'

    # Write the modified contents back to the file
    with open(file_path, 'w') as file:
        file.writelines(lines)
        
        
def update_general_items_in_input_file(new_list_to_add):
    """
    Update the list of general items in the input file with a new list.

    Args:
        new_list_to_add (list): The new list of general items to add. Should be in single line format.

    Returns:
        None
    """
    new_line_to_add = f"{config.general_items_input_tag}[dnd-table]={new_list_to_add}"
    replace_line_in_file(args.output, f"{config.general_items_input_tag}[dnd-table]=", new_line_to_add)
    
    
def update_trade_items_in_input_file(new_list_to_add):
    """
    Update the list of trade items in the input file with a new list.

    Args:
        new_list_to_add (list): The new list of general items to add. Should be in single line format.

    Returns:
        None
    """
    new_line_to_add = f"{config.trade_items_input_tag}[dnd-table]={new_list_to_add}"
    replace_line_in_file(args.output, f"{config.trade_items_input_tag}[dnd-table]=", new_line_to_add)


def generate_initial_list():
    """
    This method will generate an initial list from the master lists. It should only need to be called once and will
    populate the output file in the appropriate format.

    Args:
        None

    Returns:
        None
    """
    input_file_output = "folder=notes/stockpile\n\n"
    output_text("Running generate_initial_list() to generate base .input list.")

    # Get master list of general items.
    output_text("Get master list of general items.")
    check_semicolons_in_file(args.general)
    general_list = get_master_list(args.general)
    print_table(general_list)
    find_and_print_duplicates(general_list)

    output_text(f"Update general items based on percentage {config.general_items_percent_in_stock} of initial list size.")
    num_to_remove = len(general_list) * (1 - config.general_items_percent_in_stock)
    general_list, removed_items = randomly_remove_elements(general_list, int(num_to_remove))
    general_list = fix_list(general_list)
    general_list = convert_value_to_float(general_list)
    general_list = calculate_sell_percentage(general_list)
    print_table(general_list)

    output_text("Convert to DnD values:")
    general_list = convert_prices_to_dnd_format(general_list)
    # output_text(f"formatted_list: {formatted_list}", "note")
    print_table(general_list)

    general_list_input_format = convert_to_one_line(general_list)
    input_file_output += f"{config.general_items_input_tag}[dnd-table]={general_list_input_format}"

    # Get master list of trade/specialty items.
    output_text("Get master list of trade/specialty items.")
    check_semicolons_in_file(args.trade)
    trade_list = get_master_list(args.trade)
    print_table(trade_list)
    find_and_print_duplicates(trade_list)

    output_text(f"Update general items based on percentage {config.trade_items_percent_in_stock} of initial list size.")
    num_to_remove = len(trade_list) * (1 - config.trade_items_percent_in_stock)
    trade_list, removed_items = randomly_remove_elements(trade_list, int(num_to_remove))
    trade_list = fix_list(trade_list)
    trade_list = convert_value_to_float(trade_list)
    trade_list = calculate_sell_percentage(trade_list)
    print_table(trade_list)

    output_text("Convert to DnD values:")
    trade_list = convert_prices_to_dnd_format(trade_list)
    # output_text(f"formatted_list: {formatted_list}", "note")
    print_table(trade_list)

    trade_list_input_format = convert_to_one_line(trade_list)
    input_file_output += f"\n\n{config.trade_items_input_tag}[dnd-table]={trade_list_input_format}"

    output_text(input_file_output)

    write_to_file(args.output, input_file_output)
    
    
def convert_string_to_price_history_list(string_data):
    """
    Convert a string with specified format to a list of lists.

    Args:
        string_data (str): A string with items separated by newline characters
                           and elements within each line separated by semicolons.

    Returns:
        list: A list of lists where each inner list contains a string followed by floats.

    Example:
        Input: "Item1;1.5;2.7;3.8\nItem2;4.2;5.3;6.1\n"
        Output: [["Item1", 1.5, 2.7, 3.8], ["Item2", 4.2, 5.3, 6.1]]
    """
    list_of_lists = []
    rows = string_data.strip().split('\n')
    for row in rows:
        elements = row.split(';')
        string_item = elements[0]
        float_items = [float(item) for item in elements[1:]]
        list_of_lists.append([string_item] + float_items)
    return list_of_lists
    
    
def convert_price_history_list_to_string(list_of_lists):
    """
    Convert a list of lists to a list of strings with specified format.

    Args:
        list_of_lists (list): A list of lists where each inner list contains a string
                              followed by floats.

    Returns:
        list: A list of strings with the specified format.

    Example:
        Input: [["Item1", 1.5, 2.7, 3.8], ["Item2", 4.2, 5.3, 6.1]]
        Output: ["Item1;1.5;2.7;3.8", "Item2;4.2;5.3;6.1"]
    """
    return '\n'.join([';'.join(map(str, sublist)) for sublist in list_of_lists])
    
    
def append_price_history(item_price_list, updates, index=1):
    """
    Update the price history for multiple items in the list or add new lines for items that don't exist.

    Args:
        item_price_list (list): The list of items and their price histories.
        updates (list): A list of tuples where each tuple contains the item name and new price.
        index (int): The index of the row to use for appending history values.

    Returns:
        list: The updated list of items and their price histories.
    """
    updated_list = []

    # Iterate over each item in the list
    for item in item_price_list:
        item_name = item[0]
        updated = False

        # Iterate over each update
        for update in updates:
            # Check if the item name matches the update
            if item_name == update[0]:
                # Append the new price to the item's price history
                item.append(update[index])
                updated_list.append(item)
                updated = True
                break

        # If the item was not updated, add it to the updated list as is
        if not updated:
            updated_list.append(item)

    # Check for new items to add to the updated list
    for update in updates:
        item_name = update[0]
        price = update[index]
        if not any(item[0] == item_name for item in item_price_list):
            updated_list.append([item_name, price])

    return updated_list
    
    
def update_price_history(update_list):
    """
    This method will perform the various tasks to update the price history of a list of items.
    
    Args:
        update_list (list): The list to use for updating price history.
        
    Returns:
        None
    """
    if args.buy is None and args.sell is None:
        return
        
    if detect_currency_format(update_list[0][1]) == 'dnd_currency':
        update_list = convert_value_to_float(update_list, 1)
    if detect_currency_format(update_list[0][2]) == 'dnd_currency':
        update_list = convert_value_to_float(update_list, 2)
        
    try:
        if args.buy:
            with open(args.buy, 'r') as buy_history_file:
                history = buy_history_file.read()
                buy_history_file.close()

            history_list = convert_string_to_price_history_list(history)
            history_list = append_price_history(history_list, update_list, 1)
            price_history_string = convert_price_history_list_to_string(history_list)
        
            with open(args.buy, 'w') as buy_history_file:
                buy_history_file.write(price_history_string)
                buy_history_file.close()
                
        if args.sell:
            with open(args.sell, 'r') as sell_history_file:
                history = sell_history_file.read()
                sell_history_file.close()

            history_list = convert_string_to_price_history_list(history)
            history_list = append_price_history(history_list, update_list, 2)
            price_history_string = convert_price_history_list_to_string(history_list)
        
            with open(args.sell, 'w') as sell_history_file:
                sell_history_file.write(price_history_string)
                sell_history_file.close()
    
    except FileNotFoundError:
        output_text(f"ERROR: History file(s) not found: {args.buy} or {args.sell}", "error")


def general_update():
    """
    This method will update the list of general items. The following steps are performed.
        - Get master list of general items.
        - Get old/current lists.
        - Find items that are not on the current list.
        - Get the size for our new output list and how many items to remove to get to that size.
        - Create new list by adding all missing elements then removing {num_items_to_remove}.
        - Fix formatting of the list.
        - Adjust buy and sell prices accordingly. Format, Fix, etc.
        - Update output file with new list.
        - Log new price data to rice monitoring charts.

    Args:
        None

    Returns:
        None
    """
    # Get master list of general items.
    #output_text("Getting master list of general items.")
    check_semicolons_in_file(args.general)
    general_list = get_master_list(args.general)
    #print_table(general_list)
    find_and_print_duplicates(general_list)
    
    # Get old/current lists.
    output_text("Getting old/current general lists.")
    current_general_list, _ = get_old_lists(args.output)
    print_table(current_general_list)
    
    # Find items that are not on the current list.
    items_not_in_old_list = find_items_not_in_old_list(current_general_list, general_list)
    #output_text("Items not in current list:")
    #print_table(items_not_in_old_list)
    
    # Get the size for our new output list.
    output_list_size = int(random_with_variance(len(general_list)*config.general_items_percent_in_stock, config.general_items_percent_in_stock_variance))
    num_items_to_remove = abs(int(len(general_list) - output_list_size))
    output_text(f"Update general items based on percentage {config.general_items_percent_in_stock} of initial list size with {config.general_items_percent_in_stock_variance} variance.")
    output_text(f"general master list size:  {len(general_list)}", "note")
    output_text(f"current general list size: {len(current_general_list)}", "note")
    output_text(f"new general list size:     {output_list_size}", "note")
    output_text(f"Number of items to remove: {num_items_to_remove}", "note")
    
    # Create new list by adding all missing elements then removing {num_items_to_remove}.
    new_general_list = current_general_list + items_not_in_old_list
    new_general_list, _ = randomly_remove_elements(new_general_list, num_items_to_remove)
    
    # Fix formatting of the list.
    new_general_list = fix_list(new_general_list)
    #print_table(new_general_list)
    
    # Adjust buy and sell prices accordingly.
    new_general_list = convert_value_to_float(new_general_list)
    new_general_list = adjust_buy_prices(new_general_list, config.general_price_variance)
    new_general_list = calculate_sell_percentage(new_general_list)
    new_general_list = convert_prices_to_dnd_format(new_general_list)
    output_text("New/updated list:")
    print_table(new_general_list)
    
    # Update output file with new list.
    new_general_list_input_format = convert_to_one_line(new_general_list)
    update_general_items_in_input_file(new_general_list_input_format)
    #output_text(new_general_list_input_format)
    
    # Log new price data to price monitoring charts.
    update_price_history(new_general_list)
    

def trade_update():
    """
    This method will update the list of trade items. The following steps are performed.
        - Get master list of trade items.
        - Get old/current lists.
        - Find items that are not on the current list.
        - Determine how many items to remove, this will be the average with 15% variance.
        - Get the size for our new output list.
        - Remove random items and replace with new items until desired size is reached. 
        - Fix formatting of the list.
        - Adjust buy and sell prices accordingly. Format, Fix, etc.
        - Update output file with new list.
        - Log new price data to rice monitoring charts.

    Args:
        None

    Returns:
        None
    """
    # Get master list of trade items.
    output_text("Getting master list of trade items.")
    check_semicolons_in_file(args.trade)
    trade_list = get_master_list(args.trade)
    #print_table(trade_list)
    find_and_print_duplicates(trade_list)
    
    # Get old/current lists.
    output_text("Getting old/current trade lists.")
    _, current_trade_list = get_old_lists(args.output)
    print_table(current_trade_list)
    
    # Find items that are not on the current list.
    items_not_in_old_list = find_items_not_in_old_list(current_trade_list, trade_list)
    #output_text("Items not in current list:")
    #print_table(items_not_in_old_list)
    
    # Get the size for our new output list.
    output_list_size = int(random_with_variance(len(trade_list)*config.trade_items_percent_in_stock, config.trade_items_percent_in_stock_variance))
    num_items_to_remove = int(random_with_variance(len(current_trade_list)/2, 15))
    num_items_to_add = abs(output_list_size - (len(current_trade_list) - num_items_to_remove))
    output_text(f"Update general items based on percentage {config.general_items_percent_in_stock} of initial list size with {config.general_items_percent_in_stock_variance} variance.")
    output_text(f"general master list size:  {len(trade_list)}", "note")
    output_text(f"current general list size: {len(current_trade_list)}", "note")
    output_text(f"new general list size:     {output_list_size}", "note")
    output_text(f"Number of items to remove: {num_items_to_remove}", "note")
    output_text(f"Number of items to add:    {num_items_to_add}", "note")
    
    # Create new list by removing {num_items_to_remove} items and adding {num_items_to_add} items.
    new_trade_list, _ = randomly_remove_elements(current_trade_list, num_items_to_remove)
    trade_items_to_add, _  = randomly_remove_elements(items_not_in_old_list, len(items_not_in_old_list) - num_items_to_add)
    new_trade_list = new_trade_list + trade_items_to_add
    
    # Fix formatting of the list.
    new_trade_list = fix_list(new_trade_list)
    #print_table(new_trade_list)
    
    # Adjust buy and sell prices accordingly.
    new_trade_list = convert_value_to_float(new_trade_list)
    new_trade_list = adjust_buy_prices(new_trade_list, config.trade_price_variance)
    new_trade_list = calculate_sell_percentage(new_trade_list)
    new_trade_list = convert_prices_to_dnd_format(new_trade_list)
    output_text("New/updated list:")
    print_table(new_trade_list)
    
    # Update output file with new list.
    new_trade_list_input_format = convert_to_one_line(new_trade_list)
    update_trade_items_in_input_file(new_trade_list_input_format)
    #output_text(new_trade_list_input_format)
    
    # Log new price data to price monitoring charts.
    update_price_history(new_trade_list)


def full_update():
    """
    This method will update both the general items and the trade items list.

    Args:
        None

    Returns:
        None
    """
    general_update()
    trade_update()


if __name__ == '__main__':
    if args.initial:
        generate_initial_list()
    else:
        full_update()
