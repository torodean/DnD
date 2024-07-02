#!/usr/bin/env python3
import tkinter as tk
from tkinter import filedialog, ttk
import random
from PIL import Image, ImageTk

# Import character generation methods from creator.
from creator import generate_character_stats
from creator import calculate_hp
from creator import generate_word_from_file
from creator import calculate_modifier

folder_options = [
    "characters/non-player", 
    "characters/player", 
    "creatures/monsters", 
    "creatures/animals", 
    "creatures/humanoids", 
    "creatures/dragons", 
    "creatures/other"
]
                  
class_options = [
    "Barbarian",
    "Wizard",
    "Sorcerer",
    "Bard",
    "Ranger",
    "Cleric",
    "Druid",
    "Fighter",
    "Monk",
    "Paladin",
    "Rogue",
    "Warlock",
    "Artificer",
    "Blood Hunter"
]
                 
# Mapping of DnD classes to their potential backgrounds
class_to_backgrounds = {
    "barbarian": ["Outlander", "Tribal Nomad", "Hermit"],
    "bard": ["Entertainer", "Charlatan", "Guild Artisan"],
    "cleric": ["Acolyte", "Hermit", "Noble"],
    "druid": ["Hermit", "Outlander", "Sage"],
    "fighter": ["Soldier", "Mercenary Veteran", "Noble"],
    "monk": ["Hermit", "Noble", "Outlander"],
    "paladin": ["Noble", "Soldier", "Knight"],
    "ranger": ["Outlander", "Hunter", "Tribal Nomad"],
    "rogue": ["Charlatan", "Criminal", "Spy"],
    "sorcerer": ["Hermit", "Noble", "Sage"],
    "warlock": ["Charlatan", "Noble", "Sage"],
    "wizard": ["Sage", "Acolyte", "Hermit"],
    "artificer": ["Acolyte", "Noble", "Sage", "Hermit"],
    "blood hunter": ["Criminal", "Acolyte", "Outlander"]
}

# PHB races.        
race_options = [
    "Human",
    "Elf",
    "Dwarf",
    "Gnome",
    "Half-Elf",
    "Dragonborn",
    "Halfling",
    "Half-Orc"
]

# Mapping of DnD classes to their potential AC ranges
class_to_ac_range = {
    "barbarian": (12, 16),
    "bard": (11, 15),
    "cleric": (12, 18),
    "druid": (11, 16),
    "fighter": (14, 18),
    "monk": (12, 17),
    "paladin": (14, 18),
    "ranger": (13, 17),
    "rogue": (12, 16),
    "sorcerer": (10, 14),
    "warlock": (10, 14),
    "wizard": (10, 14),
    "Artificer": (12, 17),
    "Blood Hunter": (11, 17)
}

languages_list = [
    "Common",
    "Dwarvish",
    "Elvish",
    "Giant",
    "Gnomish",
    "Goblin",
    "Halfling",
    "Orcish",
    "Abyssal",
    "Celestial",
    "Draconic",
    "Kraul",
    "Loxodon",
    "Merfolk",
    "Minotaur",
    "Sphinx",
    "Sylvan",
    "Vedalken",
    "Infernal",
    "Primodial"
]

# Mapping of DnD classes to their core proficiencies
class_to_proficiencies = {
    "barbarian": ["Athletics", "Survival", "Strength", "Constitution"],
    "bard": ["Acrobatics", "Performance", "Sleight of Hand", "Dexterity", "Charisma"],
    "cleric": ["History", "Insight", "Medicine", "Religion", "Wisdom", "Charisma"],
    "druid": ["Nature", "Survival", "Animal Handling", "Intelligence", "Wisdom"],
    "fighter": ["Athletics", "Intimidation", "Strength", "Constitution"],
    "monk": ["Acrobatics", "Stealth", "Dexterity", "Wisdom"],
    "paladin": ["Athletics", "Religion", "Wisdom", "Charisma"],
    "ranger": ["Nature", "Survival", "Stealth", "Strength", "Dexterity"],
    "rogue": ["Acrobatics", "Deception", "Stealth", "Sleight of Hand", "Dexterity", "Intelligence"],
    "sorcerer": ["Arcana", "Deception", "Intimidation", "Constitution", "Charisma"],
    "warlock": ["Arcana", "Deception", "Intimidation", "Wisdom", "Charisma"],
    "wizard": ["Arcana", "History", "Investigation", "Intelligence", "Wisdom"],
    "artificer": ["Arcana", "History", "Investigation", "Constitution", "Intelligence"],
    "blood hunter": ["Nature", "Survival", "Stealth", "Strength", "Dexterity"]
}

