import re
import subprocess
import os
from os import path
# import shutil
import pickle
import math
import shutil
from collections import OrderedDict

import PyFoam
from PyFoam.RunDictionary.SolutionDirectory import SolutionDirectory
from PyFoam.RunDictionary.ParsedParameterFile import ParsedParameterFile
from PyFoam.Basics.DataStructures import Vector
from numpy import linspace
from PyFoam.RunDictionary.SolutionDirectory import SolutionDirectory
from PyFoam.Basics.TemplateFile import TemplateFile
from PyFoam.RunDictionary.ParsedParameterFile import ParsedParameterFile
from PyFoam.Basics.DataStructures import Vector
from PyFoam.Execution.BasicRunner import BasicRunner
from PyFoam.Applications.PlotRunner import PlotRunner
from PyFoam.Applications.Runner import Runner
from PyFoam.Execution.ParallelExecution import LAMMachine

"""

N_np: required nodes
run test.sh in nodes_dir
"""


N_np = 25

pathtemplate = "/fya_hemo/AAA_hemo"

dir = path.join(pathtemplate, f"Aorta_N0")
path_maker = lambda dir_name: os.path.join(dir, dir_name)
list_fulldir = list(map(path_maker, os.listdir(dir)))
print(list_fulldir)

N_geom = len(os.listdir(dir))


for n in range(N_np):

    np_dir = path.join(pathtemplate, f"np_{n}")
    print(np_dir)
    
    if not os.path.isdir(np_dir):
        os.mkdir(np_dir)
    else:
        try:
            shutil.rmtree(path.join(pathtemplate, f"np_{n}/Aorta_N0"))

        except:
        
            pass
            

    pathsrc = f"{pathtemplate}/test0.sh"
    pathdst = np_dir
    subprocess.run(["cp", "-r", f"{pathsrc}", f"{pathdst}"], check=True)

    pathsrc = f"{pathtemplate}/Aorta_pyfoam_flomuster0.py"
    pathdst = np_dir
    subprocess.run(["cp", "-r", f"{pathsrc}", f"{pathdst}"], check=True)

    recnp_dir = path.join(pathtemplate, f"np_{n}/Aorta_N0")
    if not os.path.isdir(recnp_dir):
        os.mkdir(recnp_dir)

    n_geom = int(N_geom / N_np)

    j = 0

    for j in range(n_geom):
        pathsrc = f"{list_fulldir[n * n_geom + j]}"
        pathdst = recnp_dir
        subprocess.run(["cp", "-r", f"{pathsrc}", f"{pathdst}"], check=True)

ngeom_add = N_geom % N_np
print(ngeom_add)
for n in range(ngeom_add):
    recnp_dir = path.join(pathtemplate, f"np_{n}/Aorta_N0")
    print(os.listdir(dir)[-1 - n])
    pathsrc = f"{list_fulldir[-1 - n]}"
    pathdst = recnp_dir
    subprocess.run(["cp", "-r", f"{pathsrc}", f"{pathdst}"], check=True)


for n in range(N_np):
    np_dir = path.join(pathtemplate, f"np_{n}")
    print(np_dir)
    os.chdir(np_dir)
    print(os.getcwd())
    #subprocess.run(f"cd /{np_dir}", shell=True, check=True)
    subprocess.Popen("sbatch test0.sh", shell=True)
