import subprocess
import pathlib
import shutil
import os

repo_url = "https://github.com/mallick-portfolio/random-api-frontend.git"
parent_dir = pathlib.Path(__file__).resolve().parent.parent

target = parent_dir / "frontend"

subprocess.run(["git", "clone", repo_url, str(target)], check=True)

# Define the current and target paths
current_path = pathlib.Path(__file__).resolve().parent / "docker-compose.yaml"
target_path = current_path.parent.parent / "docker-compose.yaml"

# Move the file
shutil.move(str(current_path), str(target_path))



# Rename the backend folder

old_folder = parent_dir / "random-api-drf"
new_folder = parent_dir / "backend"

if old_folder.exists():
    os.rename(old_folder, new_folder)
    print(f"✅ Renamed '{old_folder.name}' to '{new_folder.name}'")
else:
    print("❌ Folder 'random-api-drf' does not exist.")