"""
Main script to reproduce the experiments from the paper:
A Hitchhicker's Guide to Statistical Comparisons of Reinforcement Learning Algortihms.

------------------------------------

Possible studies:

- equal_dist_equal_var
- equal_dist_unequal_var
- unequal_dist_equal_var
- unequal_dist_unequal_var_1: here the first distribution is the one that has the smallest std
- unequal_dist_unequal_var_2: here the first distribution has the largest std

------------------------------------

Run experiments:

python3 run_experiment.py --study equal_dist_equal_var

This creates a pickle file in ./data/equal_dist_equal_var/ for each pair of distributions.

------------------------------------

Plots and Tables

- To obtain plots of the false positive rates as a function of the sample size for various tests,
just run the plot_false_positive.py script:

    python3 plot_false_positive.py --study equal_dist_equal_var

- To obtain code for latex table that contains the statistical power results use the table_from_results.py script:

    python3 table_from_results.py --study equal_dist_equal_var

"""


import sys
import pickle
from multiprocessing import Pool

import time
import numpy as np


sys.path.append('../')
from rl_stats.distributions import sample, get_distribution_pairs
from rl_stats.tests import tests_list, run_test




save = True # save results

sample_sizes = [2, 3, 5, 10, 20, 30, 40, 50, 100]
effect_sizes = [0, 0.3, 0.5, 1., 2., 3., 5.] # relative effect sizes
nb_repet = 10


def compute_stats(distrib):
    results_array = np.zeros([len(tests_list), len(sample_sizes), len(effect_sizes)])
    print('\t Computing statistical power for', distrib, 'distribution.')

    for i_t, test in enumerate(tests_list):
        if test == 'Mann-Whitney' or test=='Ranked t-test':
            median=True # set median to true when the test compares medians
        else:
            median=False

        print('\t \t Computing statistical power for', test)
        for i_s, sample_size in enumerate(sample_sizes):
            for i_e, effect in enumerate(effect_sizes):
                rejections = 0
                for i in range(nb_repet):
                    data1 = sample(distrib=distrib[0], size=sample_size, std_ratio=std_ratio[0], shift=0, median=median)
                    data2 = sample(distrib=distrib[1], size=sample_size, std_ratio=std_ratio[1], shift=effect, median=median)
                    rejection = run_test(test_id=test, data1=data1, data2=data2, alpha=0.05)
                    # check that the test did not reject for a false reason
                    if effect > 0 and rejection and data1.mean() > data2.mean():
                        rejection = False
                    rejections += int(rejection)
                # computes the false positive rate when effect_size=0, the true positive rate otherwise
                rejection_rate = rejections / nb_repet
                results_array[i_t, i_s, i_e] = rejection_rate

    if save:
        with open('./data/' + STUDY + '/results_' + STUDY + '_' + distrib[0] + '_' + distrib[1] + '.pk', 'wb') as f:
            pickle.dump(results_array, f)


if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('--study', type=str, default='equal_dist_equal_var')
    args = parser.parse_args()
    STUDY = args.study
    print('Study:', STUDY)
    if STUDY == 'unequal_dist_unequal_var_1':
        # include td3 and sac in that study
        distributions_pair_idx = [(0, 1), (0, 2), (1, 2) , (4, 3)]
    elif STUDY == 'unequal_dist_unequal_var_2':
        # include td3 and sac in that study
        distributions_pair_idx = [(0, 1), (0, 2), (1, 2), (3, 4)]
    else:
        distributions_pair_idx = [(0, 1), (0, 2), (1, 2)]

    distrib_list, std_ratio = get_distribution_pairs(STUDY, distributions_pair_idx)

    start = time.time()
    with Pool(5) as p:
        p.map(compute_stats, distrib_list)


    print('Done in', time.time() - start)

