import os
import shutil
import subprocess
import sys
import logging
from datetime import datetime

# Music configuration
MUSIC_OPTIONS = {
    "1": {"name": "Default Melodies (Classic + New Kanda/Ikebukuro)", 
          "announce_patch": "music/LaunchProductionAnnounce.uasset.xdelta",
          "needs_utility": True},
    "2": {"name": "Classic Melodies Only", 
          "announce_patch": "music/LaunchProductionAnnounce.uasset.old_all.xdelta",
          "needs_utility": True},
    "3": {"name": "New Tokyo/Shinjuku/Kanda/Ikebukuro Melodies", 
          "announce_patch": "music/LaunchProductionAnnounce.uasset.new_tky_sjk.xdelta",
          "needs_utility": True},
    "4": {"name": "No Melodies", 
          "announce_patch": None,
          "needs_utility": False}
}

MUSIC_FILE = "LaunchProductionAnnounce.uasset"
MUSIC_PATH = os.path.join("TG4AC", "Content", "DataTables", "LaunchProduction")
UTILITY_FILE = "LaunchProductionUtilityData.uasset"

# Check that the required arguments are passed
if len(sys.argv) < 4:
    print("Usage: python installer.py <install|restore|switch_music> <game_folder> <patches_folder> [music_option]")
    sys.exit(1)

# Read the command-line arguments
ACTION = sys.argv[1].strip().lower()  # 'install', 'restore', or 'switch_music'
GAME_FOLDER = sys.argv[2]  # Game folder passed as argument
PATCH_FOLDER = sys.argv[3]  # Patches folder passed as argument
MUSIC_CHOICE = sys.argv[4] if len(sys.argv) > 4 else None  # Optional music choice

# Generate backup version based on the current date
BACKUP_VERSION = f"en{datetime.now().strftime('%y%m%d')}"  # e.g., "en250214" for 2025-02-14
BACKUP_FOLDER = os.path.join(GAME_FOLDER, f"_translation_backup_{BACKUP_VERSION}")
GAME_INI_FILE = os.path.join(GAME_FOLDER, "TG4AC", "Config", "DefaultGame.ini")

# Set up logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

def backup_music_files():
    """Creates a backup of the original music and utility files if they don't exist."""
    backup_path = os.path.join(BACKUP_FOLDER, MUSIC_PATH)
    os.makedirs(backup_path, exist_ok=True)
    
    # Backup both files
    for filename in [MUSIC_FILE, UTILITY_FILE]:
        source_file = os.path.join(GAME_FOLDER, MUSIC_PATH, filename)
        if os.path.exists(source_file):
            backup_file = os.path.join(backup_path, filename)
            if not os.path.exists(backup_file):
                shutil.copy2(source_file, backup_file)
                logging.info(f"Backed up file: {filename}")

def apply_music_patch(option):
    """Applies the selected music patch and utility file if needed."""
    if option not in MUSIC_OPTIONS:
        logging.error(f"Invalid music option: {option}")
        return False

    # Get patch details
    patch_info = MUSIC_OPTIONS[option]
    
    # Get file paths
    backup_announce = os.path.join(BACKUP_FOLDER, MUSIC_PATH, MUSIC_FILE)
    target_announce = os.path.join(GAME_FOLDER, MUSIC_PATH, MUSIC_FILE)
    backup_utility = os.path.join(BACKUP_FOLDER, MUSIC_PATH, UTILITY_FILE)
    target_utility = os.path.join(GAME_FOLDER, MUSIC_PATH, UTILITY_FILE)

    # Restore original files first
    if os.path.exists(backup_announce) and os.path.exists(backup_utility):
        shutil.copy2(backup_announce, target_announce)
        shutil.copy2(backup_utility, target_utility)
    else:
        logging.error("Original file backups not found")
        return False

    # For No Melodies option, we're done after restoring originals
    if not patch_info["needs_utility"]:
        logging.info("Restored original files")
        return True
    
    # Apply patches for other options
    announce_patch = os.path.join(PATCH_FOLDER, patch_info["announce_patch"])
    utility_patch = os.path.join(PATCH_FOLDER, "music", f"{UTILITY_FILE}.xdelta")
    
    if not os.path.exists(announce_patch) or not os.path.exists(utility_patch):
        logging.error("Required patch files not found")
        return False
        
    try:
        # Apply announce patch
        temp_announce = target_announce + ".patched"
        cmd = ["xdelta3", "-d", "-s", target_announce, announce_patch, temp_announce]
        subprocess.run(cmd, check=True)
        os.replace(temp_announce, target_announce)
        
        # Apply utility patch
        temp_utility = target_utility + ".patched"
        cmd = ["xdelta3", "-d", "-s", target_utility, utility_patch, temp_utility]
        subprocess.run(cmd, check=True)
        os.replace(temp_utility, target_utility)
        
        logging.info(f"Applied music patches: {patch_info['name']}")
        return True
    except subprocess.CalledProcessError as e:
        logging.error(f"Error applying patches: {e}")
        for temp_file in [temp_announce, temp_utility]:
            if os.path.exists(temp_file):
                os.remove(temp_file)
        return False

