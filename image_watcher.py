import os
import time
import subprocess  # For interacting with Git

# Watch the current directory where the script is located
WATCH_DIR = os.path.dirname(os.path.abspath(__file__))

# Path to your local GitHub repo (ensure it's initialized and set to your GitHub repo)
REPO_DIR = "C:\\inventyv one drive for notes\\OneDrive\\All Notes and everything\\Work\\obsidian_images"
# Adjust to your actual repo path

# GitHub user and repo name
GITHUB_USER = "Ayush-parkara-inventyv"
GITHUB_REPO = "obsidian_images"  # Correct repo name with underscore

# Keep track of files already seen
seen_files = set(os.listdir(WATCH_DIR))

# Function to generate raw URL for uploaded images
def get_raw_url(filename):
    return f"https://raw.githubusercontent.com/{GITHUB_USER}/{GITHUB_REPO}/main/{filename}"

# Function to clean up filename by removing "Pasted image "
def clean_filename(filename):
    # Remove "Pasted image " from the filename, leaving the timestamp
    if filename.lower().startswith("pasted image "):
        return filename[len("Pasted image "):]
    return filename

# Debugging print to show the script has started running
print("✅ Script started successfully. Watching for new image files...")

# Infinite loop to monitor the directory
while True:
    try:
        # Get the current list of files in the watch directory
        current_files = set(os.listdir(WATCH_DIR))
        print()

        # Identify new files (those that are not in the previous list)
        new_files = current_files - seen_files
        print(f"🔎 New files detected: {new_files}")

        for file in new_files:
            # Check if the new file is an image
            if file.lower().endswith(('.png', '.jpg', '.jpeg', '.gif')):
                image_path = os.path.join(WATCH_DIR, file)

                # Clean the filename to remove "Pasted image "
                cleaned_filename = clean_filename(file)
                cleaned_image_path = os.path.join(WATCH_DIR, cleaned_filename)

                # Rename the file to the cleaned version (timestamp only)
                os.rename(image_path, cleaned_image_path)

                print(f"🖼️ Detected image: {file}")
                print(f"Renamed image to: {cleaned_filename}")

                # Add, commit, and push the image to GitHub
                print("📦 Adding, committing, and pushing to GitHub...")

                git_add_result = subprocess.run(["git", "add", cleaned_filename], cwd=REPO_DIR, capture_output=True)
                if git_add_result.returncode != 0:
                    print(f"❌ Git add failed: {git_add_result.stderr.decode()}")
                    continue

                git_commit_result = subprocess.run(["git", "commit", "-m", f"Add {cleaned_filename}"], cwd=REPO_DIR, capture_output=True)
                if git_commit_result.returncode != 0:
                    print(f"❌ Git commit failed: {git_commit_result.stderr.decode()}")
                    continue

                git_push_result = subprocess.run(["git", "push"], cwd=REPO_DIR, capture_output=True)
                if git_push_result.returncode != 0:
                    print(f"❌ Git push failed: {git_push_result.stderr.decode()}")
                    continue

                print(f"✅ Git push successful.")

                # Get the raw URL for the uploaded image
                raw_url = get_raw_url(cleaned_filename)
                print(f"✅ Image uploaded successfully! Raw GitHub URL: {raw_url}")

        # Update the list of seen files
        seen_files = current_files
        print()

    except Exception as e:
        print(f"⚠️ Error encountered: {e}")

    # Sleep for a while before checking again
    time.sleep(3)
