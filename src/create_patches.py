import os
import subprocess

# Directories to compare
ORIGINAL_DIR = r"C:\Densha5.80.02"  # Original game directory
MODIFIED_DIR = r"C:\Densha5.80.02-en"  # Directory containing modified files
PATCH_DIR = r"D:\DenshaProject\__installer\patches"  # Directory to store patches

# Directories to search for .uasset files
DIRECTORIES_TO_SEARCH = [
    "DGOREPR",
    "TG4AC\\Content\\Art\\Data_2D",
    "TG4AC\\Content\\Blueprints",
    "TG4AC\\Content\\DataTables"
]

def files_are_different(file1, file2):
    """Check if two files are different using a binary comparison."""
    return not os.path.exists(file1) or not os.path.exists(file2) or open(file1, 'rb').read() != open(file2, 'rb').read()

def create_patches():
    """Generates xdelta3 patches only for modified .uasset files."""
    for dir_to_search in DIRECTORIES_TO_SEARCH:
        full_dir_path = os.path.join(MODIFIED_DIR, dir_to_search)
        if os.path.exists(full_dir_path):
            print(f"Searching in: {full_dir_path}")
            for root, _, files in os.walk(full_dir_path):
                for file in files:
                    if file.endswith(".uasset"):
                        mod_file = os.path.join(root, file)
                        rel_path = os.path.relpath(mod_file, MODIFIED_DIR)
                        orig_file = os.path.join(ORIGINAL_DIR, rel_path)
                        patch_file = os.path.join(PATCH_DIR, rel_path + ".xdelta")

                        # Skip unchanged files
                        if os.path.exists(orig_file) and not files_are_different(orig_file, mod_file):
                            print(f"Skipping unchanged file: {rel_path}")
                            continue

                        # Create necessary directories for the patch file
                        os.makedirs(os.path.dirname(patch_file), exist_ok=True)

                        # Create patch using xdelta3
                        cmd = ["xdelta3", "-e", "-s", orig_file, mod_file, patch_file]
                        subprocess.run(cmd, check=True)
                        print(f"Created patch: {patch_file}")
        else:
            print(f"Warning: Directory not found: {full_dir_path}")

if __name__ == "__main__":
    create_patches()
