import os

root_dir = "dummy_directory"

if not os.path.exists(root_dir):
    os.makedirs(root_dir)

for i in range(4):
    dir_name = f"level_{i}"
    dir_path = os.path.join(root_dir, dir_name)
    if not os.path.exists(dir_path):
        os.makedirs(dir_path)
    for j in range(3):
        sub_dir_name = f"subdirectory_{j}"
        sub_dir_path = os.path.join(dir_path, sub_dir_name)
        if not os.path.exists(sub_dir_path):
            os.makedirs(sub_dir_path)
            
print("Dummy directory tree created!")