def backup_file(filepath):
    """Backs up a file, preserving its directory structure."""
    backup_path = os.path.join(BACKUP_FOLDER, os.path.relpath(filepath, GAME_FOLDER))
    if not os.path.exists(backup_path):
        os.makedirs(os.path.dirname(backup_path), exist_ok=True)
        shutil.copy2(filepath, backup_path)
        logging.info(f"Backed up: {filepath}")

def install():
    """Installs the mod and applies selected music option."""
    # First handle regular patches
    for root, _, files in os.walk(PATCH_FOLDER):
        for file in files:
            if file.endswith(".xdelta") and not file.startswith("LaunchProductionAnnounce"):
                rel_path = os.path.relpath(os.path.join(root, file), PATCH_FOLDER)
                original_file = os.path.join(GAME_FOLDER, rel_path.replace(".xdelta", ""))
                patch_file = os.path.join(root, file)

                if os.path.exists(original_file):
                    logging.info(f"Applying patch to: {original_file}")
                    backup_file(original_file)
                    
                    # Apply patch
                    temp_output = original_file + ".patched"
                    cmd = ["xdelta3", "-d", "-s", original_file, patch_file, temp_output]
                    subprocess.run(cmd, check=True)
                    os.replace(temp_output, original_file)
                else:
                    logging.warning(f"Original file not found: {original_file}")

    # Then handle music if option specified
    if MUSIC_CHOICE:
        backup_music_files()
        if not apply_music_patch(MUSIC_CHOICE):
            logging.error("Failed to apply music patch")
            return False

    # Update GameVersionCode
    update_game_version_code(action="install")
    logging.info("Installation completed successfully!")
    return True

def restore():
    """Restores original game files from backup."""
    if not os.path.exists(BACKUP_FOLDER):
        logging.error(f"Backup folder not found: {BACKUP_FOLDER}")
        return False

    for root, _, files in os.walk(BACKUP_FOLDER):
        for file in files:
            backup_path = os.path.join(root, file)
            relative_path = os.path.relpath(backup_path, BACKUP_FOLDER)
            original_path = os.path.join(GAME_FOLDER, relative_path)
            
            os.makedirs(os.path.dirname(original_path), exist_ok=True)
            shutil.copy2(backup_path, original_path)
            logging.info(f"Restored: {original_path}")

    # Remove backup folder
    shutil.rmtree(BACKUP_FOLDER)
    logging.info(f"Backup folder '{BACKUP_FOLDER}' deleted")

    # Restore GameVersionCode
    update_game_version_code(action="restore")
    logging.info("Restoration completed successfully!")
    return True

