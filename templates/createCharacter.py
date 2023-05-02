import os

# Define the template file path and character directory
TEMPLATE_FILE = 'characterTemplate.html'
CHARACTER_FILE = 'characterTemplate.txt'

# Define the fields to replace in the template file
FIELDS = {
    'name': '',
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

for field, value in FIELDS.items():
    temp_field = '[' + field + ']'
    template = template.replace(temp_field, value)

# Write the new character file
with open(filepath, 'w') as f:
    f.write(template)

print(f'Character file created: {filepath}')
