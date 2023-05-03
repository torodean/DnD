import os
import re
import argparse


# create an ArgumentParser object
parser = argparse.ArgumentParser()

# add an argument to the parser for the file name
parser.add_argument('-c', "--char_file", help="name of the character input file")

# parse the arguments
args = parser.parse_args()


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


# Define the template file path and character directory
TEMPLATE_FILE = 'characterTemplate.html'
CHARACTER_FILE = 'characterTemplate.txt'
#CHARACTER_FILE = args.char_file

# Define the fields to replace in the template file
FIELDS = {
    'name': '',
    'image': '',
    'race': '',
    'class': '',
    'level': '',
    'background': '',
    'strength': '',
    'dexterity': '',
    'constitution': '',
    'intelligence': '',
    'wisdom': '',
    'charisma': '',
    'proficiencies': '',
    'information': '',
    'notes': ''
}

with open(CHARACTER_FILE, 'r') as f:
    contents = f.readlines()

for line in contents:
    var = line.split('=')[0].strip()
    val = line.split('=')[1].strip()
    FIELDS[var] = val

CHAR_DIR = ""
for dirpath, dirnames, filenames in os.walk("../"):
    if 'characters' in dirnames:
        CHAR_DIR = os.path.join(dirpath, 'characters')

# Generate the character file path
char_name = FIELDS['name']
filename = f'{char_name.lower().replace(" ", "_")}.html'
filepath = os.path.join(CHAR_DIR, filename)

# Read the template file and replace the fields with the character information
with open(TEMPLATE_FILE, 'r') as f:
    template = f.read()

proficiencies = FIELDS['proficiencies'].strip().split(', ')
level = int(FIELDS['level'])
proficiency_bonus = calculate_proficiency_bonus(level)
print("Proficiency bonus for level {0} is {1}".format(level, proficiency_bonus))

# Replace the appropriate fields.
for field, value in FIELDS.items():
    temp_field = '[' + field + ']'
    template = template.replace(temp_field, value)
    if value.isdigit():
        temp_field_modifier = '[' + field + " modifier]"
        print(temp_field_modifier)
        modifier_value = calculate_modifier(int(value))
        if "level" not in field:
            print("Modifier for {0} is {1}".format(field, modifier_value))
        
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
        mod_val = calculate_modifier(int(FIELDS['intelligence']))
    elif "animal handling" in match or "insight" in match or "medicine" in match or "perception" in match or "survival" in match:
        mod_val = calculate_modifier(int(FIELDS['wisdom']))
    elif "deception" in match or "intimidation" in match or "performance" in match or "persuasion" in match:
        mod_val = calculate_modifier(int(FIELDS['charisma']))
    elif "athletics" in match:
        mod_val = calculate_modifier(int(FIELDS['strength']))
    elif "acrobatics" in match or "sleight of hand" in match or "stealth" in match:
        mod_val = calculate_modifier(int(FIELDS['dexterity']))
    
    # Add the proficiency bonus if appropriate
    if match in proficiencies:
        mod_val += proficiency_bonus
        print("Adding proficiency bonus {0} to skill {1}".format(proficiency_bonus, match))
        
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

info = FIELDS['information']
template = template.replace("[background information]", info)

notes = FIELDS['notes']
template = template.replace("[notes]", notes)

img_src = FIELDS['image']
img_filepath = os.path.join(CHAR_DIR, img_src)
ime_desc = img_src.split('.')[0] + "-image"
template = template.replace("[image-description]", ime_desc)
template = template.replace("[image-url]", img_src)

# Write the new character file
with open(filepath, 'w') as f:
    f.write(template)
    


print(f'Character file created: {filepath}')

