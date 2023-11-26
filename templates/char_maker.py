#!/usr/bin/env python3
import tkinter as tk
from tkinter import filedialog

class SimpleGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("MMORPDND Char Generator")
        
        # Generate button
        generate_button = tk.Button(root, text="Generate Char", command=self.generate_action)
        generate_button.grid(row=0, column=1, padx=2, pady=2, sticky=tk.W)

        # Save button
        save_button = tk.Button(root, text="Save", command=self.save_action)
        save_button.grid(row=0, column=0, padx=2, pady=2)

        labels = ["folder", "name", "level", "ac", "hp", "size", "type", "alignment", "speed", "resistances", "immunities", "senses", "languages", "image", "race", "class", "background", "strength", "dexterity", "constitution", "intelligence", "wisdom", "charisma", "abilities", "equipment", "proficiencies", "information"]
        
        self.vars = {}
        for label in labels:
            self.vars[label] = tk.StringVar()

        
        # Text fields with labels on the left side
        for i, label in enumerate(labels):
            tk.Label(root, text=label).grid(row=i + 1, column=0, sticky=tk.E)
            entry = tk.Entry(root, textvariable=self.vars[label], width=30)
            entry.grid(row=i + 1, column=1, sticky=tk.W)
            
            # Add trace to "class" entry to update "folder" entry
            if label == "class":
                self.vars[label].trace_add('write', lambda name, index, mode, var=self.vars['folder'], class_var=self.vars['class']: self.update_folder(var, class_var))


        img_height = 300
        img_width = 300
        
        image_box1 = tk.Canvas(root, width=img_width, height=img_height, borderwidth=1, relief="solid")
        image_box1.grid(row=1, rowspan=12, column=3, padx=1)
        
        image_box2 = tk.Canvas(root, width=img_width, height=img_height, borderwidth=1, relief="solid")
        image_box2.grid(row=13, rowspan=12, column=3, padx=1)
        
        image_box3 = tk.Canvas(root, width=img_width, height=img_height, borderwidth=1, relief="solid")
        image_box3.grid(row=1, rowspan=12, column=4, padx=1)
        
        image_box4 = tk.Canvas(root, width=img_width, height=img_height, borderwidth=1, relief="solid")
        image_box4.grid(row=13, rowspan=12, column=4, padx=1)
        
    def generate_action(self):
        print("Generate button clicked!")
        # Add your generate action logic here

    def save_action(self):
        file_path = filedialog.asksaveasfilename(defaultextension=".txt",
                                                   filetypes=[("Text files", "*.txt"),
                                                              ("All files", "*.*")])
        if file_path:
            print(f"Save button clicked! File saved to: {file_path}")
            # Add your save action logic here
            
    def update_folder(self, folder_var, class_var):
        # Update the "folder" entry based on the value of the "class" entry
        folder_text = f"characters/non-player/{class_var.get()}"
        folder_var.set(folder_text)

if __name__ == "__main__":
    root = tk.Tk()
    simple_gui = SimpleGUI(root)
    root.mainloop()

