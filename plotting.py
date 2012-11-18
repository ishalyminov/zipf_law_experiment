import matplotlib.pyplot as plot

def make_plot(in_file_name, in_info, in_frequencies):
    frequencies_sorted = sorted(set(in_frequencies))
    ranks = [len(frequencies_sorted) - index for index in xrange(len(frequencies_sorted))]
    max_rank = len(ranks)
    min_freq = min(frequencies_sorted)
    plot.scatter(ranks, frequencies_sorted)
    plot.plot(ranks, [min_freq + max_rank - rank for rank in ranks], label = 'r = R - w', color = 'green')
    title_pattern = (in_info['grauthor'], in_info['header'], in_info['sentences'], in_info['words'])
    plot.title('%s. %s: %s sentences, %s words' % title_pattern)
    plot.xlabel('rank')
    plot.ylabel('frequency')
    plot.grid(True)
    plot.legend()
    plot.savefig(in_file_name)
    plot.clf()

def make_plot_with_critical_frequency(in_file_name, in_info, in_frequencies, in_critical_frequency):
    if len(in_frequencies):
        frequencies_sorted = sorted(set(in_frequencies))
        ranks = [len(frequencies_sorted) - index for index in xrange(len(frequencies_sorted))]
        max_rank = len(ranks)
        min_freq = min(frequencies_sorted)
        plot.scatter(ranks, frequencies_sorted)
        plot.plot(ranks, [min_freq + max_rank - rank for rank in ranks], label = 'r = R - w', color = 'green')
    title_pattern = (in_info['grauthor'], in_info['header'], in_info['sentences'], in_info['words'])
    plot.title('%s. %s: %s sentences, %s words' % title_pattern)
    plot.xlabel('rank')
    plot.ylabel('frequency')
    plot.axhline(in_critical_frequency, label='critical frequency = %d' % in_critical_frequency)
    plot.grid(True)
    plot.legend()
    plot.savefig(in_file_name)
    plot.clf()

def make_plot_with_two_critical_frequencies(in_file_name, \
                                            in_info, \
                                            in_frequencies, \
                                            in_theoretical_w_cr,
                                            in_empirical_w_cr):
    if len(in_frequencies):
        frequencies_sorted = sorted(set(in_frequencies))
        ranks = [len(frequencies_sorted) - index for index in xrange(len(frequencies_sorted))]
        max_rank = len(ranks)
        min_freq = min(frequencies_sorted)
        plot.scatter(ranks, frequencies_sorted)
        plot.plot(ranks, [min_freq + max_rank - rank for rank in ranks], label = 'r = R - w', color = 'green')
    title_pattern = (in_info['grauthor'], in_info['header'], in_info['sentences'], in_info['words'])
    plot.title('%s. %s: %s sentences, %s words' % title_pattern)
    plot.xlabel('rank')
    plot.ylabel('frequency')
    plot.axhline(in_theoretical_w_cr, label='theoretical w_cr = %d' % in_theoretical_w_cr)
    plot.axhline(in_empirical_w_cr, label='empirical w_cr = %d' % in_empirical_w_cr, color='red')
    plot.grid(True)
    plot.legend()
    plot.savefig(in_file_name)
    plot.clf()

def make_histogram(in_file_name, in_title, in_values, in_normed = True):
    plot.hist(in_values, normed=in_normed)
    plot.title(in_title)
    plot.grid(True)
    plot.savefig(in_file_name)
    plot.clf()
