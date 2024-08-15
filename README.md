# Python Selenium script for edX Course Export automation

## Required python modules:
- requests
- selenium

This script will open FireFox and download edx courses as listed in the course_keys.txt file.

To do so, first enter your edx email and pw for the login function:

```
def main():
    username = "your_edx_email"
    password = "your_edx_password"
```

Course exports will be downloaded to 'exports' folder, and a simple log file is created in 'logs' folder.

There are some built in wait functions to make sure there is enough time to load the pages.. I think, not the neatest solution, but it works. 

Waiting for an export is set to 60 seconds but feel free to adjust. 
