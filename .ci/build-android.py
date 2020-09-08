import os
import platform

os.chdir('android')
if platform.system() == 'Windows':
    os.system('./gradlew assemble')
else:
    os.system('gradlew.bat assemble')

