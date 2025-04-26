#!/usr/bin/env python3
"""
Requirements.txt Updater Script

This script helps update Python requirements.txt files by creating virtual environments,
installing current dependencies, and updating them to their latest versions.
It creates backups of the original files and can show diffs between versions.
"""
import os
import sys
import shutil
import subprocess
import glob
import argparse
import atexit
import uuid
import time
from datetime import datetime
from typing import Dict, List, Optional, Any, Tuple, Set


# ANSI color codes (standard terminal colors)
class Colors:
    """Terminal color codes using ANSI escape sequences"""
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


def color_text(text: str, color_code: str) -> str:
    """
    Add color to text for terminal output
    
    Args:
        text: The text to color
        color_code: The ANSI color code to use
        
    Returns:
        Colored text string
    """
    # Check if running in a terminal that supports colors
    if sys.stdout.isatty():
        return f"{color_code}{text}{Colors.ENDC}"
    return text


# List to track all created backup files
all_backup_files = []
# List to track all temporary directories
temp_directories = []


def setup_temp_directory() -> str:
    """
    Create a temporary directory in the .tmp folder
    
    Returns:
        Path to the temporary directory
    """
    # Create base .tmp directory if it doesn't exist
    base_tmp_dir = os.path.join(os.getcwd(), ".tmp")
    os.makedirs(base_tmp_dir, exist_ok=True)
    
    # Create a unique subdirectory using timestamp and UUID
    dir_name = f"venv_{int(time.time())}_{uuid.uuid4().hex[:8]}"
    temp_dir = os.path.join(base_tmp_dir, dir_name)
    os.makedirs(temp_dir, exist_ok=True)
    
    # Add to tracking list
    temp_directories.append(temp_dir)
    return temp_dir


def cleanup_temp_directories() -> None:
    """Clean up all created temporary directories"""
    for dir_path in temp_directories:
        if os.path.exists(dir_path):
            print(f"Cleaning up temporary directory: {dir_path}")
            try:
                shutil.rmtree(dir_path)
            except Exception as e:
                print(f"Warning: Failed to remove temporary directory {dir_path}: {e}")


def create_backup(requirements_file: str) -> str:
    """
    Creates a backup of the requirements.txt file with date
    
    Args:
        requirements_file: Path to the requirements file
        
    Returns:
        Path to the created backup file
    """
    backup_date = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_dir = os.path.dirname(requirements_file)
    base_name = os.path.basename(requirements_file)
    file_name = os.path.splitext(base_name)[0]
    extension = os.path.splitext(base_name)[1]
    
    backup_name = f"{file_name}_backup_{backup_date}{extension}"
    backup_path = os.path.join(backup_dir, backup_name)
    
    shutil.copy2(requirements_file, backup_path)
    print(color_text(f"Created backup: {backup_path}", Colors.BLUE))
    
    # Add to global tracking list
    all_backup_files.append(backup_path)
    return backup_path


