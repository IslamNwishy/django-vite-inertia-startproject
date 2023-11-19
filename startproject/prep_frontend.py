# Python Standard Library Imports
import os
import subprocess

TAILWIND_FORMS_VERSION = '"^0.5.6"'


def prep_frontend(front):
    subprocess.run(["django-breeze", "create-app", front])
    with open("vite.config.js", "r+") as file:
        file_text = file.read().replace('host: "localhost"', "host: true")
        file.seek(0)
        file.write(file_text)

    file_text.replace('root: resolve("./src"),\n', "")
    with open("vite.config.build.js", "w") as file:
        file.write(file_text)

    with open("package.json", "r+") as file:
        file_text = file.read()
        file_text.replace(
            '"devDependencies": {',
            """"devDependencies": {
    "@tailwindcss/forms": """
            + TAILWIND_FORMS_VERSION
            + ",",
        )
        file_text.replace(
            '"dev": "vite",',
            """"dev": "vite",
    "build": "vite build --config vite.config.build.js && vite build --outDir ./static/dist-ssr --ssr src/ssr.jsx --config vite.config.build.js",
""",
        )
        file.seek(0)
        file.write(file_text)

    with open("src/index.html", "r") as file:
        file_text = file.read()
        file_text.replace("{% vite_asset 'main.jsx' %}", "{% vite_asset 'src/main.jsx' %}")

    with open("src/index_prod.html", "w") as file:
        file.write(file_text)

    with open("tailwind.config.js", "r+") as file:
        file_text = file.read().replace("plugins: []", "plugins: [require('@tailwindcss/forms')]")
        file.seek(0)
        file.write(file_text)

    source = "./startproject/_temp_files/react"
    dest = "./src"
    if front == "vue3":
        source = "./startproject/_temp_files/vue3/components"
        dest = "./src/components"
        # the vue3 creation processes overwrites our gitignore
        with open(".gitignore", "a") as f:
            f.write(
                """
# python bytecode
/__pycache__/
**/__pycache__/

# virtual environments
venv
env
.env

# django
*/migrations_dev/*
!*/migrations_dev/__init__.py
media
/static/*
!/static/dist
/static/dist/*
!/static/dist/.gitkeep

# vite temp files
.vite"""
            )
    allfiles = os.listdir(source)

    # iterate on all files to move them to destination folder
    for f in allfiles:
        src_path = os.path.join(source, f)
        dst_path = os.path.join(dest, f)
        if os.path.exists(dst_path):
            print(f"Path {dst_path} already exists, skipping ...")
            continue
        os.rename(src_path, dst_path)
