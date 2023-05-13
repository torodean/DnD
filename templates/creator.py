#!/bin/python3
import tkinter as tk
from tkinter import filedialog
from tkinter import PhotoImage
import os
import re
import shutil
import random
import json
from bs4 import BeautifulSoup


def append_to_file(file_path, string_to_append):
    """
    Append a string to a file.

    :param file_path: The path to the file to append to.
    :param string_to_append: The string to append to the file.
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


def calculate_hp(class_type: str, level: int, constitution: int) -> int:
    """
    Calculate the hit points (hp) of a Dungeons & Dragons (DnD) 5th edition character
    based on their class, level, and constitution modifier.

    Args:
        class_type (str): The character's class (e.g. 'fighter', 'wizard', 'rogue').
        level (int): The character's level, between 1 and 20.
        constitution (int): The character's constitution score, between 1 and 30.

    Returns:
        int: The character's hit points, based on their class and level, modified by their
           constitution modifier.

    Raises:
        ValueError: If the given class_type is not recognized.
    """
    hit_die = 0

    # Determine hit die for the class
    if class_type == 'barbarian':
        hit_die = 12
    elif class_type == 'fighter' or class_type == 'paladin' or class_type == 'ranger':
        hit_die = 10
    elif class_type == 'cleric' or class_type == 'druid' or class_type == 'monk' or class_type == 'rogue' or class_type == 'warlock':
        hit_die = 8
    elif class_type == 'sorcerer' or class_type == 'wizard':
        hit_die = 6

    # Calculate base hit points
    base_hp = hit_die + (constitution - 10) // 2

    additional_hp = 0
    # Calculate additional hit points based on level
    for i in range(2, level):
        additional_hp += random.randint(1, hit_die) + ((constitution - 10) // 2)

    # Calculate total hit points
    total_hp = base_hp + additional_hp

    return total_hp


def calculate_proficiency_bonus(level):
    """
    Calculate the proficiency bonus based on character level.

    Parameters:
        level (int): The character's level.

    Returns:
        int: The character's proficiency bonus.
    """
    if level < 5:
        return 2
    elif level < 9:
        return 3
    elif level < 13:
        return 4
    elif level < 17:
        return 5
    else:
        return 6


def roll_4d6_drop_lowest():
    """
    Rolls 4d6 and returns the sum of the highest 3 dice.
    Returns:
        int: The sum of the highest 3 dice.
    """
    rolls = [random.randint(1, 6) for _ in range(4)]
    total = sum(sorted(rolls)[1:])
    print("Rolling 4d6: {0} - Dropping lowest -> {1}".format(rolls, total))
    return total


def get_stat_priority(character_class):
    """
    Returns a list of attributes ordered by the stat priority for a given class.
    Args:
        character_class (str): The class to get the stat priority for.
    Returns:
        list: The list of attributes ordered by the stat priority.
    """
    stat_priorities = {
        'barbarian': ['strength', 'constitution', 'dexterity', 'wisdom', 'intelligence', 'charisma'],
        'bard': ['charisma', 'dexterity', 'constitution', 'intelligence', 'wisdom', 'strength'],
        'cleric': ['wisdom', 'constitution', 'strength', 'intelligence', 'dexterity', 'charisma'],
        'druid': ['wisdom', 'constitution', 'dexterity', 'intelligence', 'charisma', 'strength'],
        'fighter': ['strength', 'constitution', 'dexterity', 'wisdom', 'intelligence', 'charisma'],
        'monk': ['dexterity', 'wisdom', 'constitution', 'strength', 'intelligence', 'charisma'],
        'paladin': ['strength', 'constitution', 'charisma', 'wisdom', 'intelligence', 'dexterity'],
        'ranger': ['dexterity', 'wisdom', 'constitution', 'intelligence', 'strength', 'charisma'],
        'rogue': ['dexterity', 'intelligence', 'constitution', 'wisdom', 'strength', 'charisma'],
        'sorcerer': ['charisma', 'constitution', 'dexterity', 'wisdom', 'intelligence', 'strength'],
        'warlock': ['charisma', 'constitution', 'dexterity', 'wisdom', 'intelligence', 'strength'],
        'wizard': ['intelligence', 'constitution', 'dexterity', 'wisdom', 'charisma', 'strength']
    }
    return stat_priorities.get(character_class.lower(), [])


def adjust_stats_for_level(assigned_stats, level):
    """
    Adjust some stats for a leveled up character.
    """
    if level < 4:
        return assigned_stats
    elif level < 8:
        bonus_points = 2
    elif level < 12:
        bonus_points = 4
    elif level < 16:
        bonus_points = 6
    elif level < 19:
        bonus_points = 8
    else:
        bonus_points = 10

    print(f"level {level} awards {bonus_points} bonus attribute points")
    print(f"Original attributes: {assigned_stats}")

    # Sort the dictionary by descending values   
    sorted_dict = dict(sorted(assigned_stats.items(), key=lambda item: item[1], reverse=True))
    print(sorted_dict)

    # Calculate the maximum possible value for each key, without exceeding 22
    max_value = 22

    # Distribute bonus_points among the highest keys without exceeding 22
    for key in sorted_dict.keys():
        if sorted_dict[key] == 22 or bonus_points == 0:
            continue
        else:
            add_value = min(bonus_points, max_value - sorted_dict[key])
            sorted_dict[key] += add_value
            bonus_points -= add_value

    print(f"Updated attributes: {sorted_dict}")

    return sorted_dict


def generate_character_stats(character_class, level=1):
    """
    Generates a list of six stats for a character based on their class and level.
    Args:
        character_class (str): The character's class.
    Returns:
        list: The list of six stats.
    """
    # Get the stat priority for the character's class
    stat_priority = get_stat_priority(character_class)

    # Roll 4d6 and drop the lowest die for each of the six stats
    stats = [roll_4d6_drop_lowest() for _ in range(6)]

    # Assign the stats based on the stat priority for the character's class
    assigned_stats = {}
    for stat_name in stat_priority:
        stat_value = max(stats)
        stats.remove(stat_value)
        assigned_stats[stat_name] = stat_value

    # Adjust for character level.
    assigned_stats = adjust_stats_for_level(assigned_stats, level)

    return assigned_stats


def calculate_modifier(attribute_value):
    """
    Calculate the DnD attribute modifier based on the value of the attribute.

    Args:
        attribute_value (int): The value of the attribute.

    Returns:
        int: The modifier value for the attribute.

    Example:
        >>> calculate_modifier(15)
        2

    """
    modifier = (attribute_value - 10) // 2
    return modifier


def copy_file_to_directory(file_path, directory_path):
    """Copy a file to a directory.

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
        print(f"Directory {directory_path} does not exist. Creating directory...")
        os.makedirs(directory_path)

    # Copy the file to the directory
    print(f"Copying {file_path} to {directory_path}")
    shutil.copy(file_path, directory_path)
    print(f"File {file_path} copied to {directory_path}")


