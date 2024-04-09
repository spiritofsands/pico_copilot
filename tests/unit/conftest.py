import sys
from os.path import abspath, dirname

# Testing current sources
PACKAGE_DIR = dirname(dirname(dirname(abspath(__file__))))
sys.path.insert(0, PACKAGE_DIR)
