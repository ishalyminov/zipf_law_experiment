import os
parentdir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.sys.path.insert(0, os.path.join(parentdir, 'associative_text_model'))
import text_model

'''
    Calculates the empirical critical frequency value for the text
    (which is the highest frequency growing linearly from the bottom)
'''
def get_empirical_critical_frequency(in_frequencies):
    if not len(in_frequencies):
        return 0
    uniq_freqs = sorted(set(in_frequencies))
    critical_index = 0
    if len(uniq_freqs) > 1:
        delta_freq = uniq_freqs[1] - uniq_freqs[0]
        for freq_index in xrange(0, len(uniq_freqs) - 1):
            (freq_current, freq_next) = uniq_freqs[freq_index:freq_index + 2]
            if freq_next - freq_current == delta_freq:
                critical_index = freq_index + 1
            else:
                break
    return uniq_freqs[critical_index]

'''
    Returns the error between the theoretical and empirical critical frequencies
'''
def get_critical_frequency_error(in_dictionary):
    critical_freq = text_model.calculate_critical_frequency(in_dictionary)
    ideal_critical_freq = get_empirical_critical_frequency(in_dictionary.values())
    return critical_freq - ideal_critical_freq
