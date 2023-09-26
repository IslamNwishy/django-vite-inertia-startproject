import subprocess

TAILWIND_FORMS_VERSION = '"^0.5.6"'


def prep_frontend():
    subprocess.run(["django-breeze", "create-app", "react"])
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