def switch_music():
    """Interactive menu for switching music options."""
    if len(sys.argv) < 3:
        print("Error: Not enough arguments")
        print("Usage: installer.py switch_music <game_folder> <patches_folder> [music_option]")
        return False

    game_dir = os.path.abspath(sys.argv[2])
    patches_dir = os.path.abspath(sys.argv[3])
    temp_dir = None
    
    # Only show menu if no choice was provided as argument
    if len(sys.argv) <= 4:
        print("\nAvailable Music Options:")
        for key, option in MUSIC_OPTIONS.items():
            print(f"{key}. {option['name']}")
        choice = input("\nSelect music option (1-4): ").strip()
    else:
        choice = sys.argv[4]

    try:
        if choice not in MUSIC_OPTIONS:
            print("\nInvalid option selected")
            return False

        # Find backup folder
        backup_root = None
        for item in os.listdir(game_dir):
            if item.startswith("_translation_backup_"):
                backup_root = os.path.join(game_dir, item)
                break

        if not backup_root:
            print("Error: Could not find backup folder for restoration")
            return False

        # Get file paths
        backup_announce = os.path.join(backup_root, MUSIC_PATH, MUSIC_FILE)
        target_announce = os.path.join(game_dir, MUSIC_PATH, MUSIC_FILE)
        backup_utility = os.path.join(backup_root, MUSIC_PATH, UTILITY_FILE)
        target_utility = os.path.join(game_dir, MUSIC_PATH, UTILITY_FILE)
        
        if not os.path.exists(backup_announce) or not os.path.exists(backup_utility):
            print(f"Error: Original file backups not found")
            return False

        # Ensure target directory exists
        os.makedirs(os.path.dirname(target_announce), exist_ok=True)
        
        # Restore original files first
        shutil.copy2(backup_announce, target_announce)
        shutil.copy2(backup_utility, target_utility)

        # Get patch info
        patch_info = MUSIC_OPTIONS[choice]

        # For option 4 (No Melodies), we're done after restoring originals
        if not patch_info["needs_utility"]:
            print(f"\nSuccessfully switched to: {patch_info['name']}")
            return True

        # Get patch file paths
        announce_patch = os.path.join(patches_dir, patch_info["announce_patch"])
        utility_patch = os.path.join(patches_dir, "music", f"{UTILITY_FILE}.xdelta")
        
        if not os.path.exists(announce_patch) or not os.path.exists(utility_patch):
            print(f"Error: Required patch files not found")
            return False

        # Create temporary directory
        temp_dir = os.path.join(game_dir, "temp")
        os.makedirs(temp_dir, exist_ok=True)

        # Apply announce patch
        temp_announce = os.path.join(temp_dir, "temp_announce.uasset")
        cmd = ["xdelta3", "-d", "-s", target_announce, announce_patch, temp_announce]
        result = subprocess.run(cmd, capture_output=True, text=True)
        if result.returncode != 0:
            print(f"Error applying announce patch: {result.stderr}")
            return False
        shutil.move(temp_announce, target_announce)

        # Apply utility patch
        temp_utility = os.path.join(temp_dir, "temp_utility.uasset")
        cmd = ["xdelta3", "-d", "-s", target_utility, utility_patch, temp_utility]
        result = subprocess.run(cmd, capture_output=True, text=True)
        if result.returncode != 0:
            print(f"Error applying utility patch: {result.stderr}")
            return False
        shutil.move(temp_utility, target_utility)

        print(f"\nSuccessfully switched to: {patch_info['name']}")
        return True

    except Exception as e:
        print(f"Error during switching: {str(e)}")
        import traceback
        traceback.print_exc()
        return False
        
    finally:
        # Clean up temp directory if it exists
        if temp_dir and os.path.exists(temp_dir):
            try:
                shutil.rmtree(temp_dir)
            except Exception:
                pass

def update_game_version_code(action):
    """Updates the GameVersionCode in DefaultGame.ini."""
    if not os.path.exists(GAME_INI_FILE):
        logging.error(f"Game INI file not found: {GAME_INI_FILE}")
        return

    try:
        with open(GAME_INI_FILE, "r", encoding="utf-8") as file:
            lines = file.readlines()

        for i, line in enumerate(lines):
            if line.startswith("GameVersionCode"):
                version_code = line.strip().split("=")[1]
                
                if action == "install":
                    if not version_code.endswith(f"-{BACKUP_VERSION}"):
                        lines[i] = f"GameVersionCode={version_code}-{BACKUP_VERSION}\n"
                elif action == "restore":
                    if version_code.endswith(f"-{BACKUP_VERSION}"):
                        base_version = version_code[:-len(f"-{BACKUP_VERSION}")]
                        lines[i] = f"GameVersionCode={base_version}\n"
                break

        with open(GAME_INI_FILE, "w", encoding="utf-8") as file:
            file.writelines(lines)
    except Exception as e:
        logging.error(f"Error updating GameVersionCode: {e}")

if __name__ == "__main__":
    # Set the working directory to GAME_FOLDER
    os.chdir(GAME_FOLDER)
    
    success = False
    if ACTION == "install":
        success = install()
    elif ACTION == "restore":
        success = restore()
    elif ACTION == "switch_music":
        success = switch_music()
    else:
        logging.error("Invalid action. Use 'install', 'restore', or 'switch_music'")
    
    sys.exit(0 if success else 1)