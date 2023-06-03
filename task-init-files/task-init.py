#==========V1.0==========
import os
import pip

try:
    from bs4 import BeautifulSoup
except ImportError:
    pip.main(['install', 'beautifulsoup4'])
    from bs4 import BeautifulSoup

# Read the HTML file (source.html)
try:
    with open('source.html', 'r') as f:
        html = f.read()
except FileNotFoundError:
    print("Error: source.html not found")
    exit(1)

soup = BeautifulSoup(html, 'html.parser')

# Process each task
for task in soup.select('div[data-role^="task"]'):
    prototype = task.select_one('li:-soup-contains("Prototype:") code')
    directory = task.select_one('li:-soup-contains("Directory:") code')
    file = task.select_one('li:-soup-contains("File:") code')

    # Create the directory
    if directory:
        dir_name = directory.text
        os.makedirs(dir_name, exist_ok=True)

        # Create main.h if it doesn't exist
        main_h_path = os.path.join(dir_name, 'main.h')
        if not os.path.exists(main_h_path):
            with open(main_h_path, 'w') as f:
                f.write('#ifndef MAIN_H\n#define MAIN_H\n\n')

        # Append the prototype to main.h
        if prototype:
            with open(main_h_path, 'a') as f:
                f.write(f'{prototype.text}\n')

        # Create the file
        if file:
            file_path = os.path.join(dir_name, file.text)
            with open(file_path, 'w') as f:
                # If it's a C file, include main.h and prototype function
                if file.text.endswith('.c'):
                    f.write('#include "main.h"\n\n')
                    if prototype:
                        f.write(f'{prototype.text[:-1]} {{\n\t/* your code here */\n}}\n')

# Close the include guard in main.h
with open(main_h_path, 'a') as f:
    f.write('\n#endif /* MAIN_H */\n')

exit(0)

# This script is v1 may have some bugs, please report
# OR feel free to edit code

# Credit: BIO