# General list of additional proficiencies
additional_proficiencies = [
    "Acrobatics", "Animal Handling", "Arcana", "Athletics", "Deception",
    "History", "Insight", "Intimidation", "Investigation", "Medicine",
    "Nature", "Perception", "Performance", "Persuasion", "Religion",
    "Sleight of Hand", "Stealth", "Survival"
]

# Mapping of DnD classes to their core weapon proficiencies
class_to_weapon_proficiencies = {
    "barbarian": ["Simple Weapons", "Martial Weapons"],
    "bard": ["Simple Weapons", "Hand Crossbows", "Longswords", "Rapiers", "Shortswords"],
    "cleric": ["Simple Weapons"],
    "druid": ["Clubs", "Daggers", "Darts", "Javelins", "Maces", "Quarterstaffs", "Scimitars", "Sickles", "Slings", "Spears"],
    "fighter": ["Simple Weapons", "Martial Weapons"],
    "monk": ["Simple Weapons", "Shortswords"],
    "paladin": ["Simple Weapons", "Martial Weapons"],
    "ranger": ["Simple Weapons", "Martial Weapons"],
    "rogue": ["Simple Weapons", "Hand Crossbows", "Longswords", "Rapiers", "Shortswords"],
    "sorcerer": ["Daggers", "Darts", "Slings", "Quarterstaffs", "Light Crossbows"],
    "warlock": ["Simple Weapons"],
    "wizard": ["Daggers", "Darts", "Slings", "Quarterstaffs", "Light Crossbows"],
    "artificer": ["Simple Weapons", "Martial Weapons"],
    "blood hunter": ["Simple Weapons", "Martial Weapons"]
}

# General list of additional weapon proficiencies
additional_weapon_proficiencies = [
    "Battleaxes", "Blowguns", "Glaives", "Greataxes", "Greatswords", "Halberds",
    "Lances", "Light Hammers", "Longbows", "Mauls", "Morningstars", "Nets",
    "Pikes", "Scimitars", "Shortbows", "Tridents", "War Picks", "Warhammers",
    "Whips"
]
                
# Optional races from Monsters of the Multiverse.
multiverse_races = [
    "Tiefling", "Aarakocra", "Aasimar", "Air Genasi" "Bugbear",
    "Centaur", "Changeling", "Deep Gnome", "Duergar", "Earth Genasi",
    "Eladrin", "Fairy", "Firblog", "Fire Genasi" "Githyanki", "Gothzerai",
    "Goblin", "Goliath", "Harengon", "Hobgoblin", "Kenku", "Kobold",
    "Lizardfolk", "Minotaur", "Orc", "Satyr", "Sea Elf", "Shadar-kai",
    "Shifter", "Tabaxi", "Tortle", "Triton", "Water Genasi", "Yuan-ti"
]

# Mapping of DnD classes to possible resistances
class_to_resistances = {
    "barbarian": ["Bludgeoning", "Piercing", "Slashing"],
    "bard": ["Psychic"],
    "cleric": ["Radiant", "Necrotic"],
    "druid": ["Poison"],
    "fighter": ["Force"],
    "monk": ["Radiant"],
    "paladin": ["Radiant", "Necrotic"],
    "ranger": ["Poison"],
    "rogue": ["Lightning", "Poison"],
    "sorcerer": ["Fire", "Cold", "Lightning"],
    "warlock": ["Necrotic", "Force"],
    "wizard": ["Acid", "Thunder"],
    "artificer": ["Acid", "Fire"],
    "blood hunter": ["Fire", "Necrotic"]
}

