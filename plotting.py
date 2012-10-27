import matplotlib.pyplot as plot

def make_plot(in_file_name, in_frequencies, in_critical_frequency):
    frequencies_sorted = sorted(set(in_frequencies))
    ranks = [len(frequencies_sorted) - index for index in xrange(len(frequencies_sorted))]
    max_rank = len(ranks)
    plot.scatter(ranks, frequencies_sorted)
    plot.plot(ranks, [max_rank - rank for rank in ranks], label = 'r = R - w')
    plot.xlabel('rank')
    plot.ylabel('frequency')
    plot.axhline(in_critical_frequency, label='critical frequency = %d' % in_critical_frequency)
    plot.grid(True)
    plot.legend()
    plot.savefig(in_file_name)
    plot.clf()
