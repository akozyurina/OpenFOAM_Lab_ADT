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

def list_of_floats(arg):
    print(list(map(float, arg)))
    return list(map(float, arg))


parser = argparse.ArgumentParser(description='Script description')


parser.add_argument('--pwd', required=True, type=str)
parser.add_argument('--nodes',default='1', required=False, type=int)
parser.add_argument('--T',default='1.0', required=False, type=float)
parser.add_argument('--n_blocks',default='2', required=False, type=float)
parser.add_argument("--levels", required=False, nargs='+')
parser.add_argument('--BC',default='parabolic',required=False, type=str)
parser.add_argument('--rheology_model', default = 'Newtonian', choices = ['Newtonian', 'BirdCarreau', 'powerLaw', 'crossPowerLaw', 'herschelBulkley', 'casson'], help= 'Select the blood rheology model (e.g., Newtonian, BirdCarreau, powerLaw, crossPowerLaw, herschelBulkley, casson')


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
os.listdir(path='.')
case_directory = path.join(pathhome, f"AortaOF_N")
print(case_directory)
if not os.path.isdir(case_directory):
    os.mkdir(case_directory)


dir = path.join(pathhome, f"Aorta_N0")

for f in os.listdir(dir):
    N = f.split('_', 1)[1]
    if not os.path.isdir(path.join(pathhome, f"AortaOF_N/Aorta_{N}/postProcessing")):
        """
        change template_path
        """
        os.chdir(pathtemplate)
        template_path = path.join(pathtemplate, f"mesh_template/template")
        print(os.path.abspath(template_path))
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




        xmin = -0.12038598485339744
        xmax = 0.128764527624530172
        ymin = -0.05159100810929238
        ymax = 0.08459024385268212
        zmin = -0.21997369135082
        zmax = 0.0


        dl = 0.025 / (10 * n_blocks)
        divx = int((xmax-xmin) / dl)
        divy = int((ymax-ymin) / dl)
        divz = int(zmax -zmin / dl)
    

    
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

    
        os.chdir(path.join(pathhome, f"AortaOF_N/Aorta_{N}"))

        subprocess.run("blockMesh", shell=True, check=True)
        subprocess.run("surfaceFeatures", check=True)

        decomposePar = ParsedParameterFile(path.join(pathhome, f"AortaOF_N/Aorta_{N}", "system", "decomposeParDict"))

        decomposePar["numberOfSubdomains"] = np_snap



        #меняем модель реологии в файле transportProperties
        try: 
    # --- НАЧАЛО: Настройка модели реологии ---
            print(f"[{N}] Настройка модели реологии: {rheology_model}")
            case_path = Path(pathhome) / f"AortaOF_N/Aorta_{N}"
            transport_props_path = case_path / "constant" / "transportProperties"

            if not transport_props_path.is_file():
                print(f"ОШИБКА [{N}]: Файл {transport_props_path} не найден. Пропуск настройки реологии.")
                # continue # или sys.exit() если критично
                raise FileNotFoundError(f"Файл {transport_props_path} не найден.") # Лучше вызвать ошибку

            transportProps = ParsedParameterFile(str(transport_props_path)) # Загружаем файл

            # 1. Устанавливаем основную модель
            transportProps['transportModel'] = rheology_model

            # 2. Определяем ОБЩИЙ список ключей верхнего уровня и под-словарей для ОЧИСТКИ
            #    (все ключи и под-словари, которые *могут* принадлежать ДРУГИМ моделям)
            possible_top_level_keys = ['nu', 'nuInf', 'nu0', 'k', 'n', 'a', 'nuMin', 'nuMax', 'TRef', 'TExp']
            possible_coeffs_dicts = ["NewtonianCoeffs", "BirdCarreauCoeffs", "powerLawCoeffs", "crossPowerLaw", "hershelBulkley", "casson"] # Добавьте другие, если нужно

            # 3. Блок if/elif для установки ПАРАМЕТРОВ и ОЧИСТКИ
            if rheology_model == 'Newtonian':
                # Устанавливаем параметры Newtonian
                transportProps['nu'] = '[0 2 -1 0 0 0 0] 0.0035' # ЗАМЕНИТЕ значение!
                if 'rho' not in transportProps:
                    transportProps['rho'] = '[1 -3 0 0 0 0 0] 1050' # ЗАМЕНИТЕ значение!
                print(f"[{N}] Установлены параметры для Newtonian.")

                # Удаляем ключи ВЕРХНЕГО УРОВНЯ от других моделей (кроме nu и rho)
                for key in possible_top_level_keys:
                    if key != 'nu' and key != 'rho' and key in transportProps:
                        print(f"[{N}] Newtonian: Удаление ключа верхнего уровня '{key}'.")
                        del transportProps[key]
                # Удаляем ПОД-СЛОВАРИ от других моделей
                for name in possible_coeffs_dicts:
                    if name in transportProps:
                        print(f"[{N}] Newtonian: Удаление под-словаря '{name}'.")
                        del transportProps[name]

            elif rheology_model == 'BirdCarreau':
                coeffs_dict_name = "BirdCarreauCoeffs"
                # Создание словаря параметров BirdCarreau
                birdCarreau_params = {
                    'nu0'   : '[0 2 -1 0 0 0 0] 0.04',  
                    'nuInf' : '[0 2 -1 0 0 0 0] 0.0035', 
                    'k'     : '[0 0 1 0 0 0 0] 8.2',      
                    'n'     : '[0 0 0 0 0 0 0] 0.2128'     
                    #добавить лямбду!!!!! по умолчанию 2, надо сделать 0.64
                }
                # Присвоение под-словарю
                transportProps[coeffs_dict_name] = birdCarreau_params
                print(f"[{N}] Добавлен под-словарь '{coeffs_dict_name}' с параметрами BirdCarreau.")
                if 'rho' not in transportProps:
                    transportProps['rho'] = '[1 -3 0 0 0 0 0] 1050'

                # Удаляем ключи ВЕРХНЕГО УРОВНЯ от других моделей
                for key in possible_top_level_keys:
                    # Не удаляем ключи, которые могут быть частью этой модели (даже если они не в словаре)
                    # и rho. Безопаснее удалить все, КРОМЕ rho.
                    if key != 'rho' and key in transportProps:
                        print(f"[{N}] BirdCarreau: Удаление ключа верхнего уровня '{key}'.")
                        del transportProps[key]
                # Удаляем ПОД-СЛОВАРИ от ДРУГИХ моделей
                for name in possible_coeffs_dicts:
                    if name != coeffs_dict_name and name in transportProps:
                        print(f"[{N}] BirdCarreau: Удаление под-словаря '{name}'.")
                        del transportProps[name]

            elif rheology_model == 'powerLaw':
                coeffs_dict_name = "powerLawCoeffs"
                # Создание словаря параметров powerLaw
                powerLaw_params = {
                    'k'     : '[0 2 -1 0 0 0 0] 0.017',  
                    'n'     : '[0 0 0 0 0 0 0] 0.708',    
                    'nuMin' : '[0 2 -1 0 0 0 0] 0.0035',  
                    'nuMax' : '[0 2 -1 0 0 0 0] 0.04'    
                }
                # Присвоение под-словарю
                transportProps[coeffs_dict_name] = powerLaw_params
                print(f"[{N}] Добавлен под-словарь '{coeffs_dict_name}' с параметрами powerLaw.")
                if 'rho' not in transportProps:
                    transportProps['rho'] = '[1 -3 0 0 0 0 0] 1050'

                # Удаляем ключи ВЕРХНЕГО УРОВНЯ от других моделей
                for key in possible_top_level_keys:
                    if key != 'rho' and key in transportProps:
                        print(f"[{N}] powerLaw: Удаление ключа верхнего уровня '{key}'.")
                        del transportProps[key]
                # Удаляем ПОД-СЛОВАРИ от ДРУГИХ моделей
                for name in possible_coeffs_dicts:
                    if name != coeffs_dict_name and name in transportProps:
                        print(f"[{N}] powerLaw: Удаление под-словаря '{name}'.")
                        del transportProps[name]
            elif rheology_model == 'crossPowerLaw':
                coeffs_dict_name = "crossPowerLawCoeffs"
                # Создание словаря параметров Cross Power Law
                crossPowerLaw_params = {
                    'nu0'   : '[0 2 -1 0 0 0 0] 0.04',  
                    'nuInf' : '[0 2 -1 0 0 0 0] 0.0035', 
                    'm'     : '[0 0 1 0 0 0 0] 8.2',      
                    'n'     : '[0 0 0 0 0 0 0] 0.2128'     
                }
                # Присвоение под-словарю
                transportProps[coeffs_dict_name] = crossPowerLaw_params
                print(f"[{N}] Добавлен под-словарь '{coeffs_dict_name}' с параметрами Cross Power Law.")
                if 'rho' not in transportProps:
                    transportProps['rho'] = '[1 -3 0 0 0 0 0] 1050'
                # Удаляем ключи ВЕРХНЕГО УРОВНЯ от других моделей
                for key in possible_top_level_keys:
                    if key != 'rho' and key in transportProps:
                        print(f"[{N}] Cross Power Law: Удаление ключа верхнего уровня '{key}'.")
                        del transportProps[key]
                # Удаляем ПОД-СЛОВАРИ от ДРУГИХ моделей
                for name in possible_coeffs_dicts:
                    if name != coeffs_dict_name and name in transportProps:
                        print(f"[{N}] Cross Power Law: Удаление под-словаря '{name}'.")
                        del transportProps[name]

            elif rheology_model == 'herschelBulkley':
                coeffs_dict_name = "herschelBulkleyCoeffs"
                # Создание словаря параметров Herschel-Bulkley
                herschelBulkley_params = {
                    'tau0'  : '[0 2 -2 0 0 0 0] 0.01',  
                    'k'     : '[0 2 -1 0 0 0 0] 0.017',  
                    'n'     : '[0 0 0 0 0 0 0] 0.708'     
                }
                # Присвоение под-словарю
                transportProps[coeffs_dict_name] = herschelBulkley_params
                print(f"[{N}] Добавлен под-словарь '{coeffs_dict_name}' с параметрами Herschel-Bulkley.")
                if 'rho' not in transportProps:
                    transportProps['rho'] = '[1 -3 0 0 0 0 0] 1050'
                # Удаляем ключи ВЕРХНЕГО УРОВНЯ от других моделей
                for key in possible_top_level_keys:
                    if key != 'rho' and key in transportProps:
                        print(f"[{N}] Herschel-Bulkley: Удаление ключа верхнего уровня '{key}'.")
                        del transportProps[key]
                # Удаляем ПОД-СЛОВАРИ от ДРУГИХ моделей
                for name in possible_coeffs_dicts:
                    if name != coeffs_dict_name and name in transportProps:
                        print(f"[{N}] Herschel-Bulkley: Удаление под-словаря '{name}'.")
                        del transportProps[name]

            elif rheology_model == 'casson':
                coeffs_dict_name = "cassonCoeffs"
                # Создание словаря параметров Casson
                casson_params = {
                    'tau0'  : '[0 2 -2 0 0 0 0] 0.01',  
                    'mu'    : '[0 2 -1 0 0 0 0] 0.0035'     
                }
                # Присвоение под-словарю
                transportProps[coeffs_dict_name] = casson_params
                print(f"[{N}] Добавлен под-словарь '{coeffs_dict_name}' с параметрами Casson.")
                if 'rho' not in transportProps:
                    transportProps['rho'] = '[1 -3 0 0 0 0 0] 1050'
                # Удаляем ключи ВЕРХНЕГО УРОВНЯ от других моделей
                for key in possible_top_level_keys:
                    if key != 'rho' and key in transportProps:
                        print(f"[{N}] Casson: Удаление ключа верхнего уровня '{key}'.")
                        del transportProps[key]
                # Удаляем ПОД-СЛОВАРИ от ДРУГИХ моделей
                for name in possible_coeffs_dicts:
                    if name != coeffs_dict_name and name in transportProps:
                        print(f"[{N}] Casson: Удаление под-словаря '{name}'.")
                        del transportProps[name]
            # Добавьте здесь elif для других моделей по аналогии

            else:
                # Обработка случая, если выбрана неизвестная модель (хотя argparse должен это предотвратить)
                print(f"ПРЕДУПРЕЖДЕНИЕ [{N}]: Неизвестная модель реологии '{rheology_model}'. Параметры не установлены.")
                # Возможно, стоит вызвать ошибку: raise ValueError(...)

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

    controlDict["writeInterval"] = 0.001
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


