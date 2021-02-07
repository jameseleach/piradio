# This is test.py

import re
import os
import subprocess

def get_mpc_status():
    result = subprocess.getoutput("mpc")
    if "[playing]" in result:
        ps= False
    elif "[paused]" in result:
        ps = True
    else:
        ps = None
    
    cv = int((re.split(' |%', result)[1]))

    return ps, cv