full_width_fields = ["abilities", "equipment", "proficiencies", "information", "notes"]

class SimpleGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("MMORPDND Character Generator")
        
        # Generate character button
        generate_button = tk.Button(root, text="Generate", command=self.generate_character)
        generate_button.grid(row=0, column=1, padx=2, pady=2, sticky=tk.W)

        # Save character button
        save_button = tk.Button(root, text="Save", command=self.save_action)
        save_button.grid(row=0, column=0, padx=2, pady=2)

        self.labels = [
            "folder", "name", "level", "ac", "hp", "size", "type", "alignment", "speed", 
            "resistances", "immunities", "senses", "languages", "image", "race", "class", 
            "background", "strength", "dexterity", "constitution", "intelligence", 
            "wisdom", "charisma"
        ]
        
        self.vars = {label: tk.StringVar() for label in self.labels}
        
        # Text fields with labels on the left side
        for i, label in enumerate(self.labels, start=2):
            if label == "image":
                # Image selection box.
                image_button = tk.Button(root, text=label, command=self.select_image)
                image_button.grid(row=i, column=0, sticky=tk.W)
                entry = tk.Entry(root, textvariable=self.vars[label], width=50)
                entry.grid(row=i, column=1, sticky=tk.W)
            elif label == "name":
                # name generation box.
                image_button = tk.Button(root, text=label, command=self.generate_name)
                image_button.grid(row=i, column=0, sticky=tk.W)
                entry = tk.Entry(root, textvariable=self.vars[label], width=50)
                entry.grid(row=i, column=1, sticky=tk.W)
            elif label == "class":
                # Dropdown menu for class selection
                tk.Label(root, text=label).grid(row=i, column=0, sticky=tk.E)
                self.folder_menu = ttk.Combobox(root, textvariable=self.vars[label], values=class_options, width=50)
                self.folder_menu.grid(row=i, column=1, sticky=tk.W)
            elif label == "folder":
                # Dropdown menu for folder selection
                tk.Label(root, text=label).grid(row=i, column=0, sticky=tk.E)
                self.folder_menu = ttk.Combobox(root, textvariable=self.vars[label], values=folder_options, width=50)
                self.folder_menu.grid(row=i, column=1, sticky=tk.W)
            elif label == "race":
                # Dropdown menu for race selection
                tk.Label(root, text=label).grid(row=i, column=0, sticky=tk.E)
                self.folder_menu = ttk.Combobox(root, textvariable=self.vars[label], values=race_options, width=50)
                self.folder_menu.grid(row=i, column=1, sticky=tk.W)
            else:
                tk.Label(root, text=label).grid(row=i, column=0, sticky=tk.E)
                entry = tk.Entry(root, textvariable=self.vars[label], width=50)
                entry.grid(row=i, column=1, sticky=tk.W)
                
        # Image selection button
        self.image_box = tk.Canvas(root, width=500, height=500, borderwidth=1, relief="solid")
        self.image_box.grid(row=2, rowspan=21, column=2, padx=5)

        # Text box fields spanning two columns
        for i, label in enumerate(full_width_fields, start=25):
            tk.Label(root, text=label).grid(row=i, column=0, sticky=tk.E)
            text_widget = tk.Text(root, height=3, width=120, padx=5)
            text_widget.grid(row=i, column=1, columnspan=2, sticky=tk.W)
            self.vars[label] = text_widget
        
    def generate_character(self):
        print("Generate button clicked!")
        
        # Set the base values first.
        self.vars["folder"].set(self.random_folder())
        self.vars["level"].set(self.random_level())
        self.vars["race"].set(self.random_race())
        self.vars["class"].set(self.random_class())
        self.vars["size"].set(self.random_size())
        self.vars["type"].set(self.random_type())
        self.vars["alignment"].set(self.random_alignment())
        
        # The name and speed will depend on the race so those should come before this.
        self.vars["name"].set(self.random_name())
        self.vars["speed"].set(self.random_speed())
        
        # Make the image name based on the name.
        self.vars["image"].set(self.vars["name"].get().replace(" ", "_").lower() + ".jpg")
        
        # ac and background will depend on the class.
        self.vars["ac"].set(self.random_ac())
        self.vars["background"].set(self.random_background())
        self.vars["resistances"].set(self.random_resistances())
        self.vars["immunities"].set(self.random_immunities())
        self.vars["languages"].set(self.random_languages())
        
        # Generate random character stats based on class and level.
        char_stats = generate_character_stats(self.vars["class"].get(), int(self.vars["level"].get()))
        print(char_stats)
        self.vars["strength"].set(char_stats["strength"])
        self.vars["dexterity"].set(char_stats["dexterity"])
        self.vars["constitution"].set(char_stats["constitution"])
        self.vars["intelligence"].set(char_stats["intelligence"])
        self.vars["wisdom"].set(char_stats["wisdom"])
        self.vars["charisma"].set(char_stats["charisma"])        
        
        self.vars["senses"].set(self.random_senses())
        
        # hp will depend on the level class, and constitution.
        self.vars["hp"].set(calculate_hp(self.vars["class"].get(), int(self.vars["level"].get()), char_stats["constitution"]))
        
        for label in full_width_fields:
            self.vars[label].delete("1.0", tk.END)  # Clear the Text widget
            self.vars[label].insert(tk.END, getattr(self, f"random_{label}")())  # Insert new information

    def save_action(self):
        default_file_name = self.vars["name"].get().lower().replace(" ", "_") + ".char"
        file_path = filedialog.asksaveasfilename(initialfile=default_file_name,
                                                 defaultextension=".char",
                                                 filetypes=[("Char files", "*.char"),
                                                            ("All files", "*.*")])
        if file_path:
            print(f"Save button clicked! File saved to: {file_path}")
            with open(file_path, 'w') as file:
                for label in self.labels:
                    file.write(f"{label} = {self.vars[label].get()}\n")
                for label in full_width_fields:
                    file.write(f"{label} = {self.vars[label].get('1.0', tk.END).strip()}\n")
                    
    def update_folder(self, folder_var, class_var):
        folder_text = f"characters/non-player/{class_var.get()}"
        folder_var.set(folder_text)

    def select_image(self):
        file_path = filedialog.askopenfilename(filetypes=[("Image files", "*.jpg *.png"), ("All files", "*.*")])
        if file_path:
            self.vars["image"].set(file_path)
            self.display_image(file_path)
            
    def generate_name(self):
        name = self.random_name()
        self.vars["name"].set(name)
        return name

    def display_image(self, file_path):
        img = Image.open(file_path)
        img = img.resize((500, 500), Image.ANTIALIAS)
        img = ImageTk.PhotoImage(img)
        self.image_box.create_image(0, 0, anchor=tk.NW, image=img)
        self.image_box.image = img

    # Placeholder methods for randomization logic
    def random_folder(self):
        return "characters/non-player"
    
    def random_name(self):
        # Setup the probability matrix for word generation.
        race = self.vars["race"].get().lower()
        if race == "elf":
            input_file = "lists/elven.names"
        elif race == "halfling":
            input_file = "lists/halfling.names"
        elif race == "human":
            input_file = "lists/human.names"
        elif race == "tiefling":
            input_file = "lists/tiefling.names"
        elif race == "dwarf":
            first_name = generate_word_from_file("lists/dwarven_first.names")
            last_name = generate_word_from_file("lists/dwarven_last.names")
            return first_name + " " + last_name
        else:
            first_name = generate_word_from_file("lists/asian_first.names")
            last_name = generate_word_from_file("lists/asian_last.names")
            return first_name + " " + last_name

        name = generate_word_from_file(input_file)
        return name
    
    def biased_random(self, start, end):
        weights = [1/(i+1) for i in range(end)]  # Weights decrease as the numbers increase
        total = sum(weights)
        normalized_weights = [w/total for w in weights]  # Normalize the weights to sum to 1
        return random.choices(range(start, end + 1), weights=normalized_weights, k=1)[0]
    
    def random_level(self):
        return str(self.biased_random(1, 20))
    
    def random_ac(self):
        dnd_class = self.vars["class"].get().lower()
        ac_range = class_to_ac_range.get(dnd_class)
        if not ac_range:
            return "13"
        return random.randint(*ac_range)
    
    def random_size(self):
        return "Medium"
    
    def random_type(self):
        return "Humanoid"
    
    def random_alignment(self):
        return random.choice(["Lawful Good", "Neutral Good", "Chaotic Good", 
                              "Lawful Neutral", "True Neutral", "Chaotic Neutral",
                              "Lawful Evil", "Neutral Evil", "Chaotic Evil"])
    
    def random_speed(self):
        race = self.vars["race"].get().lower()
        if race == "gnome" or race == "dwarf":
            return "25 ft."
        elif race == "elf" or race == "vryloka" or race == "gnoll" or race == "hengeyokai" or race == "thri-kreen":
            return "35 ft."
        else:
            return "30 ft."
    
    def random_resistances(self):
        dnd_class = self.vars["class"].get().lower()
        resistances = class_to_resistances.get(dnd_class, [])
        return random.sample(resistances, 1)[0]
    
    def random_immunities(self):
        return "None"
    
    def random_senses(self):
        wisdom = int(self.vars["wisdom"].get())
        wisdom_modifier = calculate_modifier(wisdom)
        return f"Passive Perception {10 + wisdom_modifier}"
    
    def random_languages(self):
        race = self.vars["race"].get().lower()
        languages = "Common"
        if race == "elf":
            languages += ", Elvish"
        elif race == "dwarf":
            languages += ", Dwarvish"
        elif race == "orc" or race == "half-orc":
            languages += ", Orcish"
        elif race == "goliath":
            languages += ", Giant"
        elif race == "Gnome":
            languages += ", Gnomish"
        elif race == "halfling":
            languages += ", Halfling"
        elif race == "goblin":
            languages += ", Goblin"
            
        new_language = random.choice(languages_list)
        
        if new_language not in languages:
            languages += f", {new_language}"
            
        return languages
    
    def random_race(self):
        return random.choice(race_options)
    
    def random_class(self):
        return random.choice(class_options)
    
    def random_background(self):
        dnd_class = self.vars["class"].get().lower()
        backgrounds = class_to_backgrounds.get(dnd_class)
        if not backgrounds:
            return "Unknown"
        return random.choice(backgrounds)
    
    def random_abilities(self):
        return "TODO"
    
    def random_equipment(self):
        return "TODO"
    
    def random_proficiencies(self):
        dnd_class = self.vars["class"].get().lower()
        
        # core proficiencies.
        core_proficiencies = class_to_proficiencies.get(dnd_class, [])
        remaining_proficiencies = list(set(additional_proficiencies) - set(core_proficiencies))
        additional_core = random.sample(remaining_proficiencies, 1)
        
        # weapon proficiencies
        core_weapon_proficiencies = class_to_weapon_proficiencies.get(dnd_class, [])
        remaining_weapon_proficiencies = list(set(additional_weapon_proficiencies) - set(core_weapon_proficiencies))
        additional_weapon = random.sample(remaining_weapon_proficiencies, 1)
        
        all_proficiencies = list(set(core_proficiencies + additional_core + core_weapon_proficiencies + additional_weapon))
        return ", ".join(all_proficiencies)
    
    def random_information(self):
        return ("TODO")
    
    def random_notes(self):
        return ("TODO")

if __name__ == "__main__":
    root = tk.Tk()
    simple_gui = SimpleGUI(root)
    root.mainloop()
