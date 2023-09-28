import os
import subprocess

TAILWIND_FORMS_VERSION = '"^0.5.6"'


def prep_frontend(front):
    subprocess.run(["django-breeze", "create-app", front])
    with open("vite.config.js", "r+") as file:
        file_text = file.read().replace('host: "localhost"', "host: true")
        file.seek(0)
        file.write(file_text)

    with open("package.json", "r+") as file:
        file_text = file.read().replace(
            '"devDependencies": {',
            """"devDependencies": {
    "@tailwindcss/forms": """
            + TAILWIND_FORMS_VERSION
            + ",",
        )
        file.seek(0)
        file.write(file_text)

    with open("tailwind.config.js", "r+") as file:
        file_text = file.read().replace(
            "plugins: []", "plugins: [require('@tailwindcss/forms')]"
        )
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

# vite temp files
.vite"""
            )
    allfiles = os.listdir(source)

    # iterate on all files to move them to destination folder
    for f in allfiles:
        src_path = os.path.join(source, f)
        dst_path = os.path.join(dest, f)
        os.rename(src_path, dst_path)
