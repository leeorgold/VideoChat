import subprocess
import sys

import pkg_resources
from pkg_resources import DistributionNotFound, VersionConflict


def should_install_requirement(requirement):
    should_install = False
    try:
        pkg_resources.require(requirement)
    except (DistributionNotFound, VersionConflict):
        should_install = True
    return should_install


def install_packages(requirement_list):
    try:
        requirements = [
            requirement
            for requirement in requirement_list
            if should_install_requirement(requirement)
        ]
        if len(requirements) > 0:
            subprocess.check_call([sys.executable, "-m", "pip", "install", *requirements])
        else:
            print("Requirements already satisfied.")

        try:
            subprocess.check_call(["pipwin", "install", 'pyaudio'])
        except (Exception, ) as e:
            print(e)
    except Exception as e:
        print(e)


def main():
    requirements = ['numpy', 'opencv-python', 'Pillow', 'imutils', 'pipwin', 'python-dotenv', 'rsa', 'pycryptodome']
    install_packages(requirements)


if __name__ == '__main__':
    main()