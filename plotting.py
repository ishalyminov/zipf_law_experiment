import matplotlib.pyplot as plot

def make_plot(in_file_name, in_info, in_frequencies, in_critical_frequency):
    frequencies_sorted = sorted(set(in_frequencies))
    ranks = [len(frequencies_sorted) - index for index in xrange(len(frequencies_sorted))]
    max_rank = len(ranks)
    plot.scatter(ranks, frequencies_sorted)
    plot.plot(ranks, [2.0 + max_rank - rank for rank in ranks], label = 'r = R - w', color = 'green')
    title_pattern = (in_info['grauthor'], in_info['header'], in_info['sentences'], in_info['words'])
    plot.title('%s. %s: %s sentences, %s words' % title_pattern)
    plot.xlabel('rank')
    plot.ylabel('frequency')
    plot.axhline(in_critical_frequency, label='critical frequency = %d' % in_critical_frequency)
    plot.grid(True)
    plot.legend()
    plot.savefig(in_file_name)
    plot.clf()
