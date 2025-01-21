import re
import subprocess
import os
import pickle
import math
import numpy as np
import PyFoam
import argparse

from os import path
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
from collections import OrderedDict



pathtemplate = "/fya_hemo/AAA_hemo"

"""

Argparse

"""

def list_of_floats(arg):
    return list(map(float, arg))


parser = argparse.ArgumentParser(description='Script description')


parser.add_argument('--pwd', required=True, type=str)
parser.add_argument('--nodes',default='1', required=False, type=int)
parser.add_argument('--T',default='1.0', required=False, type=float)
parser.add_argument('--n_blocks',default='2', required=False, type=float)
parser.add_argument("--levels", required=False, nargs='+')
parser.add_argument('--BC',default='parabolic',required=False, type=str)


args = parser.parse_args()


pathhome = f'{args.pwd}'
nodes = args.nodes


T = args.T
n_blocks = args.n_blocks
levels = list_of_floats(args.levels)

BC = args.BC



np_node = 32
max_np = nodes * np_node
np_snap = 32 * nodes



def update_string(caseStringFile, replaceMarker, string):
    with open(caseStringFile) as _caseStringFile:
        stringFile = _caseStringFile.read()

    with open(caseStringFile, 'w') as _caseStringFile:
        stringFile = re.sub(replaceMarker, string, stringFile)
        _caseStringFile.write(stringFile)


"""
create surface meshes directory
"""

rec_directory = path.join(pathhome, f"Aorta_N0")
print(rec_directory)
if not os.path.isdir(rec_directory):
    os.mkdir(rec_directory)


"""
create openFoam directory
"""

case_directory = path.join(pathhome, f"AortaOF_N")  # /userspace/fya/AAA_test/AortaOF_N"
if not os.path.isdir(case_directory):
    os.mkdir(case_directory)


