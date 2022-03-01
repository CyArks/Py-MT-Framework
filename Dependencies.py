import os

# ToDo. Test dependencies
# Dependencies:

try:
    import pytube
except ImportError:
    os.system('cmd /c "pip install pytube"')

try:
    import pandas
except ImportError:
    os.system('cmd /c "pip install pandas"')

try:
    import oauth2client
except ImportError:
    os.system('cmd /c "pip install --upgrade oauth2client"')

try:
    import AccessData
except ImportError:
    os.error("Can't find the API Access Data File for more information vist the docs")

try:
    import googleapiclient
except ImportError:
    os.system('cmd /c "pip install googleapiclient"')
