import re
import subprocess
import os
import pickle
import math
import numpy as np
import PyFoam
import argparse
import shutil  # Для безопасного копирования/удаления
import numpy as np
import matplotlib.pyplot as plt
import pathlib
import logging # Для логирования

from pathlib import Path # Для удобной работы с путями
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


script_path = os.path.abspath(__file__)
pathtemplate = os.getcwd()
print(pathtemplate)
# pathtemplate = "/home/imcool/Desktop/OpenFOAM_Lab_ADT/OpenFOAM_Artery_Lab_ADT/CFD_AAA"

"""

Argparse

"""

def update_string(caseStringFile, replaceMarker, string):
    with open(caseStringFile) as _caseStringFile:
        stringFile = _caseStringFile.read()

    with open(caseStringFile, 'w') as _caseStringFile:
        stringFile = re.sub(replaceMarker, string, stringFile)
        _caseStringFile.write(stringFile)
def list_of_floats(arg):
    print(list(map(float, arg)))
    return list(map(float, arg))
def copy_sourses_files(pathhome, N):
    #функция копирования файлов данных в рабочую директорию
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
    return fnpath
def creat_start_mesh(pathhome, N):
    #функция создания сетки, используется только если сетка не существует в рабочей директории
    #создает файл constant/polyMesh
    xmin = -0.12038598485339744
    xmax = 0.128764527624530172
    ymin = -0.05159100810929238
    ymax = 0.08459024385268212
    zmin = -0.21997369135082
    zmax = 0.0
    dl = 0.025 / (10 * n_blocks)
    divx = int((xmax-xmin) / dl)
    divy = int((ymax-ymin) / dl)
    divz = int((zmax -zmin) / dl)
    xloc = 0
    yloc = 0
    zloc = -0.05
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
    subprocess.run("blockMesh", shell=True, check=True)
    subprocess.run("surfaceFeatures", check=True)
