#!/usr/bin/python3
# ==========V1.1==========
import os, re, sys, stat

try:
    from bs4 import BeautifulSoup
except ImportError:
    os.system("python3 -m pip install beautifulsoup4")
    from bs4 import BeautifulSoup

# Check if an HTML file is passed as a command line argument
html_file = sys.argv[1] if len(sys.argv) > 1 else "source.html"

# Read the HTML file
try:
    with open(html_file, "r") as f:
        html = f.read()
except FileNotFoundError:
    print(f"Error: {html_file} not found")
    exit(1)

soup = BeautifulSoup(html, "html.parser")

# Get the directory name
directory = soup.select_one(
    'div[data-role^="task"] li:-soup-contains("Directory:") code'
)
# Create the directory
if directory:
    dir_name = directory.text
    os.makedirs(dir_name, exist_ok=True)

# Process each task
for task in soup.select('div[data-role^="task"]'):
    prototype = task.select_one('li:-soup-contains("Prototype:") code')
    file = task.select_one('li:-soup-contains("File:") code')

    # Create the file
    if file:
        file_path = os.path.join(dir_name, file.text)
        add_exec_perms = False
        with open(file_path, "w") as f:
            # Add shebang line according to file language
            if file.text.endswith(".py"):
                f.write("#!/usr/bin/python3\n")
                add_exec_perms = True
            elif file.text.endswith(".js"):
                f.write("#!/usr/bin/node\n")
                add_exec_perms = True
            elif re.search(r"^[^.]+$(?<!password)(?<!crack)", file.text):
                f.write("#!/usr/bin/bash\n")
                add_exec_perms = True
            # Add executable permissions to the file if a shebang line was added
            if add_exec_perms:
                os.chmod(file_path, os.stat(file_path).st_mode | stat.S_IEXEC)

            # If it's a C file, include main.h and prototype function
            if file.text.endswith(".c"):
                # Create main.h if it doesn't exist
                main_h_path = os.path.join(dir_name, "main.h")
                if not os.path.exists(main_h_path):
                    with open(main_h_path, "w") as main_h_file:
                        main_h_file.write("#ifndef MAIN_H\n#define MAIN_H\n\n")

                # Append the prototype to main.h
                if prototype:
                    with open(main_h_path, "a") as main_h_file:
                        main_h_file.write(f"{prototype.text}\n")

                f.write('#include "main.h"\n\n')
                if prototype:
                    f.write(f"{prototype.text[:-1]} {{\n\t/* your code here */\n}}\n")

# Close the include guard in main.h if it was created
if os.path.exists(main_h_path):
    with open(main_h_path, "a") as f:
        f.write("\n#endif /* MAIN_H */\n")

exit(0)

# This script is v1.1 may have some bugs, please report
# OR feel free to edit code

# Credit: BIO
