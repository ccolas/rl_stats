import sys
import pickle
import matplotlib
import matplotlib.pyplot as plt
font = {'family': 'normal',
        'size': 70}
matplotlib.rc('font', **font)

sys.path.append('../')
from rl_stats.distributions import get_distribution_pairs
from rl_stats.tests import tests_list, run_test


colors = [[0, 0.447, 0.7410], [0.85, 0.325, 0.098], [0.466, 0.674, 0.188], [0.494, 0.1844, 0.556],
          [0.929, 0.694, 0.125], [0.3010, 0.745, 0.933], [0.635, 0.078, 0.184]]
red = [0.8, 0., 0.1]
path = './data/'

sample_sizes = [2, 3, 5, 10, 20, 30, 40, 50, 100]
nb_sample_sizes = len(sample_sizes)
nb_tests = len(tests_list)


def plot_false_positive(distrib):
    with open(path + STUDY + '/results_' + STUDY + '_' + distrib[0] + '_' + distrib[1] + '.pk', 'rb') as f:
        results_array = pickle.load(f)
    alphas = results_array[:, :, 0]
    fig, ax = plt.subplots(1, 1, figsize=(30, 20))
    for t in range(alphas.shape[0]):
        ax.plot(sample_sizes, alphas[t, :], linewidth=15)
    plt.axhline(y=0.05, color='k', linestyle='--', linewidth=10, alpha=0.8)
    leg = ax.legend(tests_list + ['α = 0.05'], loc=9, frameon=False)
    for line in leg.get_lines():
        line.set_linewidth(15.0)
    ax.spines['top'].set_linewidth(10)
    ax.spines['right'].set_linewidth(10)
    ax.spines['bottom'].set_linewidth(10)
    ax.spines['left'].set_linewidth(10)
    ax.set_xscale('log')
    ax.set_xticks(sample_sizes)
    ax.get_xaxis().set_major_formatter(matplotlib.ticker.ScalarFormatter())
    ax.get_xaxis().get_major_formatter().labelOnlyBase = False
    ax.set_yticks([0, 0.1, 0.2, 0.3])
    ax.set_ylim([-0.01, alphas.max()])
    lab1 = plt.xlabel('Sample size (log scale)')
    lab2 = plt.ylabel('False positive rate')
    plt.savefig('./data/' + STUDY + '/type_1_error_' + distrib[0] + '_' + distrib[1] + '.png', bbox_extra_artists=(lab1, lab2), bbox_inches='tight', dpi=100)


if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('--STUDY', type=str, default='equal_dist_equal_var')
    args = parser.parse_args()
    STUDY = args.STUDY
    print('Study:', STUDY)

    if STUDY == 'unequal_dist_unequal_var_1':
        # include td3 and sac in that study
        distributions_pair_idx = [(0, 1), (0, 2), (1, 2), (4, 3)]
    elif STUDY == 'unequal_dist_unequal_var_2':
        # include td3 and sac in that study
        distributions_pair_idx = [(0, 1), (0, 2), (1, 2), (3, 4)]
    else:
        distributions_pair_idx = [(0, 1), (0, 2), (1, 2)]

    distrib_list, std_ratio = get_distribution_pairs(STUDY, distributions_pair_idx)

    for distrib in distrib_list:
        plot_false_positive(distrib)
