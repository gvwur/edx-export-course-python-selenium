# Python Selenium script for edX Course Export automation

## Required python modules:
- requests
- selenium

This script will open FireFox via Selenium and automatically download edx courses as listed in the course_keys.txt file.

Start the script, you will be prompted to enter your edx email and password:

```
def main():
    username = input("Enter your edX email: ")
    password = getpass.getpass("Enter your edX password: ")
```

Course exports will be downloaded to 'exports' folder, and a simple log file is created in 'logs' folder.

There are some built in wait functions to make sure there is enough time to load the pages.. I think, not the neatest solution, but it works. 

Waiting for an export is set to 60 seconds but feel free to adjust. 