dir = path.join(pathhome, f"Aorta_N0")
for f in os.listdir(dir):
    N = f.split('_', 1)[1]

    print(os.path.isdir(path.join(pathhome, f"AortaOF_N/Aorta_{N}/processor1/0.25")))

    if not os.path.isdir(path.join(pathhome, f"AortaOF_N/Aorta_{N}/processor1/0.25")):

        

        """
        change template_path
        """
        os.chdir(pathtemplate)
        print(pathtemplate)
        template_path = path.join(f"mesh_template/template")

        templateCase = SolutionDirectory(template_path, archive=None, paraviewLink=False)

        case = templateCase.cloneCase(path.join(pathhome, f"AortaOF_N/Aorta_{N}"))

        os.chdir(pathhome)

        pathsrc = path.join(pathhome, f"Aorta_N0/Aorta_{N}/triSurface")
        pathdst = path.join(pathhome, f"AortaOF_N/Aorta_{N}/constant")
        subprocess.run(["cp", "-r", f"{pathsrc}", f"{pathdst}"], check=True)

        pathsrc_1 = path.join(pathhome, f"Aorta_N0/Aorta_{N}/transportProperties")
        pathdst_1 = path.join(pathhome, f"AortaOF_N/Aorta_{N}/constant")
        subprocess.run(["cp", "-r", f"{pathsrc_1}", f"{pathdst_1}"], check=True)

        pathsrc_2 = path.join(pathhome, f"Aorta_N0/Aorta_{N}/controlDict")
        pathdst_2 = path.join(pathhome, f"AortaOF_N/Aorta_{N}/system")
        subprocess.run(["cp", "-r", f"{pathsrc_2}", f"{pathdst_2}"], check=True)

    


        fnpath = path.join(pathhome, f"Aorta_N0/Aorta_{N}/Mesh_parameters.dat")
    
        with open(fnpath, 'rb') as dump_in:
            Mesh_parameters = pickle.load(dump_in)




        xmin = Mesh_parameters['Bounding_box'][0]
        xmax = Mesh_parameters['Bounding_box'][1]
        ymin = Mesh_parameters['Bounding_box'][2]
        ymax = Mesh_parameters['Bounding_box'][3]
        zmin = Mesh_parameters['Bounding_box'][4]
        zmax = Mesh_parameters['Bounding_box'][5]


        dl = 0.025 / (100 * n_blocks)
        divx = int((xmax-xmin) / dl)
        divy = int((ymax-ymin) / dl)
        divz = int(zmax -zmin / dl)
    

    
        xloc = Mesh_parameters['location_in_mesh'][0]
        yloc = Mesh_parameters['location_in_mesh'][1]
        zloc = Mesh_parameters['location_in_mesh'][2]

        dist = levels[0]
        lv = int(levels[1])

        controlDict = ParsedParameterFile(path.join(pathhome, f"AortaOF_N/Aorta_{N}", "system", "controlDict"))

        controlDict["deltaT"] = 1
        controlDict.writeFile()

        BlockMeshDict = ParsedParameterFile(path.join(pathhome, f"AortaOF_N/Aorta_{N}", "system", "blockMeshDict"))

        BlockMeshDict[
            "vertices"] = f"(  ({xmin} {ymin} {zmin})\n ({xmax} {ymin} {zmin})\n ({xmax} {ymax} {zmin})\n ({xmin} {ymax} {zmin})\n ({xmin} {ymin} {zmax})\n ({xmax} {ymin} {zmax})\n ({xmax} {ymax} {zmax})\n ({xmin} {ymax} {zmax}))"
        BlockMeshDict["blocks"] = f"(hex (0 1 2 3 4 5 6 7) ({divx} {divy} {divz}) simpleGrading (1 1 1))"
        BlockMeshDict.writeFile()

    
        os.chdir(path.join(pathhome, f"AortaOF_N/Aorta_{N}"))

        subprocess.run("blockMesh", shell=True, check=True)
        subprocess.run("surfaceFeatures", check=True)

        decomposePar = ParsedParameterFile(path.join(pathhome, f"AortaOF_N/Aorta_{N}", "system", "decomposeParDict"))

        decomposePar["numberOfSubdomains"] = np_snap
        decomposePar.writeFile()
    
        subprocess.run("decomposePar", check=True)

    
        os.chdir(pathhome)
        update_string(path.join(pathhome, f"AortaOF_N/Aorta_{N}/system/snappyHexMeshDict"),
                    rf"  locationInMesh",
                    f"    locationInMesh ( {xloc}   {yloc}  {zloc} );")
        


        update_string(path.join(pathhome, f"AortaOF_N/Aorta_{N}/system/snappyHexMeshDict"),
                    rf"        levels",
                    f"        levels ( ({dist} {lv})); // levels must be ordered nearest first")
        
        

        os.chdir(path.join(pathhome, f"AortaOF_N/Aorta_{N}"))
        print(os.getcwd())
        subprocess.run([f"mpirun", "-np", f"{np_snap}", "snappyHexMesh", "-parallel"], check=True)

        """
        reconstruct 
        """

        subprocess.run(["reconstructParMesh", "-latestTime"], check=True)

        
        """
        change path  snappy polyMesh num_dir2
        """
        if os.path.isdir(path.join(pathhome, f"AortaOF_N/Aorta_{N}/3")):
            num_dir = 3
        else:
            num_dir = 2

        directory = path.join(pathhome, f"AortaOF_N/Aorta_{N}/{num_dir}/polyMesh")
        for fn in os.listdir(directory):
            update_string(path.join(pathhome, f"AortaOF_N/Aorta_{N}/{num_dir}/polyMesh/{fn}"),
                        f'location    "{num_dir}/polyMesh";',
                        'location    "constant/polyMesh";')

        subprocess.run(["rm", "-rf", f"{path.join(pathhome, f'AortaOF_N/Aorta_{N}/constant/polyMesh')}"], check=True)
        pathsrc = path.join(pathhome, f"AortaOF_N/Aorta_{N}/{num_dir}/polyMesh")
        pathdst = path.join(pathhome, f"AortaOF_N/Aorta_{N}/constant")
        subprocess.run(["cp", "-r", f"{pathsrc}", f"{pathdst}"], check=True)
        pathrm = path.join(pathhome, f"AortaOF_N/Aorta_{N}/{num_dir}")
        subprocess.run(["rm", "-rf", f"{pathrm}"], check=True)

        for n in range(np_snap):
            pathrm = path.join(pathhome, f"AortaOF_N/Aorta_{N}/processor{n}")
            subprocess.run(["rm", "-rf", f"{pathrm}"], check=True)

        """
        rename patches

        update_string(f"/home/yana/AortaOF_N/Aorta_{N}/constant//polyMesh/boundary",
                    f"6",
                    f"3")

        update_string(f"/home/yana/AortaOF_N/Aorta_{N}/constant//polyMesh/boundary",
                    f"topWall",
                    f"inlet")
        update_string(f"/home/yana/AortaOF_N/Aorta_{N}/constant//polyMesh/boundary",
                    f"bottomWall",
                    f"outlet")

        remove parse block
        """

        """
        prepare unsteady solver
        """

    

        """
        prepare BC
        """
        

        pathsrc = path.join(pathtemplate, f"0_template/{BC}/0")
        pathdst = path.join(pathhome, f"AortaOF_N/Aorta_{N}")
        subprocess.run(["cp", "-r", f"{pathsrc}", f"{pathdst}"], check=True)

        pathsrc1 = path.join(pathtemplate, f"0_template/{BC}/Make")
        pathdst1 = path.join(pathhome, f"AortaOF_N/Aorta_{N}")
        subprocess.run(["cp", "-r", f"{pathsrc1}", f"{pathdst1}"], check=True)



        pathsrc3 = path.join(pathtemplate, f"0_template/{BC}/Mesh_test.C")
        pathdst3 = path.join(pathhome, f"AortaOF_N/Aorta_{N}")
        subprocess.run(["cp", "-r", f"{pathsrc3}", f"{pathdst3}"], check=True)

        os.chdir(path.join(pathhome, f"AortaOF_N/Aorta_{N}"))
        print(os.getcwd())
        # subprocess.run(f"wmake", shell=True, check=True, cwd=os.getcwd())
        subprocess.run(f"Mesh_test", shell=True, check=True, cwd=os.getcwd())

        area_us = np.loadtxt(path.join(pathhome, f"AortaOF_N/Aorta_{N}/U_norm/area_us.txt"), dtype=float)
        area = area_us[0]
        us = area_us[1]

        update_string(path.join(pathhome, f"AortaOF_N/Aorta_{N}/constant/transportProperties"),
                    f'key1',
                    f'{area}')
        update_string(path.join(pathhome, f"AortaOF_N/Aorta_{N}/constant/transportProperties"),
                    f'key2',
                    f'{us}')

       
        decomposePar = ParsedParameterFile(path.join(pathhome, f"AortaOF_N/Aorta_{N}", "system", "decomposeParDict"))

        decomposePar["numberOfSubdomains"] = max_np
        decomposePar.writeFile()

        subprocess.run("decomposePar", shell=True, check=True)
    


    os.chdir(path.join(pathhome, f"AortaOF_N/Aorta_{N}"))
    
    controlDict = ParsedParameterFile(path.join(pathhome, f"AortaOF_N/Aorta_{N}", "system", "controlDict"))
    controlDict["deltaT"] = 0.0005
    controlDict["writeInterval"] = 0.25
    controlDict["endTime"] = round(4*T, 2)
    controlDict.writeFile()


    if not os.path.isdir(path.join(pathhome, f"AortaOF_N/Aorta_{N}/processor1/{round(4*T, 2)}")):
        subprocess.run(f"mpirun -np {max_np} pimpleFoam -parallel", shell=True, check=True)
    

    controlDict = ParsedParameterFile(path.join(pathhome, f"AortaOF_N/Aorta_{N}", "system", "controlDict"))

    controlDict["writeInterval"] = 0.01
    controlDict["endTime"] = round(T * 5, 2)
    controlDict.writeFile()

    try:
        subprocess.run(f"mpirun -np {max_np} pimpleFoam -parallel", shell=True, check=True)

    finally:
        subprocess.run(f"reconstructPar -time '{round(4*T, 2)}:{round(5*T, 2)}'", shell=True, check=True)

        for n in range(max_np):
            pathrm = path.join(pathhome, f"AortaOF_N/Aorta_{N}/processor{n}")
            subprocess.Popen(["rm", "-rf", f"{pathrm}"])

        """
        postprocessing
        """
        subprocess.run(["pimpleFoam", "-postProcess", "-func", "wallShearStress"], check=True)
