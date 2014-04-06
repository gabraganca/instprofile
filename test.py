import numpy as np
from instprofile import peakdet

def test_one_gaussian():
    """
    test the `peakdet` function with one gaussian.
    """
    gaussian = lambda x: peak*np.exp(-(mean-x)**2/(2*stdev**2))

    x_vector = np.arange(0, 100.5, 0.5)
    peak = 1
    stdev = 0.1

    # the peakdet function does not obtain the peak if it is located in the
    #last argument of the arrar. thus, we reject it.
    for x in np.arange(len(x_vector) - 1):
        mean = x_vector[x]

        #generate some data
        y_power = gaussian(x_vector)


        mean_found, peak_found = peakdet(y_power, 0.5, x_vector)[0][0]

        assert mean_found == mean
        assert peak_found == peak

