# Open-source Security Check

![Preview](https://github.com/KillzMckinzie/OpenSourceSecurityCheck/blob/c4cb588d912a40edd9bd4ec0df3dacce56f0c661/Main%20screen.png)

Open-Source Security Check is an application that will scan a chosen directory for sensitive information by using two different modes. Deep scan and quick scan. Quick scan will check filenames for senstive keywords that can be changed in the options menu. Deep scan will scan file names and filedata for sensitive information such as keywords, emails, credit card information, phone numbers and social-security numbers. 


# How it Works

1. Open application
2. Choose scan type
3. Edit the scan parameters in the options menu
    1. Add, edit, delete keywords, directories and filetypes to ignore
        1. Add "none" to filter nonetype files in the ignored filetypes tab
4. browse to directory
5. Scan

# Scan complete

Once the scan is complete, you will be presented with a treeview of all files scanned. These can be then filtered out by clicking the filter checkbox, and you will see just the files that have been flagged based on the criteria set. 

# Python
Python 3.7.1 and greater

# Disclaimer
I am not a developer, there will be useless code, errors, you may even question your sanity as to why I did something the way I did it. The code might be unreadable and hard to follow. It might not work perfectly or for all scenarios. 
