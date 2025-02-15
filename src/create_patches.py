import os
import subprocess
import shutil

# Directories to compare
ORIGINAL_DIR = r"C:\Densha5.80.02"  # Original game directory
MODIFIED_DIR = r"C:\Densha5.80.02-en"  # Directory containing modified files
PATCH_DIR = r"D:\DenshaProject\__installer\patches"  # Directory to store patches

# Music file paths
MUSIC_PATH = os.path.join("TG4AC", "Content", "DataTables", "LaunchProduction")
BASE_MUSIC_FILE = "LaunchProductionAnnounce.uasset"
BASE_UTILITY_FILE = "LaunchProductionUtilityData.uasset"

# Special handling for music file variants
MUSIC_VARIANTS = {
    "default": BASE_MUSIC_FILE,
    "new_ike_kan": BASE_MUSIC_FILE + ".bak.new_ike_kan",
    "new_tky_sjk": BASE_MUSIC_FILE + ".bak.new_tky_sjk",
    "old_all": BASE_MUSIC_FILE + ".bak.old_all"
}

# Directories to search for other files
DIRECTORIES_TO_SEARCH = [
    "DGOREPR",
    "TG4AC\\Content\\Art\\Data_2D",
    "TG4AC\\Content\\Blueprints",
    "TG4AC\\Content\\DataTables",
    "TG4AC\\Content\\Sound"
]

# File extensions to process
FILE_EXTENSIONS = (".uasset", ".acb", ".awb")

def create_patches():
    """Generates xdelta3 patches for modified .uasset, .acb, and .awb files."""
    # Clean up existing patches directory
    if os.path.exists(PATCH_DIR):
        print(f"Removing existing patches directory: {PATCH_DIR}")
        shutil.rmtree(PATCH_DIR)
    os.makedirs(PATCH_DIR)
    print("Created fresh patches directory")

    # Create music patches directory
    music_patch_dir = os.path.join(PATCH_DIR, "music")
    os.makedirs(music_patch_dir, exist_ok=True)
    
    # Get the original announce file from its exact location
    original_announce = os.path.join(ORIGINAL_DIR, MUSIC_PATH, BASE_MUSIC_FILE)
    if not os.path.exists(original_announce):
        print(f"ERROR: Could not find original announce file at {original_announce}")
        return
    print(f"Found original announce file: {original_announce}")

    # Get the original utility file from its exact location
    original_utility = os.path.join(ORIGINAL_DIR, MUSIC_PATH, BASE_UTILITY_FILE)
    if not os.path.exists(original_utility):
        print(f"ERROR: Could not find original utility file at {original_utility}")
        return
    print(f"Found original utility file: {original_utility}")

    # Create patches for each music variant
    modified_music_dir = os.path.join(MODIFIED_DIR, MUSIC_PATH)
    for variant_name, variant_file in MUSIC_VARIANTS.items():
        mod_file_path = os.path.join(modified_music_dir, variant_file)
        if os.path.exists(mod_file_path):
            # Determine patch name
            if variant_name == "default":
                patch_name = f"{BASE_MUSIC_FILE}.xdelta"
            else:
                patch_name = f"{BASE_MUSIC_FILE}.{variant_name}.xdelta"
            
            patch_path = os.path.join(music_patch_dir, patch_name)
            print(f"\nCreating patch for {variant_name}...")
            print(f"Source: {original_announce}")
            print(f"Target: {mod_file_path}")
            
            # Create the patch
            cmd = ["xdelta3", "-e", "-s", original_announce, mod_file_path, patch_path]
            try:
                subprocess.run(cmd, check=True)
                print(f"Created patch: {patch_path}")
            except subprocess.CalledProcessError as e:
                print(f"Error creating patch for {variant_file}: {e}")
        else:
            print(f"Warning: Variant file not found: {mod_file_path}")

    # Create patch for music utility file
    mod_file_path = os.path.join(modified_music_dir, BASE_UTILITY_FILE)
    patch_name = f"{BASE_UTILITY_FILE}.xdelta"
    patch_path = os.path.join(music_patch_dir, patch_name)
    cmd = ["xdelta3", "-e", "-s", original_utility, mod_file_path, patch_path]
    try:
        subprocess.run(cmd, check=True)
        print(f"Created patch: {patch_path}")
    except subprocess.CalledProcessError as e:
        print(f"Error creating patch for {BASE_UTILITY_FILE}: {e}")

    # Now handle all other files with specified extensions
    print("\nProcessing other files...")
    for dir_to_search in DIRECTORIES_TO_SEARCH:
        full_dir_path = os.path.join(MODIFIED_DIR, dir_to_search)
        if os.path.exists(full_dir_path):
            print(f"Searching in: {full_dir_path}")
            for root, _, files in os.walk(full_dir_path):
                for file in files:
                    # Skip music variants and utility data as they're handled separately
                    if any(variant in file for variant in MUSIC_VARIANTS.values()) or file == BASE_UTILITY_FILE:
                        continue
                        
                    if file.endswith(FILE_EXTENSIONS):
                        mod_file = os.path.join(root, file)
                        rel_path = os.path.relpath(mod_file, MODIFIED_DIR)
                        orig_file = os.path.join(ORIGINAL_DIR, rel_path)
                        patch_file = os.path.join(PATCH_DIR, rel_path + ".xdelta")

                        if not os.path.exists(orig_file):
                            print(f"Original file not found: {orig_file}")
                            continue

                        if open(orig_file, 'rb').read() == open(mod_file, 'rb').read():
                            print(f"Skipping unchanged file: {rel_path}")
                            continue

                        os.makedirs(os.path.dirname(patch_file), exist_ok=True)
                        
                        cmd = ["xdelta3", "-e", "-s", orig_file, mod_file, patch_file]
                        try:
                            subprocess.run(cmd, check=True)
                            print(f"Created patch: {patch_file}")
                        except subprocess.CalledProcessError as e:
                            print(f"Error creating patch for {file}: {e}")
        else:
            print(f"Warning: Directory not found: {full_dir_path}")

if __name__ == "__main__":
    create_patches()