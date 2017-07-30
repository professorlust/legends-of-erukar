import numpy as np

class Random:
    '''For all customized random purposes'''
    def get_from_custom_distribution(random_value, bins, values):
        return values[np.digitize(random_value, bins)]

    def create_random_distribution(possibilities, weights, min_weight=-0.3):
        bins, actual_possibilities = zip(*Random.calculate_bin_widths(weights, possibilities, min_weight))
        values = np.array(actual_possibilities)
        return Random.order_bins_and_values(bins, values)

    def calculate_bin_widths(bins, values, min_weight=-0.3):
        '''Determines the probablistic proportions for binning'''
        W = list(zip(bins,values))
        if all(w_i <= min_weight for w_i, _ in W) or len(set(W)) == 1:
            return [1/len(W)] * len(W)

        W_prime = [w_i for w_i in W if w_i[0] > min_weight]
        weights = [Random.clusterize(w_i, W_prime) for w_i in W_prime]
        return [((w_i / sum([w for w, val in weights])), val) for w_i,val in weights]

    def order_bins_and_values(bins, values):
        '''Orders the bins in an increasing order and adjusts the values accordingly'''
        sortedzip = sorted(zip(bins, values), key=lambda x: x[0])
        bins, values = zip(*sortedzip)
        return np.add.accumulate(bins), values

    def clusterize(w_i, W):
        '''
        Uses cluster algorithm developed for this project as follows:
        where N is the length, w_i is the current weight, and W is the set of weights
        1 / (N * (1 + (-w_i + sum(W))/(N-1) - w_i))
        '''
        min_W = max(min(0, min([w for w,_ in W])), 0)
        return (w_i[0] - min_W)/(max([w for w,_ in W])-min_W), w_i[1]
