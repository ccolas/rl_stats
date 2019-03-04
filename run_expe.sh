#!/bin/sh
#SBATCH --mincpus 24
#SBATCH -p longq
#SBATCH -t 15:00:00
#SBATCH -e run_expe.sh.err
#SBATCH -o run_expe.sh.out
rm log.txt; 
export EXP_INTERP='/cm/shared/apps/intel/composer_xe/python3.5/intelpython3/bin/python3' ;
$EXP_INTERP run_experiment.py --study equal_dist_equal_var &
$EXP_INTERP run_experiment.py --study equal_dist_unequal_var &
$EXP_INTERP run_experiment.py --study unequal_dist_equal_var &
$EXP_INTERP run_experiment.py --study unequal_dist_unequal_var_1 &
$EXP_INTERP run_experiment.py --study unequal_dist_unequal_var_2 &
wait
