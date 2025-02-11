#!/usr/bin/env python3
import os
import random
from datetime import datetime
import subprocess
import platform
from pathlib import Path

# List of commit messages for variety
COMMIT_MESSAGES = [
    "Update documentation",
    "Fix typo",
    "Minor improvements",
    "Refactor code",
    "Update dependencies",
    "Add comments",
    "Clean up",
    "Optimize performance",
    "Update configuration",
    "Fix formatting",
    "Update readme",
    "Code cleanup",
    "Minor tweaks",
    "Update version",
    "Improve structure",
    "Fix indent",
    "Update settings",
    "Enhance readability",
    "Update resources",
    "Fix spacing",
    "Update templates",
    "Improve organization",
    "Update modules",
    "Fix alignment",
    "Update packages",
    "General maintenance",
    "Routine update",
    "System maintenance",
    "Regular update",
    "Daily backup"
]

def setup_git_config():
    """Configure git if not already configured"""
    try:
        subprocess.run(['git', 'config', 'user.name'], check=True, capture_output=True)
        subprocess.run(['git', 'config', 'user.email'], check=True, capture_output=True)
    except subprocess.CalledProcessError:
        subprocess.run(['git', 'config', '--global', 'user.name', 'brayheart'])
        subprocess.run(['git', 'config', '--global', 'user.email', 'tylerhbray@gmail.com'])

def ensure_number_file():
    """Create number.txt if it doesn't exist"""
    number_file = Path('number.txt')
    if not number_file.exists():
        with open(number_file, 'w') as f:
            f.write('0')

def read_number():
    """Read the current number from file"""
    with open('number.txt', 'r') as f:
        return int(f.read().strip())

def write_number(num):
    """Write the new number to file"""
    with open('number.txt', 'w') as f:
        f.write(str(num))

def make_random_changes():
    """Make small random changes to create multiple unique commits"""
    changes = [
        ("Update number and documentation", lambda: write_number(read_number() + 1)),
        ("Update configuration settings", lambda: Path('config.txt').touch()),
        ("Update system files", lambda: Path('system.txt').touch()),
    ]
    return random.choice(changes)

def git_commit(message=None):
    """Stage and commit changes"""
    subprocess.run(['git', 'add', '.'])
    if message is None:
        message = random.choice(COMMIT_MESSAGES)
    subprocess.run(['git', 'commit', '-m', message])

def git_push():
    """Push changes to GitHub"""
    result = subprocess.run(['git', 'push'], capture_output=True, text=True)
    if result.returncode == 0:
        print("Changes pushed to GitHub successfully.")
    else:
        print("Error pushing to GitHub:")
        print(result.stderr)

def setup_windows_task():
    """Set up Windows Task Scheduler instead of cron"""
    script_path = os.path.abspath(__file__)
    random_hour = random.randint(0, 23)
    random_minute = random.randint(0, 59)
    
    task_name = "DailyNumberUpdate"
    command = (
        f'schtasks /create /tn {task_name} /tr "python {script_path}" '
        f'/sc daily /st {random_hour:02d}:{random_minute:02d} /f'
    )
    
    try:
        subprocess.run(command, shell=True, check=True)
        print(f"Task scheduled to run at {random_hour:02d}:{random_minute:02d} daily")
    except subprocess.CalledProcessError as e:
        print(f"Error setting up scheduled task: {e}")

def main():
    try:
        # Initial setup
        setup_git_config()
        ensure_number_file()
        
        # Determine number of commits for today (1-3)
        num_commits = random.randint(1, 3)
        
        # Make multiple commits
        for _ in range(num_commits):
            # Make random changes
            change_description, change_function = make_random_changes()
            change_function()
            
            # Commit and push
            git_commit()
            git_push()
            
            # Small delay between commits to make them look more natural
            if _ < num_commits - 1:  # Don't sleep after the last commit
                subprocess.run(['timeout', '/t', str(random.randint(30, 180))], shell=True)

        # Schedule next run
        if platform.system() == 'Windows':
            setup_windows_task()
        else:
            print("This script is configured for Windows. For Linux/Mac, please set up cron manually.")

    except Exception as e:
        print(f"Error: {str(e)}")
        exit(1)

if __name__ == "__main__":
    main()