def print_prob_matrix(prob_matrix):
    """
    Prints a probability matrix to the console in JSON format.

    Parameters:
        prob_matrix (dict): A dictionary representing the probability matrix,
        where each key is an input character and the corresponding value is a dictionary
        of output characters and their probabilities.
    """
    # Convert the probability matrix to a JSON string with indentation and line breaks
    json_str = json.dumps(prob_matrix, indent=4, sort_keys=True)

    # Print the JSON string
    print(json_str)


def generate_prob_matrix(words):
    """
    Generates a probability matrix based on a list of words.

    Parameters:
        words (list of str): A list of words to use in generating the probability matrix.

    Returns:
        A dictionary representing the probability matrix, where each key is an input character
        and the corresponding value is a dictionary of output characters and their probabilities.

    Example:
        >>> words = ["cat", "dog", "cut", "cog", "cot", "caught"]
        >>> prob_matrix = generate_prob_matrix(words)
        >>> prob_matrix
    {
        'c': {'a': 0.4, 'u': 0.2, 'o': 0.4},
        'a': {'t': 0.5, 'u': 0.5},
        't': {},
        'd': {'o': 1.0},
        'o': {'g': 0.6666666666666666, 't': 0.3333333333333333},
        'g': {'h': 1.0},
        'u': {'t': 0.5, 'g': 0.5},
        'h': {'t': 1.0}
    }

    Note that the probabilities for each output character are normalized so that they sum to 1.0.
    """
    # Create an empty dictionary to store the probability matrix
    prob_matrix = {}

    # Iterate over the words in the list
    for word in words:
        # Iterate over the characters in the word
        for i in range(len(word)):
            input_char = word[i]

            # Get the dictionary of output characters and their counts for this input character
            output_counts = prob_matrix.get(input_char, {})

            # Increment the count for the next character in the word, if there is one
            if i < len(word) - 1:
                output_char = word[i + 1]
                output_counts[output_char] = output_counts.get(output_char, 0) + 1

            # Update the dictionary for this input character in the probability matrix
            prob_matrix[input_char] = output_counts

    # Convert the counts in the probability matrix to probabilities
    for input_char, output_counts in prob_matrix.items():
        total_count = sum(output_counts.values())
        output_probs = {output_char: count / total_count for output_char, count in output_counts.items()}
        prob_matrix[input_char] = output_probs

    return prob_matrix