# Функция для чтения данных из файла
    # def read_data(file_path):
    #     data = {"time": [], "field": [], "min_value": [], "max_value": []}
        
    #     with open(file_path, "r") as file:
    #         for line in file:
    #             # Пропуск пустых строк и комментариев
    #             if line.strip() == "" or line.startswith("#"):
    #                 continue
                
    #             # Разделение строки на части
    #             parts = line.split()
                
    #             try:
    #                 # Извлечение значений
    #                 time = float(parts[0])
    #                 field = parts[1]
                    
    #                 # Обработка векторных значений (например, для U)
    #                 min_value = np.array([float(x) for x in parts[2][1:-1].split(",")])
    #                 max_value = np.array([float(x) for x in parts[4][1:-1].split(",")])
                    
    #                 # Сохранение данных
    #                 data["time"].append(time)
    #                 data["field"].append(field)
    #                 data["min_value"].append(min_value)
    #                 data["max_value"].append(max_value)
                
    #             except Exception as e:
    #                 print(f"Ошибка при обработке строки: {line.strip()} - {e}")
        
    #     return data

    # # Путь к файлу
    # file_path = (path.join(pathhome, f"AortaOF_N/Aorta_{N}", "postProcessing/minMaxComponents/2/fieldMinMax.dat"))


    # # Чтение данных
    # data = read_data(file_path)

    # # Преобразование списков в массивы NumPy
    # times = np.array(data["time"])
    # fields = np.array(data["field"])
    # min_values = np.array(data["min_value"])
    # max_values = np.array(data["max_value"])
    # # Выбор данных для поля 'U'
    # u_indices = [i for i, field in enumerate(fields) if field == "U"]
    # u_times = times[u_indices]
    # u_min_values = np.linalg.norm(min_values[u_indices], axis=1)  # Модуль минимального значения
    # u_max_values = np.linalg.norm(max_values[u_indices], axis=1)  # Модуль максимального значения
    # # Создание графика
    # plt.figure(figsize=(10, 6))

    # # График минимальных значений
    # plt.plot(u_times, u_min_values, label="Min |U|", color="blue", linestyle="--")

    # # График максимальных значений
    # plt.plot(u_times, u_max_values, label="Max |U|", color="red")

    # # Настройка графика
    # plt.title("Минимальные и максимальные значения модуля скорости во времени")
    # plt.xlabel("Время")
    # plt.ylabel("Модуль скорости")
    # plt.legend()
    # plt.grid(True)
    # plt.show()
    # # Сохранение графика
    # results_graphics = (path.join(pathhome, f"/results_graphics/plot_minmax_novikov_01/"))
    # plt.savefig("{BC}.png")
