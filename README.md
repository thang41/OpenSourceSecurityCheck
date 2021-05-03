# Open-source Security Check

![Preview](https://github.com/KillzMckinzie/OpenSourceSecurityCheck/blob/861a73abd45cd65046b24564b0964a17a04c1a92/Images/Main%20screen.png)

Open-Source Security Check is an application that will scan a chosen directory for sensitive information by using two different modes. Deep scan and quick scan. Quick scan will check filenames for senstive keywords that can be changed in the options menu. Deep scan will scan file names and filedata for sensitive information such as keywords, emails, credit card information, phone numbers and social-security numbers. 


# How it Works

1. Open application
2. Choose scan type
3. Edit the scan parameters in the options menu
    1. Add, edit, delete keywords, ignored directories and filetypes
        1. Add "none" to filter nonetype files in the ignored filetypes tab
4. browse to directory
5. Scan

# Scan complete

Once the scan is complete, you will be presented with a treeview of all files scanned. These can be then filtered out by clicking the flagged files checkbox, and you will see just the files that have been flagged based on the criteria set. It also checks to see if you're using an administrative account. 

There is also a "report" that is generated. This was meant to be much more focused and less applicable to everyone. It is generic and will supply the same information after every scan. This was intended but not the original plan. It was originally meant to be unique depending on what sensitive information was found and ways to help hide/mitigate that to prevent a bad actor from finding it. 

# Example Scan

![Example Scan](https://github.com/KillzMckinzie/OpenSourceSecurityCheck/blob/8ad1181e3853c527a93ecbd95dd65da8484da697/Images/After%20Deep%20Scan.png)

# Python
Python 3.7.1 and greater

# Disclaimer
I am not a developer, there will be useless code and errors. You may even question your sanity as to why I did something the way I did it. The code might be unreadable and hard to follow at times. It might not work perfectly or for all scenarios. 
