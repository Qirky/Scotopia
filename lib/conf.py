import sys

PORT = 59123

# Do not change the following

SYSTEM  = 0
WINDOWS = 0
MAC_OS  = 1
LINUX   = 2

if sys.platform.startswith('darwin'):

    SYSTEM = MAC_OS

elif sys.platform.startswith('win'):

    SYSTEM = WINDOWS

elif sys.platform.startswith('linux'):

    SYSTEM = LINUX