def check_git_available() -> bool:
    """
    Checks if git is available on the system
    
    Returns:
        True if git is available, False otherwise
    """
    try:
        subprocess.run(["git", "--version"], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        return True
    except (subprocess.SubprocessError, FileNotFoundError):
        return False


def show_file_diff(original_file: str, updated_file: str) -> str:
    """
    Shows differences between two files using git diff or other tools
    
    Args:
        original_file: Path to the original file
        updated_file: Path to the updated file
        
    Returns:
        String containing the diff output
    """
    if not check_git_available():
        return color_text("Git is not available on your system. Cannot display diff.", Colors.YELLOW)
    
    try:
        # Use git diff with --no-index to compare files outside repository
        result = subprocess.run(
            ["git", "diff", "--no-index", "--color=always", original_file, updated_file], 
            check=False, 
            stdout=subprocess.PIPE, 
            stderr=subprocess.PIPE,
            text=True
        )
        
        # git diff --no-index returns exit code 1 when files differ, which is normal
        if result.returncode > 1:
            return color_text(f"Error executing git diff: {result.stderr}", Colors.RED)
        
        if not result.stdout.strip():
            return color_text("No changes detected in the file.", Colors.YELLOW)
        
        return result.stdout
    except Exception as e:
        return color_text(f"Error executing diff: {str(e)}", Colors.RED)


def parse_requirements(file_path: str) -> List[str]:
    """
    Parse a requirements file and return a list of package specifications
    
    Args:
        file_path: Path to the requirements file
        
    Returns:
        List of package specifications
    """
    requirements = []
    with open(file_path, 'r') as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith('#'):
                requirements.append(line)
    return requirements


def update_requirements(requirements_file: str, use_freeze: bool = False) -> Dict[str, str]:
    """
    Updates requirements.txt file by creating venv, installing and updating packages
    
    Args:
        requirements_file: Path to the requirements file
        use_freeze: Whether to use pip freeze (include all subdependencies)
        
    Returns:
        Dictionary containing paths to the updated and backup files
    """
    file_dir = os.path.dirname(requirements_file)
    if not file_dir:
        file_dir = "."
    
    print(color_text(f"\nUpdating file: {requirements_file}", Colors.CYAN))
    
    # Parse original requirements to maintain the same format
    original_requirements = parse_requirements(requirements_file)
    
    # Create backup
    backup_file = create_backup(requirements_file)
    
    # Create local temporary directory
    temp_dir = setup_temp_directory()
    venv_path = os.path.join(temp_dir, "venv")
    
    try:
        # Create venv
        print(color_text(f"Creating virtualenv in: {venv_path}", Colors.BLUE))
        subprocess.run([sys.executable, "-m", "venv", venv_path], check=True)
        
        # Path to pip in venv
        if os.name == 'nt':  # Windows
            pip_path = os.path.join(venv_path, "Scripts", "pip")
            python_path = os.path.join(venv_path, "Scripts", "python")
        else:  # Linux/MacOS
            pip_path = os.path.join(venv_path, "bin", "pip")
            python_path = os.path.join(venv_path, "bin", "python")
        
        # Update pip
        print(color_text("Updating pip...", Colors.BLUE))
        subprocess.run([pip_path, "install", "--upgrade", "pip"], check=True)
        
        # Install packages from requirements.txt
        print(color_text(f"Installing packages from {requirements_file}...", Colors.BLUE))
        subprocess.run([pip_path, "install", "-r", requirements_file], check=True)
        
        if use_freeze:
            # Use pip freeze to get all dependencies
            print(color_text("Generating requirements using pip freeze (including all subdependencies)...", Colors.BLUE))
            temp_requirements = os.path.join(temp_dir, "requirements_updated.txt")
            
            with open(temp_requirements, "w") as f:
                subprocess.run([pip_path, "freeze"], stdout=f, check=True)
            
            # Copy updated requirements.txt
            shutil.copy2(temp_requirements, requirements_file)
        else:
            # Update each package to the latest version (direct dependencies only)
            print(color_text("Updating packages to latest versions (direct dependencies only)...", Colors.BLUE))
            updated_packages = []
            
            for req in original_requirements:
                # Extract package name (remove version specifiers)
                package_name = req.split('==')[0].split('>=')[0].split('<=')[0].split('>')[0].split('<')[0].split('~=')[0].strip()
                
                # Update the package
                print(color_text(f"Updating {package_name}...", Colors.BLUE))
                try:
                    subprocess.run([pip_path, "install", "--upgrade", package_name], check=True)
                    
                    # Get the installed version
                    result = subprocess.run(
                        [pip_path, "show", package_name], 
                        check=True, 
                        stdout=subprocess.PIPE, 
                        text=True
                    )
                    
                    # Extract version
                    version = None
                    for line in result.stdout.splitlines():
                        if line.startswith("Version:"):
                            version = line.split(":", 1)[1].strip()
                            break
                    
                    if version:
                        updated_packages.append(f"{package_name}=={version}")
                    else:
                        updated_packages.append(req)
                except subprocess.SubprocessError:
                    print(color_text(f"Failed to update {package_name}, keeping original specification", Colors.YELLOW))
                    updated_packages.append(req)
            
            # Write updated requirements
            with open(requirements_file, "w") as f:
                for package in updated_packages:
                    f.write(f"{package}\n")
        
        print(color_text(f"Updated file: {requirements_file}", Colors.GREEN))
        
        # Return both original backup and updated file
        return {"updated_file": requirements_file, "backup_file": backup_file}
    
    except Exception as e:
        print(color_text(f"Error during update: {str(e)}", Colors.RED))
        raise
    
    finally:
        # Cleanup will be handled by the atexit handler
        pass


def remove_backup_files() -> None:
    """Remove all created backup files"""
    for backup_file in all_backup_files:
        if os.path.exists(backup_file):
            try:
                os.remove(backup_file)
                print(color_text(f"Removed backup: {backup_file}", Colors.BLUE))
            except Exception as e:
                print(color_text(f"Failed to remove backup file {backup_file}: {e}", Colors.RED))


def get_user_input(prompt: str, valid_options: Optional[List[str]] = None) -> str:
    """
    Get user input with validation
    
    Args:
        prompt: The prompt to display to the user
        valid_options: List of valid input options
        
    Returns:
        User input string
    """
    while True:
        user_input = input(color_text(prompt, Colors.BOLD)).strip().lower()
        if valid_options and user_input not in valid_options:
            print(color_text(f"Please enter one of: {', '.join(valid_options)}", Colors.YELLOW))
            continue
        return user_input


def parse_arguments() -> argparse.Namespace:
    """
    Parse command-line arguments
    
    Returns:
        Parsed arguments namespace
    """
    parser = argparse.ArgumentParser(
        description="""
        Requirements.txt Updater - A tool to update Python project dependencies.
        This script finds requirements.txt files, creates a backup, and updates
        dependencies to their latest versions while preserving their format.
        """,
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    
    parser.add_argument(
        'files', 
        nargs='*', 
        help='Specific requirements.txt files to update. If not provided, script will search for them.'
    )
    
    parser.add_argument(
        '-a', '--all', 
        action='store_true', 
        help='Update all found requirements.txt files without asking'
    )
    
    parser.add_argument(
        '-y', '--yes', 
        action='store_true',
        help='Answer yes to all prompts'
    )
    
    parser.add_argument(
        '-q', '--quiet', 
        action='store_true',
        help='Minimal output'
    )
    
    parser.add_argument(
        '-f', '--freeze',
        action='store_true',
        help='Use pip freeze to include all subdependencies in requirements file'
    )
    
    parser.add_argument(
        '-d', '--direct-only',
        action='store_true',
        help='Include only direct dependencies (not subdependencies) in requirements file'
    )
    
    parser.add_argument(
        '--keep-backups',
        action='store_true',
        help='Keep backup files after completion'
    )
    
    parser.add_argument(
        '--delete-backups',
        action='store_true',
        help='Delete backup files after completion'
    )
    
    return parser.parse_args()


def main() -> None:
    """
    Main function for the requirements updater script
    """
    # Register cleanup function
    atexit.register(cleanup_temp_directories)
    
    args = parse_arguments()
    
    # Handle conflicting arguments
    if args.freeze and args.direct_only:
        print(color_text("Error: Cannot specify both --freeze and --direct-only", Colors.RED))
        sys.exit(1)
        
    if args.keep_backups and args.delete_backups:
        print(color_text("Error: Cannot specify both --keep-backups and --delete-backups", Colors.RED))
        sys.exit(1)
    
    # Check if specific files are provided
    if args.files:
        requirements_files = args.files
        for file_path in requirements_files:
            if not os.path.exists(file_path):
                print(color_text(f"Error: File not found: {file_path}", Colors.RED))
                sys.exit(1)
    else:
        # Find all requirements.txt files
        requirements_files = glob.glob("**/requirements.txt", recursive=True)
    
    if not requirements_files:
        print(color_text("No requirements.txt files found", Colors.YELLOW))
        return
    
    if not args.quiet:
        print(color_text(f"\nFound {len(requirements_files)} requirements.txt files:", Colors.CYAN))
        for i, file_path in enumerate(requirements_files, 1):
            print(color_text(f"  {i}. {file_path}", Colors.CYAN))
    
    # Determine which files to update
    update_all = args.all or args.yes
    if not update_all and not args.quiet:
        print(color_text("\nOptions:", Colors.BOLD))
        update_all_input = get_user_input("Do you want to update all files? (yes/no): ", ["yes", "no", "y", "n"])
        update_all = update_all_input in ["yes", "y"]
    
    # Determine whether to use pip freeze
    use_freeze = args.freeze
    if not args.freeze and not args.direct_only and not args.quiet:
        print(color_text("\nDependency Options:", Colors.BOLD))
        print(color_text("1. Update only direct dependencies (cleaner requirements files)", Colors.CYAN))
        print(color_text("2. Include all subdependencies with pip freeze (more complete but verbose)", Colors.CYAN))
        freeze_choice = get_user_input("Choose option (1/2): ", ["1", "2"])
        use_freeze = freeze_choice == "2"
    
    updated_files = []
    
    for req_file in requirements_files:
        if not update_all and not args.quiet:
            update_this = get_user_input(f"\nUpdate {req_file}? (yes/no): ", ["yes", "no", "y", "n"])
            if update_this not in ["yes", "y"]:
                print(color_text(f"Skipping {req_file}", Colors.YELLOW))
                continue
        
        try:
            result = update_requirements(req_file, use_freeze=use_freeze)
            updated_files.append(result)
        except Exception as e:
            print(color_text(f"Error updating {req_file}: {e}", Colors.RED))
    
    # Summary
    if updated_files:
        if not args.quiet:
            print(color_text("\n" + "="*50, Colors.GREEN))
            print(color_text("UPDATE SUMMARY", Colors.GREEN + Colors.BOLD))
            print(color_text("="*50, Colors.GREEN))
            print(color_text(f"Updated {len(updated_files)} requirements.txt files:", Colors.GREEN))
        
        for file_info in updated_files:
            updated_file = file_info["updated_file"]
            backup_file = file_info["backup_file"]
            
            print(color_text(f"\n- {updated_file}", Colors.GREEN))
            
            # Check file diff
            if check_git_available() and not args.quiet:
                print(color_text("\nChanges in file (diff):", Colors.BOLD))
                diff_output = show_file_diff(backup_file, updated_file)
                print(diff_output)
    else:
        print(color_text("\nNo files were updated", Colors.YELLOW))
    
    # Ask about backup files
    delete_backups = args.delete_backups
    keep_backups = args.keep_backups
    
    if not delete_backups and not keep_backups and all_backup_files and not args.quiet:
        print(color_text("\nBackup Management:", Colors.BOLD))
        print(color_text(f"Created {len(all_backup_files)} backup files during this operation.", Colors.CYAN))
        delete_choice = get_user_input("Do you want to delete backup files? (yes/no): ", ["yes", "no", "y", "n"])
        delete_backups = delete_choice in ["yes", "y"]
    
    if delete_backups:
        remove_backup_files()
    else:
        print(color_text("\nBackup files have been preserved.", Colors.BLUE))
    
    print(color_text("\nAll operations completed", Colors.GREEN + Colors.BOLD))


if __name__ == "__main__":
    main() 