def setting_reology_model(pathhome, N, rheology_model):
    #функция для настройки модели реологии
    try: 
        case_path = Path(pathhome) / f"AortaOF_N/Aorta_{N}"
        transport_props_path = case_path / "constant" / "transportProperties"
        transportProps = ParsedParameterFile(str(transport_props_path)) # Загружаем файл
        transportProps['transportModel'] = rheology_model

        possible_top_level_keys = ['nu', 'nuInf', 'nu0', 'k', 'n', 'a', 'nuMin', 'nuMax', 'TRef', 'TExp']
        possible_coeffs_dicts = ["NewtonianCoeffs", "BirdCarreauCoeffs", "powerLawCoeffs", "CrossPowerLaw", "HershelBulkley", "Casson"]

        if rheology_model == 'Newtonian':
            transportProps['nu'] = '[0 2 -1 0 0 0 0] 0.0035'
            if 'rho' not in transportProps:
                transportProps['rho'] = '[1 -3 0 0 0 0 0] 1050'
            
            for key in possible_top_level_keys:
                if key != 'nu' and key != 'rho' and key in transportProps:
                    del transportProps[key]
            for name in possible_coeffs_dicts:
                if name in transportProps:
                    del transportProps[name]

        elif rheology_model == 'BirdCarreau':
            coeffs_dict_name = "BirdCarreauCoeffs"
            birdCarreau_params = {
                'nu0'   : '[0 2 -1 0 0 0 0] 0.04',  
                'nuInf' : '[0 2 -1 0 0 0 0] 0.0035', 
                'k'     : '[0 0 1 0 0 0 0] 8.2',      
                'n'     : '[0 0 0 0 0 0 0] 0.2128'     
                #добавить лямбду!!!!! по умолчанию 2, надо сделать 0.64
            }
            transportProps[coeffs_dict_name] = birdCarreau_params
            if 'rho' not in transportProps:
                transportProps['rho'] = '[1 -3 0 0 0 0 0] 1050'

            for key in possible_top_level_keys:
                if key != 'rho' and key in transportProps:
                    print(f"[{N}] BirdCarreau: Удаление ключа верхнего уровня '{key}'.")
                    del transportProps[key]
            for name in possible_coeffs_dicts:
                if name != coeffs_dict_name and name in transportProps:
                    del transportProps[name]

        elif rheology_model == 'powerLaw':
            coeffs_dict_name = "powerLawCoeffs"
            powerLaw_params = {
                'k'     : '[0 2 -1 0 0 0 0] 0.017',  
                'n'     : '[0 0 0 0 0 0 0] 0.708',    
                'nuMin' : '[0 2 -1 0 0 0 0] 0.0035',  
                'nuMax' : '[0 2 -1 0 0 0 0] 0.04'    
            }
            transportProps[coeffs_dict_name] = powerLaw_params
            if 'rho' not in transportProps:
                transportProps['rho'] = '[1 -3 0 0 0 0 0] 1050'


            for key in possible_top_level_keys:
                if key != 'rho' and key in transportProps:
                    del transportProps[key]
            for name in possible_coeffs_dicts:
                if name != coeffs_dict_name and name in transportProps:
                    del transportProps[name]

        elif rheology_model == 'CrossPowerLaw':
            coeffs_dict_name = "CrossPowerLawCoeffs"
            CrossPowerLaw_params = {
                'nu0'   : '[0 2 -1 0 0 0 0] 0.04',  
                'nuInf' : '[0 2 -1 0 0 0 0] 0.0035', 
                'm'     : '[0 0 1 0 0 0 0] 8.2',      
                'n'     : '[0 0 0 0 0 0 0] 0.2128'     
            }
            transportProps[coeffs_dict_name] = CrossPowerLaw_params
            if 'rho' not in transportProps:
                transportProps['rho'] = '[1 -3 0 0 0 0 0] 1050'

            for key in possible_top_level_keys:
                if key != 'rho' and key in transportProps:
                    del transportProps[key]
            for name in possible_coeffs_dicts:
                if name != coeffs_dict_name and name in transportProps:
                    del transportProps[name]

        elif rheology_model == 'herschelBulkley':
            coeffs_dict_name = "herschelBulkleyCoeffs"
            herschelBulkley_params = {
                'tau0'  : '[0 2 -2 0 0 0 0] 0.01',  
                'k'     : '[0 2 -1 0 0 0 0] 0.017',  
                'n'     : '[0 0 0 0 0 0 0] 0.708'     
            }

            transportProps[coeffs_dict_name] = herschelBulkley_params
            if 'rho' not in transportProps:
                transportProps['rho'] = '[1 -3 0 0 0 0 0] 1050'
            for key in possible_top_level_keys:
                if key != 'rho' and key in transportProps:
                    del transportProps[key]
            for name in possible_coeffs_dicts:
                if name != coeffs_dict_name and name in transportProps:
                    del transportProps[name]

        elif rheology_model == 'Casson':
            coeffs_dict_name = "CassonCoeffs"
            Casson_params = {
                'tau0'  : '[0 2 -2 0 0 0 0] 0.01',  
                'mu'    : '[0 2 -1 0 0 0 0] 0.0035'     
            }
            transportProps[coeffs_dict_name] = Casson_params
            if 'rho' not in transportProps:
                transportProps['rho'] = '[1 -3 0 0 0 0 0] 1050'
            for key in possible_top_level_keys:
                if key != 'rho' and key in transportProps:
                    del transportProps[key]
            for name in possible_coeffs_dicts:
                if name != coeffs_dict_name and name in transportProps:
                    del transportProps[name]

        else:
            # Обработка случая, если выбрана неизвестная модель (хотя argparse должен это предотвратить)
            print(f"ПРЕДУПРЕЖДЕНИЕ [{N}]: Неизвестная модель реологии '{rheology_model}'. Параметры не установлены.")
            # Возможно, стоит вызвать ошибку: raise ValueError(...)
            exit()
        # 4. Финальная запись файла (только ОДНА)
        transportProps.writeFile()
        print(f"[{N}] Файл {transport_props_path.name} окончательно обновлен для модели {rheology_model}.")

        # --- КОНЕЦ: Настройка модели реологии ---
    except FileNotFoundError as e:
        print(f"ОШИБКА [{N}]: {e}")
        # sys.exit(1) # или continue
    except Exception as e:
        print(f"ОШИБКА [{N}] при обновлении {transport_props_path}: {e}")
        # sys.exit(1) # или continue