def generate_word(prob_matrix, min_length=4, max_length=10):
    """
    Generate a random word using a probability matrix.

    Parameters:
        prob_matrix (dict): A dictionary representing the probability matrix for generating words.
        min_length (int): The minimum length of the generated word. Default value is 4.
        max_length (int): The maximum length of the generated word. Default value is 10.

    Returns:
        A string representing the generated word.

    Algorithm:
        1. Choose a random length between min_length and max_length.
        2. Initialize the word with a random input character.
        3. Generate the next characters based on the probabilities in the matrix.
            a. Get the output probabilities for the current input character.
            b. Create a list of possible next characters based on their probabilities.
            c. Choose a random next character from the list.
            d. Update the word and the input character for the next iteration.
        4. Return the generated word.
    """
    # Choose a random length between min_length and max_length
    length = random.randint(min_length, max_length)

    # Initialize the word with a random input character
    input_char = random.choice(list(prob_matrix.keys()))
    while prob_matrix.get(input_char) is None or not prob_matrix.get(input_char):
        # print(f"reloading {input_char}")
        input_char = random.choice(list(prob_matrix.keys()))

    # print(f"input_char: {input_char}")
    word = input_char

    # Generate the next (length - 1) characters based on the probabilities in the matrix
    for i in range(length - 1):
        output_probs = prob_matrix.get(input_char)

        # print(f"output_probs: {output_probs}")
        while output_probs is None or not output_probs:
            # print(f"reloading {output_probs}")
            os.system("sleep 1")
            output_probs = prob_matrix.get(input_char)

        # print(f"output_probs: {output_probs}")
        temp_list = []
        for possible_char in output_probs:
            # print("{0} -> {1}".format(possible_char, output_probs[possible_char]))
            for i in range(int(output_probs[possible_char] * 25)):  # 25 only pulls anything over 4%
                temp_list.append(possible_char)

        # print(f"temp_list: {temp_list}")
        next_char = random.choice(temp_list)
        output_probs = prob_matrix.get(next_char)

        if len(word) + 1 == length:
            return word + next_char
        else:
            while output_probs is None or not output_probs:
                # print(f"reloading {next_char}")
                next_char = random.choice(temp_list)
                output_probs = prob_matrix.get(next_char)

        # print(f"next char {next_char}")
        word += next_char
        input_char = next_char

    return word


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


class Variables:
    """
    A class to store app wide variables.
    """

    def __init__(self):
        self.current_prob_matrix = None
        self.current_file = ""
        self.current_list = []
        self.characters_folder = ""
        self.output_file_folder = ""
        self.character_template_file = "characterTemplate.html"
        self.set_character_folder(True)

        # Define the root directory
        self.root_dir = os.getcwd()
        self.trash_dir = self.root_dir + "/trash"

    def set_character_folder(self, npc=True):
        for dirpath, dirnames, filenames in os.walk("../"):
            if 'characters' in dirnames:
                if not npc:
                    self.characters_folder = os.path.join(dirpath, 'characters/player')
                    break
                else:
                    self.characters_folder = os.path.join(dirpath, 'characters/non-player')
                    break
            else:
                self.characters_folder = '.'  # used for testing mainly

        print(f"Character folder set to: {self.characters_folder}")

    def trash_file(self, file):
        move_file(file, self.trash_dir)

    def reset(self):
        self.current_file = ""
        self.current_list = []
        self.current_prob_matrix = {}


# Define a global variable containing the declared vars. Use this so they are all only defined once and can be
# updated/stored throughout the applications lifetime.
global_vars = Variables()


