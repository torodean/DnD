import os
import shutil

def copy_images(source_dir, dest_dir):
    for root, _, files in os.walk(source_dir):
        img_folder = os.path.join(root, "img")
        if os.path.exists(img_folder) and os.path.isdir(img_folder):
            for img_file in files:
                if img_file.lower().endswith((".png", ".jpg", ".jpeg", ".gif")):
                    source_path = os.path.join(img_folder, img_file)
                    dest_path = os.path.join(dest_dir, img_file)
                    #shutil.copy(source_path, dest_path)
                    print(f"Copied: {source_path} -> {dest_path}")

if __name__ == "__main__":
    script_dir = os.path.dirname(os.path.abspath(__file__))
    campaign_dir = os.path.join(script_dir, "..", "campaign")
    dest_img_dir = os.path.join(script_dir, "img")

    copy_images(campaign_dir, dest_img_dir)