def snappyhexmesh_create_mesh(pathhome, N, xloc, yloc, zloc, dist, lv):
    os.chdir(pathhome)
    #сдвигаем точку для snappyHexMesh внутрь аорты
    update_string(path.join(pathhome, f"AortaOF_N/Aorta_{N}/system/snappyHexMeshDict"),
                rf"  locationInMesh",
                f"    locationInMesh ( {xloc}   {yloc}  {zloc} );")
    #меняем уровень детализации для измельчения сетки в проблемных областях
    update_string(path.join(pathhome, f"AortaOF_N/Aorta_{N}/system/snappyHexMeshDict"),
                rf"        levels",
                f"        levels ( ({dist} {lv})); // levels must be ordered nearest first")
    
    
    #запускаем snappyHexMesh для построения сетки на нашей геометрии в параллельном режиме
    os.chdir(path.join(pathhome, f"AortaOF_N/Aorta_{N}"))
    tmp = os.getcwd()
    try:
        result = subprocess.run(
            ["mpirun", "-np", f"{np_snap}", "snappyHexMesh", "-parallel"],
            check=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        print("snappyHexMesh completed successfully.")
        print(result.stdout)
    except subprocess.CalledProcessError as e:
        print("Error in snappyHexMesh:")
        print(e.stderr)



    #запуск рекомпозиции построенной сетки
    subprocess.run(["reconstructParMesh", "-latestTime"], check=True)

    
    """
    change path  snappy polyMesh num_dir2
    """
    if os.path.isdir(path.join(pathhome, f"AortaOF_N/Aorta_{N}/3")):
        num_dir = 3
    else:
        num_dir = 2
    print(num_dir)
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

    


parser = argparse.ArgumentParser(description='Script description')
parser.add_argument('--pwd', required=True, type=str)
parser.add_argument('--nodes',default='1', required=False, type=int)
parser.add_argument('--T',default='1.0', required=False, type=float)
parser.add_argument('--n_blocks',default='2', required=False, type=float)
parser.add_argument("--levels", required=False, nargs='+')
parser.add_argument('--BC',default='parabolic',required=False, type=str)
parser.add_argument('--rheology_model', default = 'Newtonian', choices = ['Newtonian', 'BirdCarreau', 'powerLaw', 'CrossPowerLaw', 'HerschelBulkley', 'Casson'], help= 'Select the blood rheology model (e.g., Newtonian, BirdCarreau, powerLaw, CrossPowerLaw, herschelBulkley, Casson')


args = parser.parse_args()
pathhome = path.join(pathtemplate, f"example1")
nodes = args.nodes
T = args.T
n_blocks = args.n_blocks
levels = list_of_floats(args.levels)
BC = args.BC
rheology_model = args.rheology_model
np_node = 8
max_np = nodes * np_node
np_snap = 8 * nodes




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
os.listdir(path='.')
case_directory = path.join(pathhome, f"AortaOF_N")
print(case_directory)
if not os.path.isdir(case_directory):
    os.mkdir(case_directory)
dir = path.join(pathhome, f"Aorta_N0")


for f in os.listdir(dir):
    N = f.split('_', 1)[1]
    if not os.path.isdir(path.join(pathhome, f"AortaOF_N/Aorta_{N}/postProcessing")):
        
        #настраиваем пути
        os.chdir(pathtemplate)
        template_path = path.join(pathtemplate, f"mesh_template/template")
        templateCase = SolutionDirectory(template_path, archive=None, paraviewLink=False)
        case = templateCase.cloneCase(path.join(pathhome, f"AortaOF_N/Aorta_{N}"))
        os.chdir(pathhome)

        #копируем в рабочую директорию файлы для запуска
        fnpath = copy_sourses_files(pathhome, N)

        #из скопированный файлов читаем данные для построения сетки
        with open(fnpath, 'rb') as dump_in:
            Mesh_parameters = pickle.load(dump_in)

        #создаем начальную сетку, если она не существует
        os.chdir(path.join(pathhome, f"AortaOF_N/Aorta_{N}"))
        mesh_dir_path = path.join(pathhome, f"AortaOF_N/Aorta_{N}", "constant", "polyMesh")
        mesh_exists = path.isdir(mesh_dir_path)
        if not mesh_exists:
            creat_start_mesh(pathhome, N)
            xloc = 0.0
            yloc = 0.0
            zloc = -0.05
            dist = levels[0]
            lv = int(levels[1])

        #настройка параметров для параллельного запуска
        decomposePar = ParsedParameterFile(path.join(pathhome, f"AortaOF_N/Aorta_{N}", "system", "decomposeParDict"))
        decomposePar["numberOfSubdomains"] = np_snap

        #изменяем файлы для выбранной реологии в файле transportProperties
        setting_reology_model(pathhome, N, rheology_model)
        #разделение существующей сетки на процессоры
        decomposePar.writeFile()
        subprocess.run("decomposePar", check=True)

        #запуск snappyHexMesh для построения сетки
        snappyhexmesh_create_mesh(pathhome, N, xloc, yloc, zloc, dist, lv)



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
        print("Запуск wmake")
        subprocess.run(f"wmake", shell=True, check=True, cwd=os.getcwd())
        try: 
            subprocess.run(["chmod", "+x", "./Mesh_test"], check=True)
        except:
            print("не получилось добавить право на исполнение")
            exit
        subprocess.run(f"./Mesh_test", shell=True, check=True, cwd=os.getcwd())
        
        
        area_us = np.loadtxt(path.join(pathhome, f"AortaOF_N/Aorta_{N}/U_norm/area_us.txt"), dtype=float)
        area = area_us[0]
        us = area_us[1]
        print(area, us)
        update_string(path.join(pathhome, f"AortaOF_N/Aorta_{N}/constant/transportProperties"),
                    f'key1',
                    f'{area}')
        update_string(path.join(pathhome, f"AortaOF_N/Aorta_{N}/constant/transportProperties"),
                    f'key2',
                    f'{us}')

          # --- ДОБАВИТЬ ДЛЯ ОТЛАДКИ ---
        fvSolution_final_path = path.join(pathhome, f"AortaOF_N/Aorta_{N}", "system", "fvSolution")
        print(f"--- DEBUG: Checking content of {fvSolution_final_path} BEFORE final decomposePar ---")
        try:
            with open(fvSolution_final_path, 'r') as f:
                # Читаем и ищем строку с решателем для p
                content = f.read()
                print(content) # Печатаем весь файл для проверки
                if "solver           GAMG;" in content and "p\n    {" in content:
                     print("--- DEBUG: GAMG found for p. Correct.")
                elif "solver          DICPCG;" in content and "p\n    {" in content:
                     print("--- DEBUG: DICPCG found for p. WRONG FILE CONTENT!")
                else:
                     print("--- DEBUG: Solver for p not found or format unexpected.")
        except FileNotFoundError:
            print(f"--- DEBUG: ERROR - {fvSolution_final_path} not found!")
        print(f"--- DEBUG: End check ---")
        input(">>> Press Enter to run decomposePar and continue...") # Пауза для просмотра
        # --- КОНЕЦ ОТЛАДОЧНОГО БЛОКА ---

        decomposePar = ParsedParameterFile(path.join(pathhome, f"AortaOF_N/Aorta_{N}", "system", "decomposeParDict"))

        decomposePar["numberOfSubdomains"] = max_np
        decomposePar.writeFile()

        subprocess.run("decomposePar", shell=True, check=True)
    

    
    os.chdir(path.join(pathhome, f"AortaOF_N/Aorta_{N}"))
    
    controlDict = ParsedParameterFile(path.join(pathhome, f"AortaOF_N/Aorta_{N}", "system", "controlDict"))
    controlDict["deltaT"] = 0.01
    controlDict["writeInterval"] = 0.01
    controlDict["endTime"] = round(2 * T, 2)
    controlDict.writeFile()


    if not os.path.isdir(path.join(pathhome, f"AortaOF_N/Aorta_{N}/processor1/{round(2*T, 2)}")):
        subprocess.run(f"mpirun -np {max_np} pimpleFoam -parallel", shell=True, check=True)
    

    controlDict = ParsedParameterFile(path.join(pathhome, f"AortaOF_N/Aorta_{N}", "system", "controlDict"))

    controlDict["writeInterval"] = 0.01
    controlDict["endTime"] = round(2 * T, 2)
    controlDict.writeFile()

    try:
        subprocess.run(f"mpirun -np {max_np} pimpleFoam -parallel", shell=True, check=True)

    finally:
        subprocess.run(f"reconstructPar -time '{round(1*T, 2)}:{round(2*T, 2)}'", shell=True, check=True)

        for n in range(max_np):
            pathrm = path.join(pathhome, f"AortaOF_N/Aorta_{N}/processor{n}")
            subprocess.Popen(["rm", "-rf", f"{pathrm}"])

        """
        postprocessing
        """
        subprocess.run(["pimpleFoam", "-postProcess", "-func", "wallShearStress"], check=True)
        subprocess.run(["postProcess", "-func", "minMaxComponents"], check = True)