def get_character_fields(file):
    char_fields = {}
    # Open the current file and read in the contents.
    with open(file, 'r') as f:
        contents = f.readlines()

    for line in contents:
        var = line.split('=')[0].strip().lower()
        val = line.split('=')[1].strip().lower()
        char_fields[var] = val

    for field in char_fields:
        print(field)

    # check to make sure class is defined.
    if "class" not in char_fields:
        print(f"ERROR: No 'class' value found in char_fields: {char_fields}")
        return

    return char_fields


class Creator:
    def __init__(self):
        self.last_user_input = None
        self.gui = tk.Tk()
        self.gui.geometry("850x500")
        self.gui.title("File Browser")

        # Load icon image
        icon = PhotoImage(file='{}/../mmorpdnd.png'.format(global_vars.root_dir))
        # Set icon image
        self.gui.tk.call('wm', 'iconphoto', self.gui._w, icon)

        # Create the menu bar
        menubar = tk.Menu(self.gui)
        # Create a file menu and add it to the menu bar
        filemenu = tk.Menu(menubar, tearoff=0)
        filemenu.add_command(label="Exit", command=self.gui.quit)

        # Create a frame for the file path display and edit box
        path_frame = tk.Frame(self.gui)
        path_frame.pack(fill=tk.X, padx=10, pady=10)

        # Create a label for the file path display
        path_label = tk.Label(path_frame, text="Input File:")
        path_label.pack(side=tk.LEFT, padx=(0, 5))

        # Create an editable text box for the file path display
        self.path_text = tk.Entry(path_frame, width=82)
        self.path_text.pack(side=tk.LEFT, fill=tk.X, expand=True)

        # Bind a function to the Entry widget that is called whenever the text is modified
        # self.path_text.bind('<KeyRelease>', self.path_text_updated)

        # Create a button to open the file browser
        browse_button = tk.Button(path_frame, text="Browse", command=self.browse_files)
        browse_button.pack(side=tk.LEFT, padx=(5, 0))

        # Create a frame for the yes and no buttons
        top_button_frame = tk.Frame(self.gui)
        top_button_frame.pack(side=tk.TOP, pady=10)

        # Create a button to open the file browser
        generate_word_button = tk.Button(top_button_frame, text="Generate Word", command=self.generate_word)
        generate_word_button.pack(side=tk.LEFT, padx=10)

        # Create a button to open the file browser
        generate_char_button = tk.Button(top_button_frame, text="Generate Char", command=self.generate_char)
        generate_char_button.pack(side=tk.LEFT, padx=10)

        # Create an npc checkbox
        self.npc_checkbox_value = tk.BooleanVar(value=True)
        self.npc_checkbox_value.set(True)  # Set the variable to True
        npc_checkbox = tk.Checkbutton(top_button_frame, text="NPC", variable=self.npc_checkbox_value,
                                      command=self.checkbox_changed)
        npc_checkbox.pack(side=tk.LEFT, padx=1)

        # Create a trash checkbox
        self.trash_checkbox_value = tk.BooleanVar(value=False)
        self.trash_checkbox_value.set(False)  # Set the variable to False
        trash_checkbox = tk.Checkbutton(top_button_frame, text="Trash", variable=self.trash_checkbox_value,
                                        command=self.checkbox_changed)
        trash_checkbox.pack(side=tk.LEFT, padx=1)

        # Create a button to open the file browser
        create_page_button = tk.Button(top_button_frame, text="Create Page", command=self.create_page)
        create_page_button.pack(side=tk.LEFT, padx=10)

        # Create a button to open the file browser
        test_button = tk.Button(top_button_frame, text="Test Button", command=self.test)
        test_button.pack(side=tk.LEFT, padx=10)

        # Create a frame for the large text box and scrollbar
        text_frame = tk.Frame(self.gui)
        text_frame.pack(side=tk.TOP, fill=tk.BOTH, padx=(10, 0), pady=10, expand=True)
        text_frame.pack_propagate(False)

        # Create a text widget for the large text box
        self.large_text = tk.Text(text_frame)
        self.large_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Create a scrollbar and attach it to the text widget
        scrollbar = tk.Scrollbar(text_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y, padx=(0, 10))
        self.large_text.config(yscrollcommand=scrollbar.set)
        scrollbar.config(command=self.large_text.yview)

        # Create a frame for the yes and no buttons
        button_frame = tk.Frame(self.gui)
        button_frame.pack(side=tk.BOTTOM, pady=10)

        # Create a button to store "yes"
        self.yes_button = tk.Button(button_frame, text="Yes", command=self.yes)
        self.yes_button.pack(side=tk.LEFT, padx=(10, 5))

        # Create a button to store "no"
        self.no_button = tk.Button(button_frame, text="No", command=self.no)
        self.no_button.pack(side=tk.LEFT, padx=(5, 10))

        # Create a button to store "reset"
        self.reset_button = tk.Button(button_frame, text="Reset", command=self.reset)
        self.reset_button.pack(side=tk.LEFT, padx=(5, 10))

        self.no_button.config(state="disabled")
        self.yes_button.config(state="disabled")
        test_button.config(state="disabled")

    def create_page(self):
        """
        Reads the input file and generates an HTML file with elements containing the values from the input file. The output file is saved to the output_file_folder. Uses BeautifulSoup to parse the generated HTML file and prints the formatted HTML to the console.
        :return: None
        """
        self.update_input_file()

        if not global_vars.current_file.endswith(".input"):
            self.output_text(f"Wrong input file type: {global_vars.current_file}")
            self.output_text(f"File should end with '.input'")
            return

        # read input file
        with open(input_file, 'r') as f:
            lines = f.readlines()

        folder = "."

        for line in lines:
            if "folder" in line:
                folder = line.split('=')[1]

        for dirpath, dirnames, filenames in os.walk("../"):
            if folder in dirnames:
                global_vars.output_file_folder = dirpath
                break
            else:
                global_vars.output_file_folder = '.'  # used for testing mainly

        print(f"Output file folder set to: {global_vars.output_file_folder}")

        # create HTML file
        with open(global_vars.current_file, 'w') as f:
            # write HTML boilerplate
            f.write('<!DOCTYPE html>\n<html>\n<head>\n<title></title>\n</head>\n<body>\n')

            # iterate over lines in input file
            for line in lines:
                # parse line
                variable_class, value = line.strip().split('=')
                variable = variable_class.split('[')[0]
                class_name = variable_class.split('[')[1].split(']')[0]

                # create HTML element
                html_element = f'<div class="{class_name}"><h2>{variable}</h2><p>{value}</p></div>'

                # write HTML element to file
                f.write(html_element)

            # close HTML file
            f.write('</body>\n</html>')

        # parse HTML file with BeautifulSoup
        with open('output.html', 'r') as f:
            html = f.read()
            soup = BeautifulSoup(html, 'html.parser')

        # print formatted HTML
        print(soup.prettify())

    def checkbox_changed(self):
        """
        This method is called when either the NPC or trash_files checkboxes are checked or unchecked.
        It retrieves the values of the checkboxes and prints a message indicating whether they are enabled or disabled.
        If the NPC checkbox is enabled, it sets the character folder to the NPC folder using the `set_character_folder()` method in the `global_vars` module.
        """
        npc = self.npc_checkbox_value.get()
        trash_files = self.trash_checkbox_value.get()
        if npc:
            print("NPC Checkbox enabled")
        else:
            print("NPC Checkbox disabled")

        if trash_files:
            print("trash_files Checkbox enabled")
        else:
            print("trash_files Checkbox disabled")

        global_vars.set_character_folder(npc)

    def generate_char(self):

        self.update_input_file()

        if not global_vars.current_file.endswith(".char"):
            self.output_text(f"Wrong input file type: {global_vars.current_file}")
            self.output_text(f"File should end with '.char'")
            return

        # Define the fields to replace in the template file
        char_fields = get_character_fields(global_vars.current_file)

        char_class = char_fields['class']

        # Default to level 1 if none defined.
        if "level" not in char_fields:
            char_level = 1
        else:
            char_level = int(char_fields['level'])

        # Create character stats to fill in if none are defined.
        char_stats = generate_character_stats(char_class, char_level)
        attributes = ["strength", "constitution", "wisdom", "charisma", "dexterity", "intelligence"]
        for attribute in attributes:
            if attribute not in char_fields:
                self.output_text(f"Generated value for {attribute} as {char_stats[attribute]}")
                char_fields[attribute] = str(char_stats[attribute])

        if "hp" not in char_fields:
            hp = calculate_hp(char_class, int(char_fields['level']), int(char_fields['constitution']))
            self.output_text(f"Calculated hp as {hp}.")

        # Generate the character file path
        char_name = char_fields['name']
        filename = f'{char_name.lower().replace(" ", "_")}.html'
        filepath = os.path.join(global_vars.characters_folder, filename)

        # Read the template file and replace the fields with the character information
        with open(global_vars.character_template_file, 'r') as f:
            template = f.read()

        proficiencies = char_fields['proficiencies'].strip().split(', ')
        proficiency_bonus = calculate_proficiency_bonus(char_level)
        self.output_text("Proficiency bonus for level {0} is {1}".format(char_level, proficiency_bonus))

        # Replace the appropriate fields.
        for field, value in char_fields.items():
            temp_field = '[' + field + ']'
            if "senses" in field:
                if char_fields['senses'].strip() != "" and "None" not in char_fields['senses']:
                    value += ", Passive Perception: {0}".format(10 + calculate_modifier(int(char_fields['wisdom'])))
                else:
                    value = "Passive Perception = {0}".format(10 + calculate_modifier(int(char_fields['wisdom'])))
            template = template.replace(temp_field, value)
            if value.isdigit():
                temp_field_modifier = '[' + field + " modifier]"
                modifier_value = calculate_modifier(int(value))
                if "level" not in field:
                    self.output_text("Modifier for {0} is {1}".format(field, modifier_value))

                # Add the proficiency bonus to the modifier.
                if field in proficiencies:
                    modifier_value += proficiency_bonus

                # Update the proficiency bonus to have a +.
                if modifier_value >= 0:
                    modifier_value_str = "+" + str(modifier_value)
                else:
                    modifier_value_str = str(modifier_value)
                template = template.replace(temp_field_modifier, modifier_value_str)

        for prof in proficiencies:
            temp_field_proficient = '[' + prof + " proficiency]"
            template = template.replace(temp_field_proficient, "<i class=\"fas fa-check\"></i>")

        pattern = r'\[(.*?) modifier\]'
        matches = re.findall(pattern, template)
        for match in matches:
            mod_val = 0
            if "arcana" in match or "history" in match or "investigation" in match or "nature" in match or "religion" in match:
                mod_val = calculate_modifier(int(char_fields['intelligence']))
            elif "animal handling" in match or "insight" in match or "medicine" in match or "perception" in match or "survival" in match:
                mod_val = calculate_modifier(int(char_fields['wisdom']))
            elif "deception" in match or "intimidation" in match or "performance" in match or "persuasion" in match:
                mod_val = calculate_modifier(int(char_fields['charisma']))
            elif "athletics" in match:
                mod_val = calculate_modifier(int(char_fields['strength']))
            elif "acrobatics" in match or "sleight of hand" in match or "stealth" in match:
                mod_val = calculate_modifier(int(char_fields['dexterity']))

            # Add the proficiency bonus if appropriate
            if match in proficiencies:
                mod_val += proficiency_bonus
                self.output_text("Adding proficiency bonus {0} to skill {1}".format(proficiency_bonus, match))

            # Set the values as string formatted.
            if mod_val >= 0:
                skill_modifier = '+' + str(mod_val)
            else:
                skill_modifier = str(mod_val)

            # Update the template.
            template = template.replace(f'[{match} modifier]', skill_modifier)

        pattern_prof = r'\[(.*?) proficiency\]'
        matches = re.findall(pattern_prof, template)
        for match in matches:
            empty_prof_modifier = "-"
            template = template.replace(f'[{match} proficiency]', empty_prof_modifier)

        # Replace the information block.
        info = char_fields['information']
        template = template.replace("[background information]", info)

        # Replace the notes block.
        notes = char_fields['notes']
        template = template.replace("[notes]", notes)

        # Replace the image block.
        img_src = "img/" + char_fields['image']
        img_dir = global_vars.characters_folder + "/img"
        img_desc = img_src.split('/')[1].split('.')[0] + "-image"
        template = template.replace("[image-description]", img_desc)
        template = template.replace("[image-url]", img_src)

        try:
            copy_file_to_directory(img_src, img_dir)
            if self.trash_checkbox_value.get():
                global_vars.trash_file(img_src)
        except ValueError as e:
            print(f"An error occurred: {e}")

        # Update abilities
        abilities = char_fields['abilities'].split(',')
        abilities_output = ""
        for ability in abilities:
            abilities_output += "<li><strong>"
            abilities_output += ability.strip()
            abilities_output += ":</strong>["
            abilities_output += ability.strip()
            abilities_output += " description]</li>"
        template = template.replace("[abilities list]", abilities_output)

        # Update equipment
        equipment = char_fields['equipment'].split(',')
        equipment_output = ""
        for equip in equipment:
            equipment_output += "<li><strong>"
            equipment_output += equip.strip()
            equipment_output += ":</strong>["
            equipment_output += equip.strip()
            equipment_output += " description]</li>"
        template = template.replace("[equipment list]", equipment_output)

        # Write the new character file
        with open(filepath, 'w') as f:
            f.write(template)

        print(f'Character file created: {filepath}')

        # move the files to the trash if this option is selected.
        if self.trash_checkbox_value.get():
            global_vars.trash_file(global_vars.current_file)

    def output_text(self, text):
        print(text)
        # Append the given text to the large_text widget
        self.large_text.config(state="normal")
        self.large_text.insert(tk.END, text + '\n')
        self.large_text.config(state="disabled")

        # Scroll to the bottom of the widget
        self.large_text.see("end")

    def test(self):
        """
        Method for testing.

        :return:
            None
        """
        self.output_text("test text")

    def get_user_choice(self):
        # Disable the buttons
        self.yes_button.config(state=tk.ACTIVE)
        self.no_button.config(state=tk.ACTIVE)

        # Create a BooleanVar to store the user's choice
        user_choice = tk.BooleanVar()

        # Define the functions that will be called when the buttons are clicked
        def yes_button_callback():
            self.yes()
            nonlocal user_choice
            user_choice.set(True)
            self.gui.quit()

        def no_button_callback():
            self.no()
            nonlocal user_choice
            user_choice.set(False)
            self.gui.quit()

        def reset_button_callback():
            self.reset()
            nonlocal user_choice
            user_choice.set(False)
            self.gui.quit()

        # Configure the buttons to call the appropriate functions
        self.yes_button.config(command=yes_button_callback)
        self.no_button.config(command=no_button_callback)
        self.reset_button.config(command=reset_button_callback)

        # Start the main event loop
        self.gui.mainloop()

        self.yes_button.config(state=tk.DISABLED)
        self.no_button.config(state=tk.DISABLED)

        # Return the user's choice
        return user_choice.get()

    def yes(self):
        self.last_user_input = "yes"
        print(f"last_user_input set to {self.last_user_input}")

    def no(self):
        self.last_user_input = "no"
        print(f"last_user_input set to {self.last_user_input}")

    def reset(self):
        self.output_text("Resetting...")
        self.last_user_input = "reset"
        print(f"last_user_input set to {self.last_user_input}")

    def browse_files(self):
        # Use the file dialog to get a file path
        file_path = filedialog.askopenfilename()

        # Update the text in the editable box with the selected file path
        self.path_text.delete(0, tk.END)
        self.path_text.insert(0, file_path)

    def update_input_file(self):
        print("Updating input file.")
        if self.path_text.get() is None:
            self.output_text("No file input!")
        else:
            file = self.path_text.get()
            if file == global_vars.current_file:
                return
            else:
                global_vars.reset()
                global_vars.current_file = file
                self.output_text(f"Updated current work file to: {file}")
                if file.endswith(".char") or file.endswith(".names"):
                    global_vars.current_list = read_lines_from_file(file)

    def generate_word(self):
        print("Generating word.")
        self.update_input_file()
        global_vars.current_prob_matrix = generate_prob_matrix(global_vars.current_list)
        print_prob_matrix(global_vars.current_prob_matrix)
        while self.last_user_input != "reset":
            word = "{0}".format(generate_word(global_vars.current_prob_matrix))
            self.output_text(f"Generated word: {word}")
            self.output_text("Do you want to append this word to the file? (y/n)")
            # Get the user's choice
            self.get_user_choice()
            if self.last_user_input == "yes":
                append_to_file(global_vars.current_file, word)
                self.output_text("Word appended to file.")
            elif self.last_user_input == "no":
                self.output_text("Word NOT appended to file.")
                continue
            else:
                continue

    def run(self):
        self.gui.mainloop()


if __name__ == '__main__':
    app = Creator()
    app.run()
