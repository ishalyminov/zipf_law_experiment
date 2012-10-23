import matplotlib.pyplot as plot

def make_plot(in_file_name, in_frequencies, in_critical_frequency):
    frequencies_sorted = sorted(in_frequencies)
    ranks = [len(frequencies_sorted) - index for index in xrange(len(frequencies_sorted))]

    plot.scatter(ranks, frequencies_sorted)
    plot.axhline(in_critical_frequency)
    plot.savefig(in_file_name)
    plot.clf()
