from time import sleep
import os
import win32net

if 'logonserver' in os.environ:
    server = os.environ['logonserver'][2:]
else:
    server = None

def if_user_is_admin(Server):
    groups = win32net.NetUserGetLocalGroups(Server, os.getlogin())
    isadmin = False
    for group in groups:
        if group.lower().startswith('admin'):
            isadmin = True
    return isadmin, groups


# Function usage
is_admin, groups = if_user_is_admin(server)

# Result handeling
if is_admin == True:
    print('You are a admin user!')
else:
    print('You are not an admin user.')
print('You are in the following groups:')
for group in groups:
    print(group)

sleep(10)
#if error: no module named win32api, run these lines in cmd
#pip uninstall pipywin32
#pip uninstall pywin32
#pip install pywin32
