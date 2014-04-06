import numpy as np
from instprofile import *


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


def test_two_gaussians():
    """
    Test the `peakdet` function with two gaussians.
    """
    gaussians = lambda x: peak_1*np.exp(-(mean_1-x)**2/(2*stdev_1**2)) + \
                          peak_2*np.exp(-(mean_2-x)**2/(2*stdev_2**2))

    x_vector = np.arange(0, 100.5, 0.5)

    mean_1 = 25
    mean_2 = 75

    peak_1 = 1.5
    peak_2 = 2

    stdev_1 = 0.1
    stdev_2 = 0.05

    #generate some data
    y_power = gaussians(x_vector)


    values = peakdet(y_power, 0.5, x_vector)[0]

    assert mean_1 == values[0, 0] and peak_1 == values[0, 1]
    assert mean_2 == values[1, 0] and peak_2 == values[1, 1]


def test_fit_gauss():
    gaussian = lambda x: peak*(1/np.sqrt(2*np.pi*(stdev**2)))*\
                               np.exp(-(mean-x)**2/(2*stdev**2))

    x_vector = np.arange(0, 100.5, 0.5)
    mean = 50
    peak = 1
    stdev = 0.1

    y_power = gaussian(x_vector)

    assert np.allclose(fit_gauss(x_vector, y_power, [peak, mean, stdev]),
                       [peak, mean, stdev])
