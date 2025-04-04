export PATH=$PATH:/home/imcool/Desktop/OpenFOAM_Lab_ADT/OpenFOAM_Artery_Lab_ADT/CFD_AAA/example1

path=$(pwd)

rm -rf "/home/imcool/Desktop/OpenFOAM_Lab_ADT/OpenFOAM_Artery_Lab_ADT/CFD_AAA/example1/AortaOF_N/Aorta_novikov_01"
rm -rf "/home/imcool/Desktop/OpenFOAM_Lab_ADT/OpenFOAM_Artery_Lab_ADT/CFD_AAA/example1/AortaOF_N/Aorta_shishcenko_02"
python3 Aorta_pyfoam_flomuster0.py --pwd $path --levels 0.007 1 --n_blocks 1 --rheology_model Newtonian
cp -r "/home/imcool/Desktop/OpenFOAM_Lab_ADT/OpenFOAM_Artery_Lab_ADT/CFD_AAA/example1/AortaOF_N/Aorta_novikov_01" "/home/imcool/Desktop/OpenFOAM_Lab_ADT/OpenFOAM_Artery_Lab_ADT/CFD_AAA/results/Aorta_novikov_01/Newtonian"
cp -r "/home/imcool/Desktop/OpenFOAM_Lab_ADT/OpenFOAM_Artery_Lab_ADT/CFD_AAA/example1/AortaOF_N/Aorta_shishcenko_02" "/home/imcool/Desktop/OpenFOAM_Lab_ADT/OpenFOAM_Artery_Lab_ADT/CFD_AAA/results/Aorta_shishcenko_02/Newtonian"


# rm -rf "/home/imcool/Desktop/OpenFOAM_Lab_ADT/OpenFOAM_Artery_Lab_ADT/CFD_AAA/example1/AortaOF_N/Aorta_novikov_01"
# rm -rf "/home/imcool/Desktop/OpenFOAM_Lab_ADT/OpenFOAM_Artery_Lab_ADT/CFD_AAA/example1/AortaOF_N/Aorta_shishcenko_02"
# python3 Aorta_pyfoam_flomuster0.py --pwd $path --levels 0.007 1 --n_blocks 1 --rheology_model powerLaw
# cp -r "/home/imcool/Desktop/OpenFOAM_Lab_ADT/OpenFOAM_Artery_Lab_ADT/CFD_AAA/example1/AortaOF_N/Aorta_novikov_01" "/home/imcool/Desktop/OpenFOAM_Lab_ADT/OpenFOAM_Artery_Lab_ADT/CFD_AAA/results/Aorta_novikov_01/powerLaw"
# cp -r "/home/imcool/Desktop/OpenFOAM_Lab_ADT/OpenFOAM_Artery_Lab_ADT/CFD_AAA/example1/AortaOF_N/Aorta_shishcenko_02" "/home/imcool/Desktop/OpenFOAM_Lab_ADT/OpenFOAM_Artery_Lab_ADT/CFD_AAA/results/Aorta_shishcenko_02/powerLaw"


# rm -rf "/home/imcool/Desktop/OpenFOAM_Lab_ADT/OpenFOAM_Artery_Lab_ADT/CFD_AAA/example1/AortaOF_N/Aorta_novikov_01"
# rm -rf "/home/imcool/Desktop/OpenFOAM_Lab_ADT/OpenFOAM_Artery_Lab_ADT/CFD_AAA/example1/AortaOF_N/Aorta_shishcenko_02"
# python3 Aorta_pyfoam_flomuster0.py --pwd $path --levels 0.007 1 --n_blocks 1 --rheology_model BirdCarreau
# cp -r "/home/imcool/Desktop/OpenFOAM_Lab_ADT/OpenFOAM_Artery_Lab_ADT/CFD_AAA/example1/AortaOF_N/Aorta_novikov_01" "/home/imcool/Desktop/OpenFOAM_Lab_ADT/OpenFOAM_Artery_Lab_ADT/CFD_AAA/results/Aorta_novikov_01/BirdCarreau"
# cp -r "/home/imcool/Desktop/OpenFOAM_Lab_ADT/OpenFOAM_Artery_Lab_ADT/CFD_AAA/example1/AortaOF_N/Aorta_shishcenko_02" "/home/imcool/Desktop/OpenFOAM_Lab_ADT/OpenFOAM_Artery_Lab_ADT/CFD_AAA/results/Aorta_shishcenko_02/BirdCarreau"

