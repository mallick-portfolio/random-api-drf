import subprocess
import pathlib
import shutil


repo_url = "https://github.com/mallick-portfolio/random-api-frontend.git"


target = pathlib.Path(__file__).resolve().parent.parent / "frontend"

subprocess.run(["git", "clone", repo_url, str(target)], check=True)

# Define the current and target paths
current_path = pathlib.Path(__file__).resolve().parent / "docker-compose.yaml"
target_path = current_path.parent.parent / "docker-compose.yaml"

# Move the file
shutil.move(str(current_path), str(target_path))

