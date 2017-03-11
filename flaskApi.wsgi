import sys, os

realPath = os.path.realpath(__file__)
dirPath = os.path.dirname(realPath)
sys.path.append(dirPath)

from flaskApi import app as application
