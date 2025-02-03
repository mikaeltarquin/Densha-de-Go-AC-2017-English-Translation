import os
import shutil
import subprocess
import sys
import logging
from datetime import datetime

# Check that the required arguments are passed
if len(sys.argv) < 4:
    print("Usage: python installer.py <install|restore> <game_folder> <patches_folder>")
    sys.exit(1)

# Read the command-line arguments
ACTION = sys.argv[1].strip().lower()  # 'install' or 'restore'
GAME_FOLDER = sys.argv[2]  # Game folder passed as argument
PATCH_FOLDER = sys.argv[3]  # Patches folder passed as argument

# Generate backup version based on the current date
BACKUP_VERSION = f"en{datetime.now().strftime('%y%m%d')}"  # e.g., "en250201" for 2025-02-01
BACKUP_FOLDER = os.path.join(GAME_FOLDER, f"_translation_backup_{BACKUP_VERSION}")
GAME_INI_FILE = os.path.join(GAME_FOLDER, "TG4AC", "Config", "DefaultGame.ini")


# Set the working directory to GAME_FOLDER
os.chdir(GAME_FOLDER)

# Set up logging to output to the console
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

def backup_file(filepath):
    """Backs up the original .uasset file if not already backed up."""
    backup_path = os.path.join(BACKUP_FOLDER, os.path.relpath(filepath, GAME_FOLDER))
    if not os.path.exists(backup_path):
        os.makedirs(os.path.dirname(backup_path), exist_ok=True)
        shutil.copy2(filepath, backup_path)
        logging.info(f"Backed up: {filepath}")

def apply_xdelta_patch(original, patch):
    """Applies an xdelta3 patch and overwrites the original file."""
    temp_output = original + ".patched"  # Temporary file to avoid direct overwrite
    cmd = ["xdelta3", "-d", "-f", "-s", original, patch, temp_output]
    
    # Run the process in the background without creating new windows
    result = subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, text=True, shell=True)
    
    if result.returncode != 0:
        logging.error(f"Error applying patch: {result.stderr}")
    else:
        # Replace the original file with the patched version
        os.replace(temp_output, original)
        logging.info(f"Patched: {original}")

def install():
    """Installs the mod by applying patches to all .uasset files."""
    for root, _, files in os.walk(PATCH_FOLDER):
        for file in files:
            if file.endswith(".xdelta"):
                # Construct the path to the original .uasset file
                rel_path = os.path.relpath(os.path.join(root, file), PATCH_FOLDER).replace(".xdelta", "")
                original_file = os.path.join(GAME_FOLDER, rel_path)
                patch_file = os.path.join(root, file)

                # If the original .uasset file exists, back it up and apply the patch
                if os.path.exists(original_file):
                    logging.info(f"Applying patch to: {original_file}")
                    backup_file(original_file)
                    apply_xdelta_patch(original_file, patch_file)
                else:
                    logging.warning(f"Warning: Original file does not exist for patch {patch_file}")

    # Update GameVersionCode after installation
    update_game_version_code(action="install")
    logging.info("Installation completed successfully!")

def restore():
    """Restores original game files from backup."""
    for root, _, files in os.walk(BACKUP_FOLDER):
        for file in files:
            original_path = os.path.join(GAME_FOLDER, os.path.relpath(os.path.join(root, file), BACKUP_FOLDER))
            shutil.copy2(os.path.join(root, file), original_path)
            logging.info(f"Restored: {original_path}")

    # Remove the backup folder after restore
    shutil.rmtree(BACKUP_FOLDER)
    logging.info(f"Backup folder '{BACKUP_FOLDER}' deleted.")

    # Restore GameVersionCode after uninstallation by removing only the added suffix
    update_game_version_code(action="restore")
    logging.info("Restoration completed successfully!")

def update_game_version_code(action):
    """Updates the GameVersionCode in DefaultGame.ini."""
    if not os.path.exists(GAME_INI_FILE):
        logging.error(f"Error: {GAME_INI_FILE} does not exist!")
        return

    try:
        logging.info(f"Reading {GAME_INI_FILE} to update GameVersionCode...")
        with open(GAME_INI_FILE, "r", encoding="utf-8") as file:  # Explicitly specify UTF-8 encoding
            lines = file.readlines()

        # Find the GameVersionCode line and update it
        for i, line in enumerate(lines):
            if line.startswith("GameVersionCode"):
                version_code = line.strip().split("=")[1]
                logging.info(f"Found GameVersionCode: {version_code}")

                if action == "install":
                    # If action is install, add the suffix
                    if not version_code.endswith(f"-{BACKUP_VERSION}"):
                        lines[i] = f"GameVersionCode={version_code}-{BACKUP_VERSION}\n"
                        logging.info(f"Updated GameVersionCode to: {version_code}-{BACKUP_VERSION}")
                    else:
                        logging.info(f"Suffix '{BACKUP_VERSION}' already present in GameVersionCode.")

                elif action == "restore":
                    # If action is restore, remove the suffix
                    if version_code.endswith(f"-{BACKUP_VERSION}"):
                        base_version = version_code[:-len(f"-{BACKUP_VERSION}")]
                        lines[i] = f"GameVersionCode={base_version}\n"
                        logging.info(f"Restored GameVersionCode to: {base_version}")
                    else:
                        logging.info(f"No suffix found in GameVersionCode, no changes made.")
                break
        else:
            logging.warning("GameVersionCode not found in the ini file!")

        # Write the updated lines back to the file
        with open(GAME_INI_FILE, "w", encoding="utf-8") as file:
            file.writelines(lines)
        logging.info(f"Updated GameVersionCode in {GAME_INI_FILE}")
    except Exception as e:
        logging.error(f"Error updating GameVersionCode: {e}")

if __name__ == "__main__":
    if ACTION == "install":
        install()
    elif ACTION == "restore":
        restore()
    else:
        logging.error("Invalid choice. Please use 'install' or 'restore'.")
