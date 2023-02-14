from datetime import datetime
import os
print("----------")
ts_file = f"{datetime.now().strftime('%y%m%d-%H%M')}"
ts_db = f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
ts_time = f"{datetime.now().strftime('%H:%M:%S')}"
print(f"{ts_time} starting {os.path.basename(__file__)}")
import time
start_time = time.time()

from dotenv import load_dotenv
load_dotenv()
USER = os.getenv("USER")

import sys
sys.path.append(f"/Users/{USER}/Python/indeXee")

# import my_utils
# import grist_BB
# import grist_PE
# import dbee

# get script name
import sys
loc = f"{sys.argv[0][18:-3]}"

# get line numbers
from inspect import currentframe
def ln():
    """
    print line numbers with f"{ln()}"
    """
    cf = currentframe()
    return cf.f_back.f_lineno

import pprint
pp = pprint.PrettyPrinter(indent=4)

count = 0
count_row = 0

test = True
v = True # verbose mode

print(f"{os.path.basename(__file__)} boilerplate loaded -----------\n")
####################
# SCRIPT_TITLE

### Script-specific imports



### Global Variables



### Functions



### Main

with open("test.txt", 'w') as file:
    file.write(ts_db)


########################################################################################################

if __name__ == '__main__':
    print()
    print()
    print('-------------------------------')
    print(f"{os.path.basename(__file__)}")
    print()
    print(f"{count=}")
    print()
    print('-------------------------------')
    run_time = round((time.time() - start_time), 1)
    if run_time > 60:
        print(f'{os.path.basename(__file__)} finished in {run_time/60} minutes.')
    else:
        print(f'{os.path.basename(__file__)} finished in {run_time}s.')
    print()




