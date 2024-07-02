#!/usr/bin/env python3
import tkinter as tk
from tkinter import filedialog, ttk
import random
#from PIL import Image, ImageTk

# Import character generation methods from creator.
from creator import generate_character_stats
from creator import calculate_hp

folder_options = ["characters/non-player", 
                  "characters/player", 
                  "creatures/monsters", 
                  "creatures/animals", 
                  "creatures/humanoids", 
                  "creatures/dragons", 
                  "creatures/other"]
                  
class_options = ["Barbarian",
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
                 "Blood Hunter"]
# PHB races.        
race_options = ["Human",
                "Elf",
                "Dwarf",
                "Gnome",
                "Half-Elf",
                "Dragonborn",
                "Halfling",
                "Half-Orc"]
                
# Optional races from Monsters of the Multiverse.
multiverse_races = ["Tiefling", "Aarakocra", "Aasimar", "Air Genasi" "Bugbear",
                    "Centaur", "Changeling", "Deep Gnome", "Duergar", "Earth Genasi",
                    "Eladrin", "Fairy", "Firblog", "Fire Genasi" "Githyanki", "Gothzerai",
                    "Goblin", "Goliath", "Harengon", "Hobgoblin", "Kenku", "Kobold",
                    "Lizardfolk", "Minotaur", "Orc", "Satyr", "Sea Elf", "Shadar-kai",
                    "Shifter", "Tabaxi", "Tortle", "Triton", "Water Genasi", "Yuan-ti"]

full_width_fields = ["abilities", "equipment", "proficiencies", "information", "notes"]

class SimpleGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("MMORPDND Char Generator")
        
        # Generate character button
        generate_button = tk.Button(root, text="Generate Char", command=self.generate_character)
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
        self.vars["senses"].set(self.random_senses())
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
        
        # hp will depend on the level class, and constitution.
        self.vars["hp"].set(calculate_hp(self.vars["class"].get(), int(self.vars["level"].get()), char_stats["constitution"]))
        
        for label in full_width_fields:
            self.vars[label].delete("1.0", tk.END)  # Clear the Text widget
            self.vars[label].insert(tk.END, getattr(self, f"random_{label}")())  # Insert new information

    def save_action(self):
        file_path = filedialog.asksaveasfilename(defaultextension=".char",
                                                 filetypes=[("Char files", "*.char"),
                                                            ("All files", "*.*")])
        if file_path:
            print(f"Save button clicked! File saved to: {file_path}")
            with open(file_path, 'w') as file:
                for label in self.labels:
                    if label in full_width_fields:
                        file.write(f"{label} = {self.vars[label].get('1.0', tk.END).strip()}\n")
                    else:
                        file.write(f"{label} = {self.vars[label].get()}\n")
                    
    def update_folder(self, folder_var, class_var):
        folder_text = f"characters/non-player/{class_var.get()}"
        folder_var.set(folder_text)

    def select_image(self):
        file_path = filedialog.askopenfilename(filetypes=[("Image files", "*.jpg *.png"), ("All files", "*.*")])
        if file_path:
            self.vars["image"].set(file_path)
            self.display_image(file_path)
            
    def generate_name(self):
        return "generated name"

    def display_image(self, file_path):
        #img = Image.open(file_path)
        #img = img.resize((500, 500), Image.ANTIALIAS)
        #img = ImageTk.PhotoImage(img)
        self.image_box.create_image(0, 0, anchor=tk.NW, image=img)
        self.image_box.image = img

    # Placeholder methods for randomization logic
    def random_folder(self):
        return "characters/non-player"
    
    def random_name(self):
        return "Abigail Reed"
    
    def biased_random(self, start, end):
        weights = [1/(i+1) for i in range(end)]  # Weights decrease as the numbers increase
        total = sum(weights)
        normalized_weights = [w/total for w in weights]  # Normalize the weights to sum to 1
        return random.choices(range(start, end + 1), weights=normalized_weights, k=1)[0]
    
    def random_level(self):
        return str(self.biased_random(1, 20))
    
    def random_ac(self):
        return "13 (studded leather armor)"
    
    def random_size(self):
        return "Medium"
    
    def random_type(self):
        return "Humanoid"
    
    def random_alignment(self):
        return random.choice(["Lawful Good", "Neutral Good", "Chaotic Good", 
                              "Lawful Neutral", "True Neutral", "Chaotic Neutral",
                              "Lawful Evil", "Neutral Evil", "Chaotic Evil"])
    
    def random_speed(self):
        return "30 ft."
    
    def random_resistances(self):
        return "None"
    
    def random_immunities(self):
        return "None"
    
    def random_senses(self):
        return "Passive Perception 12"
    
    def random_languages(self):
        return "Common"
    
    def random_image(self):
        return "abigail_reed.jpg"
    
    def random_race(self):
        return random.choice(race_options)
    
    def random_class(self):
        return random.choice(class_options)
    
    def random_background(self):
        return "Farmer"    
    
    def random_abilities(self):
        return "TODO"
    
    def random_equipment(self):
        return "TODO"
    
    def random_proficiencies(self):
        return "TODO"
    
    def random_information(self):
        return ("TODO")
    
    def random_notes(self):
        return ("TODO")

if __name__ == "__main__":
    root = tk.Tk()
    simple_gui = SimpleGUI(root)
    root.mainloop()

