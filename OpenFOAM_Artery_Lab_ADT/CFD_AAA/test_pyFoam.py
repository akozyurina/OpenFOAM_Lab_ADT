#!/usr/bin/python
#
#$ -cwd
#$ -j y
#$ -S /opt/rocks/bin/python
#$ -m be
#
 
import sys,os
from os import path
 
os.environ["WM_64"]="1"
 
#pathtemplate = "/opt/openfoam10/tutorials/incompressible/icoFoam/cavity"
import PyFoam
import PyFoam.FoamInformation #inform about openFOAM
import PyFoam.RunDictionary #work with dictionary (files .dict), setup of solutions
import PyFoam.Applications # utilites OpenFOAM, for example blockMesh, snappyHexMesh, simpleFoam
import PyFoam.Execution #process of execution (run, stop, processes)
import PyFoam.Basics #helping functions and classes
import PyFoam.LogAnalysis #analisys log-files by OpenFOAM
import PyFoam.ThirdParty #integration libraries numpy, mathplotlib and others
import os

import re
import subprocess
import os
import pickle
import math
import numpy as np
import PyFoam
import argparse

from os import path
from PyFoam.RunDictionary.ParsedParameterFile import ParsedParameterFile
from PyFoam.RunDictionary.SolutionDirectory import SolutionDirectory
from PyFoam.RunDictionary.ParsedParameterFile import ParsedParameterFile
from PyFoam.Applications.BlockMeshRewrite import BlockMesh
from PyFoam.Execution.BasicRunner import BasicRunner


# Укажите имя папки вашего case
case_name = "/media/adt/Transcend/CFD_AAA/cavity"
# Проверка, существует ли папка
if not os.path.exists(case_name):
    os.makedirs(case_name)
    print(f"Создана директория '{case_name}'")


#Создаем объект словаря
try:
    blockMeshDict_path = os.path.join(case_name, "system", "blockMeshDict")
    blockMeshDict = ParsedParameterFile(blockMeshDict_path)
    print("Файл blockMeshDict найден")
except Exception as e:
    print("Ошибка при чтении blockMeshDict: ", e)
    print("Создаем blockMeshDict")
    blockMeshDict = ParsedParameterFile(blockMeshDict_path, create=True)

#do blockMesh
try:
    blockMeshDict.writeFile()
    print("blockMesh выполнен")
except Exception as e:
    print(f"Ошибка при запуске blockMesh: {e}")



#do icoFoam
# os.chdir(path.join(case_name))
# print(os.getcwd())
# run(["mpirun", "-np", f"{np_snap}", "icoFoam"], check=True)

#do paraFoam -builtin
controlDict_path = os.path.join(case_name, "system", "controlDict")
controlDict = ParsedParameterFile(controlDict_path)

# controlDict["writeInterval"] = 0.01
# controlDict["endTime"] = round(T * 5, 2)
controlDict.writeFile()