# rm -rf "/home/imcool/Desktop/OpenFOAM_Lab_ADT/OpenFOAM_Artery_Lab_ADT/CFD_AAA/example1/AortaOF_N/Aorta_novikov_01"
# rm -rf "/home/imcool/Desktop/OpenFOAM_Lab_ADT/OpenFOAM_Artery_Lab_ADT/CFD_AAA/example1/AortaOF_N/Aorta_shishcenko_02"
# python3 Aorta_pyfoam_flomuster0.py --pwd $path --levels 0.007 1 --n_blocks 1 --rheology_model Casson
# cp -r "/home/imcool/Desktop/OpenFOAM_Lab_ADT/OpenFOAM_Artery_Lab_ADT/CFD_AAA/example1/AortaOF_N/Aorta_novikov_01" "/home/imcool/Desktop/OpenFOAM_Lab_ADT/OpenFOAM_Artery_Lab_ADT/CFD_AAA/results/Aorta_novikov_01/casson"
# cp -r "/home/imcool/Desktop/OpenFOAM_Lab_ADT/OpenFOAM_Artery_Lab_ADT/CFD_AAA/example1/AortaOF_N/Aorta_shishcenko_02" "/home/imcool/Desktop/OpenFOAM_Lab_ADT/OpenFOAM_Artery_Lab_ADT/CFD_AAA/results/Aorta_shishcenko_02/casson"

# rm -rf "/home/imcool/Desktop/OpenFOAM_Lab_ADT/OpenFOAM_Artery_Lab_ADT/CFD_AAA/example1/AortaOF_N/Aorta_novikov_01"
# rm -rf "/home/imcool/Desktop/OpenFOAM_Lab_ADT/OpenFOAM_Artery_Lab_ADT/CFD_AAA/example1/AortaOF_N/Aorta_shishcenko_02"
# python3 Aorta_pyfoam_flomuster0.py --pwd $path --levels 0.007 1 --n_blocks 1 --rheology_model CrossPowerLaw
# cp -r "/home/imcool/Desktop/OpenFOAM_Lab_ADT/OpenFOAM_Artery_Lab_ADT/CFD_AAA/example1/AortaOF_N/Aorta_novikov_01" "/home/imcool/Desktop/OpenFOAM_Lab_ADT/OpenFOAM_Artery_Lab_ADT/CFD_AAA/results/Aorta_novikov_01/crossPowerLaw"
# cp -r "/home/imcool/Desktop/OpenFOAM_Lab_ADT/OpenFOAM_Artery_Lab_ADT/CFD_AAA/example1/AortaOF_N/Aorta_shishcenko_02" "/home/imcool/Desktop/OpenFOAM_Lab_ADT/OpenFOAM_Artery_Lab_ADT/CFD_AAA/results/Aorta_shishcenko_02/crossPowerLaw"

# rm -rf "/home/imcool/Desktop/OpenFOAM_Lab_ADT/OpenFOAM_Artery_Lab_ADT/CFD_AAA/example1/AortaOF_N/Aorta_novikov_01"
# rm -rf "/home/imcool/Desktop/OpenFOAM_Lab_ADT/OpenFOAM_Artery_Lab_ADT/CFD_AAA/example1/AortaOF_N/Aorta_shishcenko_02"
# python3 Aorta_pyfoam_flomuster0.py --pwd $path --levels 0.007 1 --n_blocks 1 --rheology_model HerschelBulkley
# cp -r "/home/imcool/Desktop/OpenFOAM_Lab_ADT/OpenFOAM_Artery_Lab_ADT/CFD_AAA/example1/AortaOF_N/Aorta_novikov_01" "/home/imcool/Desktop/OpenFOAM_Lab_ADT/OpenFOAM_Artery_Lab_ADT/CFD_AAA/results/Aorta_novikov_01/herschelBulkley"
# cp -r "/home/imcool/Desktop/OpenFOAM_Lab_ADT/OpenFOAM_Artery_Lab_ADT/CFD_AAA/example1/AortaOF_N/Aorta_shishcenko_02" "/home/imcool/Desktop/OpenFOAM_Lab_ADT/OpenFOAM_Artery_Lab_ADT/CFD_AAA/results/Aorta_shishcenko_02/herschelBulkley"

