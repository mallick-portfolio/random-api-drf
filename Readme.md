# 🚀 Full Project Bootstrap Script

This project includes a Python script that automates the setup of a full-stack development environment.

---

## 🔧 What This Script Does

1. 🗂 Creates a new project folder (e.g., `trello_project`)
2. 📦 Clones the **backend** and **frontend** GitHub repositories into that folder
3. ✏️ Renames the folders to `backend/` and `frontend/`
4. 📁 Moves the `docker-compose.yml` file from `backend/` to the project root
5. 💻 Opens the project in Visual Studio Code
6. 💻 Open terminal and run "docker compose up --build" or "docker-compose up --build"
7. Copy both .env.example to .env and update the value.

---

## 📦 Requirements

Make sure you have the following installed:

- [Python 3.7+](https://www.python.org/)
- [Git](https://git-scm.com/)
- [Docker](https://www.docker.com/)
- [Docker Compose](https://docs.docker.com/compose/)
- [Visual Studio Code](https://code.visualstudio.com/)
- ✅ The `code` command available in your shell (enable via:
  `Ctrl+Shift+P → Shell Command: Install 'code' command in PATH` in VS Code)

---

## 🧾 Project Structure After Setup

---

### 🛠️ How to Use

1. Create a new Python file named `setup.py` in any folder.

2. Paste the following code into `setup.py`.

3. Run the script:

```bash
python3 setup.py
```

```python
import os
import subprocess
from pathlib import Path
import shutil
import time

# === CONFIGURATION ===
parent_folder_name = "trell_project"
backend_repo_url = "https://github.com/mallick-portfolio/random-api-drf.git"
frontend_repo_url = "https://github.com/mallick-portfolio/random-api-frontend.git"

# === PATH SETUP ===
base_dir = Path(__file__).resolve().parent
project_dir = base_dir / parent_folder_name
backend_original = project_dir / "random-api-drf"
frontend_original = project_dir / "random-api-frontend"
backend_final = project_dir / "backend"
frontend_final = project_dir / "frontend"
docker_compose_src = backend_final / "docker-compose.yaml"
docker_compose_dest = project_dir / "docker-compose.yaml"

# === 1. Create parent folder ===
project_dir.mkdir(parents=True, exist_ok=True)
print(f"📁 Created project folder: {project_dir}")

# === 2. Clone Backend ===
if not backend_original.exists() and not backend_final.exists():
    subprocess.run(["git", "clone", backend_repo_url, str(backend_original)], check=True)
    os.rename(backend_original, backend_final)
    print("✅ Backend cloned and renamed.")
else:
    print("⚠️ Backend folder already exists. Skipping clone.")

# === 3. Clone Frontend ===
if not frontend_original.exists() and not frontend_final.exists():
    subprocess.run(["git", "clone", frontend_repo_url, str(frontend_original)], check=True)
    os.rename(frontend_original, frontend_final)
    print("✅ Frontend cloned and renamed.")
else:
    print("⚠️ Frontend folder already exists. Skipping clone.")

# === 4. Move docker-compose.yml ===
if docker_compose_src.exists():
    shutil.move(str(docker_compose_src), str(docker_compose_dest))
    print("📦 Moved docker-compose.yml to project root.")
else:
    print("⚠️ docker-compose.yml not found in backend folder.")

# === 5. Open in VS Code ===
subprocess.Popen(["code", "."], cwd=project_dir)
print("🚀 Opened project in VS Code.")

# === 6. Run docker-compose (optional) ===
time.sleep(2)  # Optional delay
try:
    subprocess.run(["docker-compose", "up", "--build"], cwd=project_dir, check=True)
except subprocess.CalledProcessError as e:
    print("❌ Docker Compose failed:", e)

```
