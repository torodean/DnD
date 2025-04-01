from PIL import Image
import os

def resize_to_icon(input_path, output_path, size=(64, 64)):
    # Open the image
    img = Image.open(input_path).convert("RGBA")  # Preserve transparency

    # Resize while maintaining aspect ratio
    img.thumbnail(size, Image.Resampling.LANCZOS)  # High-quality resizing

    # Create a new square canvas with transparent background
    new_img = Image.new("RGBA", size, (0, 0, 0, 0))
    
    # Calculate position to center the resized image
    paste_x = (size[0] - img.width) // 2
    paste_y = (size[1] - img.height) // 2
    new_img.paste(img, (paste_x, paste_y), img)  # Use mask for transparency

    # Save as ICO
    new_img.save(output_path, "ICO")

# Use the script's current directory
current_folder = os.path.dirname(os.path.abspath(__file__))
target_size = (128, 128)  # Set your desired icon size here

# Process all PNG files in the current folder
for filename in os.listdir(current_folder):
    if filename.lower().endswith(".png"):  # Case-insensitive check
        # Full path to input file
        input_path = os.path.join(current_folder, filename)
        # Keep the base filename, change extension to .ico
        base_name = os.path.splitext(filename)[0]
        output_filename = f"{base_name}.ico"
        output_path = os.path.join(current_folder, output_filename)
        
        resize_to_icon(input_path, output_path, target_size)
        print(f"Converted {filename} to {output_filename}")