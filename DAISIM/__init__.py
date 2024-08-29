import sys
import os

project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(project_root)
sys.path.append(project_root+"/daisim")
# # Print the PYTHONPATH variable
# print(f'PYTHON_PATH: {sys.path}')