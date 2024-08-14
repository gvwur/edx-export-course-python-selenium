# Python Selenium script for edX Course Export automation

## Required python modules:
requests
selenium

This script will open FireFox and download edX Course Exports as listed in the course_keys.txt file. 

To do so, first enther your edx email and pw for the login function:

```
def main():
    username = "your_edx_email"
    password = "your_edx_password"
```

Course exports will be downloaded to 'exports' folder, and a simple log file is created in 'logs' folder.
