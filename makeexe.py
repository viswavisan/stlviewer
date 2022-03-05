

import os
supportfilesfolder='D:/SIT/stored/'
py='Prog_input_tool_V6.py'

cmd='pyinstaller --onefile '
for file in os.listdir(supportfilesfolder):cmd+='--add-data="'+supportfilesfolder+file+';stored" '
cmd+=py
print(cmd)
#os.system(cmd)


