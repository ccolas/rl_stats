"""
Design a latex table containing the statistical powers for various effect sizes.

The code in code_for_latex_table.txt must be used before \begin{document} in the latex file

"""

import sys

import pickle

sys.path.append('../')
from rl_stats.distributions import get_distribution_pairs
from rl_stats.tests import tests_list, run_test

path = './data/'

sample_sizes = [2, 3, 5, 10, 20, 30, 40, 50, 100]
effect_sizes = [0, 0.3, 0.5, 1., 2., 3., 5.]
nb_sample_sizes = len(sample_sizes)
nb_effect_sizes = len(effect_sizes)
nb_tests = len(tests_list)

effect_sizes_to_plot = [2, 3, 4]  # indexes of the three effect sizes you want in the table

tests_list = ['t-test', 'Welch', 'Mann-Whit.', 'r. t-test', 'boot.', 'permut.']


def write_latex_table(distrib):

    with open(path + STUDY + '/results_' + STUDY + '_' + distrib[0] + '_' + distrib[1] + '.pk', 'rb') as f:
        results_array = pickle.load(f)

    string_out = " \\begin{table} \n \caption{Statistical power when comparing samples from " + distrib[0] + "," + distrib[1] + ", " + STUDY + ".} \n " \
                 " \\footnotesize \n \centering \n   \\begin{tabular}{ccccccc} \n    \\toprule \n "

    for i in range(nb_effect_sizes):

        cells = []
        for j in range(nb_sample_sizes):
            row = []
            for k in range(nb_tests):
                row.append("{:.3f}".format(results_array[k, j, i]))
            cells.append(row)

        if i in effect_sizes_to_plot:
            if i == 2:
                term = 'Small'
            elif i == 3:
                term = 'Medium'
            elif i == 4:
                term = 'Large'
            string_out += " \multicolumn{4}{c}{" + term +" relative effect size: $\epsilon~=~" + str(effect_sizes[i]) + "$}  \\\\ \n" \
                          " \cmidrule(r){1-4} \n N & t-test & Welch & Mann-Whit. & r. t-test & boot. & permut. \\\\ \n  \midrule \n"

            for j in range(len(sample_sizes)):
                string_out += str(sample_sizes[j]) + ' &'
                all_line = 0
                for k in range(nb_tests):
                    if float(cells[j][k]) > 0.8:
                        string_out += ' \\textbf{\databar{' + str(cells[j][k]) + '}} &'
                        if float(cells[j][k]) > 0.9:
                            all_line += 1
                    else:
                        string_out += ' \databar{'+str(cells[j][k]) + '} &'
                string_out = string_out[:-1] + '\\\\ \n'
                if all_line == nb_tests:
                    break

    string_out += "  \end{tabular} \n \end{table}"

    file_name = path + STUDY + '/results_' + STUDY + '_' + distrib[0] + '_' + distrib[1] + '_effect.txt'
    with open(file_name, "w") as f:
        f.write(string_out)


if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('--STUDY', type=str, default='equal_dist_equal_var')
    args = parser.parse_args()
    STUDY = args.STUDY
    print('Study:', STUDY)

    if STUDY == 'unequal_dist_unequal_var_1':
        # include td3 and sac in that STUDY
        distributions_pair_idx = [(0, 1), (0, 2), (1, 2), (4, 3)]
    elif STUDY == 'unequal_dist_unequal_var_2':
        # include td3 and sac in that STUDY
        distributions_pair_idx = [(0, 1), (0, 2), (1, 2), (3, 4)]
    else:
        distributions_pair_idx = [(0, 1), (0, 2), (1, 2)]

    distrib_list, std_ratio = get_distribution_pairs(STUDY, distributions_pair_idx)

    for distrib in distrib_list:
        write_latex_table(distrib)
