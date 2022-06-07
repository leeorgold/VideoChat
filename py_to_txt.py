import os


def get_main_folder_name():
    return os.getcwd().split('\\')[-1]


def main():
    with open('project_code.py', 'w') as text_file:
        for dirpath, dirnames, filenames in os.walk(os.getcwd(), topdown=True):
            if not (dirpath.endswith('__') or '.idea' in dirpath or 'venv' in dirpath):
                dirtext = f"""

#############################################
""" + f"# package: {dirpath[dirpath.index(get_main_folder_name()):]}".center(45) + """
############################################# 
"""
                text_file.write(dirtext)

                for filename in filenames:
                    if filename.endswith('.py') and filename != 'py_to_txt.py' and filename != 'project_code.py':
                        filename_text = f"""

# ----------------------------
# file: {filename}
# ----------------------------

"""
                        text_file.write(filename_text)
                        print(f'adding file: {dirpath}\\{filename}')
                        with open(f'{dirpath}\\{filename}', 'r') as python_file:
                            data = python_file.read()
                            text_file.write(data)


if __name__ == '__main__':
    main()