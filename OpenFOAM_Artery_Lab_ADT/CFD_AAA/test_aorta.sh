export PATH=$PATH://home/imcool/Desktop/OpenFOAM_Lab_ADT/OpenFOAM_Artery_Lab_ADT/CFD_AAA/example1

path=$(pwd)

rm -rf "/home/imcool/Desktop/OpenFOAM_Lab_ADT/OpenFOAM_Artery_Lab_ADT/CFD_AAA/example1/AortaOF_N/Aorta_novikov_01"
rm -rf "/home/imcool/Desktop/OpenFOAM_Lab_ADT/OpenFOAM_Artery_Lab_ADT/CFD_AAA/example1/AortaOF_N/Aorta_shishcenko_02"
python3 Aorta_pyfoam_flomuster0.py --pwd $path --levels 0.0007 1 --n_blocks 1 --rheology_model BirdCarreau
 #rm -rf "/home/imcool/Desktop/OpenFOAM_Lab_ADT/OpenFOAM_Artery_Lab_ADT/CFD_AAA/example1/AortaOF_N/Aorta_novikov_01"
#rm -rf "/home/imcool/Desktop/OpenFOAM_Lab_ADT/OpenFOAM_Artery_Lab_ADT/CFD_AAA/example1/AortaOF_N/Aorta_shishcenko_02"
#python3 Aorta_pyfoam_flomuster0.py --pwd $path --levels 0.0007 1 --n_blocks 1 --BC custom
#rm -rf "/home/imcool/Desktop/OpenFOAM_Lab_ADT/OpenFOAM_Artery_Lab_ADT/CFD_AAA/example1/AortaOF_N/Aorta_novikov_01"
#rm -rf "/home/imcool/Desktop/OpenFOAM_Lab_ADT/OpenFOAM_Artery_Lab_ADT/CFD_AAA/example1/AortaOF_N/Aorta_shishcenko_02"
#python3 Aorta_pyfoam_flomuster0.py --pwd $path --levels 0.0007 1 --n_blocks 1 --BC plug
