#!/bin/bash -l
#SBATCH -o output_pos
#SBATCH --nodes=1
#SBATCH --partition=epyc


#SBATCH --job-name=scirep
#SBATCH --ntasks-per-node=32    # Number of MPI tasks per 1 node
#SBATCH --cpus-per-task=1       # Number of OpenMP threads for each MPI process/rank
#SBATCH --time=6-00:00:00
#SBATCH --partition=epyc
#SBATCH --exclude=node06


# General SLURM Parameters
echo "# SLURM_JOBID  = ${SLURM_JOBID}"
echo "# SLURM_JOB_NODELIST = ${SLURM_JOB_NODELIST}"
echo "# SLURM_NNODES = ${SLURM_NNODES}"
echo "# SLURM_NTASKS = ${SLURM_NTASKS}"
echo "# SLURM_CPUS_PER_TASK = ${SLURM_CPUS_PER_TASK}"
echo "# SLURMTMPDIR = ${SLURMTMPDIR}"
echo "# Submission directory = ${SLURM_SUBMIT_DIR}"

# modules
source /usr/share/modules/init/bash
module purge
module load mpi/openmpi-4.1.4
echo "# mpi: " $(which mpirun)
export OMP_NUM_THREADS=$SLURM_CPUS_PER_TASK
source /share/OpenFOAM/OpenFOAM-8/etc/bashrc
export OMPI_MCA_pml=ucx

source /fya_hdd/fya/aaa/bin/activate

export PATH=$PATH:/fya_hdd/fya/AAA_test


path=$(pwd)
echo $path

python3 Aorta_pyfoam_flomuster0.py --pwd $path --levels 0.0007 1 --n_blocks 0.8
